import re

def parse_sail_file(file_path):
    """
    Parses the Sail file and initializes instruction_table and clause_patterns.
    """
    relevant_clauses = [
        "union clause",
        "mapping clause encdec",
        "mapping clause assembly"
    ]

    instruction_table = {}
    clause_patterns = {}

    with open(file_path, "r") as file:
        content = file.read()

    partition_pattern = re.compile(r"union clause ast = (\w+) : .*")
    partitions = partition_pattern.split(content)

    instruction_pattern = re.compile(r"RISCV_\w+")

    for i in range(1, len(partitions), 2):
        union_clause = partitions[i]

        if i + 1 < len(partitions):
            partition = partitions[i + 1]
            process_partition(partition, instruction_pattern, relevant_clauses, instruction_table, clause_patterns)
        else:
            print(f"Warning: partition index {i + 1} out of range")

    return instruction_table, clause_patterns

def process_partition(partition, instruction_pattern, relevant_clauses, instruction_table, clause_patterns):
    """
    Processes each partition, extracting instructions and tailoring Sail code.
    """
    instruction_names = set(instruction_pattern.findall(partition))

    for instruction_name in instruction_names:
        clean_instruction_name = instruction_name.replace("RISCV_", "").lower()

        if clean_instruction_name not in instruction_table:
            instruction_table[clean_instruction_name] = {clause: "NO" for clause in relevant_clauses}

        for clause in relevant_clauses:
            if clause in partition:
                instruction_table[clean_instruction_name][clause] = "YES"

        if clean_instruction_name not in clause_patterns:
            clause_patterns[clean_instruction_name] = partition

        parse_clauses(partition, clean_instruction_name, instruction_table)

def parse_clauses(partition, instruction_name, instruction_table):
    """
    Parses and tailors clauses in the Sail partition, adding them to the instruction table.
    """
    add_clause_to_table(partition, instruction_name, instruction_table, 
                        r"mapping encdec_uop : uop <-> bits\(7\) = \{.*?\}", 
                        clean_braces=True)

    add_clause_to_table(partition, instruction_name, instruction_table, 
                        r"mapping clause encdec =.*?\<->.*?\n", 
                        clean_braces=False)

    add_clause_to_table(partition, instruction_name, instruction_table, 
                        r"function clause execute.*?=.*?\{.*?\}", 
                        clean_braces=False, remove_commas=True)

    add_clause_to_table(partition, instruction_name, instruction_table, 
                        r"mapping utype_mnemonic : uop <-> string = \{.*?\}", 
                        clean_braces=True)

    add_clause_to_table(partition, instruction_name, instruction_table, 
                        r"mapping clause assembly =.*?\<->.*?\n", 
                        clean_braces=False)

def add_clause_to_table(partition, instruction_name, instruction_table, pattern, clean_braces=False, remove_commas=False):
    """
    Finds and adds tailored clauses from the partition to the instruction table.
    """
    clause_pattern = re.compile(pattern, re.DOTALL)
    match = clause_pattern.search(partition)
    if match:
        tailored_clause = match.group(0)
        tailored_clause = re.sub(r"\bRISCV_\w+\s*<->.*?;", 
                                 lambda m: m.group(0) if instruction_name in m.group(0) else '', tailored_clause)
        if clean_braces:
            tailored_clause = re.sub(r"^\{|\}$", '', tailored_clause, flags=re.DOTALL).strip()
        if remove_commas:
            tailored_clause = re.sub(r",\s*}", "}", tailored_clause)
            tailored_clause = re.sub(r"\{\s*,", "{", tailored_clause)
        instruction_table[instruction_name].setdefault("sail_code", []).append(tailored_clause)

