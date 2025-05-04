    def eliminate_non_productive_symbols(self):
        productive = set()

        # Step 1: Find all productive symbols (those that eventually lead to terminals)
        changed = True
        while changed:
            changed = False
            for lhs, rhss in self.productions.items():
                for rhs in rhss:
                    if all(symbol.islower() or symbol in productive for symbol in rhs):
                        if lhs not in productive:
                            productive.add(lhs)
                            changed = True

        # Step 2: Remove unproductive rules
        new_productions = {}
        for lhs in self.productions:
            if lhs in productive:
                valid_rhs = []
                for rhs in self.productions[lhs]:
                    if all(symbol.islower() or symbol in productive for symbol in rhs):
                        valid_rhs.append(rhs)
                if valid_rhs:
                    new_productions[lhs] = valid_rhs

        self.productions = new_productions