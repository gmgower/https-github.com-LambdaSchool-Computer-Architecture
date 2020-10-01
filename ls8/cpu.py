  
"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0  # Program counter, the index (address) of the current instruction
        self.ram = [0] * 256 # length and the index will stop at 255
        self.register = [0] * 8 # returns 8 zeros and stores values (0-7)

     # MAR contains the address that is being read or written to.
    #ram_read() should accept the address (MAR) to read and return the value stored #there.
    def ram_read(self, MAR):
        # MAR is mem address register to read data from
        return self.ram[MAR]

    # MDR contains the data that was read or the data to write.
    # ram_write() should accept a value(MDR) to write, and the address (MAR) to write it to.
    def ram_write(self, MAR, MDR):
        self.ram[MDR] = MAR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # read the memory address that's stored in register PC, 
        # and store that result in IR, the Instruction Register. 
        running = True

        while running:
            IR = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1) # register
            operand_b = self.ram_read(self.pc + 2) # immediate

            opcode = IR

            if opcode == HLT:
                sys.exit()

            # Set the value of a register to an integer.
            elif opcode == LDI:
                self.register[operand_a] = operand_b
                # Jump over operands to go to next instruction
                self.pc += 3

            # Print the register address
            elif opcode == PRN:
                print("HERE: ", self.pc)
                print(self.register[operand_a])
                self.pc += 2