import sys
# open a filename

# try:
#     f = open('print8.ls8', 'r')
#     lines = f.read()
#     # print(lines)

#     raise Exception('hi')
# except:
#     print(f.closed)

# print(len(sys.argv))

if (len(sys.argv)) != 2:
    print("remember to pass the second file name")
    print("usage: python3 fileio.py <second_file_name.py>")
    sys.exit()

try:
    with open(sys.argv[1]) as f:
        for line in f:
            # parse the file to isolate the binary opcodes
            possible_number = line[:line.find('#')]
            if possible_number == '':
                continue # skip to next iteration of loop
            
            regular_int = int(possible_number, 2)
            print(regular_int)

            # line = line[:line.find('#')].strip()

except FileNotFoundError:
    print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
    sys.exit()