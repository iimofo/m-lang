import re

# Token types
TOKENS = {
    'KEYWORD': r'\b(let|func|return|View|Text|Button|if|else|for|while|component)\b',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'NUMBER': r'\d+',
    'STRING': r'"[^"]*"',  # String tokens, e.g., "Hello"
    'SYMBOL': r'[\(\)\{\}\[\]\.,]',  # Includes parentheses, braces, brackets, commas
    'WHITESPACE': r'\s+',
    'OPERATOR': r'[\+\-\*/=<>!&|]',  # Operators like +, -, *, etc.
    'NEWLINE': r'\n',
}

# Lexer class
class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_pos = 0
        self.current_line = 1  # Start on line 1

    def tokenize(self):
        while self.current_pos < len(self.source_code):
            match = None
            for token_type, regex in TOKENS.items():
                pattern = re.compile(regex)
                match = pattern.match(self.source_code, self.current_pos)
                if match:
                    if token_type != 'WHITESPACE':  # Ignore whitespace tokens
                        self.tokens.append((token_type, match.group(0), self.current_line))
                    self.current_pos = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {self.source_code[self.current_pos]} at line {self.current_line}")

            # Update the current line number
            if '\n' in match.group(0):
                self.current_line += match.group(0).count('\n')

        return self.tokens


# Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        ast = []
        while self.current_token_index < len(self.tokens):
            ast.append(self.parse_statement())
        return ast

    def parse_statement(self):
        token_type, token_value, line_number = self.tokens[self.current_token_index]
        if token_type == 'KEYWORD':
            if token_value == 'View':
                return self.parse_view()
            elif token_value == 'let':
                return self.parse_assignment()
            elif token_value == 'func':
                return self.parse_function()
            elif token_value == 'component':
                return self.parse_component()
            elif token_value == 'Text':
                return self.parse_text()
            elif token_value == 'Button':
                return self.parse_button()  # Adding Button parsing here
            else:
                raise SyntaxError(f"Unexpected keyword: {token_value} at line {line_number}")
        elif token_type == 'IDENTIFIER':
            return self.parse_component_call()
        else:
            raise SyntaxError(f"Unexpected token: {token_value} at line {line_number}")

    def parse_text(self):
        self.expect('KEYWORD', 'Text')
        self.expect('SYMBOL', '(')
        text_value = self.expect('STRING')
        self.expect('SYMBOL', ')')
        return ('Text', text_value)

    def parse_view(self):
        self.expect('KEYWORD', 'View')
        self.expect('SYMBOL', '{')
        elements = []
        while not self.match('SYMBOL', '}'):
            elements.append(self.parse_statement())
        self.expect('SYMBOL', '}')
        return ('View', elements)

    def parse_assignment(self):
        self.expect('KEYWORD', 'let')
        name = self.expect('IDENTIFIER')
        self.expect('OPERATOR', '=')
        value = self.expect('STRING') or self.expect('NUMBER')
        return ('Assignment', name, value)

    def parse_function(self):
        self.expect('KEYWORD', 'func')
        name = self.expect('IDENTIFIER')
        self.expect('SYMBOL', '(')
        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', '{')
        body = []
        while not self.match('SYMBOL', '}'):
            body.append(self.parse_statement())
        self.expect('SYMBOL', '}')
        return ('Function', name, body)

    def parse_component(self):
        self.expect('KEYWORD', 'component')
        name = self.expect('IDENTIFIER')
        self.expect('SYMBOL', '{')
        body = []
        while not self.match('SYMBOL', '}'):
            body.append(self.parse_statement())
        self.expect('SYMBOL', '}')  # Look for the closing brace
        return ('Component', name, body)  # Return the name along with the body

    def parse_button(self):
        self.expect('KEYWORD', 'Button')
        self.expect('SYMBOL', '(')
        button_text = self.expect('STRING')
        self.expect('SYMBOL', ')')
        return ('Button', button_text)

    def parse_component_call(self):
        name = self.expect('IDENTIFIER')
        self.expect('SYMBOL', '(')
        self.expect('SYMBOL', ')')
        return ('CallComponent', name)

    def expect(self, expected_type, expected_value=None):
        token_type, token_value, line_number = self.tokens[self.current_token_index]
        if token_type != expected_type or (expected_value and token_value != expected_value):
            raise SyntaxError(f"Expected {expected_value or expected_type}, but got {token_value} at line {line_number}")
        self.current_token_index += 1
        return token_value

    def match(self, expected_type, expected_value=None):
        token_type, token_value, line_number = self.tokens[self.current_token_index]
        if token_type == expected_type and (not expected_value or token_value == expected_value):
            return True
        return False


# Interpreter class
class Interpreter:
    def __init__(self):
        self.environment = {}

    def reset(self):
        self.environment = {}

    def interpret(self, ast):
        for node in ast:
            self.evaluate(node)

    def evaluate(self, node):
        node_type = node[0]

        if node_type == 'View':
            print("Rendering View with elements:", node[1])
        elif node_type == 'Assignment':
            name, value = node[1], node[2]
            self.environment[name] = value
            print(f"Assigned {name} = {value}")
        elif node_type == 'Function':
            name, body = node[1], node[2]
            print(f"Defined function {name} with body {body}")
        elif node_type == 'Component':
            name, body = node[1], node[2]  # Correct unpacking here
            self.environment[name] = ('Component', body)
            print(f"Defined component {name}")
        elif node_type == 'CallComponent':
            name = node[1]
            component = self.environment.get(name)
            if component and component[0] == 'Component':
                print(f"Rendering component {name}")
                for statement in component[1]:
                    self.evaluate(statement)
            else:
                print(f"Component {name} not found.")
        elif node_type == 'Button':
            print(f"Rendering Button with text: {node[1]}")
        elif node_type == 'Text':
            print(f"Rendering Text: {node[1]}")

# Example usage
source_code = '''
component MyCustomView {
    Text("This is my custom view")
    Button("Click me")
}

MyCustomView()
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

interpreter = Interpreter()
interpreter.interpret(ast)
