import sys
import os
import subprocess
from typing import List
import lexer
from graphviz import Digraph

class PTNode:
    def __init__(self, name: str):
        self.name = name
        self.children: List['PTNode'] = []

    def add(self, child: 'PTNode'):
        self.children.append(child)

class Parser:
    def __init__(self, tokens: List[lexer.Token]):
        self.tokens = tokens
        self.pos = 0

    @property
    def current(self) -> lexer.Token:
        return self.tokens[self.pos]

    def eat(self, ttype: lexer.TokenType) -> lexer.Token:
        if self.current.type == ttype:
            tok = self.current
            self.pos += 1
            return tok
        raise RuntimeError(f"Expected {ttype} but got {self.current.type}")

    def parse(self) -> PTNode:
        root = PTNode('Timeline')
        while self.current.type != lexer.TokenType.EOF:
            if self.current.type == lexer.TokenType.COMMA:
                comma_tok = self.eat(lexer.TokenType.COMMA)
                root.add(PTNode(comma_tok.value))
                continue
            root.add(self.parse_statement())
        return root

    def parse_statement(self):
        stmt = PTNode("Statement")
        kw = self.eat(lexer.TokenType.KEYWORD).value
        stmt.add(PTNode(kw))
        self.eat(lexer.TokenType.LPAREN)
        stmt.add(PTNode('('))

        first = True
        while self.current.type != lexer.TokenType.RPAREN:
            if not first:
                self.eat(lexer.TokenType.COMMA)
                stmt.add(PTNode(','))

            # 🛠️ NEW: Allow any STRING or NUMBER as a positional argument
            if self.current.type in (lexer.TokenType.STRING, lexer.TokenType.NUMBER):
                arg = PTNode("PositionalArg")
                token = self.eat(self.current.type)
                display = f'"{token.value}"' if token.type == lexer.TokenType.STRING else token.value
                arg.add(PTNode(display))
                stmt.add(arg)
            else:
                stmt.add(self.parse_assignment())

            first = False

        self.eat(lexer.TokenType.RPAREN)
        stmt.add(PTNode(')'))
        return stmt



    def parse_assignment(self) -> PTNode:
        node = PTNode('Assignment')
        idt = self.eat(lexer.TokenType.IDENTIFIER)
        node.add(PTNode(idt.value))
        eq = self.eat(lexer.TokenType.ASSIGN)
        node.add(PTNode(eq.value))
        if self.current.type == lexer.TokenType.STRING:
            lit = self.eat(lexer.TokenType.STRING)
            node.add(PTNode(f'"{lit.value}"'))
        elif self.current.type == lexer.TokenType.NUMBER:
            num = self.eat(lexer.TokenType.NUMBER)
            node.add(PTNode(num.value))
        else:
            raise RuntimeError(f"Expected literal but got {self.current.type}")
        return node

def tree_to_dot(root: PTNode) -> Digraph:
    dot = Digraph(format='png')
    dot.attr('node', shape='ellipse', fontname='monospace')
    def visit(node: PTNode, parent_id: str = None):
        nid = str(id(node))
        dot.node(nid, label=node.name)
        if parent_id:
            dot.edge(parent_id, nid)
        for child in node.children:
            visit(child, nid)
    visit(root)
    return dot

if __name__ == '__main__':
    try:
        code = input("Enter your DSL (empty to quit): ").strip()
        if not code:
            sys.exit(0)
        tokens = lexer.lexer(code)
        parser = Parser(tokens)
        tree = parser.parse()
        dot_path = tree_to_dot(tree).render(filename='parse_tree', cleanup=True)
        print(f"Parse‐tree image written to {dot_path}")
        if sys.platform.startswith('darwin'):
            subprocess.call(['open', dot_path])
        elif sys.platform.startswith('win'):
            os.startfile(dot_path)
        else:
            subprocess.call(['xdg-open', dot_path])
    except Exception as e:
        print(f"Error: {e}")
