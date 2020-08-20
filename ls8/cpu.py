"""CPU functionality."""

import sys

ADD = 0b10100000
SUB = 0B10100001
MULT = 0b10100010
DIV = 0b10100011
PRN = 0b01000111
LDI = 0b10000010
HLT = 0b00000001
POP = 0b01000110
PUSH = 0b01000101


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        self.ram = [0] * 256 # Ram
        self.reg = [0] * 8 # Register
        self.pc = 0 # Program Counter
        self.sp = 244 # Stack pointer (0xf4 means 244)

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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MULT':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV':
            answer = self.reg[reg_a] / self.reg[reg_b]
            self.reg[reg_a] = answer
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
                
            IR = self.ram_read(self.pc) 
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
