from graphviz import Digraph

class FiniteAutomatonToGrammar:
    def __init__(self, states, alphabet, start_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions
        self.non_terminals = {state: chr(65 + i) for i, state in enumerate(states)}

    def generate_grammar(self):
        grammar = {}
        for state in self.states:
            non_terminal = self.non_terminals[state]
            grammar[non_terminal] = []

            for symbol in self.alphabet:
                if (state, symbol) in self.transitions:
                    next_state = self.transitions[(state, symbol)]
                    next_non_terminal = self.non_terminals[next_state]
                    grammar[non_terminal].append(f"{symbol}{next_non_terminal}")

            if state in self.final_states:
                grammar[non_terminal].append("ε")

        return grammar

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                transitions_for_symbol = [next_state for (s, sym), next_state in self.transitions.items() if s == state and sym == symbol]
                if len(transitions_for_symbol) != 1:
                    return False
        return True

    def ndfa_to_dfa(self):
        dfa_states = []
        dfa_transitions = {}
        dfa_final_states = set()

        initial_dfa_state = [self.start_state]
        dfa_states.append(initial_dfa_state)

        def get_dfa_transition(state_list, symbol):
            next_state_list = []
            for state in state_list:
                if (state, symbol) in self.transitions:
                    next_state_list.append(self.transitions[(state, symbol)])
            return next_state_list

        unprocessed_states = [initial_dfa_state]
        while unprocessed_states:
            current_state = unprocessed_states.pop()
            for symbol in self.alphabet:
                next_state = get_dfa_transition(current_state, symbol)

                if next_state:
                    if next_state not in dfa_states:
                        dfa_states.append(next_state)
                        unprocessed_states.append(next_state)

                    dfa_transitions[(tuple(current_state), symbol)] = tuple(next_state)

                    if any(state in self.final_states for state in next_state):
                        dfa_final_states.add(tuple(next_state))

        return dfa_states, dfa_transitions, dfa_final_states

    def generate_graph(self):
        dot = Digraph(format='png', engine='dot')

        for state in self.states:
            if state == self.start_state:
                dot.node(state, shape='circle', color='red')
            elif state in self.final_states:
                dot.node(state, shape='doublecircle', color='green')
            else:
                dot.node(state, shape='circle')

        for (state, symbol), next_state in self.transitions.items():
            dot.edge(state, next_state, label=symbol)

        dot.render('finite_automaton_graph')
        print("Graph has been saved to 'finite_automaton_graph.png'.")


states = ['q0', 'q1', 'q2', 'q3']
alphabet = ['a', 'b', 'c']
start_state = 'q0'
final_states = ['q3']
transitions = {
    ('q0', 'a'): 'q0',
    ('q0', 'b'): 'q1',
    ('q1', 'a'): 'q2',
    ('q1', 'b'): 'q1',
    ('q2', 'a'): 'q0',
    ('q2', 'b'): 'q3'
}

fa_to_grammar = FiniteAutomatonToGrammar(states, alphabet, start_state, final_states, transitions)
grammar = fa_to_grammar.generate_grammar()

for non_terminal, productions in grammar.items():
    print(f"{non_terminal} → {' | '.join(productions)}")

if fa_to_grammar.is_deterministic():
    print("\nThe FA is Deterministic.")
else:
    print("\nThe FA is Non-Deterministic.")

dfa_states, dfa_transitions, dfa_final_states = fa_to_grammar.ndfa_to_dfa()

print("\nDFA States:", [str(state) for state in dfa_states])
print("DFA Final States:", [str(state) for state in dfa_final_states])
print("DFA Transitions:")
for (state, symbol), next_state in dfa_transitions.items():
    print(f"  {state} --{symbol}--> {next_state}")

fa_to_grammar.generate_graph()
