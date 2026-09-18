import random
class DoublyLinkedListBase:
    class Node:
        __slots__ = 'element', 'prev', 'next'
        def __init__(self, element, prev, next):
            self.element = element
            self.prev = prev
            self.next = next

    def __init__ (self):
        self.header = self.Node(None, None, None)
        self.trailer = self.Node(None, None, None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def _insert(self, e, predecessor, successor):
        newest = self.Node(e, predecessor, successor)
        predecessor.next = newest
        successor.prev = newest
        self.size += 1
        return newest

    def delete(self, node):
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1
        element = node.element
        node.prev = node.next = node.element = None
        return element

class PositionalList(DoublyLinkedListBase):

        class Position:

            def __init__(self, container, node):
                self._container = container
                self._node = node

            def element(self):
                return self._node.element

            def __eq__(self, other):
                return type(other) is type(self) and other._node is self._node

            def __ne__(self, other):
                return not (self == other)

        def _validate(self, p):

            if not isinstance(p, self.Position):
                raise TypeError('p must be proper Position type')
            if p._container is not self:
                raise ValueError('p does not belong to this container')
            if p._node.next is None:
                raise ValueError('p is no longer valid')
            return p._node

        def _make_position(self, node):
            if node is self.header or node is self.trailer:
                return None
            else:
                return self.Position(self, node)

        def first(self):

            return self._make_position(self.header.next)

        def last(self):

            return self._make_position(self.trailer.prev)

        def before(self, p):

            node = self._validate(p)
            return self._make_position(node.prev)

        def after(self, p):

            node = self._validate(p)
            return self._make_position(node.next)

        def __iter__(self):

            cursor = self.first()
            while cursor is not None:
                yield cursor.element()
                cursor = self.after(cursor)

        def _insert_between(self, e, predecessor, successor):

            node = super()._insert(e, predecessor, successor)
            return self._make_position(node)

        def add_first(self, e):

            return self._insert_between(e, self.header, self.header.next)

        def add_last(self, e):

            return self._insert_between(e, self.trailer.prev, self.trailer)

        def add_before(self, p, e):

            original = self._validate(p)
            return self._insert_between(e, original._prev, original)

        def add_after(self, p, e):

            original = self._validate(p)
            return self._insert_between(e, original, original._next)

        def delete(self, p):
            original = self._validate(p)
            return super().delete(original)


        def replace(self, p, e):
            original = self._validate(p)
            old_value = original._element
            original._element = e
            return old_value

class PriorityQueueBase:
    class _Item:
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key

    def is_empty(self):
        return len(self) == 0


class PriorityQueue(PriorityQueueBase):  # base class defines _Item

    def __init__(self):
        self._data = PositionalList()

    def __len__(self):

        return len(self._data)

    def add(self, key: int, value: object):
        self._data.add_last(self._Item(key, value))

    def min(self):
        p = self._find_min()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self):
        p = self._find_min()
        item = self._data.delete(p)
        return (item._key, item._value)

    def _find_min(self):
        if self.is_empty():
            raise ValueError('Priority queue is empty')
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self._data.after(walk)
        return small
#until the line below, most of the code above, I got from zybook as i was unsure where to start, the rest below were wriiten by me#
#---------------------------------------------------------------------------------------------------------------------------------#

def luggage_id():
    return random.randint(1000, 9999)

class Luggage:
    def __init__(self, passenger_name, travel_class):
        self.id = luggage_id()
        self.passenger_name = passenger_name
        self.travel_class = travel_class
        self.priority = self.set_priority()

    def set_priority(self):
       Priority = {"First Class":1, "Economy Plus":2, "Economy":3}
       return Priority.get(self.travel_class, 3)

    def __str__(self):
        return f"{self.passenger_name} - {self.travel_class} - ID: {self.id} - Priority: {self.priority}"

class luggagequeue(PriorityQueue):
    def add_luggage(self, luggage):
        self.add(luggage.priority, luggage)

    def display_queue(self):
        if self.is_empty():
            print('Queue is empty')
        else:
            for item in self._data:
                print(item._value)

    def display_queue_priority(self):
        if self.is_empty():
            print('No luggage in queue')
        else:
            for item in self._data:
                luggage = item._value
                print(f"Luggage ID: {luggage.id}, Priority: {luggage.priority}")

def travel_classvaldation():
    while True:
        travel_class = input("Enter a travel class name (First Class, Economy Plus, and Economy): ").strip()
        if travel_class.strip() in ["First Class", "Economy Plus", "Economy"]:
            return travel_class
        print("Invalid travel class name")

def main():

    print("Welcome to Luggage ID Generator ")
    luggage = luggagequeue()
    ask_again = False
    while not ask_again:
        print("1. Generate Luggage ID")
        print("2. View Luggage Queue")
        print("3. View Luggage Priority")
        print("4. Exit")
        user_choice = input("Enter your choice:").strip()

        print()

        if user_choice == '1':
            passenger = input("Enter passenger name: ")
            travelclass = travel_classvaldation()
            new_luggage = Luggage(passenger, travelclass)
            luggage.add_luggage(new_luggage)
            print(f"Luggage ID generated: {new_luggage.id}\n")

        elif user_choice == '2':
            luggage.display_queue()

        elif user_choice == '3':
            luggage.display_queue_priority()

        elif user_choice == '4':
            print("Thank you for using Luggage ID Generator")
            ask_again = True

        else:
            print("Invalid input")
            print(user_choice)

main()