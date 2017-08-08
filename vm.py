class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=repr(self.type),
            value=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()

RESERVED = {
    'OR': Token('OP', 'OR'),
    'AND': Token('OP', 'AND'),
    'IF': Token('IF', 'IF'),
    'ELSE': Token('ELSE', 'ELSE'),
    'WHILE': Token('WHILE', 'WHILE'),
    'FUNCTION': Token('FUNCTION','FUNCTION')
}
LEFT_ASSOCIATIVITY = 0
RIGHT_ASSOCIATIVITY = 1
OPERATORS = {
'or' : (1, LEFT_ASSOCIATIVITY),
'and' : (2, LEFT_ASSOCIATIVITY),
'<' : (3, LEFT_ASSOCIATIVITY),
'<=' : (3, LEFT_ASSOCIATIVITY),
'>' : (3, LEFT_ASSOCIATIVITY),
'>=' : (3, LEFT_ASSOCIATIVITY),
'!=' : (3, LEFT_ASSOCIATIVITY),
'==' : (3, LEFT_ASSOCIATIVITY),
'+' : (4, LEFT_ASSOCIATIVITY),
'-' : (4, LEFT_ASSOCIATIVITY),
'*' : (5, LEFT_ASSOCIATIVITY),
'/' : (5, LEFT_ASSOCIATIVITY),
'//' : (5, LEFT_ASSOCIATIVITY),
'%' : (5, LEFT_ASSOCIATIVITY),
'**' : (6, RIGHT_ASSOCIATIVITY)
}

class Lexer():
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
        
    def id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED.get(result.upper(), Token('ID', result))
        return token
    
    def in_operator(self, char):
        return any(char in op for op in OPERATORS.keys()) 

    def operator(self):
        result = ''
        while self.current_char is not None and not self.current_char.isalpha() and self.in_operator(self.current_char):
            result +=self.current_char
            self.advance()
        if result == '=':
            return Token('=', '=')       
        elif result in OPERATORS.keys():
                return Token ('OP', result)
        else:
            self.error()
            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        token = Token('CONST', float(result))
        return token

    def get_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char == '\n':
                self.advance()
                tokens.append(Token('\n', '\n'))
                
            elif self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char.isalpha():
                tokens.append(self.id())

            elif self.current_char.isdigit():
                 tokens.append(self.number())
                
            elif self.current_char == '\n':
                self.advance()
                tokens.append(Token('\n', '\n'))
                
            elif self.in_operator(self.current_char):
                tokens.append(self.operator())

            elif self.current_char == ',':
                self.advance()
                tokens.append(Token(',', ','))
                
            elif self.current_char == '(':
                self.advance()
                tokens.append(Token('(', '('))

            elif self.current_char == '(':
                self.advance()
                tokens.append(Token('(', '('))

            elif self.current_char == ')':
                self.advance()
                tokens.append(Token(')', ')'))

            elif self.current_char == '{':
                self.advance()
                tokens.append(Token('{', '{'))

            elif self.current_char == '}':
                self.advance()
                tokens.append(Token('}', '}'))                                    
            else:
                self.error()
        return tokens

class Operator():
    def __init__(self,type):
        self.type= type


class Const():
    def __init__(self, value):
        self.value = value

class Assign():
    def __init__(self, name):
        self.name = name
        
class Var():
    def __init__(self, name):
        self.name = name
        
class FunctionDeclaration():
    def __init__(self, name, arguments, block):
        self.name = name
        self.arguments = arguments
        self.block = block
        
class FunctionCall():
    def __init__(self, name):
        self.name = name

class IfStatement():
    def __init__(self, condition, consequent, alternative):
        self.condition=condition
        self.consequent=consequent
        self.alternative=alternative
        
class WhileStatement():
    def __init__(self, condition, block):
        self.condition=condition
        self.block=block  

