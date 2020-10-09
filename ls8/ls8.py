#!/usr/bin/env python3

"""Main."""
import sys
from cpu import *
cpu = CPU()
# Parse the CLI for submitted program commands
# program_file_test = sys.argv
program = sys.argv[1]
cpu.load(program)
cpu.run()

#!/usr/bin/env python3

# """Main."""

# import sys
# from cpu import *

# cpu = CPU()

# cpu.load(sys.argv[1])
# cpu.run()