def generate_c_logic(instruction, partition):
    """
    Generates encode, decode, and print logic based on instruction type.
    """
    if "UTYPE" in partition:
        return (
            "uint32_t imm = instr->imm;\n"
            "uint32_t rd = instr->rd;\n"
            "uint32_t op = instr->uop;\n"
            "instr->binary = (imm << 12) | (rd << 7) | op;\n",
            "instr->imm = (binary >> 12) & 0xFFFFF;\n"
            "instr->rd = (binary >> 7) & 0x1F;\n"
            "instr->uop = binary & 0x7F;\n",
            "printf(\"%s r%d, %d\", \"LUI\", instr->rd, instr->imm);\n"
        )
    elif "JTYPE" in partition:
        return (
            "uint32_t imm = instr->imm;\n"
            "uint32_t rd = instr->rd;\n"
            "instr->binary = (imm << 12) | (rd << 7) | 0b1101111;\n",
            "instr->imm = (binary >> 12) & 0xFFFFF;\n"
            "instr->rd = (binary >> 7) & 0x1F;\n",
            "printf(\"%s r%d, %d\", \"JAL\", instr->rd, instr->imm);\n"
        )
    elif "ITYPE" in partition:
        return (
            "uint32_t imm = instr->imm;\n"
            "uint32_t rd = instr->rd;\n"
            "uint32_t op = instr->iop;\n"
            "instr->binary = (imm << 20) | (rd << 7) | op;\n",
            "instr->imm = (binary >> 20) & 0xFFF;\n"
            "instr->rd = (binary >> 7) & 0x1F;\n"
            "instr->iop = binary & 0x7F;\n",
            "printf(\"%s r%d, %d\", \"ORI\", instr->rd, instr->imm);\n"
        )
    elif "RTYPE" in partition:
        return (
            "uint32_t rd = instr->rd;\n"
            "uint32_t rs1 = instr->rs1;\n"
            "uint32_t rs2 = instr->rs2;\n"
            "uint32_t funct3 = instr->funct3;\n"
            "uint32_t funct7 = instr->funct7;\n"
            "instr->binary = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | instr->rop;\n",
            "instr->rd = (binary >> 7) & 0x1F;\n"
            "instr->funct3 = (binary >> 12) & 0x7;\n"
            "instr->rs1 = (binary >> 15) & 0x1F;\n"
            "instr->rs2 = (binary >> 20) & 0x1F;\n"
            "instr->funct7 = (binary >> 25) & 0x7F;\n"
            "instr->rop = binary & 0x7F;\n",
            "printf(\"%s r%d, r%d, r%d\", \"ADD\", instr->rd, instr->rs1, instr->rs2);\n"
        )
    else:
        return (
            "instr->binary = (instr->rd << 7) | instr->binary;\n",
            "instr->rd = (binary >> 7) & 0x1F;\n",
            "printf(\"%s r%d\", \"GENERIC\", instr->rd);\n"
        )

def generate_dynamic_c_code(instruction_table, clause_patterns):
    """
    Generates dynamic C code for the given instruction table and clause patterns.
    """
    c_code = []
    c_code.append("#include <stdio.h>")
    c_code.append("#include <stdint.h>")
    c_code.append("")

    for instruction, clauses in instruction_table.items():
        if clauses.get('mapping clause encdec') == "YES" or clauses.get('mapping clause assembly') == "YES":
            partition = clause_patterns.get(instruction, "")

            fields = re.findall(r"\b(bits\(\d+\)|regidx|uop|bop|rop|sop|iop|imm|rd|rs1|rs2|funct3|funct7)\b", partition)
            field_defs = set(f"    uint32_t {field};" for field in fields if "bits" not in field)
            field_defs.add("    uint32_t binary;")

            c_code.append(f"struct {instruction.lower()}_t {{")
            c_code.extend(field_defs)
            c_code.append("};")
            c_code.append("")

            encode_logic, decode_logic, print_logic = generate_c_logic(instruction, partition)

            if clauses.get('mapping clause encdec') == "YES":
                c_code.append(f"void encode_{instruction.lower()}(struct {instruction.lower()}_t *instr) {{")
                c_code.append(encode_logic.strip())
                c_code.append("}")
                c_code.append("")

                c_code.append(f"void decode_{instruction.lower()}(uint32_t binary, struct {instruction.lower()}_t *instr) {{")
                c_code.append(decode_logic.strip())
                c_code.append("}")
                c_code.append("")

            if clauses.get('mapping clause assembly') == "YES":
                c_code.append(f"void print_assembly_{instruction.lower()}(struct {instruction.lower()}_t *instr) {{")
                c_code.append(print_logic.strip())
                c_code.append("}")
                c_code.append("")

    return "\n".join(c_code)

def save_c_code_to_file(c_code, file_path):
    """
    Saves the generated C code to the specified file path.
    """
    with open(file_path, "w") as output_file:
        output_file.write(c_code)
    print(f"Dynamic C code for instructions has been written to {file_path}")

def display_instruction_info(instruction_table):
    """
    Displays the instruction information.
    """
    for instr, code_blocks in instruction_table.items():
        print(f"\nInstruction: {instr}")
        for clause, status in code_blocks.items():
            if clause == "sail_code":
                print("\n".join(status))
            else:
                print(f"{clause}: {status}")