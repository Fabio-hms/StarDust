from collections import defaultdict

class AFN:
    def __init__(self, states, alphabet, transitions, start, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.finals = finals

def epsilon_closure(states, transitions):
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for next_state in transitions.get((state, ""), []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def move(states, symbol, transitions):
    result = set()
    for state in states:
        result.update(transitions.get((state, symbol), []))
    return result

def afn_to_afd(afn):
    start_closure = frozenset(epsilon_closure([afn.start], afn.transitions))
    unmarked = [start_closure]
    d_states = {start_closure: 'D0'}
    d_transitions = {}
    d_finals = set()
    count = 1

    while unmarked:
        current = unmarked.pop()
        for symbol in afn.alphabet:
            if symbol == "":
                continue
            target = frozenset(epsilon_closure(move(current, symbol, afn.transitions), afn.transitions))
            if not target:
                continue
            if target not in d_states:
                d_states[target] = f'D{count}'
                count += 1
                unmarked.append(target)
            d_transitions[(d_states[current], symbol)] = d_states[target]
        if any(s in afn.finals for s in current):
            d_finals.add(d_states[current])

    return {
        "states": list(d_states.values()),
        "start": 'D0',
        "finals": list(d_finals),
        "transitions": d_transitions
    }
