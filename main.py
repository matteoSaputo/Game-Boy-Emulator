from rom import load_rom
from cpu import CPU
from memory import Memory

def main():
    rom = load_rom('roms/PokemonYellow.gb')
    memory = Memory(rom)
    cpu = CPU(memory)
    
    while True:
        pc, curr_inst = cpu.step()
        if curr_inst not in cpu.known_opcodes:
            print(f"Unknown opcode {hex(curr_inst)} at {hex(pc-1)} – stopping.")
            break
        # TODO: update graphics, handle input, audio, etc.
        
if __name__ == "__main__":
    main()