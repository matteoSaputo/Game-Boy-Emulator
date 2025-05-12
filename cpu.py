ZFLAG, NFLAG, HFLAG, CFLAG = 0x80, 0x40, 0x20, 0x10

class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.cycles = 0 # total T-states
        self.instruction_set = {
            0x00: self.op_nop,
            0x01: self.op_ld_bc_d16,
            0x02: self.op_ld_bc_ptr_a
        }
        self.cb_instruction_set = {

        }
        self.registers = {
            'A': 0x01, 'F': 0xB0, # accumulator and flags
            'B': 0x00, 'C': 0x13,
            'D': 0x00, 'E': 0xD8, 
            'H': 0x01, 'L': 0x4D,
            'SP': 0xFFFE,   # stack pointer 
            'PC': 0x0100    # start after BIOS
        }
        
    def step(self):
        # --- Fetch instruction ---
        pc = self.registers['PC'] & 0xFFFF
        opcode = self.memory.read_byte(pc)
        print(f"Reading opcode: {hex(opcode)} at PC: {hex(pc)}")
        
        # --- Decode instruction ---
        if opcode == 0xCB: # two byte instrucion
            cbop = self.memory.read_byte((pc+1) & 0xFFFF)
            handler = self.cb_instruction_set[cbop]
        else:
            handler = self.instruction_set.get(opcode)
            if not handler:
                print(f"Unknown opcode {hex(opcode)} at {hex(pc)} – stopping.")
                return False

        # --- Execute instruction ---
        cycles = handler(pc) # call the handler which should update regs, mem, pc, and return # of cycles
        self.cycles += cycles

        return True
        # TODO: Implement opcode instructions  

    # Flag helpers (for readability in handlers)
    def set_flag(self, mask):   
        self.registers['F'] |= mask
    def clear_flag(self, mask): 
        self.registers['F'] &= ~mask
    def test_flag(self, mask):  
        return bool(self.registers['F'] & mask)

    # Register‐pair getters/setters
    def get_AF(self): 
        return (self.registers['A']<<8) | self.registers['F']
    def set_AF(self,v): 
        self.registers['A']=v>>8; self.registers['F']=v&0xF0
    def get_BC(self): 
        return (self.registers['B']<<8) | self.registers['C']
    def set_BC(self,v): 
        self.registers['B']=v>>8; self.registers['C']=v&0xF0
    def get_DE(self): 
        return (self.registers['D']<<8) | self.registers['E']
    def set_DE(self,v): 
        self.registers['D']=v>>8; self.registers['E']=v&0xF0
    def get_HL(self): 
        return (self.registers['H']<<8) | self.registers['L']
    def set_HL(self,v): 
        self.registers['H']=v>>8; self.registers['L']=v&0xF0

    def increment_pc(self, num):
        pc = self.registers['PC']
        self.registers['PC'] = (pc + num) & 0xFFFF
    
    def move_pc(self, addr):
        self.registers['PC'] = addr
    
    # --- Data movement ---
    def op_nop(self, pc):
        # NOP, one byte long, 4 cycles
        self.increment_pc(1)
        return 4
    
    def op_ld_bc_d16(self, pc):
        # read two immediate bytes (little-endian)
        lo = self.memory.read_byte((pc + 1) & 0xFFFF)
        hi = self.memory.read_byte((pc + 2) & 0xFFFF)
        value = (hi << 8) | lo
        
        # store into BC register pair
        self.registers['B'] = (value >> 8) & 0xFF
        self.registers['C'] = value & 0xFF
        
        # advance PC past opcode + two data bytes
        self.increment_pc(3)
        return 12
    
    def op_ld_bc_ptr_a(self, pc):
        #compute address from BC pair
        addr = (self.registers['B'] << 8) | self.registers['C']
        #write A into [BC]
        self.memory.write_byte(addr, self.registers['A'])
        
        self.increment_pc(1)
        return 8
    
    # --- Arithmetic and Logic ---

    # --- 16-bit Arithmetic ---

    # --- Control-flow ---

    # --- CB-prefixed bit ops ---

    # --- Miscellaneous ops ---