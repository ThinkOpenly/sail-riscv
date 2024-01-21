-- useful_functions.sail

val extension : (string) -> bool

function extension(ext) = {
  -- Base ISA extensions
  match ext {
    "A" => misa.A() == 0b1,
    "C" => misa.C() == 0b1,
    "D" => misa.D() == 0b1,
    "E" => misa.E() == 0b1,
    "F" => misa.F() == 0b1,
    "I" => misa.I() == 0b1,
    "M" => misa.M() == 0b1,
    "N" => misa.N() == 0b1,
    "S" => misa.S() == 0b1,
    "U" => misa.U() == 0b1,
    "V" => misa.V() == 0b1,
    "Zicsr" => misa.CSR() == 0b1,
    "Zifencei" => misa.IFenceI() == 0b1,
    "Zim" => misa.M() == 0b1,
    "Zkr" => misa.Kernel() == 0b1,
    "Zmedeleg" => misa.MEDELEG() == 0b1,
    "Zmideleg" => misa.MIDELEG() == 0b1,
    "Zpmp" => misa.PMP() == 0b1,
    "Zrelro" => misa.Relro() == 0b1,
    _ => false
  }
}
