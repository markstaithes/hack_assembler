"""A Hack assembler that takes as input an assembly program with extension .asm,
and outputs a hack machine language program with extension .hack.
The assembler is called via command line, with the first
positional argument following the program name being a hack assembly file, eg:
    'python3 assembler.py program_name.asm'
The specification for this assembler guarantees that the input assembly program
is correct."""

import sys

arguments = sys.argv[:]
assert len(arguments) == 2, "improper command line input"
filename = sys.argv[1]
src = Parser(filename)
code = Evaluator()
newfilename = filename.split('.')[0] + '.hack'
machine_code = open(newfilename, w)
instruct_num = 0
binary_command = ''
while src.has_more_commands():
    instruct_num +=1
    if src.is_a_instruct():
        address = src.address
        binary_address = code.val2bin(address)
        binary_command = '0' + binary_address
    elif src.is_c_instruct():
        binary_command = '111'
        binary_command += code.dest_eval(src.dest)
        binary_command += code.comp_eval(src.comp)
        binary_command += code.jump_eval(src.jump)
    machine_code.write(binary_command + '\n')
    src.advance()
machine_code.close()

class Parser:
    """ A Parser object encapsulates access to the input code. Reads an
    assembly language command, parses it, and provides convenient access to the
    command's components (fields and symbols). In addition, removes all white
    space and comments."""
    def __init__(self, infile):
        self.instructions = Parser.clean_lines(infile)
        self.advance()

    def clean_lines(program_file):
        instructions = []
        with open(program_file) as f:
            for line in f:
                if line[0] == '/':
                    pass #ignore comments
                line = line.strip(' /')
                if line == '':
                    pass #ignore empty lines
                cleanline = ''
                for char in line:
                    if char == '/':
                        break #ignore comments
                    cleanline += char
                cleanline.strip() #remove whitespace between instructions and comments
                instructions.append(cleanline) 
         return instructions

    def is_l_instruct(self):
        return self.command[0] == '('

    def is_a_instruct(self):
        return self.command[0] == '@'

    def is_c_instruct(self):
        return not self.is_l_instruct() and not self.is_a_instruct():
    
    def has_more_commands(self):
        return self.instructions is not []

    def advance(self):
        self.command = self.instructions.pop(0)
        if self.is_a_instruct():
            self.address = self.command[1:]
        #if c instruct, parse the c instruction fields
        elif self.is_c_instruct():
            command_fields = self.command.split('=')
            destination = command_fields[0]
            # c commands may be 3 or 2 fields. If 3 fields, ';' denotes the start
            # of the third, ie the jump field follows ';'
            command_fields = command_fields[1].split(';')
            if len(command_fields) == 2:
                computation = command_fields[0]
                jump = command_fields[1]
            else:
                computation = command_fields[0]
                jump = ''
            self.dest = destination
            self.comp = computation
            self.jump = jump
        elif self.is_l_instruct
            ####
            ## Implement after successful testing for non-symbolic programs
            ###
            pass
        else:
            raise TypeError('invalid command
            "{command}"'.format(command=self.command)

    @property
    def dest(self):
        return self.dest

    @property
    def comp(self):
        return self.comp

    @property
    def jump(self):
        return self.jump
    
    @property
    def address(self):
        return self.address

class Evaluator:
    """An evaluator object provides the facility for translating Hack assembly
    mnemonics into binary code according to the specifications of the Hack
    assembly language."""
    
    def __init__(self):
        self.dest_dic()
        self.comp_dic()
        self.jump_dic() 

    def dest_dic(self):
        """Implements a hash table for the c-instruction destination field 
        mnemonics of the Hack assembly language."""
        pass

    def comp_dic(self):
        """Implements a hash table for the c-instruction computation field 
        mnemonics of the Hack assembly language."""
        pass
    
    def jump_dic(self):
        """Implements a hash table for the c-instruction jump field  mnemonics 
        of the Hack assembly language."""
        pass

    def val2bin(value):
        """Converts a decimal value to binary"""
        pass

    def dest_eval(destination):
        """Converts a c-command destination mnemonic to binary"""    
        pass

    def comp_eval(computation):
        """Converts a c-command computation mnemonic to binary"""
        pass
    
    def jump_eval(jump):
        "Converts a c-command jump mnemonic to binary"""
        pass


