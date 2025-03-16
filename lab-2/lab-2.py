import graphviz

class Automaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def convert_to_regular_grammar(self):
        non_terminals = {state.upper() for state in self.states}
        terminals = self.alphabet
        productions = {state.upper(): [] for state in self.states}

        for (state, char), next_states in self.transitions.items():
            for next_state in next_states:
                productions[state.upper()].append(char + next_state.upper())

        for final_state in self.final_states:
            productions[final_state.upper()].append("")

        start_symbol = self.start_state.upper()
        final_symbols = {state.upper() for state in self.final_states}

        return non_terminals, terminals, productions, start_symbol, final_symbols

    def is_deterministic(self):
        for (state, char), next_states in self.transitions.items():
            if len(next_states) > 1:
                return False
        return True

    def convert_to_dfa(self):
        dfa_states = set()
        dfa_transitions = {}
        dfa_start_state = frozenset([self.start_state])
        dfa_final_states = set()
        unprocessed_states = [dfa_start_state]
        state_mapping = {dfa_start_state: "q0"}
        state_counter = 1

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            dfa_states.add(current_state)
            for symbol in self.alphabet:
                next_state = frozenset(
                    sum((self.transitions.get((sub_state, symbol), []) for sub_state in current_state), []))
                if next_state:
                    state_name = "q" + "".join(sorted(next_state)).replace("q", "")
                    if next_state not in state_mapping:
                        state_mapping[next_state] = state_name
                        unprocessed_states.append(next_state)
                    dfa_transitions[(state_mapping[current_state], symbol)] = [state_mapping[next_state]]

        for state in dfa_states:
            if any(sub_state in self.final_states for sub_state in state):
                dfa_final_states.add(state_mapping[state])

        return Automaton(
            states=set(state_mapping.values()),
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            start_state=state_mapping[dfa_start_state],
            final_states=dfa_final_states,
        )

    def visualize(self, is_nfa=True):
        dot = graphviz.Digraph(format='png', engine='dot')

        for state in self.states:
            if state == self.start_state:
                dot.node(state, shape='ellipse', style='filled', fillcolor='lightblue', label=f"start\n{state}")
            elif state in self.final_states:
                dot.node(state, shape='doublecircle', label=f"final\n{state}")
            else:
                dot.node(state, shape='ellipse', label=state)

        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                if is_nfa:
                    dot.edge(state, next_state, label=symbol)
                else:
                    dot.edge(state, next_state, label=symbol)

        if is_nfa:
            dot.render('nfa_automaton')  
            print("NFA Graph generated as 'nfa_automaton.png'")
        else:
            dot.render('dfa_automaton')  
            print("DFA Graph generated as 'dfa_automaton.png'")

def main():
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b", "c"}

    transitions = {
        ('q0', 'a'): ['q0', 'q1'],
        ('q1', 'b'): ['q1'],
        ('q2', 'b'): ['q3'],
        ('q1', 'a'): ['q2'],
        ('q2', 'a'): ['q0'],
    }
    
    start_state = "q0"
    final_states = {"q3"}

    automaton = Automaton(states, alphabet, transitions, start_state, final_states)

    non_terminals, terminals, productions, start_symbol, final_symbols = automaton.convert_to_regular_grammar()
    print("Regular Grammar:")
    print("Non-terminals (VN):", non_terminals)
    print("Terminals (VT):", terminals)
    print("Productions (P):", productions)
    print("Start Symbol:", start_symbol)
    print("Final Symbols:", final_symbols)

    print("Is Deterministic:", automaton.is_deterministic())

    automaton.visualize(is_nfa=True)

    dfa = automaton.convert_to_dfa()

    print("\nDFA States:", dfa.states)
    print("DFA Alphabet:", dfa.alphabet)
    print("DFA Transitions:")
    for (state, symbol), next_states in dfa.transitions.items():
        print(f"  ({state}, {symbol}) -> {next_states}")
    print("DFA Start State:", dfa.start_state)
    print("DFA Final States:", dfa.final_states)

    dfa.visualize(is_nfa=False)

if __name__ == "__main__":
    main()
