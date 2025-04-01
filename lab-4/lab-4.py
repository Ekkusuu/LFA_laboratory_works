import random
import re

def generate_from_regex(regex, max_repeats=5):
    steps = []
    
    def expand(pattern):
        if '|' in pattern:
            options = re.findall(r'\((.*?)\)', pattern)
            for option in options:
                choices = option.split('|')
                chosen = random.choice(choices)
                pattern = pattern.replace(f'({option})', chosen, 1)
                steps.append(f"Chose from {choices} -> {chosen}")
        
        pattern = re.sub(r'(\w)\+', lambda m: (
            steps.append(f"Expanding {m.group(1)}+ -> {m.group(1) * random.randint(1, max_repeats)}") 
            or m.group(1) * random.randint(1, max_repeats)), pattern)
        
        pattern = re.sub(r'(\w)\*', lambda m: (
            steps.append(f"Expanding {m.group(1)}* -> {m.group(1) * random.randint(0, max_repeats)}") 
            or m.group(1) * random.randint(0, max_repeats)), pattern)
        
        pattern = re.sub(r'(\w)\?', lambda m: (
            steps.append(f"Expanding {m.group(1)}? -> {m.group(1) if random.choice([True, False]) else ''}") 
            or (m.group(1) if random.choice([True, False]) else '')), pattern)
        
        pattern = re.sub(r'(\w)\^(\d+)', lambda m: (
            steps.append(f"Expanding {m.group(1)}^{m.group(2)} -> {m.group(1) * int(m.group(2))}") 
            or m.group(1) * int(m.group(2))), pattern)

        return pattern
    
    result = expand(regex)

    return result, steps

regexes = [
    "O(P|Q|R)+2(3|4)",
    "A*B(C|D|E)F(G|H|i)^2",
    "J+K(L|M|N)*O?(P|Q)^3"
]

for regex in regexes:
    print(f"\nProcessing Regex: {regex}")
    result, steps = generate_from_regex(regex)
    
    for step in steps:
        print(" -", step)
    
    print(f"Generated String: {result}\n")
