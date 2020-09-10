"""
A class and functions for a hashtable that takes a string as a key and a value of anything

TODO: Find and fix the bug that makes it so that you could find a None if you try to get a value
      that is in the table and increment until its found (there should not be "holes" between an index based
      off a hash of a key the index of that key if that key is in the table), and then change the "get" method to
      return None if a None is seen (this is mostly an optimization problem (as if the key isn't in the table
      it requires the whole table to be searched to make sure), but in some cases it gave wrong values
      (duplicate keys in the table with different values)).

Inspiration: The hours I "invested" writing similar code in C for my final project in Mechanics of Programming
Special Thanks: Coffee
Authors:
    Cameron Myron
"""

from dataclasses import dataclass


@dataclass
class Hashtable:
    # The array of (key, val) pairs
    table: [[str, object]]
    # The current capacity of the hashtable (the length of "table")
    capacity: int
    # The number of (key, val) pairs currently in "table"
    size: int = 0

    """
    Creates a new (empty) Hashtable with the given starting capacity
    
    @param self: self
    @param capacity: The starting capacity of the new Hashtable
    """

    def __init__(self, capacity: int):
        self.table = [None] * capacity
        self.capacity = capacity

    """
    Increases the size of this Hashtable by the given factor and rehash the (key, val) pairs
    
    NOTE: May have a bug in it
    
    NOTE: Not "idiot proof"... Don't try plugging in a factor below 2
    
    @param self: self
    @param factor: The factor in which to increase the capacity of this Hashtable (new_capacity=old_capacity*factor)
    """

    def rehash(self, factor: int = 2):
        nt: [[str, object]] = [None] * self.capacity * factor
        for p in self.table:
            if p is not None:
                for i in range(self.capacity):
                    t0 = (hash(p[0]) + i) % self.capacity
                    if nt[t0] is None:
                        nt[t0] = p
                        break
        self.table = nt
        self.capacity *= factor

    """
    Store a (key, val) pair in the Hashtable. Can't store the value None. Will overwrite previous values in a (key, val)
    pair if given a key and different value.
    
    NOTE: May have a bug in it
    
    NOTE: If the Hashtable is somehow completely filled up (which shouldn't happened because it dynamically rehashes
    itself), it will not store the given (key, val) pair.
    
    @param self: self
    @param s: The given key to store with the (key, val) pair
    @param e: The given value to store with the (key, val) pair
    """

    def set(self, s: str, e: object):
        if e is None:
            print("Error: Can't store None Type")
            return
        while self.capacity / 2 < self.size + 1:
            self.rehash()
        for i in range(self.capacity):
            t0 = (hash(s) + i) % self.capacity
            if self.table[t0] is None:
                self.size += 1
                self.table[t0] = [s, e]
                return
            elif self.table[t0][0] == s:
                self.table[t0] = [s, e]
                return

        print("Error: Can't add '" + s + "'")

    """
    Gets the value stored with the given key in the Hashtable. Will return None if the given key isn't in the
    Hashtable
    
    NOTE: This method was changed to be less efficient in order to workaround a bug that violated assumptions this
    method needs to be efficient in all cases. With the current implementation the method needs to search the whole
    table in order to say that a key isn't in it.
    
    @param self: self
    @param s: The key to search for in the Hashtable
    @return: The value stored with the given key in the Hashtable or None
    """

    def get(self, s: str) -> object:
        for i in range(self.capacity):
            t0 = (hash(s) + i) % self.capacity
            if self.table[t0] is not None:
                if self.table[t0][0] == s:
                    return self.table[t0][1]
        return None


"""
This is just for testing out the Hashtable
"""

if __name__ == "__main__":
    f: Hashtable = Hashtable(1)
    print(f)
    f.set("at", Hashtable(5))
    f.get("at").set("z", 1)
    print(f)
    f.get("at").set("s", 1)
    print("->" + str(f.get("at")))
