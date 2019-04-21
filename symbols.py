"""A module containing the symbol table used by a Hack assembler while
translating an assembly program."""

class SymbolTable:
    """A SymbolTable object contains a dictionary mapping symbols (found in
    assembly programs), to their associated values, and facilities for accessing
    the dictionary."""

    def __init__(self):
        self.create_table()

    def create_table(self):
        """Create the symbol table, and add the predefined symbols of the Hack 
        assembly language"""
        
        table = {
        'SP' : 0,
        'LCL' : 1,
        'ARG' : 2,
        'THIS' : 3,
        'THAT' : 4,
        'R0' : 0,
        'R1' : 1,       
        'R2' : 2,   
        'R3' : 3,       
        'R4' : 4,
        'R5' : 5,
        'R6' : 6,       
        'R7' : 7,   
        'R8' : 8,       
        'R9' : 9,
        'R10' : 10,
        'R11' : 11,       
        'R12' : 12,   
        'R13' : 13,       
        'R14' : 14,
        'R15' : 15,
        'SCREEN' : 16384,
        'KBD' : 24576
        }
        self.table = table

    def add_symbol(self, symbol, value):
        """Adds a symbol to the symbol table"""

        self.table[symbol] = value

    def get_value(self, symbol):
        """Returns the value associated with the input symbol/key in the symbol
        table. If there is no such key, returns None."""

        if symbol in self.table:
            return self.table[symbol]
        else:
            return None

    def in_table(self, symbol):
        """Returns True if the input symbol is in the symbol table."""
        
        return True if symbol in self.table else False
