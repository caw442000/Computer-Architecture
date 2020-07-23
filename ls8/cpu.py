"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
NOP = 0b00000000
PUSH = 0b01000101
POP = 0b01000110
SP = 0b00000111
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.reg[7] = 0xF4
        self.sp = 7
        self.branch_table = {}
        self.branch_table[HLT] = self.handle_hlt
        self.branch_table[LDI] = self.handle_ldi
        self.branch_table[PRN] = self.handle_prn
        self.branch_table[MUL] = self.handle_mul
        self.branch_table[ADD] = self.handle_add
        self.branch_table[CALL] = self.handle_call
        self.branch_table[RET] = self.handle_ret
        self.branch_table[NOP] = self.handle_nop
        self.branch_table[POP] = self.handle_pop
        self.branch_table[PUSH] = self.handle_push

      
        


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


    def handle_add(self):
        reg_num_1 = self.ram_read(self.pc + 1)
        reg_num_2 = self.ram_read(self.pc + 2)
        self.alu("ADD", reg_num_1, reg_num_2)
        self.pc += 3

    def handle_pop(self):
        # get register number to put value in
        reg_num = self.ram_read(self.pc + 1)
        # use stack pointer to get the value
        value = self.ram_read(self.sp)
        # put the value into the given register
        self.reg[reg_num] = value
        # now will increment the stack pointer:
        self.sp += 1
        # increment our stack pointer
        self.pc += 2

    def handle_push(self):
        # decriment the stack pointer
        self.sp -= 1
        # get the register number
        reg_num = self.ram_read(self.pc + 1)
        # get a value from the given register
        value = self.reg[reg_num]
        # put the value at the stack pointer address
        self.ram_write(self.sp, value)
        # increment program counter by 2
        self.pc += 2

    def handle_call(self):
        ### push command after CALL onto the stack
        return_address = self.pc + 2
     
        #### Get register number
        reg_num = self.ram[self.pc + 1]
        ### get the address to jump to, from the register
        subroutine_address = self.reg[reg_num]

        # push it on stack
        # decrement stack pointer
        # self.reg[7] -= 1
        self.sp -= 1
        # self.sp = self.reg[7]


        print(self.sp)
    
        # this gets the address in the register for the top of stack
        top_of_stack_address =self.reg[self.sp]
    
        ### put return address on the stack
        self.ram_write(sp, return_address)
        

        
        ### then look at register, jump to that address
        self.pc = subroutine_address

    def handle_ret(self):
        
        # pop the return address off the stack
        top_of_stack_address = self.reg[self.sp]
        return_address = self.ram_read(top_of_stack_address)
        self.reg[self.sp] += 1
        # go to return address: set the pc to return address
        self.pc = return_address



    def run(self):
        """Run the CPU."""
        
        while self.running:
            ir = self.ram[self.pc]
            self.branch_table[ir]()


    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value