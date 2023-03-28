#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 19 Mar 2023 17:32:13

@author: gsfran
"""

from __future__ import annotations

from copy import deepcopy


class DFA:

    def __init__(
        self, Q: set[int],
        Sigma: set[str],
        delta: dict[tuple[int, str], int],
        q0: int,
        F: set[int]
    ) -> None:
        """Creates a Deterministic Finite Automaton

        Args:
            Q (set): States of the automaton
            Sigma (set): Symbols
            delta (dict[tuple(str, str), str]): Transition functions
                Format:
                {(current state, symbol): next state}
            q0 (str): Initial state
            F (set): Final states
        """
        self.states = Q
        self.symbols = Sigma
        self.transitions = delta
        self.initial_state = q0
        self.final_states = F

    def __repr__(self) -> str:
        return (
            f'DFA(\n\t{self.states},\n\t{self.symbols},'
            f'\n\t{self.transitions},\n\t{self.initial_state},'
            f'\n\t{self.final_states}\n)'
        )

    def run(self, word: str) -> bool:
        """Runs the defined automaton

        Args:
            word (str): The input word

        Returns:
            bool: True if word is in the defined automata language,
            otherwise False
        """
        self.state = self.initial_state
        while word:
            self.state = self.transitions[(self.state, word[0])]
            word = word[1:]

        return self.state in self.final_states

    def minimize(self) -> DFA:
        """Not used.

        Returns:
            Minimized DFA.
        """
        # return the minimal DFA
        # the minimisation.pdf which is a section
        # of the lecture notes :
        # Thorsten Altenkirch, Venanzio Capretta, and Henrik Nilsson.
        # "Languages and Computation." (2019).
        return minimize_dfa(self)


D = []

# D0 -- example from video
# a's must not follow b's
D.append(
    DFA(
        Q={0, 1, 2},
        Sigma={'a', 'b'},
        delta={
            (0, 'a'): 0,
            (0, 'b'): 1,
            (1, 'a'): 2,
            (1, 'b'): 1,
            (2, 'a'): 2,
            (2, 'b'): 2
        },
        q0=0,
        F={0, 1}
    )
)

# D1 -- example from video
# a % 2 must equal b % 2
D.append(
    DFA(
        Q={0, 1, 2, 3},
        Sigma={'a', 'b'},
        delta={
            (0, 'a'): 2,
            (0, 'b'): 1,
            (1, 'a'): 0,
            (1, 'b'): 3,
            (2, 'a'): 0,
            (2, 'b'): 3,
            (3, 'a'): 1,
            (3, 'b'): 2
        },
        q0=0,
        F={0, 3}
    )
)

# D2 -- example from minimisation.pdf
# test case : D2.minimize()
D.append(
    DFA(
        Q={0, 1, 2, 3, 4, 5},
        Sigma={'a', 'b'},
        delta={
            (0, 'a'): 1,
            (0, 'b'): 4,
            (1, 'a'): 2,
            (1, 'b'): 3,
            (2, 'a'): 2,
            (2, 'b'): 2,
            (3, 'a'): 2,
            (3, 'b'): 3,
            (4, 'a'): 5,
            (4, 'b'): 4,
            (5, 'a'): 5,
            (5, 'b'): 4
        },
        q0=0,
        F={2, 3}
    )
)


def run_dfa(dfa: DFA) -> bool:

    word = input('Enter word: ')
    return dfa.run(word=word)


def minimize_dfa(dfa: DFA):

    pairs = {}
    states = sorted(dfa.states)
    n = 0

    # creates list of all state-pairs
    for r in states[:]:
        for s in states[-1:n:-1]:
            pairs[(r, s)] = 0
        n += 1

    # marks all pairs containing final states
    for (r, s) in pairs.keys():
        if (r in dfa.final_states) ^ (s in dfa.final_states):
            pairs[(r, s)] = 1

    # creates a list of marked state pairs, and a dictionary of unmarked pairs
    marked = [key_ for key_ in pairs.keys() if pairs[key_]]
    unmarked = {key_: [] for key_ in pairs.keys() if not pairs[key_]}

    def mark_pair(key_: tuple[int, int]) -> None:
        """Marks a state pair and checks for any linked pairs to mark.

        Args:
            key_ (tuple[int, int]): The state pair to mark [(r, s)].
        """
        marked.append(unmarked[key_])
        try:
            for _ in unmarked[key_]:
                mark_pair(_)
        except KeyError:
            pass
        unmarked.pop(key_)

    # Checks all unmarked state pairs, with indeterminate pairs
    # being flagged for later marking.
    unmarked_copy = deepcopy(unmarked)
    for (r, s) in unmarked_copy.keys():
        for symbol in sorted(dfa.symbols):
            p = dfa.transitions[r, symbol]
            q = dfa.transitions[s, symbol]

            if p == q:
                # Same state, no info.
                continue
            elif p == r and q == s:
                # No point in adding the same state pair under itself.
                continue
            elif (p, q) in marked:
                # Distinguishable!
                mark_pair((r, s))
                break
            else:
                # Records the pair for deferred marking.
                unmarked[(p, q)].append((r, s))

    # Minimizes the dfa by removing extraneous states
    # and redirecting states which point to them
    min_transitions = deepcopy(dfa.transitions)
    for (p, q) in unmarked.keys():
        for key_, value_ in dfa.transitions.items():
            if value_ == q:
                min_transitions[key_] = p
            if key_[0] == q:
                min_transitions.pop(key_)
                # for symbol_ in dfa.symbols:
                #     print(f'popping: {q, symbol_}')

    return DFA(
        Q=dfa.states,
        Sigma=dfa.symbols,
        delta=min_transitions,
        q0=dfa.initial_state,
        F=dfa.final_states
    )


def main():

    while True:
        choice = input(f'Enter DFA number (0-{len(D)-1}) (X to exit): ')
        try:
            choice = int(choice)
        except ValueError:
            if choice.lower() == 'x':
                quit()
            print('Invalid input.\n')
            break

        if choice >= len(D):
            print('DFA does not exist.\n')
            break
        else:
            action = input(
                f'D{choice} = {D[choice]}\n\n'
                f'Enter choice: \n\n1: Run DFA\n2: Minimize DFA\nX: Exit\n\n'
                f'or input anything else to go back: '
            )
            if action == '1':
                result = run_dfa(D[choice])
                print(result)
            if action == '2':
                min_dfa = minimize_dfa(D[choice])
                print(min_dfa)
            if action.lower() == 'x':
                print('Goodbye.')
                quit()


if __name__ == '__main__':
    main()
