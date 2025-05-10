class Memory:
    def __init__(self, rom):
        self.mem = [0] * 0x10000
        for i in range(len(rom)):
            self.mem[i] = rom[i]
            
    def read_byte(self, addr):
        return self.mem[addr]
    
    def write_byte(self, addr, value):
        self.mem[addr] = value