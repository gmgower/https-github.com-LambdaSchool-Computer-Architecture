"""CPU functionality."""

import sys

# program_filename = sys.argv[1]
# print(program_filename)
# sys.exit()
# print(sys.argv)
# sys.exit()

LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111
HLT = 0b00000001


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
        self.running = True
        # self.LDI = 0b10000010
        # self.PRN = 0b01000111
        # self.HLT = 0b00000001

        # self.MULT = 0b10100010

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

    # MAR contains the address that is being read or written to.
    #ram_read() should accept the address (MAR) to read and return the value stored #there.

    def ram_read(self, MAR):
        return self.ram[MAR]

    # MDR contains the data that was read or the data to write.
    # ram_write() should accept a value(MDR) to write, and the address (MAR) to write it to.

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

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
            # register_num = self.ram_read(PC + 1) # operand_a (address)
            # value = self.ram_read(PC + 2) # operand_b (value)
            # print('-----------------')
            # print(f"run: IR:",IR)
            # print('-----------------')

            # self.trace()
            if IR == LDI:
                self.trace()
                # print("HI")
                register_num = self.ram_read(
                    self.pc + 1)  # operand_a (address)
                value = self.ram_read(self.pc + 2)  # operand_b (value)
                # adds the value to the register
                self.reg[register_num] = value
                # print('-----------------')
                # print(f'LDI: value ', self.reg[register_num])
                self.pc += 3

            elif IR == MUL:
                num_reg_a = self.ram_read(self.pc + 1)
                num_reg_b = self.ram_read(self.pc + 2)
                self.alu('MULT', num_reg_a, num_reg_b)
                self.pc += 3

            elif IR == PRN:
                self.trace()
                register_num = self.ram_read(
                    self.pc + 1)  # operand_a (address)
                value = self.reg[register_num]
                # print('-----------------')
                print(value)
                self.pc += 2

            elif IR == HLT:
                self.trace()
            #     # print('LLLLL')
                self.running = False

            else:

                print('Unknown instruction')
                self.running = False