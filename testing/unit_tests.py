# run using: pytest testing\unit_tests.py (make sure to do pip install -r requirements.txt)
import pytest
from ..cpu import CPU
from ..memory import Memory

def make_cpu_with_bytes(test_bytes):
    padding   = [0] * 0x100
    rom_data  = padding + test_bytes
    rom_data += [0] * max(0x8000 - len(rom_data), 0)  # Ensure at least 32KB total
    rom_bytes = bytes(rom_data)

    mem = Memory(rom_bytes)
    cpu = CPU(mem)
    cpu.registers['cycles'] = 0
    return cpu


def test_nop():
    cpu = make_cpu_with_bytes([0x00]) # NOP
    initial_pc = cpu.registers['PC']
    assert cpu.step() # returns True
    assert cpu.registers['PC'] == (initial_pc + 1) & 0xFFFF
    assert cpu.cycles == 4

def test_ld_bc_d16():
    # opcode 0x01, imm_lo=0x34, imm_hi=0x12
    cpu = make_cpu_with_bytes([0x01, 0x34, 0x12])
    initial_pc = cpu.registers['PC']
    assert cpu.step()
    assert cpu.registers['B'] == 0x12
    assert cpu.registers['C'] == 0x34
    assert cpu.registers['PC'] == (initial_pc + 3) & 0xFFFF
    assert cpu.cycles == 12

def test_ld_bc_ptr_a():
    # prepare A=0xAB, BC=0xC000, opcode 0x02
    cpu = make_cpu_with_bytes([0x02])
    cpu.registers['A'] = 0xAB
    cpu.registers['B'] = 0xC0
    cpu.registers['C'] = 0x00
    assert cpu.step()
    # memory at 0x2000 should now be 0xAB
    assert cpu.memory.read_byte(0xC000) == 0xAB
    assert cpu.cycles == 8
