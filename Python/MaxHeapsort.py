import datetime
class MaxHeap:
    def __init__(self, items=[]):
        super().__init__()
        self.heap = [0]
        for i in items:
            self.heap.append(i)
            self.__floatUp(len(self.heap) - 1)
    def push(self, data):
        self.heap.append(data)
        self.__floatUp(len(self.heap) -  1)

    def peek(self):
        if self.heap[1]:
            return self.heap[1]
        else:
            return False

    def pop(self):
        if len(self.heap) > 2:
            self.__swap(1, len(self.heap) - 1)
            max = self.heap.pop()
            self.__bubbleDown(1)
        elif len(self.heap) == 2:
            max = self.heap.pop()
        else:
            max = False
        return max

    def __str__(self):
        return str(self.heap[0:len(self.heap)])

    def printArray(self):
        print("|\t", end='')
        for i in range(1, len(self.heap)):
            print(str(i) + "\t|\t", end='')

        print()
        print("|\t", end='')

        for i in range(1, len(self.heap)):
            print(str(self.heap[i]) + "\t|\t", end='')
        print()

    def __swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def __floatUp(self, index):
        parent = index // 2
        if index <= 1:
            return
        elif self.heap[index] > self.heap[parent]:
            self.__swap(index, parent)
            self.__floatUp(parent)

    def __bubbleDown(self, index):
        left = index * 2
        right = left * 2 + 1
        largest = index
        if len(self.heap) > left and self.heap[largest] < self.heap[left]:
            largest = left
        if len(self.heap) > right and self.heap[largest] < self.heap[right]:
            largest = right
        if largest != index:
            self.__swap(index, largest)
            self.__bubbleDown(largest)
def read_file(filename):
    with open(filename, "r") as file:
        data = file.read()
        return data

def parse_logs(*logs):
    entries = []
    for log in logs:
        lines = log.strip().split("\n")
        for line in lines:
            try:
                timestamp_str = line.split(" ", 2)[:2]
                timestamp = datetime.datetime.strptime(" ".join(timestamp_str), "%m/%d/%Y %I:%M%p")
                entries.append((timestamp, line))
            except Exception as e:
                print(f"Skipping Line due to error: {line} - {e}")
    return entries

def sort_logsbydate(log_entries):
    heap = MaxHeap()
    for entry in log_entries:
        heap.push((entry[0].timestamp(), entry[1]))

    sorted_logs = []
    while len(heap.heap) > 1:
        item = heap.pop()
        sorted_logs.append(item[1])

    return sorted_logs[::-1]


def main():
    print("Abenezer Lemma,\nProgram 8")
    print()

    data1 = read_file("FrontDoor.txt")
    data2 = read_file("SideDoor.txt")
    data3 = read_file("ServerDoor.txt")

    entries = parse_logs(data1, data2, data3)


    heap = MaxHeap()
    for entry in entries:

        heap.push((entry[0].timestamp(), entry[1]))

    sorted_entries = []
    while len(heap.heap) > 1:
        item = heap.pop()
        sorted_entries.append(item[1])


    sorted_entries.reverse()


    for line in sorted_entries:
        print(line)

main()
# AVL62270002 bDA669AQ