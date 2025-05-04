import re
from enum import Enum, auto
from typing import List, Union

class TokenType(Enum):
    KEYWORD = auto()
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    OPERATOR = auto()
    EOF = auto()

VALID_KEYWORDS = {"event", "person", "link"}
VALID_IDENTIFIERS = {"born", "died", "type", "caused", "related"}

class Token:
    def __init__(self, type: TokenType, value: Union[str, int, float]):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

token_specification = [
    ('KEYWORD',    r'\b(event|person|link)\b'),
    ('STRING',     r'"[^"]*"'),
    ('NUMBER',     r'\b\d{1,4}(-\d{1,4})?\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('ASSIGN',     r'='),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('COMMA',      r','),
    ('OPERATOR',   r'[+\-*/^]'),
    ('SKIP',       r'[ \t]+'),
    ('MISMATCH',   r'.'),
]

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
compiled_regex = re.compile(token_regex)

def lexer(code: str) -> List[Token]:
    tokens = []
    for match in compiled_regex.finditer(code):
        type = match.lastgroup
        value = match.group(type)
        if type == 'KEYWORD':
            tokens.append(Token(TokenType.KEYWORD, value))
        elif type == 'STRING':
            tokens.append(Token(TokenType.STRING, value.strip('"')))
        elif type == 'NUMBER':
            tokens.append(Token(TokenType.NUMBER, value))
        elif type == 'IDENTIFIER':
            if value not in VALID_IDENTIFIERS:
                raise RuntimeError(f"Error: Invalid identifier '{value}'")
            tokens.append(Token(TokenType.IDENTIFIER, value))
        elif type == 'ASSIGN':
            tokens.append(Token(TokenType.ASSIGN, value))
        elif type == 'LPAREN':
            tokens.append(Token(TokenType.LPAREN, value))
        elif type == 'RPAREN':
            tokens.append(Token(TokenType.RPAREN, value))
        elif type == 'COMMA':
            tokens.append(Token(TokenType.COMMA, value))
        elif type == 'OPERATOR':
            tokens.append(Token(TokenType.OPERATOR, value))
        elif type == 'SKIP':
            continue
        elif type == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
    tokens.append(Token(TokenType.EOF, ''))
    return tokens

if __name__ == '__main__':
    while True:
        try:
            code = input("Enter history graph DSL (or 'exit' to quit): ").strip()
            if code.lower() == 'exit':
                break
            token_stream = lexer(code)
            for token in token_stream:
                print(token)
        except Exception as e:
            print(f"Error: {e}")
