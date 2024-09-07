# Name: Tej Singh
# OSU Email: singhte@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: Monday, August 15th, 2023
# Description: A collection of hash map functions that perform different
#              operations, which demonstrate my ability to implement
#              hash maps with singly chaining in my Python programs.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds an element to the hash map.

        :param self:  the hash map being passed
        :param key:   the key that determines the bucket
        :param value: the value that should be added to the hash map

        :return:      None
        """
        # resize hash map if load deems necessary
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)
        # determine which bucket to put in
        bucket = self._hash_function(key) % self._capacity
        node = self._buckets[bucket].contains(key)
        # if key doesn't already exist, insert node with key/value pair
        if node == None:
            self._buckets[bucket].insert(key, value)
            self._size += 1
        # if key exists, simply update value
        else:
            node.value = value

    def empty_buckets(self) -> int:
        """
        Returns the amount of empty buckets.

        :param self: the hash map being passed

        :return:     amount of empty buckets
        """
        count = 0
        # iterate through hash map and count empty buckets
        for i in range(self._capacity):
            if self._buckets[i].length() <= 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Calculates the table load.

        :param self: the hash map being passed

        :return:     the table load
        """
        return self._size / self._capacity # return the hash map table load

    def clear(self) -> None:
        """
        Empties the hash map.

        :param self: the hash map being passed

        :return:     None
        """
        self._buckets = DynamicArray()
        # iterate through hash map and empty the buckets
        for i in range(self._capacity):
            self._buckets.append(LinkedList())
        # update the size of hash map
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map.

        :param self:         the hash map being passed
        :param new_capacity: the capacity to resize to

        :return:             None
        """
        # only resize hash map if new capacity is at least 1
        if new_capacity >= 1:
            # find next prime if new capacity isn't a prime number
            if not(self._is_prime(new_capacity)):
                new_capacity = self._next_prime(new_capacity)
            # get list of key/value pairs, update capacity, and clear hash map
            data = self.get_keys_and_values()
            self._capacity = new_capacity
            self.clear()
            # using list of key/value pairs, rehash them into hash map
            for i in range(data.length()):
                self.put(data[i][0], data[i][1])

    def get(self, key: str):
        """
        Returns the value being held by the passed key.

        :param self: the hash map being passed
        :param key:  the key to get

        :return:     the value held by the key
        """
        # determine bucket to look in and find node with key
        bucket = self._hash_function(key) % self._capacity
        node = self._buckets[bucket].contains(key)
        # return value associated with key if key exists
        if node == None:
            return None
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Determines whether the hashmap holds the passed key.

        :param self: the hash map being passed
        :param key:  the key to find

        :return:     boolean representing if key was found
        """
        # only look for key if hash map not empty
        if self._size > 0:
            # determine bucket to look in and find node with key
            bucket = self._hash_function(key) % self._capacity
            node = self._buckets[bucket].contains(key)
            # return true if key exists in hash map and false if not
            if node == None:
                return False
            else:
                return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the passed key from the hash map.

        :param self: the hash map being passed
        :param key:  the key to remove

        :return:     None
        """
        # determine bucket to remove from
        bucket = self._hash_function(key) % self._capacity
        # remove node with key and update size if key exists
        if self._buckets[bucket].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns list of key and value pairs in the hash map.

        :param self: the hash map being passed

        :return:     list of key and value pairs
        """
        da = DynamicArray()
        # iterate through every bucket and linked list in hash map
        for i in range(self._capacity):
            for node in self._buckets[i]:
                # add key/value pairs to a dynamic array
                da.append((node.key, node.value))
        return da

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a list of all modes and their frequency.

    :param da: dynamic array of values

    :return:   list of key and value pairs and the max frequency
    """
    # use a hash map to organize values and their frequencies
    map = HashMap(11, hash_function_2)
    modes = DynamicArray()
    maxFrequency = 0
    # add keys from dynamic array and update values of hash map
    for i in range(da.length()):
        _mode_add(map, str(da[i]))
    # iterate through hash map buckets
    for i in range(map._capacity):
        # this for loop runs ONCE for each bucket
        for node in map._buckets[i]:
            # reset list of modes and update max frequency if value
            # is greater than max frequency.
            if node.value > maxFrequency:
                maxFrequency = node.value
                modes = DynamicArray()
                modes.append(node.key)
            # add mode to list of modes if value is equal to max
            # frequency.
            elif node.value == maxFrequency:
                modes.append(node.key)
    return (modes, maxFrequency)

def _mode_add(map: HashMap, key: str) -> None:
    """
    Adds a key to hashmap and increases the value by 1 if key found.

    :param map: hash map to add key to
    :param key: the key to add

    :return:    None
    """
    # resize hash map if load deems necessary
    if map.table_load() >= 1.0:
        map.resize_table(map._capacity * 2)
    # determine which bucket to put in
    bucket = map._hash_function(key) % map._capacity
    node = map._buckets[bucket].contains(key)
    # if key doesn't already exist, insert node with key and value of one
    if node == None:
        map._buckets[bucket].insert(key, 1)
        map._size += 1
    # if key exists, simply add one to value
    else:
        node.value += 1

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")