# Building and Compiling the Project

## Prerequisites

1. **Install Sail**
   Follow the [installation guide](https://github.com/rems-project/sail/blob/sail2/INSTALL.md).

2. **Check OCaml Version**
   Ensure OCaml version 5.1.0 or higher is installed:
   ```bash
   ocamlc -version
   ```
   If the version is lower, create a new opam switch:
   ```bash
   opam switch create 5.1.0
   eval $(opam env)
   ```

## Building the Project

### 1. Build the Sail Parser

1. Clone the Sail repository:
   ```bash
   git clone https://github.com/ThinkOpenly/sail.git
   ```
2. Navigate into the repository:
   ```bash
   cd sail
   ```
3. Build the parser:
   ```bash
   make
   ```

### 2. Set Up the Environment for RISC-V Sail

1. Initialize the opam environment:
   ```bash
   eval $(opam env)
   ```
2. Update the `PATH` to include the Sail repository:
   ```bash
   export PATH=<path-to-sail-repository>:$PATH
   ```
   Replace `<path-to-sail-repository>` with the actual path to your Sail repository.
3. Clone the RISC-V Sail repository:
   ```bash
   git clone https://github.com/ThinkOpenly/sail-riscv.git
   ```

### 3. Build the Project

Run the following command to build the project:
```bash
make json
```

### Optional: Debugging and Logging

To enable debugging and save outputs, navigate to the `sail-riscv` folder and run the following commands:

1. Change to the `sail-riscv` directory:
   ```bash
   cd sail-riscv
   ```
2. Activate debug mode:
   ```bash
   export SAIL_DEBUG=1
   ```
3. Save debug and JSON output to files:
   ```bash
   make json > output.json 2> debug.log
   ```
   Replace `output.json` and `debug.log` with your preferred filenames.
