class Memory:
    def __init__(self, rom):
        # store raw ROM and compute number of 16KB banks
        self.rom = rom
        self.num_banks = len(rom) // 0x4000
        self.current_bank = 1
        self.ram_enabled = False
        
        # full 64KB address space0
        self.mem = [0] * 0x10000
        
        # map fixed bank 0
        self.mem[0x0000:0x4000] = list(self.rom[0x0000:0x40000])
        # map bank 1
        self.map_bank(self.current_bank)
        
    def map_bank(self, bank_num):
        # MBC1 never lets bank 0 into
        bank = bank_num % self.num_banks
        if bank == 0:
            bank = 1
        self.current_bank = bank
        
        start = bank * 0x4000
        end = start + 0x4000
        self.mem[0x4000:0x8000] = list(self.rom[start:end])
            
    def read_byte(self, addr):
        return self.mem[addr]
    
    def write_byte(self, addr, value):
        # ---- MBC1 control registers ----
        if 0x0000 <= addr <= 0x1fff:
            # RAM enable (for catridges with external save RAM)
            self.ram_enabled = (value & 0x0F) == 0x0A
            return
    
        if 0x2000 <= addr <= 0x3FFF:
            # lower 5 bits of ROM bank number
            new_bank = (self.current_bank & 0x60) | (value & 0x1F)
            self.map_bank(new_bank)
            return
        
        if 0x4000 <= addr <= 0x5FFF:
            # upper 2 bits of bank number (for large ROMs)
            upper = (value & 0x03) << 5
            new_bank = (self.current_bank & 0x1F) | upper
            self.map_bank(new_bank)
            return
        
        self.mem[addr] = value