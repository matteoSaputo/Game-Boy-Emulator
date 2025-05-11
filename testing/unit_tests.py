# run using: pytest testing\unit_tests.py (make sure to do pip install -r requirements.txt)
import pytest
from ..cpu import CPU
from ..memory import Memory

def make_cpu_with_bytes(bytes_):
    # pad to at least one bank so addressing works
    rom = bytes(bytes_ + [0] * (0x4000 - len(bytes_)))
    mem = Memory(rom)
    cpu = CPU(mem)
    # reset cycles if you track them
    cpu.registers['cycles'] = 0
    return cpu

def test_nop():
    cpu = make_cpu_with_bytes([0x00]) # NOP
    initial_pc = cpu.registers['PC']
    assert cpu.step() # returns True
    assert cpu.registers['PC'] == (initial_pc + 1) & 0xFFFF
    assert cpu.registers['cycles'] == 4

def test_ld_bc_d16():
    # opcode 0x01, imm_lo=0x34, imm_hi=0x12
    cpu = make_cpu_with_bytes([0x01, 0x34, 0x12])
    initial_pc = cpu.registers['PC']
    assert cpu.step()
    assert cpu.registers['B'] == 0x12
    assert cpu.registers['C'] == 0x34
    assert cpu.registers['PC'] == (initial_pc + 3) & 0xFFFF
    assert cpu.registers['cycles'] == 12

def test_ld_ptrbc_a():
    # prepare A=0xAB, BC=0x2000, opcode 0x02
    cpu = make_cpu_with_bytes([0x02])
    cpu.registers['A'] = 0xAB
    cpu.registers['B'] = 0x20
    cpu.registers['C'] = 0x00
    assert cpu.step()
    # memory at 0x2000 should now be 0xAB
    assert cpu.memory.read_byte(0x2000) == 0xAB
    assert cpu.registers['cycles'] == 8
