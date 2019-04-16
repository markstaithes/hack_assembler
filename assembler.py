"""A Hack assembler that takes as input an assembly program with extension .asm,
and outputs a hack machine language program with extension .hack.
The assembler is called via command line, with the first
positional argument following the program name being a hack assembly file, eg:
    'python3 assembler.py program_name.asm'
The specification for this assembler guarantees that the input assembly program
is correct."""

import sys
import parse_eval
import symbols

arguments = sys.argv[:]
assert len(arguments) == 2, "improper command line input"
filename = sys.argv[1]
newfilename = filename.split('.')[0] + '.hack'
machine_code = open(newfilename, 'w')
# First pass over file creates entries for each loop variable in the symbol table
# No instructions are written the first pass
first_pass = True
table = symbols.SymbolTable()
for _ in range(2):
    src = parse_eval.Parser(filename)
    code = parse_eval.Evaluator()
    instruct_num = 0 
    # variable used to assign a memory location to new address variables
    # starts at 16 by spec of Hack assembly language
    var_mem_loc = 16
    binary_command = ''
    while src.has_more_commands():
        src.advance()
        instruct_num +=1
        if src.is_a_instruct():
            if first_pass:
                break
            src.parse_a_instruct()
            try:
                address = int(src.address)
            except TypeError: # address is a symbol
                # if the symbol is not in the symbol table
                if not table.get_value(address): 
                    table.add_symbol(address, var_mem_loc)
                    var_mem_loc += 1
                address = table.get_value(address)
            binary_command = '{0:016b}'.format(address)
        elif src.is_c_instruct():
            if first_pass:
                break
            src.parse_c_instruct()
            binary_command = '111'
            binary_command += code.comp_eval(src.comp)
            binary_command += code.dest_eval(src.dest)
            binary_command += code.jump_eval(src.jump)
        elif src.is_l_instruct():
            if not first_pass:
                break
            symbol = src.parse_l_instruct()
            table.add_symbol(symbol, instruct_num)
        else:
            raise TypeError('invalid command "{command}"'.format(command=src.command))
        if not first_pass:
            machine_code.write(binary_command + '\n')   
    if first_pass:
        first_pass = False
machine_code.close()
