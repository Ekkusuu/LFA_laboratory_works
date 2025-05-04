import string

class CFG:
    def __init__(self, productions, start_symbol):
        self.productions = productions
        self.start_symbol = start_symbol
        self.used_variables = set(productions.keys())
        self.terminal_to_variable = {}

    def generate_new_variable(self):
        for letter in string.ascii_uppercase:
            if letter not in self.used_variables:
                self.used_variables.add(letter)
                return letter
        for i in range(26, 702):
            var = string.ascii_uppercase[i // 26 - 1] + string.ascii_uppercase[i % 26]
            if var not in self.used_variables:
                self.used_variables.add(var)
                return var

    def eliminate_epsilon_productions(self):
        nullable_variables = self.find_nullable_variables()
        new_productions = {}
        for lhs in self.productions:
            new_productions[lhs] = set()
            for rhs in self.productions[lhs]:
                self.generate_new_productions(lhs, rhs, nullable_variables, new_productions)
        self.productions = {lhs: [rhs for rhs in rhs_list if rhs != 'ε']
                            for lhs, rhs_list in new_productions.items()}

    def find_nullable_variables(self):
        nullable = set()
        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                if rhs == 'ε':
                    nullable.add(lhs)
        changed = True
        while changed:
            changed = False
            for lhs in self.productions:
                for rhs in self.productions[lhs]:
                    if all(symbol in nullable for symbol in rhs if symbol.isupper()) and lhs not in nullable:
                        nullable.add(lhs)
                        changed = True
        return nullable

    def generate_new_productions(self, lhs, rhs, nullable_variables, new_productions):
        rhs_list = list(rhs)
        nullable_indices = [i for i, symbol in enumerate(rhs_list) if symbol in nullable_variables]
        num_nullable = len(nullable_indices)
        if num_nullable == 0:
            new_productions[lhs].add(rhs)
        else:
            for i in range(1 << num_nullable):
                new_rhs = list(rhs_list)
                for j, idx in enumerate(nullable_indices):
                    if (i >> j) & 1 == 0:
                        new_rhs[idx] = ''
                new_rhs = ''.join(new_rhs).replace('', '')
                if new_rhs != '':
                    new_productions[lhs].add(new_rhs)

    def eliminate_unit_productions(self):
        unit_productions = {}
        for lhs in self.productions:
            unit_productions[lhs] = set()
            for rhs in self.productions[lhs]:
                if len(rhs) == 1 and rhs.isupper():
                    unit_productions[lhs].add(rhs)
        visited = set()
        changes = True
        while changes:
            changes = False
            for lhs in list(unit_productions.keys()):
                if lhs in visited:
                    continue
                visited.add(lhs)
                for rhs in list(unit_productions[lhs]):
                    for prod in self.productions.get(rhs, []):
                        if prod != rhs and prod not in self.productions[lhs]:
                            self.productions[lhs].append(prod)
                            changes = True
                    self.productions[lhs] = [p for p in self.productions[lhs] if p != rhs]
        self.productions = {lhs: list(set(rhs)) for lhs, rhs in self.productions.items()}

    def eliminate_inaccessible_symbols(self):
        reachable = set()
        to_process = {self.start_symbol}
        while to_process:
            symbol = to_process.pop()
            if symbol not in reachable:
                reachable.add(symbol)
                for production in self.productions.get(symbol, []):
                    for char in production:
                        if char.isupper():
                            to_process.add(char)
        self.productions = {lhs: [rhs for rhs in rhss if all(c not in self.productions or c in reachable or not c.isupper() for c in rhs)]
                            for lhs, rhss in self.productions.items() if lhs in reachable}

    def replace_long_productions(self):
        new_productions = {}
        for lhs in self.productions:
            new_productions[lhs] = set()
        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                if len(rhs) <= 2:
                    new_productions[lhs].add(rhs)
                else:
                    symbols = list(rhs)
                    prev_var = self.generate_new_variable()
                    new_productions.setdefault(prev_var, set()).add(symbols[0] + symbols[1])
                    for i in range(2, len(symbols) - 1):
                        next_var = self.generate_new_variable()
                        new_productions.setdefault(next_var, set()).add(prev_var + symbols[i])
                        prev_var = next_var
                    new_productions[lhs].add(prev_var + symbols[-1])
        self.productions = new_productions

    def replace_terminals_in_rules(self):
        new_productions = {}
        for lhs in self.productions:
            new_productions[lhs] = set()
            for rhs in self.productions[lhs]:
                if len(rhs) == 1:
                    new_productions[lhs].add(rhs)
                else:
                    new_rhs = ''
                    for symbol in rhs:
                        if symbol.islower():
                            if symbol in self.terminal_to_variable:
                                var = self.terminal_to_variable[symbol]
                            else:
                                if symbol not in self.terminal_to_variable or len(self.productions.get(self.terminal_to_variable[symbol], [])) > 1:
                                    var = self.generate_new_variable()
                                    self.terminal_to_variable[symbol] = var
                                    new_productions.setdefault(var, set()).add(symbol)
                                else:
                                    var = self.terminal_to_variable[symbol]
                            new_rhs += var
                        else:
                            new_rhs += symbol
                    new_productions[lhs].add(new_rhs)
        self.productions = new_productions

    def display_productions(self):
        start_rhs_list = sorted(self.productions.get(self.start_symbol, []))
        start_rhs_str = " | ".join(start_rhs_list)
        print(f'{self.start_symbol} -> {start_rhs_str}')
        for lhs in sorted(self.productions):
            if lhs != self.start_symbol:
                rhs_list = sorted(self.productions[lhs])
                rhs_str = " | ".join(rhs_list)
                print(f'{lhs} -> {rhs_str}')


productions = {
    'S': ['aA', 'AC'],
    'A': ['a', 'ASC', 'BC', 'aD'],
    'B': ['b', 'bA'],
    'C': ['ε', 'BA'],
    'E': ['aB'],
    'D': ['abC']
}
start_symbol = 'S'

cfg = CFG(productions, start_symbol)

cfg.eliminate_epsilon_productions()
cfg.eliminate_unit_productions()
cfg.eliminate_inaccessible_symbols()
cfg.replace_long_productions()
cfg.replace_terminals_in_rules()

cfg.display_productions()