class RPN ():    #преобразование из инфиксной в постфиксную нотацию
    def __init__(self):
        self.out = []
        self.stack =[]
        
    def isoperator(self, token):
        return token.value in OPERATORS.keys()

    def associative(self, token, associativity):
        return OPERATORS[token.value][1] == associativity
    
    def precedence(self, token1, token2):
        return OPERATORS[token1.value][0] - OPERATORS[token2.value][0]
    
    def add_token(self, token):
        if self.isoperator(token):
            while len(self.stack) != 0 and self.isoperator(self.stack[-1]):
                if (self.associative(token, LEFT_ASSOCIATIVITY) and self.precedence(token, self.stack[-1]) <= 0)\
                   or (self.associative(token, RIGHT_ASSOCIATIVITY) and self.precedence(token, self.stack[-1]) < 0):
                    self.out.append(self.stack.pop())
                    continue
                break
            self.stack.append(token)
        elif token.type == '(':
            self.stack.append(token)
        elif token.type == ')':
            while len(self.stack) != 0 and self.stack[-1].type != '(':
                self.out.append(self.stack.pop())
            self.stack.pop()
        else:
            self.out.append(token)
            
    def end_of_expression(self):
        while len(self.stack) !=0:
            self.out.append(self.stack.pop())
        result = self.out
        self.out =[]
        return result
    
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.rpn = RPN()

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self, token_type):
        self.pos +=1
        if self.current_token.type == token_type:
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            else:
                self.current_token = Token('EOF',None)
        else:
            self.error()
            
    def new_line(self):
        while self.current_token.type == '\n':
            self.advance('\n')
            
    def statement_list(self):
        result = self.statement()
        while self.current_token.type == '\n':
            self.new_line()
            result+=self.statement()
        return result

    def statement(self):
        result= []
        if self.current_token.type == 'ID':
            if self.tokens[self.pos+1].type == '(':
                result+=self.function_call()
            else:
                result+=self.assignment_statement()
        elif self.current_token.type == 'FUNCTION':
            result.append(self.function_declaration())
        elif self.current_token.type == 'IF':
            result.append(self.if_statement())
        elif self.current_token.type == 'WHILE':
            result.append(self.while_statement())
        return result
    
    def if_statement(self):
        self.advance('IF')
        condition=self.expression()
        consequent=self.block()
        last_pos=self.pos
        self.new_line()
        if self.current_token.type == 'ELSE':
            self.advance('ELSE')
            alternative=self.block()
        else:
            self.pos=last_pos
            self.current_token = self.tokens[last_pos]
            alternative=[]
        
        return IfStatement(condition, consequent, alternative)
    
    def while_statement(self):
        self.advance('WHILE')
        condition=self.expression()
        block=self.block()
        return WhileStatement(condition,block)
        
    def block(self):
        self.new_line()
        self.advance('{')
        block=self.statement_list()
        self.advance('}')
        return block
    
    def function_call(self):
        result=[]
        name=self.current_token.value
        self.advance('ID')
        result+=self.arguments()
        result.append(FunctionCall(name))
        return result
    
    def arguments(self):
        result =[]
        self.advance('(')
        result.append(self.get_argument())
        while self.current_token.type == ',':
            self.advance(',')
            result.append(self.get_argument())
        self.advance(')')
        return result
    
    def get_argument(self):
        if self.current_token.type == 'ID':
            argument=Var(self.current_token.value)
            self.advance('ID')
            return argument
        else:
            argument=Const(self.current_token.value)
            self.advance('CONST')
            return argument
        
    def arguments_declaration(self):
        self.advance('(')
        result = [self.current_token.value]
        self.advance('ID')
        while self.current_token.type == ',':
            self.advance(',')
            result.append(self.current_token.value)
            self.advance('ID')
        self.advance(')')
        return result
    
    def function_declaration(self):
        self.advance('FUNCTION')
        name=self.current_token.value
        self.advance('ID')
        args=self.arguments_declaration()
        self.new_line()
        self.advance('{')
        block = self.statement_list()
        self.advance('}')
        return FunctionDeclaration(name, args, block)


    def assignment_statement(self):
        var=self.current_token.value
        self.advance('ID')
        self.advance('=')
        result=self.expression()
        result.append(Assign(var))
        return result
    
    def expression (self):
        result = []
        while self.current_token.type in ('OP','ID','CONST','(',')'):
            self.rpn.add_token(self.current_token)
            self.advance(self.current_token.type)
        for token in self.rpn.end_of_expression():
            if token.type == 'CONST':
                result.append(Const(token.value))
            elif token.type == 'OP':
                result.append(Operator(token.value))
            elif token.type == 'ID':
                result.append(Var(token.value))
        return result
        
    def parse(self):
        code = self.statement_list()
        if self.current_token.type == 'EOF':
            return code
        else:
            self.error()
        return code
    
