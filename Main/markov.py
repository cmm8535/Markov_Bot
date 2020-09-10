"""



Inspired By: https://www.cs.princeton.edu/courses/archive/fall19/cos126/assignments/markov/
Authors:
    Cameron Myron
"""

import random
from dataclasses import dataclass

from Main.hashtable import Hashtable


@dataclass
class Markov:
    # The hashtable that stores probabilities of a character following a sequence of characters
    sequence_state: Hashtable
    # The hashtable that stores probabilities of a sequence of characters starting a message
    starter_state: [int, Hashtable]
    # The order of the Markov model
    k: int

    """
    Initializes a new Markov model of order k with no data in it.
    
    @param self: self
    @param k: Order of the Markov model
    """

    def __init__(self, k: int):
        self.k = k
        self.sequence_state = Hashtable(50)
        self.starter_state = [0, Hashtable(50)]

    """
    Initializes a new Markov model based on a saved state.
    
    TODO: The whole function
    
    @param self: self
    @param path: A string that has the file path to the saved state
    """

    # def __init__(self, path: str):
    #    return

    """
    Gathers the number of occurrences for various things in a given string and adds these occurrences to the data.
    
    TODO: Maybe clean up the code a bit. Otherwise think of better ways to store the probabilities rather than a 
    hashtable.
    
    @param self: self
    @param s: A string
    """

    def parse(self, s: str):
        if len(s) < self.k + 1:
            return
        t0: str = s[:self.k]
        if self.starter_state[1].get(t0) is None:
            self.starter_state[1].set(t0, 1)
        else:
            self.starter_state[1].set(t0, self.starter_state[1].get(t0) + 1)
        self.starter_state[0] += 1

        for i in range(len(s) - self.k):
            t0 = s[i:i + self.k + 1]
            if self.sequence_state.get(t0[:-1]) is None:
                self.sequence_state.set(t0[:-1], [0, Hashtable(5)])
            if self.sequence_state.get(t0[:-1])[1].get(t0[-1]) is None:
                self.sequence_state.get(t0[:-1])[1].set(t0[-1], 1)
            else:
                self.sequence_state.get(t0[:-1])[1].set(t0[-1], self.sequence_state.get(t0[:-1])[1].get(t0[-1]) + 1)
            self.sequence_state.get(t0[:-1])[0] += 1

    """
    Calls parse() and passes it the text in the given file.
    
    TODO: The whole function
    
    @param self: self
    @param path: A string that has the file path to a text file to parse
    """

    # def parse_file(self, path: str):
    #    return

    """
    Helper function to get a starting sequence of letters based off off the probability of it occurring.
    Will return None if the model "doesn't" know a starting sequence (which means it has no data).
    
    TODO: Make it so that it returns a sequence that starts a sentence (which would be a forced English standard
    but for now I can't think of a better way).
    
    @param self: self
    @return: A sequence of letters that starts has started a message or None
    """

    def new_starter(self) -> str:
        t0: float
        r: float = random.random()
        for i in self.starter_state[1].table:
            if i is not None:
                t0 = i[1] / self.starter_state[0]
                if r < t0:
                    return i[0]
                else:
                    r -= t0

    """
    Will generate and return text with the given length based on the model's current data. If it can't generate
    text (no data or a potential bug) it will return an error message.
    
    @param self: self
    @param l: The desired length of the generated text
    @return: The generated text or an error message
    """

    def generate(self, l: int) -> str:
        if l < self.k:
            return "Error: Length of the output is too short"

        rtn: str = self.new_starter();
        if rtn is None:
            return "Error: No Data"
        t0: [int, Hashtable]
        t1: float
        t2: int = len(rtn)
        r: float
        while len(rtn) < l:
            t0 = self.sequence_state.get(rtn[-self.k:])
            if t0 is None:
                rtn += ("\n" + self.new_starter())
                if len(rtn) >= l:
                    return rtn[:l]
                t0 = self.sequence_state.get(rtn[-self.k:])
            r = random.random()
            for i in t0[1].table:
                if i is not None:
                    t1 = i[1] / t0[0]
                    if r < t1:
                        rtn += i[0]
                        break
                    else:
                        r -= t1
            if len(rtn) == t2:
                return "Error: Unique substring given (might be a RANDOM glitch)"
            t2 = len(rtn)
        return rtn

    """
    Will save the current state of the Markov model in a file so that the data is persistent.
    
    TODO: The whole function
    
    @param self: self
    @param path: A string that has the file path to where the state should be saved
    """

    # def save(self, path: str):
    #    return


if __name__ == "__main__":
    m: Markov = Markov(10)
    # The text below is from my Analysis of Algorithms homework
    m.parse("""(project) Translate the following pseudo-code into working code. The function should be named minChange.
(The first argument is the amount of money and the second argument is a list of denominations. It returns
the minimum number of coins required.) You will also need to write code for ⊕ and min. The ⊕ operation
is understood here as an extension of regular addition so that it also works on Failure; Failure plus anything
is Failure. The function min is also extended to work with Failure; numbers are understood as smaller than
Failure.""")
    print(m.generate(1000))
