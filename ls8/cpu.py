"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Create memory
        self.ram = [0] * 256  # length and the index will stop at 255
        # I think add lines 27 (register), 28 (pc) and 29 (running) from comp.py
        self.reg = [0] * 8  # returns 8 zeros and stores values (0-7)
        # Program counter, the index (address) of the current instruction
        self.pc = 0
        self.SP = 7 # R7 is reserved
        self.reg[self.SP] = 0xF4
        self.running = True
 
        # Instructions
        self.LDI =  0b10000010
        self.MUL =  0b10100010
        self.PRN =  0b01000111
        self.PUSH = 0b01000101
        self.POP =  0b01000110
        self.HLT =  0b00000001

        # Turning the branch table into an object to be able to update easier
        self.branchtable = {
            self.LDI: self.ldi,
            self.MUL: self.multiply,
            self.PRN: self.prn,
            self.HLT: self.halt,
            self.PUSH: self.push,
            self.POP: self.pop            
        }

    def load(self, program_filename):
        """Load a program into memory."""

        address = 0

        with open(program_filename) as f:  # opens file
            for line in f:  # reads file line by line
                # try:
                # print(line, end='')  # prints line by line and gets rid of extra lines (end='' prints %)
                # line = int(line) # turns the line into int instead of string, line = int(line, 2) 2 means is added for binary
                line = line.split('#')
                line = line[0].strip()  # list
                # except ValueError:
                if line == '':
                    continue
                # turns the line into int instead of string store the address in memory
                self.ram[address] = int(line, base=2)

                address += 1  # add one and goes to the next

    # MAR contains the address that is being read or written to.
    #ram_read() should accept the address (MAR) to read and return the value stored #there.

    def ram_read(self, MAR):
        return self.ram[MAR]

    # MDR contains the data that was read or the data to write.
    # ram_write() should accept a value(MDR) to write, and the address (MAR) to write it to.

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR


    # Branch Table

    def ldi(self):
        # print("HI")
        register_num = self.ram_read(self.pc + 1)  # operand_a (address)
        value = self.ram_read(self.pc + 2)  # operand_b (value)
        # adds the value to the register
        self.reg[register_num] = value
        # print('-----------------')
        # print(f'LDI: value ', self.reg[register_num])
        self.pc += 3
    
    def multiply(self):
        num_reg_a = self.ram_read(self.pc + 1)
        num_reg_b = self.ram_read(self.pc + 2)
        self.alu('MULT', num_reg_a, num_reg_b)
        self.pc += 3

    def prn(self):
        register_num = self.ram_read(self.pc + 1)  # operand_a (address)
        value = self.reg[register_num]
        # print('-----------------')
        print(value)
        self.pc += 2

    def push(self):
        # decrement the stack pointer 
        self.reg[self.SP] -= 1
        
        #copy value from register into memory
        register_num = self.ram[self.pc + 1]
        value = self.reg[register_num]  # this value to push

        stack_position = self.reg[self.SP] # index into memory
        self.ram[stack_position] = value # store the value on the stack
        
        self.pc += 2

    def pop(self):
        # current stack pointer position
        stack_position = self.reg[self.SP]

        # get current value from memory(RAM) from stack pointer
        value = self.ram[stack_position]

        # add the value to the register
        register_num = self.ram[self.pc + 1]
        self.reg[register_num] = value
        # Increment the stack pointer position
        self.reg[self.SP] += 1

        self.pc += 2

    def halt(self):
        self.running = False
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self, LABEL=str()):

        print(f"{LABEL} TRACE --> PC: %02i | RAM: %03i %03i %03i | Register: " % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02i" % self.reg[i], end='')

            print(" | Stack:", end='')

            for i in range(240, 244):
                print(" %02i" % self.ram_read(i), end='')

        print()

    def run(self):
        """Run the CPU."""
        # self.trace()
        # print('-----------------')

        # Program counter, the index (address) of the current instruction
        # Reads the memory address that's stored in register
        # PC = self.pc
        # print(f'Run: pc', PC)

        # print('-----------------')
        # Figures out the instruction length to make the while loop more readable
        #instruction_length = ???
        while self.running:

            # Stores the result in "Instruction Register" from the memory (RAM) address from the program
            IR = self.ram_read(self.pc)

            if self.branchtable.get(IR):
                self.trace()
                self.branchtable[IR]()
            else:
                print('Unknown instruction')
                self.trace("End")
                self.running = False
