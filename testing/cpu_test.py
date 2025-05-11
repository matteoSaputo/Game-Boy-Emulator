# run using: python -m testing.cpu_test
from rom import load_rom
from memory import Memory
from cpu import CPU

def main():
    rom_bytes = load_rom("roms/halt_bug.gb")
    mem = Memory(rom_bytes)
    cpu = CPU(mem)

    # Run until CPU.step() returns False (unimplemented opcode)
    while cpu.step():
        pass

    print("CPU test ROM halted unexpectedly.")

if __name__ == "__main__":
    main()
