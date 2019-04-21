"""
A module containing the Parser and Evaluator classes used by HackAssembler
objects.
"""

class Parser:
    """ A Parser object encapsulates access to the input code. Reads an
    assembly language command, parses it, and provides convenient access to the
    command's components (fields and symbols). In addition, removes all white
    space and comments."""

    def __init__(self, infile):
        self.instructions = self.clean_lines(infile)

    def clean_lines(self, program_file):
        """This method 'cleans' the input instructions, given by an input
        assembly file, and outputs a python list of strings, each string being
        a Hack assembly instruction. The 'cleaning' is done  by removing all
        comments and whitespace."""

        instructions = []
        with open(program_file) as f:
            for line in f:
                if line[0] != '/': # ignore comments
                    line = line.strip(' \n') # remove whitespace and eol
                    if line != '': # ignore empty lines
                        instructions.append(line)
        instructions = list(map(self.remove_comments, instructions))
        return instructions

    def remove_comments(self, line):
        """Takes as input  a line(string) of Hack assembly code. Removes inline
        comments from the line.
        Outputs the clean line as a string."""

        cleanline = ''
        for char in line:
            if char == '/':
                break
            cleanline += char
        cleanline = cleanline.strip()
        return cleanline

    def is_l_instruct(self):
        """Returns True if the current instruction is a loop var declaration."""

        return self.command[0] == '('

    def is_a_instruct(self):
        """Returns True if the current instruction is an a-instruction."""

        return self.command[0] == '@'

    def is_c_instruct(self):
        """Returns True if the current instruction is a c-instruction."""

        return not self.is_l_instruct() and not self.is_a_instruct()
    
    def has_more_commands(self):
        """Returns True if there are assembly instruction remaining, ie if there
        are still instructions to be parsed."""

        return True if self.instructions else False

    def advance(self):
        """Assigns the next assembly instruction as the current instruction, ie
        current instruction being parsed. Removes the assembly instruction from
        the list of assembly instructions."""

        self.command = self.instructions.pop(0)
    
    def parse_a_instruct(self):
        """Parses an a-instruction and assigns the address to the corresponding
        instance attribute."""
        
        self.address = self.command[1:]

    def parse_c_instruct(self):
        """Parses a c-instruction into the 3 c instruction fields, ie
        destination, computation and jump. Binds these fields to the
        corresponding instance attributes."""

        if '=' in self.command and ';' in self.command:
                fields = self.command.split('=')
                destination = fields[0]
                fields = fields[1].split(';')
                computation = fields[0]
                jump = fields[1]
        # if ';' is omitted, then jump is null
        elif '=' in self.command:
            fields = self.command.split('=')
            destination = fields[0]
            computation = fields[1]
            jump = ''
        # if '=' is ommitted, then dest is null
        elif ';' in self.command:
            fields = self.command.split(';')
            computation = fields[0]
            jump = fields[1]
            destination = ''
        # if both '=' and ';' are omitted, then both dest and jump are null
        else:
            computation = self.command
            destination = jump = ''
        self.dest = destination
        self.comp = computation
        self.jump = jump

    def parse_l_instruct(self):
        """Parses a loop variable declaration, ie an 'l-instruction.'  
        Returns the 'instruction' minus  the first and last characters (ie the
        parens), which is the loop var name."""

        return self.command[1:][:-1]

class Evaluator:
    """An evaluator object provides the facility for translating Hack assembly
    mnemonics into binary code according to the specifications of the Hack
    assembly language."""
    
    def __init__(self):
        self.dest_dic()
        self.comp_dic()
        self.jump_dic() 

    def dest_dic(self):
        """Implements a dictionary for the c-instruction destination field 
        mnemonics of the Hack assembly language."""
        
        self.dest = {
        '' : '000', 
        'M' : '001', 
        'D' : '010', 
        'MD' : '011', 
        'A' : '100', 
        'AM' : '101', 
        'AD' : '110', 
        'AMD' : '111'
        }

    def comp_dic(self):
        """Implements a dictionary for the c-instruction computation field 
        mnemonics of the Hack assembly language."""

        self.comp = {
        '0' : '0101010',
        '1' : '0111111',
        '-1' : '0111010',
        'D' : '0001100',
        'A' : '0110000',
        '!D' : '0001101',
        '!A' : '0110001',
        '-D' : '0001111',
        '-A' : '0110011',
        'D+1' : '0011111',
        'A+1' : '0110111',
        'D-1' : '0001110',
        'A-1' : '0110010',
        'D+A' : '0000010',
        'D-A' : '0010011',
        'A-D' : '0000111',
        'D&A' : '0000000',
        'D|A' : '0010101',
        'M' : '1110000',
        '!M' : '1110001',
        '-M' : '1110011',
        'M+1' : '1110111',
        'M-1' : '1110010',
        'D+M' : '1000010',
        'D-M' : '1010011',
        'M-D' : '1000111',
        'D&M' : '1000000',
        'D|M' : '1010101'
        }
    
    def jump_dic(self):
        """Implements a dictionary for the c-instruction jump field  mnemonics 
        of the Hack assembly language."""

        self.jump = {
        '' : '000',
        'JGT' : '001',
        'JEQ' : '010',
        'JGE' : '011',
        'JLT' : '100',
        'JNE' : '101',
        'JLE' : '110',
        'JMP' : '111'
        }

    def dest_eval(self, destination):
        """Converts a c-command destination mnemonic to binary"""    
        return self.dest[destination]

    def comp_eval(self, computation):
        """Converts a c-command computation mnemonic to binary"""
        return self.comp[computation]
    
    def jump_eval(self, jump):
        "Converts a c-command jump mnemonic to binary"""
        return self.jump[jump]
