from flags import ZFLAG, NFLAG, HFLAG, CFLAG

# --- Data movement (LD, NOP, etc.) ---

""" NOP
Opcode: 0x00, Number of Bytes: 1, Number of Cycles: 1, 
Flags: - - - -
Only advances the program counter by 1. 
Performs no other operations that would have an effect.
"""
def op_nop(cpu, pc):
    # NOP, one byte long, 4 cycles
    cpu.increment_pc(1)
    return 4

""" LD BC, d16
Opcode: 0x01, Number of Bytes: 3, Number of Cycles: 3
Flags: - - - -
Load the 2 bytes of immediate data into register pair BC.
The first byte of immediate data is the lower byte (i.e., bits 0-7), 
and the second byte of immediate data is the higher byte (i.e., bits 8-15).
"""
def op_ld_bc_d16(cpu, pc):
    # read two immediate bytes (little-endian)
    lo = cpu.memory.read_byte((pc + 1) & 0xFFFF)
    hi = cpu.memory.read_byte((pc + 2) & 0xFFFF)
    value = (hi << 8) | lo
        
    # store into BC register pair
    cpu.registers['B'] = (value >> 8) & 0xFF
    cpu.registers['C'] = value & 0xFF
        
    # advance PC past opcode + two data bytes
    cpu.increment_pc(3)
    return 12
    
""" LD (BC), A
Opcode: 0x02, Number of Bytes: 1, Number of Cycles: 2
Flags: - - - -
Store the contents of register A in the memory location specified 
by register pair BC.
"""
def op_ld_bc_ptr_a(cpu, pc):
    #compute address from BC pair
    addr = (cpu.registers['B'] << 8) | cpu.registers['C']
    #write A into [BC]
    cpu.memory.write_byte(addr, cpu.registers['A'])
        
    cpu.increment_pc(1)
    return 8

code_map = {
    0x00: op_nop,
    0x01: op_ld_bc_d16,
    0x02: op_ld_bc_ptr_a
}