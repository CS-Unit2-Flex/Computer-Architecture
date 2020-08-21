"""CPU functionality."""

import sys

# 8-bit
# ADD = 0b10100000
# SUB = 0b10100001
# MULT = 0b10100010
# DIV = 0b10100011
# AND = 0b10101000
# MOD = 0b10100100
# NOT = 0b01101001
# OR = 0b10101010
# XOR = 0b10101011
# CMP = 0b10100111
# SHL = 0b10101100
# SHR = 0b10101101
# DEC = 0b01100110
# INC = 0b01100101
# PRN = 0b01000111
# PRA = 0b01001000
# LD = 0b10000011
# LDI = 0b10000010
# HLT = 0b00000001
# POP = 0b01000110
# PUSH = 0b01000101
# CALL = 0b01010000
# RET = 0b00010001
# JMP = 0b01010100
# JEQ = 0b01010101
# JNE = 0b01010110

# hex
ADD = 0xA0
SUB = 0xA1
MULT = 0xA2
DIV = 0xA3
AND = 0xA8
MOD = 0xA4
NOT = 0x69
OR = 0xAA
XOR = 0xAB
CMP = 0xA7
SHL = 0xAC
SHR = 0xAD
INC = 0x66
DEC = 0x65
PRN = 0x47
PRA = 0x48
LD = 0x83
LDI = 0x82
HLT = 0x01
POP = 0x46
PUSH = 0x45
CALL = 0x50
RET = 0x11
JMP = 0x54
JEQ = 0x55
JNE = 0x56

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        self.ram = [0] * 256 # Ram
        self.reg = [0] * 8 # Register
        self.pc = 0 # Program Counter
        self.sp = 7 # Stack Pointer ()
        self.equal_flag = 0
        self.less_than_flag = 0
        self.greater_than_flag = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: python3 ls8.py examples/filename")
            sys.exit(1)
        # print(sys.argv[1])
        try:
            with open(sys.argv[1]) as f:
                for instruction in f:
                    try:
                        instruction = instruction.split("#", 1)[0]
                        instruction = int(instruction, 2)
                        self.ram[address] = instruction
                        address += 1
                    except ValueError: 
                        pass
        except FileNotFoundError:
            print(f"{sys.argv[1]} not found")
            sys.exit(1)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # Base Maths
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.reg[reg_a] &= 255
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
            self.reg[reg_a] &= 255
        elif op == 'MULT':
            self.reg[reg_a] *= self.reg[reg_b]
            self.reg[reg_a] &= 255
        elif op == 'DIV':
            answer = self.reg[reg_a] / self.reg[reg_b]

        # Additional alu operations
        elif op == 'AND':
            # print(self.reg[reg_a], self.reg[reg_b])
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]
            self.reg[reg_a] &= 255
        elif op == 'NOT':
            # print(self.reg[reg_a])
            self.reg[reg_a]  = int(bin(~self.reg[reg_a]), 2) 
            self.reg[reg_a] &= 255
        elif op == 'OR':
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
            print(self.reg[reg_a])
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
            self.reg[reg_a] &= 255
        elif op == 'CMP': # CMP == Compare
            # Check equality
            if self.reg[reg_a] == self.reg[reg_b]:
                self.equal_flag = 1
            else:
                self.equal_flag = 0

            # Check Less
            if self.reg[reg_a] < self.reg[reg_b]:
                self.less_than_flag = 1
            else:
                self.less_than_flag = 0

            # Check Greater
            if self.reg[reg_a] > self.reg[reg_b]:
                self.greater_than_flag = 1
            else:
                self.greater_than_flag = 0
        elif op == 'SHL':
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
            self.reg[reg_a] &= 255
        elif op == 'SHR':
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
            self.reg[reg_a] &= 255
        elif op == 'INC':
            self.reg[reg_a] -= 1
            self.reg[reg_a] &= 255
        elif op == 'DEC':
            self.reg[reg_a] += 1
            self.reg[reg_a] &= 255
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # pass
        self.trace()
        keep_running = True
        while keep_running:
                
            IR = self.ram_read(self.pc) # IR = Instruction Register
            op1 = self.ram_read(self.pc + 1)
            op2 = self.ram_read(self.pc + 2)


            if IR == PRN: 
                self.handle_PRN(op1)
                self.pc += 2
            elif IR == LDI: 
                self.handle_LDI(op1, op2)
                self.pc += 3
            elif IR == PUSH: 
                # pass
                self.handle_PUSH(self.reg[op1])
                self.pc += 2
            elif IR == POP:
                # pass
                v = self.handle_POP()
                self.reg[op1] = v
                self.pc += 2
            elif IR == CALL:
                self.reg[self.sp] -= 1
                self.handle_PUSH(self.pc + 2)
                registry_placeholder = self.reg[self.ram[self.pc + 1]]
                self.pc = registry_placeholder
            elif IR == RET:
                self.pc = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
            elif IR == JMP:
                address = self.reg[self.ram[self.pc + 1]]
                self.pc = address
            elif IR == JEQ: # Judge Equal
                registry_addr = self.ram[self.pc + 1]

                if self.equal_flag == 1:
                    self.pc = self.reg[registry_addr]
                else:
                    self.pc += 2
            elif IR == JNE: # Judge Not Equal
                registry_addr = self.ram[self.pc + 1]
                if self.equal_flag == 0:
                    self.pc = self.reg[registry_addr]
                else:
                    self.pc += 2
            elif IR == PRA:
                # letter = chr(self.reg[op1], end = '')
                print(chr(self.reg[op1]), end = '')
                self.pc += 2
            elif IR == LD:
                self.reg[op1] = self.ram[self.reg[op2]]
                self.pc += 3
            

            # ALU 
            elif IR == DEC:
                self.alu('DEC', op1, op2)
                self.pc += 2
            elif IR == INC:
                self.alu('INC', op1, op2)
                self.pc += 2
            elif IR == SHL:
                self.alu('SHL', op1, op2)
                self.pc += 3
            elif IR == SHR:
                self.alu('SHR', op1, op2)
                self.pc += 3
            elif IR == CMP:
                self.alu('CMP', self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3
            elif IR == HLT:
                keep_running = False
            elif IR == ADD: 
                # pass
                self.alu('ADD', op1, op2)
                self.pc += 3
            elif IR == SUB:
                # pass
                self.alu('SUB', op1, op2)
                self.pc += 3
            elif IR == MULT:
                self.alu('MULT', op1, op2)
                self.pc += 3
            elif IR == DIV:
                # pass
                if op2 == 0:
                    keep_running = False
                self.alu('DIV', op1, op2)
                self.pc += 3
            elif IR == AND:
                self.alu('AND', op1, op2)
                self.pc += 3
            elif IR == MOD:
                if op2 == 0:
                    keep_running == False
                self.alu('MOD', op1, op2)
                self.pc += 3
            elif IR == NOT:
                self.alu('NOT', op1, op2)
                self.pc += 2
            elif IR == OR:
                self.alu('OR', op1, op2)
                self.pc += 3
            elif IR == XOR:
                self.alu('XOR', op1, op2)
                self.pc += 3
            else:
                cont = False

    def handle_PUSH(self, v):
        # pass
        self.sp -= 1
        self.ram_write(self.sp, v)

    def handle_POP(self):
        # # pass
        v = self.ram_read(self.sp)
        self.sp += 1
        return v

    def ram_read(self, MAR): # MAR = Memory Adress Register
        # pass
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): # MDR = Memory Data Register, MAR = Memory Adress Register
        # pass
        self.ram[MAR] = MDR
        return

    def handle_LDI(self, k, v): # k = key, v = value
        self.reg[k] = v

    def handle_PRN(self, value):
        print(self.reg[value])

