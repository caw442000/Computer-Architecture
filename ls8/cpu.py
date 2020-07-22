"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
NOP = 0b00000000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        # self.reg[7] = 0xF4
        self.branch_table = {}
        self.branch_table[HLT] = self.handle_hlt
        self.branch_table[LDI] = self.handle_ldi
        self.branch_table[PRN] = self.handle_prn
        self.branch_table[MUL] = self.handle_mul
        self.branch_table[NOP] = self.handle_nop
        


    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]

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
        #    ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(filename) as f:
            for line in f:
                line = line.split("#")[0].strip()
                if line == "":
                    continue
                else:
                    self.ram[address] = int(line, 2)
                    address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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

  
    
    def handle_hlt(self):
        self.running = False
        self.pc += 1

    def handle_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3

    def handle_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2


    def handle_nop(self):
        self.pc += 1


    def handle_mul(self):
        reg_num_1 = self.ram_read(self.pc + 1)
        reg_num_2 = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_num_1, reg_num_2)
        self.pc += 3

    def run(self):
        """Run the CPU."""
        
        while self.running:
            ir = self.ram[self.pc]
            self.branch_table[ir]()

            # if ir == HLT:
            #     self.HLT()
            # elif ir == LDI:
            #     self.LDI()
            # elif ir == PRN:
            #     self.PRN()
            # elif ir == MUL:
            #     self.MUL()
            # else:
            #     print(f"Instruction '{ir}'' at address '{self.pc}' is not recognized")
            #     self.pc += 1


    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value