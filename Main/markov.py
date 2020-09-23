"""



Inspired By: https://www.cs.princeton.edu/courses/archive/fall19/cos126/assignments/markov/
Authors:
    Cameron Myron
"""

import random
from dataclasses import dataclass
from pickle import Pickler


@dataclass
class Markov:
    # The Dictionary that stores probabilities of a symbol following a sequence of symbols
    sequence_state = {}
    # The (int, Dictionary) pair that stores probabilities of a sequence of symbols starting a sequence (it
    # is a list because tuples are immutable)
    starter_state = [0, {}]  # [int, Dictionary]
    # The order of the Markov model
    k = 0  # int
    # Model's name
    n = ""
    # Model's data's type (this is a str)
    t = ""
    # Number of times the model has been saved
    v = 0

    """
    Initializes a new Markov model of order k with no data in it.
    
    @param self: self
    @param int k: Order of the Markov model
    """

    def __init__(self, n, t, k):
        self.k = k
        self.n = n
        self.t = t
        self.sequence_state = {}
        self.starter_state = [0, {}]

    """
    Gathers the number of occurrences for various things in a given sequence and adds these occurrences to the data.
    
    TODO: Maybe clean up the code a bit. Otherwise think of better ways to store the probabilities rather than a 
    Dictionary.
    
    @param self: self
    @param (Object) o: A n-tuple of objects (which includes strings)
    """

    def parse(self, o):
        if len(o) < self.k + 2:
            return
        t0 = tuple(o[:self.k + 1])
        if t0 not in self.starter_state[1]:
            self.starter_state[1][t0] = 1
        else:
            self.starter_state[1][t0] = self.starter_state[1][t0] + 1
        self.starter_state[0] += 1

        for i in range(len(o) - (self.k + 1)):
            t0 = tuple(o[i:i + self.k + 2])
            if t0[:-1] not in self.sequence_state:
                self.sequence_state[t0[:-1]] = [0, {}]
            if (t0[-1],) not in self.sequence_state[t0[:-1]][1]:
                self.sequence_state[t0[:-1]][1][(t0[-1],)] = 1
            else:
                self.sequence_state[t0[:-1]][1][(t0[-1],)] = self.sequence_state[t0[:-1]][1][(t0[-1],)] + 1
            self.sequence_state[t0[:-1]][0] += 1

    """
    NOTE: Both parse_file functions could crash the program... Try to think of a more elegant way than shoving
    a whole book worth of text into a single string... I am not splitting it by line because it destroys the grammatical
    structure (although I might change that later).
    """

    """
    Calls parse() and passes it the text in the given file.
    
    @param self: self
    @param str path: A string that has the file path to a text file to parse
    """

    def parse_file(self, path):
        with open(path, "r") as f:
            if self.t == "letters":
                self.parse(f.read())
            elif self.t == "words":
                self.parse(tuple(f.read().split(" ")))

    """
    Calls parse() and passes it the text in the given file with at most n characters

    @param self: self
    @param str path: A string that has the file path to a text file to parse
    @param int n: Maximum number of characters to read
    """

    def parse_n_file(self, path, n):
        with open(path, "r") as f:
            if self.t == "letters":
                self.parse(f.read(n))
            elif self.t == "words":
                self.parse(tuple(f.read(n).split(" ")))


    """
    Helper function to get a starting sequence of symbols based off the probability of it occurring.
    Will return None if the model "doesn't" know a starting sequence (which means it has no data).
    
    @param self: self
    @return: A sequence of symbols that starts has started a sequence or None
    """

    def new_starter(self):
        r = 1 - random.random()
        for i in self.starter_state[1].items():
            t0 = i[1] / self.starter_state[0]
            if r < t0:
                return i[0]
            else:
                r -= t0

    """
    Will generate and return a sequence with the given length based on the model's current data. If it can't generate
    a sequence (no data or a potential bug) it will return an error message.
    
    @param self: self
    @param int l: The desired length of the generated text
    @return: The generated sequence or an error message
    """

    def generate(self, l):
        if l < self.k + 1:
            return "Error: Length of the output is too short"

        rtn = []
        key = self.new_starter()  # (Tuple)
        if key is None:
            return "Error: No Data"
        # t0: [int, Dictionary]
        t2 = len(rtn)
        while len(rtn) + len(key) < l:
            if key in self.sequence_state:
                t0 = self.sequence_state[key]
            else:
                rtn += list(key)
                key = self.new_starter()
                if len(rtn) + len(key) >= l:
                    rtn += list(key)
                    return rtn[:l]
                t0 = self.sequence_state[key]
            r = 1 - random.random()
            for i in t0[1].items():
                t1 = i[1] / t0[0]
                if r < t1:
                    rtn.append(key[0])
                    key = tuple(list(key[1:]) + list(i[0]))
                    break
                else:
                    r -= t1
            if len(rtn) == t2:
                return "Error: Unique substring given (might be a RANDOM glitch)"
            t2 = len(rtn)
        return tuple(rtn)

    """
    Will save the current state of the Markov model in a file with the name in the format of "nv".
    
    @param self: self
    """

    def save(self):
        with open(self.n + str(self.v), "wb") as f:
            Pickler(f).dump(self)
            self.v += 1


"""(project) Translate the following pseudo-code into working code. The function should be named minChange.
    (The first argument is the amount of money and the second argument is a list of denominations. It returns
    the minimum number of coins required.) You will also need to write code for ⊕ and min. The ⊕ operation
    is understood here as an extension of regular addition so that it also works on Failure; Failure plus anything
    is Failure. The function min is also extended to work with Failure; numbers are understood as smaller than
    Failure."""

if __name__ == "__main__":
    m = Markov("test", 1)
    # The text below is from my Analysis of Algorithms homework
    nt = tuple("Cats are great aren't they?".split(" "))
    m.parse(nt)
    print(" ".join(m.generate(25)))
    print()
    m2 = Markov("test", 1)
    s = "Cats are great aren't they?"
    m2.parse(s)
    print("".join(m2.generate(25)))
