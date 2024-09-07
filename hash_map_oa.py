# Name: Tej Singh
# OSU Email: singhte@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: Monday, August 15th, 2023
# Description: A collection of hash map functions that perform different
#              operations, which demonstrate my ability to implement
#              hash maps with open addressing in my Python programs.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        :param key:   the key that determines the initial bucket
        :param value: the value that should be added to the hash map

        :return:      None
        """
        # resizes the hash map if necessary
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)
        # calculates initial bucket to look in
        bucket = self._hash_function(key) % self._capacity
        initialBucket = bucket
        probe = 0
        added = False
        while not(added):
            # inserts new hash entry if bucket empty
            if self._buckets[bucket] == None:
                self._buckets[bucket] = HashEntry(key, value)
                self._size += 1
                added = True
            # inserts new hash entry if bucket has tombstone
            elif self._buckets[bucket].is_tombstone == True:
                self._buckets[bucket] = HashEntry(key, value)
                self._size += 1
                added = True
            # replaces existing value if bucket has same key
            elif self._buckets[bucket].key == key:
                self._buckets[bucket].value = value
                added = True
            # quadratically probe to the next bucket          
            else:
                probe += 1
                bucket = (initialBucket + (probe ** 2)) % self._capacity

    def table_load(self) -> float:
        """
        Calculates the table load.

        :param self: the hash map being passed

        :return:     the table load
        """
        return self._size / self._capacity # return the hash map table load

    def empty_buckets(self) -> int:
        """
        Returns the amount of empty buckets.

        :param self: the hash map being passed

        :return:     amount of empty buckets
        """
        count = 0
        # iterate through hash map and count filled buckets
        for bucket in self:
            count += 1
        # return empty bucket count
        return self._capacity - count

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map.

        :param self:         the hash map being passed
        :param new_capacity: the capacity to resize to

        :return:             None
        """
        # only resize hash map if new capacity is greater than or equal to size
        if new_capacity >= self._size:
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

    def get(self, key: str) -> object:
        """
        Returns the value being held by the passed key.

        :param self: the hash map being passed
        :param key:  the key to get

        :return:     the value held by the key
        """
        # only look for key if hash map is not empty
        if self._size > 0:
            # determine initial bucket to look in
            bucket = self._hash_function(key) % self._capacity
            initialBucket = bucket
            probe = 0
            # quadratically probe through hash map 
            for i in range(self._capacity):
                # if the key is found in hash map, return the associated value
                if self._buckets[bucket]:
                    if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone == False:
                        return self._buckets[bucket].value
                # if key not found, quadratically probe to the next bucket
                probe += 1
                bucket = (initialBucket + (probe ** 2)) % self._capacity
            return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines whether the hashmap holds the passed key.

        :param self: the hash map being passed
        :param key:  the key to find

        :return:     boolean representing if key was found
        """
        # only look for key if hash map is not empty
        if self._size > 0:
            # determine initial bucket to look in
            bucket = self._hash_function(key) % self._capacity
            initialBucket = bucket
            probe = 0
            # iterate through hash map
            for i in range(self._capacity):
                # if the key is found in hash map, return true
                if self._buckets[bucket]:
                    if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone == False:
                        return True
                # if key not found, quadratically probe to the next bucket
                probe += 1
                bucket = (initialBucket + (probe ** 2)) % self._capacity
            return False
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
        initialBucket = bucket
        probe = 0
        # iterate through hash map
        for i in range(self._capacity):
            # if the key is found in hash map, set tombstone to true
            if self._buckets[bucket]:
                if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone == False:
                    self._buckets[bucket].is_tombstone = True
                    self._size -= 1
                    break
            # if key not found, quadratically probe to the next bucket
            probe += 1
            bucket = (initialBucket + (probe ** 2)) % self._capacity

    def clear(self) -> None:
        """
        Empties the hash map.

        :param self: the hash map being passed

        :return:     None
        """
        self._buckets = DynamicArray()
        # iterate through hash map and empty the buckets
        for i in range(self._capacity):
            self._buckets.append(None)
        # update the size of hash map
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns list of key and value pairs in the hash map.

        :param self: the hash map being passed

        :return:     list of hash entries
        """
        da = DynamicArray()
        # iterate through every bucket in hash map
        for bucket in self:
            da.append((bucket.key, bucket.value))
        return da

    def __iter__(self):
        """
        Create iterator for hash map loop.

        :param self: the hash map being passed

        :return:     instance of self
        """
        self._index = 0 # start iterating at index 0
        return self     # return instance of self

    def __next__(self):
        """
        Obtain next value and advance iterator.

        :param self: the hash map being passed

        :return:     value held in hash map index
        """
        try:
            # initialize value to see if it is empty
            value = self._buckets[self._index]
            # keep iterating through hashmap until hash entry is not empty
            while value == None or value.is_tombstone == True:
                self._index += 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration
        # update index and return the value       
        self._index += 1
        return value

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)