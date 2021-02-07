#!/usr/bin/python

import unicodedata
import os
import sys

#== Data and variables =========================================

SysLib = {
    'inc'   : '1 +',
    'dec'   : '1 -',
    'over'  : '2 pick',
    'pick3' : '3 pick',
    'dup2'  : 'over over',
    'dupdu' : 'dup dup',
    'swap'  : '2 roll',
    'rot'   : '3 roll',
    'unrot' : '3 rolld',
    'rolla' : 'depth roll',
    'rollad': 'depth rolld',
    'drop2' : '2 dropn',
    'nip'   : 'swap drop',
    'neg'   : '0 swap -',
    'keep1' : 'rollad depth 1 - dropn',
    'keep2' : 'rollad rollad depth 2 - dropn',
    ':'     : 'ip dec swap sto',
    '+='    : 'dup rot + swap dup rot swap = $',
    '++'    : '1 swap +=',
    '-='    : 'dup rot + swap dup rot swap = $',
    '--'    : '1 swap -=',
    '*='    : 'dup rot + swap dup rot swap = $',
    '/='    : 'dup rot + swap dup rot swap = $',
    '%='    : 'dup rot + swap dup rot swap = $',
}



#== Functions ==================================================

class RPN_Calc :
    Run = True
    VarStack = []
    VarStackBackup = []
    Memory = {}
    MemoryBackup = {}
    CommandStack = []
    ip = 0
    Errors = []
    round_max = 11
    round = round_max
    file_name_memory = "memory.rpn"
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError: return False
        try:
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):  return False
        return True
    def is_string(self, s):
        return not self.is_number(s)
        if s[0] == '"' and s[-1] == '"' : return True
        if s[0] == "'" and s[-1] == "'" : return True
        return False
    def check_quotation_oddity(self, string):
        if not (string.count('"') % 2 == 0 and string.count("'") % 2 == 0) :
            self.erorr_quotation()
            return False
        return True
    def extract_quoted(self, string) :
        if string.count('"') + string.count("'") == 0 :
            return string
        if string[0] == '"' and string[-1] == '"' :
            return string[1:-1]
        if string[0] == "'" and string[-1] == "'" :
            return string[1:-1]
        return string
    def print_status(self) :
        print()
        print("[", len(self.VarStack), "]", ':', self.ip)
        for var in self.VarStack:
            if self.is_number(var) : 
                if var.is_integer() : var = int(var)
                print(" ", round(var, self.round))
            else : print(" ", var)
        return None
    def backup(self) :
        self.VarStackBackup = self.VarStack.copy()
        return True
    def undo(self) :
        self.VarStack = self.VarStackBackup
        return True
    def error(self, message) :
        print(message)
        return None
    def error_index(self) :
        self.Errors.append("Error: Insufficient arguments in STACK")
        return None
    def error_not_string(self) :
        self.Errors.append("Error: value is not a String")
        return None
    def error_no_variable(self):
        self.Errors.append("Variable undefined")
        return None
    def erorr_quotation(self):
        self.Errors.append("Quotation error: quotes count not odd")
        return None
    def save_memory_needed (self) :
        self.MemoryBackup = self.Memory.copy()
        self.load_memory()
        needed = self.Memory != self.MemoryBackup
        if needed : self.Memory = self.MemoryBackup
        return needed
    def get_current_path (self) :
        return os.path.dirname( os.path.abspath( sys.argv[0] ))
    def get_file_name_memory (self) :
        return self.get_current_path() + os.sep + self.file_name_memory
    def save_memory(self) :
        if not self.save_memory_needed() : return None
        f = open(self.get_file_name_memory(), "w")
        for key in self.Memory :
            f.write(self.Memory[key] +' '+ key +' '+ 'sto')
        f.close()
        return None
    def load_memory (self) :
        f = open(self.get_file_name_memory(), 'r')
        for line in f.readlines() :
            self.interpret(line)
        f.close()
        return True
    def pop(self) :
        if len(self.Errors) : return None
        try:
            return self.VarStack.pop()
        except IndexError : self.error_index()
    def pop_number(self) :
        value = self.pop()
        if len(self.Errors) : return None
        if value is None : return None
        if self.is_string(value) :
            if value in self.Memory :
                self.interpret( self.Memory[value] )
                return self.pop_number()
            else : 
                self.error_no_variable()
                return None
        return value
    def push (self, value) :
        if self.is_number(value) : 
            value = float(value)
            value = round(value, self.round_max)
        self.VarStack.append(value)
    def push_command(self, command) : 
        if self.ip == len(self.CommandStack) : self.ip += 1
        self.CommandStack.append(command)
    def interpret_single_ariphmetic_div (self, command) :
        if command == '/' :
            x = self.pop()
            y = self.pop()
            if len(self.Errors) : return False
            self.push( y / x )
            return True
        if command == '%' :
            x = self.pop()
            y = self.pop()
            if len(self.Errors) : return False
            self.push( y % x )
            return True
        return False
    def interpret_single_ariphmetic (self, command):
        if command == 'sum' : 
            nums = []
            for i in self.VarStack :
                if self.is_number(i) : nums.append(i)
            self.push( sum(nums) )
            return True
        if command == '+' :
            x = self.pop_number()
            y = self.pop_number()
            if len(self.Errors) : return False
            self.push( y + x )
            return True
        if command == '-' :
            x = self.pop_number()
            y = self.pop_number()
            if len(self.Errors) : return False
            self.push( y - x )
            return True
        if command == '*' :
            x = self.pop_number()
            y = self.pop_number()
            if len(self.Errors) : return False
            self.push( y * x )
            return True
        if command in ['**', '^'] :
            x = self.pop_number()
            y = self.pop_number()
            if len(self.Errors) : return False
            self.push( y ** x )
            return True
        return False
    def interpret_single_roll (self, command):
        if command == 'roll' :
            depth = int(self.pop())
            if depth <= 1 : return True
            a = []
            for i in range(1, depth+1) : a.append( self.pop() )
            if len(self.Errors) : return False
            for i in range(depth-2, -1, -1) : self.push( a[i] )
            self.push( a[depth-1] )
            return True
        return False
    def interpret_single_rolld (self, command) :
        if command == 'rolld' :
            depth = int(self.pop())
            if depth <= 1 : return True
            a = []
            for i in range(1, depth+1) : a.append( self.pop() )
            if len(self.Errors) : return False
            self.push( a[0] )
            for i in range(depth-1, 1-1, -1) : self.push( a[i] )
            return True
        return False
    def interpret_single_pick (self, command):
        if command == 'pick' :
            x = int( self.pop() )
            if len(self.Errors) : return False
            try :
                y = self.VarStack[-x]
                self.push( y )
            except IndexError : self.error_index()
            return True
        if command == 'unpick' :
            i = self.pop()
            value = self.pop()
            if len(self.Errors) : return False 
            try : self.VarStack[int(-i)] = value
            except IndexError : self.error_index()
            return True
        return False
    def interpret_single_dup (self, command) :
        if command in ['dup', 'push'] : 
            last = self.pop()
            if len(self.Errors) : return False
            self.push( last )
            self.push( last )
            return True
        if command == 'dupn' :
            x = int( self.pop() )
            if len(self.Errors) : return False
            try :
                for i in range(x) :
                    y = self.VarStack[-x]
                    self.push( y )
            except IndexError : self.error_index()
            return True
        if command == 'ndupn' :
            n = self.pop()
            value = self.pop()
            if len(self.Errors) : return False
            for i in range( int(n) ) :
                self.push( value )
            self.push( n )
            return True
        return False
    def interpret_single_drop (self, command) :
        if command in ['drop', 'pop'] : 
            self.pop()
            if len(self.Errors) : return False
            return True
        if command == 'dropn' : 
            n = int( self.pop() )
            for i in range(n) : self.pop()
            if len(self.Errors) : return False
            return True
        return False
    def interpret_single_helper (self, command) :
        if command == 'depth' : 
            self.push( float( len(self.VarStack) ) )
            return True
        if command in ['clear', 'clr'] : 
            self.VarStack.clear()
            return True
        if command in ['eval'] :
            value = self.pop()
            if len(self.Errors) : return False
            if not self.is_string(value) : return True
            value = self.extract_quoted(value)
            self.interpret( value )
            return True
        if command in ['ip'] :
            self.push(self.ip)
            return True
        return False
    def interpret_single_memory (self, command) :
        if command in ['store', 'str', 'sto', '='] :
            name = self.pop()
            value = self.pop()
            if len(self.Errors) : return False
            if not self.is_string(name) : 
                self.error_not_string()
                return False
            self.Memory[name] = str(value)
            return True
        if command in ['read', 'recall', 'rcl', '$'] :
            name = self.pop()
            if len(self.Errors) : return False
            if not self.is_string(name) : 
                self.error_not_string()
                return False
            if name in self.Memory : 
                self.interpret( self.Memory[name] )
            else : self.error_no_variable()
            return True
        if command in ['purge'] :
            name = self.pop()
            if len(self.Errors) : return False
            if not self.is_string(name) : 
                self.error_not_string()
                return False
            if name in self.Memory : 
                del self.Memory[name]
            return True
        return False
    def interpret_single_save (self, command) :
        if command == 'save' :
            self.save_memory()
            return True
        if command == 'load' :
            self.load_memory()
            return True
        return False
    def interpret_single (self, command):
        if len(self.Errors) : return False
        if self.is_number(command) : 
            self.push(float(command))
            return True
        if command in SysLib : 
            self.interpret(SysLib[command])
            return True
        if self.interpret_single_ariphmetic(command) :      return True
        if self.interpret_single_ariphmetic_div(command) :  return True
        if self.interpret_single_roll(command) :            return True
        if self.interpret_single_rolld(command) :           return True
        if self.interpret_single_pick(command) :            return True
        if self.interpret_single_dup(command) :             return True
        if self.interpret_single_drop(command) :            return True
        if self.interpret_single_helper(command) :          return True
        if self.interpret_single_memory(command) :          return True
        if self.interpret_single_save(command) :            return True
        if command in ["exit", "quit", "close", 'q'] :
            self.save_memory()
            self.Run = False
            return True
        #self.Errors.append('Command unknown')
        if self.is_string(command) : 
            self.push(command)
            return True
        return False
    def interpret(self, command_string) :
        if not self.check_quotation_oddity(command_string):
            return None
        for command in command_string.split():
            # $variable => variable $
            if command[0] == '$' and len(command) > 1 : 
                self.interpret(command[1:] +' '+ command[0])
                continue
            # string: => string :
            # variable$ => variable $
            if command[-1] in [':', '$'] and len(command) > 1: 
                self.interpret(command[0:-1] +' '+ command[-1])
                continue
            # if last part of string is ++ or -- add a space
            tail = command[len(command)-2:]
            if len(command) > 2 and (tail == '++' or tail == '--') :
                self.interpret(command[:-2] +' '+ tail)
                continue
            # execute command as a simple single command and push it to the command history stack if it is ok
            if calc.interpret_single(command) : 
                self.push_command(command)
            else : break
        return None 



#== Command loop ===============================================
calc = RPN_Calc()
calc.load_memory()
while calc.Run :
    if len(calc.Errors) : calc.undo()
    calc.print_status()
    for error in calc.Errors :
        print(error)
        calc.Errors.clear()
    commandString = input("> ")
    calc.backup()
    calc.interpret(commandString)
