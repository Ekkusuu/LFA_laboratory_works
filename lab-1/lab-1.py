import random

class Grammar:
    def __init__(self, VN, VT, P, start_symbol):
        self.VN = VN 
        self.VT = VT
        self.P = P 
        self.start_symbol = start_symbol

    def generate_string(self):
        current = self.start_symbol
        result = ""
        while any(symbol in self.VN for symbol in current):
            for symbol in current:
                if symbol in self.VN:
                    replacement = random.choice(self.P[symbol])
                    current = current.replace(symbol, replacement, 1)
                    break
        return current

    def generate_multiple_strings(self, count=5):
        return [self.generate_string() for _ in range(count)]

    def to_finite_automaton(self):
        states = set(self.VN) | {"q_accept"}
        alphabet = set(self.VT)
        transitions = {}
        start_state = self.start_symbol
        final_states = {"q_accept"}
        
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) == 1 and production in self.VT:
                    transitions.setdefault((non_terminal, production), []).append("q_accept")
                else:
                    transitions.setdefault((non_terminal, production[0]), []).append(production[1:])
        
        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def accepts(self, input_string):
        current_state = self.start_state
        
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)][0]
            else:
                return False
        
        return current_state in self.final_states

class Main:
    @staticmethod
    def run():
        grammar_rules = {
            "S": ["dA"],
            "A": ["aB", "bA"],
            "B": ["bC", "aB", "d"],
            "C": ["cB"]
        }

        grammar = Grammar(VN={"S", "A", "B", "C"}, VT={"a", "b", "c", "d"}, P=grammar_rules, start_symbol="S")
        print("Generated strings:", grammar.generate_multiple_strings())

        finite_automaton = grammar.to_finite_automaton()
        user_input = input("Enter a string to check: ")
        print(f"Accepts '{user_input}'?:", finite_automaton.accepts(user_input))

if __name__ == "__main__":
    Main.run()