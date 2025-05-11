class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.cycles = 0
        self.instruction_set = {
            0x00: self.op_nop,
            0x01: self.op_ld_bc_d16,
            0x02: self.op_ld_bc_ptr_a
        }
        self.registers = {
            'A': 0x01, 'F': 0xB0, # accumulator and flags
            'B': 0x00, 'C': 0x13,
            'D': 0x00, 'E': 0xD8, 
            'H': 0x01, 'L': 0x4D,
            'SP': 0xFFFE,   # stack pointer 
            'PC': 0x0100    # 
        }
        
    def step(self):
        # --- Fetch instruction ---
        pc = self.registers['PC'] & 0xFFFF
        opcode = self.memory.read_byte(pc)
        print(f"Reading opcode: {hex(opcode)} at PC: {hex(pc)}")
        
        # --- Decode instruction ---
        handler = self.instruction_set.get(opcode)
        if not handler:
            print(f"Unknown opcode {hex(opcode)} at {hex(pc)} – stopping.")
            return False

        # --- Execute instruction ---
        cycles = handler(pc) # call the handler which should update regs, mem, pc, and return # of cycles
        self.cycles += cycles

        return True
        # TODO: Decode and execute instruction  

    def increment_pc(self, num):
        pc = self.registers['PC']
        self.registers['PC'] = (pc + num) & 0xFFFF
    
    def move_pc(self, addr):
        self.registers['PC'] = addr
        
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