"""A Hack assembler that takes as input an assembly program with extension .asm,
and outputs a hack program with extension .hack.
The assembler is called via command line, with the first
positional argument following the program name being a hack assembly file, eg:
    'python3 assembler.py program_name.asm'
The specification for this assembler guarantees that the input assembly program
is correct."""

import sys
import parse_eval
import symbols

class HackAssembler:
    """HackAssembler objects are the driver of the two-pass assembly process. 
    They take a Hack assembly program filename as input, and provide the 
    facilities for generating a Hack program as output. 
    """

    def __init__(self, filename):
        self.assembly_file = filename
        self.create_hack_file(filename)
        self.table = symbols.SymbolTable()

    def create_hack_file(self, filename):
        """Creates a new .hack file in the current directory and opens it for
        writing. The file object is bound to the instance attribute
        self.machine_code. 
        Takes as input a filename for a Hack assembly file in the 
        program's parent directory. Output filename is identical to input
        filename, ie:
        input = program.asm
        output = program.hack
        """
        
        if filename.endswith('.asm'):
            newfilename = filename.replace('.asm', '.hack')
        else:
            raise TypeError('improper file type: expecting a .asm file')
        self.machine_code = open(newfilename, 'w')

    def write_hack_file(self, command):
        """Writes a single line to the Hack machine code output file"""
        
        self.machine_code.write(command + '\n')  
    
    def close_hack_file(self):
        """Closes the Hack machine code output file for writing"""
        
        self.machine_code.close()

    def first_pass(self):
        """Identifies all the loop var instructions in the assembly program and
        adds the corresponding entries to the symbol table. No instructions are
        written the first pass. Invalid command types raise an Exception.
        """
        
        src = parse_eval.Parser(self.assembly_file)
        code = parse_eval.Evaluator()
        instruct_num = -1
        while src.has_more_commands():
            src.advance()
            # the first pass is only concerned with identifying loop variables
            if src.is_a_instruct() or src.is_c_instruct():
                instruct_num += 1
            elif src.is_l_instruct():
                # loop var instructions are not actual instructions, so the
                # instruction count does not increase
                symbol = src.parse_l_instruct()
                self.table.add_symbol(symbol, instruct_num + 1)
            else:
                raise TypeError('invalid command "{command}"'.format(command=src.command))   

    def second_pass(self):
        """The essential function of the Assembler. For every assembly command
        in the input assembly file, a Hack machine language command is outputed
        to the Hack output file. Loop var declarations are
        ignored the second pass. Any other symbols in the assembly file are
        assumed to be address variables, and are added to the symbol table upon
        initial evaluation."""

        src = parse_eval.Parser(filename)
        code = parse_eval.Evaluator()
        instruct_num = -1
        # variable used to assign a memory location to new address variables
        # starts at 16 by spec of Hack assembly language
        var_mem_loc = 16
        binary_command = ''
        while src.has_more_commands():
            src.advance()
            if src.is_a_instruct():
                instruct_num +=1
                src.parse_a_instruct()
                try:
                    address = int(src.address)
                except ValueError: # address is a symbol
                    # if the symbol is not in the symbol table
                    if not self.table.in_table(src.address): 
                        self.table.add_symbol(src.address, var_mem_loc)
                        var_mem_loc += 1
                    address = self.table.get_value(src.address)
                binary_command = '{0:016b}'.format(address)
            elif src.is_c_instruct():
                instruct_num += 1
                src.parse_c_instruct()
                binary_command = '111'
                binary_command += code.comp_eval(src.comp)
                binary_command += code.dest_eval(src.dest)
                binary_command += code.jump_eval(src.jump)
            # loop var declarations are ignored.
            if not src.is_l_instruct():
                self.write_hack_file(binary_command)   
##########
###main###
##########
if __name__ == '__main__':
    arguments = sys.argv[:]
    assert len(arguments) == 2, "improper command line input"
    filename = arguments[1]
    assembler = HackAssembler(filename)
    assembler.first_pass()
    assembler.second_pass()
    assembler.close_hack_file()
