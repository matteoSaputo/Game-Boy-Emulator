from rom import load_rom
from cpu import CPU
from memory import Memory

def main():
    rom = load_rom('roms/PokemonYellow.gb')
    memory = Memory(rom)
    cpu = CPU(memory)
    
    while cpu.step():
        pass
        # TODO: update graphics, handle input, audio, etc.
        
if __name__ == "__main__":
    main()