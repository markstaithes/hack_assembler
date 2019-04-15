"""A Hack assembler that takes as input an assembly program with extension .asm,
and outputs a hack machine language program with extension .hack.
The assembler is called via command line, with the first
positional argument following the program name being a hack assembly file, eg:
    'python3 assembler.py program_name.asm'
The specification for this assembler guarantees that the input assembly program
is correct."""

import sys
import parse_eval

arguments = sys.argv[:]
assert len(arguments) == 2, "improper command line input"
filename = sys.argv[1]
src = parse_eval.Parser(filename)
code = parse_eval.Evaluator()
newfilename = filename.split('.')[0] + '.hack'
machine_code = open(newfilename, 'w')
instruct_num = 0
binary_command = ''
while src.has_more_commands():
    src.advance()
    instruct_num +=1
    if src.is_a_instruct():
        address = int(src.address)
        binary_command = '{0:016b}'.format(address)
    elif src.is_c_instruct():
        binary_command = '111'
        binary_command += code.comp_eval(src.comp)
        binary_command += code.dest_eval(src.dest)
        binary_command += code.jump_eval(src.jump)
    elif src.is_l_instruct():
        pass
    machine_code.write(binary_command + '\n')
machine_code.close()
