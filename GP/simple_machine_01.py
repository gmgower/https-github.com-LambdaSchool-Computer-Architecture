import sys


PRINT_TIM      = 0b00000001
HALT           = 0b00000010
PRINT_NUM      = 0b01000011
SAVE           = 0b10000100  # LDI
PRINT_REGISTER = 0b01000101
ADD            = 0b10000110


memory = [0] * 256


def load_memory():
    if (len(sys.argv)) != 2:
        print("remember to pass the second file name")
        print("usage: python3 fileio.py <second_file_name.py>")
        sys.exit()

    address = 0
    try:
        with open(sys.argv[1]) as f:
            for line in f:
                # parse the file to isolate the binary opcodes
                possible_number = line[:line.find('#')]
                if possible_number == '':
                    continue # skip to next iteration of loop
                
                instruction = int(possible_number, 2)

                memory[address] = instruction

    except FileNotFoundError:
        print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
        sys.exit()

load_memory()
          
# cabinets in your shop: registers
# storage unit: cache
# warehouse outside town: RAM


# registers
# physically located on CPU, treat as variables

# R0-R7
registers = [0] * 8

# cpu should now step through memory and take actions based on commands it finds

# a data-driven machine

# program counter, a pointer
pc = 0
running = True

while running:
    command = memory[pc]

    num_args = command >> 6

    if command == PRINT_TIM:
        print("tim!")

    elif command == PRINT_NUM:
        number = memory[pc + 1]
        print(number)

    elif command == SAVE:
        # get out the arguments
        # pc+1 is reg idx, pc+2 value
        reg_idx = memory[pc + 1]
        value = memory[pc + 2]

        # put the value into the correct register
        registers[reg_idx] = value

    elif command == PRINT_REGISTER:
        # get out the argument
        reg_idx = memory[pc + 1]
        
        # the argument is a pointer to a register
        value = registers[reg_idx]
        print(value)

    elif command == ADD:
        # pull out the arguments
       reg_idx_1 = memory[pc + 1] 
       reg_idx_2 = memory[pc + 2] 

        # add regs together
       registers[reg_idx_1] = registers[reg_idx_1] + registers[reg_idx_2]

    elif command == HALT:
        running = False

    else:
        print('unknown command!')
        running = False

    pc += 1 + num_args