class Interpreter():
    def __init__(self, code):
        self.code = code
        self.environment = {}
        self.stack = []
        
    def executing(self, command):
        method_name = 'execute_' + type(command).__name__
        execute = getattr(self, method_name, self.missing_method)
        return execute(command)

    def missing_method(self, command):
        raise Exception('Missing Execute_{} method'.format(type(command).__name__))

    def pop_n(self, n):
        if len(self.stack) < n:
            print ('not enough elements for pop: %d needed, %d left' % (n, len(self.stack)))
        top = self.stack[-n:]
        self.stack[-n:] = []
        return top

    def var_search (self, name):
        environment=self.environment
        while environment is not None and name not in environment:  #Поиск в текущем окружении и в родительских окружениях
            if '' in environment:
                environment=environment['']
            else:
                environment = None
        return environment

    def execute_Const(self, command):
        self.stack.append(command.value)

    def execute_Var(self, command):
        name=command.name
        environment = self.var_search(name)
        if environment:
            self.stack.append(environment[name])
        else:
            raise NameError(name)

    def execute_Assign(self, command):
        name=command.name
        environment = self.var_search(name)
        if environment:
            environment[name]=self.stack.pop()
        else:
            self.environment[name]=self.stack.pop()
        
    def execute_Operator(self, command):
        args=self.pop_n(2)
        if command.type == 'or':
            self.stack.append(args[0] or args[1])
        elif command.type == 'and':
            self.stack.append(args[0] and args[1])
        elif command.type == '<':
            self.stack.append(args[0] < args[1])
        elif command.type == '<=':
            self.stack.append(args[0] <= args[1])
        elif command.type == '>':
            self.stack.append(args[0] > args[1])
        elif command.type == '>=':
            self.stack.append(args[0] >= args[1])
        elif command.type == '!=':
            self.stack.append(args[0] != args[1])
        elif command.type == '==':
            self.stack.append(args[0] == args[1])
        elif command.type == '+':
            self.stack.append(args[0] + args[1])
        elif command.type == '-':
            self.stack.append(args[0] - args[1])
        elif command.type == '*':
            self.stack.append(args[0] * args[1])
        elif command.type == '/':
            self.stack.append(args[0] / args[1])
        elif command.type == '%':
            self.stack.append(args[0] % args[1])
        elif command.type == '**':
            self.stack.append(args[0] ** args[1])
        elif command.type == '//':
            self.stack.append(args[0] // args[1])
            
    def execute_FunctionDeclaration(self, command):
        self.environment[command.name]=command

    def execute_FunctionCall(self, command):
        environment = self.var_search(command.name)
        function=environment[command.name]
        self.environment={'':self.environment} #по ключу '' находится родительское окружение
        vals=self.pop_n(len(function.arguments))
        self.environment.update(dict(zip(function.arguments, vals)))
        for command in function.block:
            self.executing(command)
        self.environment=self.environment['']
        
    def execute_IfStatement(self, command):
        self.execute_Block(command.condition)
        condition = self.stack.pop()
        if condition:
            self.execute_Block(command.consequent)
        else:
            self.execute_Block(command.alternative)
            
    def execute_WhileStatement(self, command):
        self.execute_Block(command.condition)
        condition = self.stack.pop()
        while condition:
            self.execute_Block(command.block)
            self.execute_Block(command.condition)
            condition = self.stack.pop()
        
    def execute_Block(self,block):
        for command in block:
            self.executing(command)

    def interpret(self):
        self.execute_Block(self.code)

    
def main():
    program = """
a=0
b=0
c=0
function func (arg1,arg2)
{
arg=arg2
a=arg1+arg
}
while b <= 10
{
b=b+1
}
func(b,5)
c=a+b
if a+b==c
{
d=1
}
e= 4 + 2 * (10 / (25 // (7 + 1) - 1)) ** (2 + 3) % 7 - 3
"""
    lexer = Lexer(program)
    tokens= lexer.get_tokens()
    #print("Tokens:",tokens)
    parser=Parser(tokens)
    code=parser.parse()
    #print ([type(com).__name__ for com in code])
    interpreter=Interpreter(code)
    interpreter.interpret()
    print("Global environment", interpreter.environment)

        
if __name__ == '__main__':
    main()
