class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.known_opcodes = []
        self.registers = {
            'A': 0x01, 'F': 0xB0, 'B': 0x00, 'C': 0x13,
            'D': 0x00, 'E': 0xD8, 'H': 0x01, 'L': 0x4D,
            'SP': 0xFFFE, 'PC': 0x0100
        }
        
    def step(self):
        # Fetch instruction
        opcode = self.memory.read_byte(self.registers['PC'])
        print(f"Executing opcode: {hex(opcode)} at PC: {hex(self.registers['PC'])}")
        self.registers['PC'] += 1
        # TODO: Decode and execute instruction  
        return self.registers['PC'], opcode      