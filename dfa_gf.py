#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 19 Mar 2023 17:32:13

@author: gsfran
"""

from __future__ import annotations


class DFA:

    def __init__(
        self, Q: set[int], Sigma: set[str],
        delta: dict[tuple[int, str], int],
        q0: int, F: set[int]
    ) -> None:
        """Initializes the Deterministic Finite Automaton

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
            f'DFA({self.states},\n\t{self.symbols},\n\t{self.transitions},'
            f'\n\t{self.initial_state},\n\t{self.final_states})'
        )

    def run(self, word: str) -> bool:
        """Runs the defined automaton

        Args:
            word (str): The input word

        Returns:
            bool: True if word is in the defined automata language,
            otherwise False
        """
        current_state = self.initial_state
        while word:
            current_state = self.transitions[(current_state, word[0])]
            word = word[1:]

        return current_state in self.final_states

    def minimize(self) -> DFA:
        # return the minimal DFA
        # the minimisation.pdf which is a section
        # of the lecture notes :
        # Thorsten Altenkirch, Venanzio Capretta, and Henrik Nilsson.
        # "Languages and Computation." (2019).
        ...


# example from video
# no a's may follow b's
D0 = DFA(
    Q={0, 1, 2},
    Sigma={'a', 'b'},
    delta={
        (0, 'a'): 0, (0, 'b'): 1, 
        (1, 'a'): 2, (1, 'b'): 1,
        (2, 'a'): 2, (2, 'b'): 2
    },
    q0=0,
    F={0, 1}
)

# example from video
# a % 2 must equal b % 2
D1 = DFA(
    Q={0, 1, 2, 3},
    Sigma={'a', 'b'},
    delta={
        (0, 'a'): 2, (0, 'b'): 1,
        (1, 'a'): 0, (1, 'b'): 3,
        (2, 'a'): 0, (2, 'b'): 3,
        (3, 'a'): 1, (3, 'b'): 2
    },
    q0=0,
    F={0, 3}
)

# example from minimisation.pdf
# test case : D2.minimize()
D2 = DFA({0, 1, 2, 3, 4, 5}, {'a', 'b'},
         {(0, 'a'): 1, (0, 'b'): 4,
          (1, 'a'): 2, (1, 'b'): 3,
          (2, 'a'): 2, (2, 'b'): 2,
          (3, 'a'): 2, (3, 'b'): 3,
          (4, 'a'): 5, (4, 'b'): 4,
          (5, 'a'): 5, (5, 'b'): 4},
         0,
         {2, 3})



def main():
    choice = int(input(f'Enter DFA number: '))
    

if __name__ == '__main__':
    main()