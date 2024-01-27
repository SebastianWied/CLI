class OneWayNode:  # For one way linked lists
    def __init__(self, value, nextNode=None):
        self.next = nextNode  # pointer to next node in linked list
        self.value = value

    def getNextNode(self):
        return self.next

    def checkLinked(self):
        if self.next is None:
            return False
        return True

    def setNextNode(self, nextNode):
        self.next = nextNode

    def getValue(self):
        return self.value


class Queue:
    def __init__(self):
        self.head = None
        self.last = None
        self.size = 0

    def enqueue(self, value):
        if not self.head:  # If queue is empty, create a new head node
            node = OneWayNode(value)
            self.head = node
            self.last = node
            self.size += 1
        else:  # Else, create a new node and link it to head
            node = OneWayNode(value)
            self.last.setNextNode(node)
            self.last = node
            self.size += 1

    def dequeue(self):
        if self.size == 0:
            return None  # Return none if trying to pull out a nonexistent node
        toDequeue = self.head
        newHead = toDequeue.getNextNode()
        self.head = newHead
        dequeuedValue = toDequeue.value
        self.size -= 1
        return dequeuedValue

    def peek(self):  # Look at head without dequeuing it
        head = self.head
        if head is None:
            return None
        return head.getValue()

    def getSize(self):
        return self.size

    def isEmpty(self):
        if self.size == 0:
            return True
        return False


class Stack:
    def __init__(self):
        self.primary = Queue()
        self.secondary = Queue()
        self.size = 0

    def push(self, value):
        if self.primary.isEmpty():
            self.primary.enqueue(value)
        else:
            # Keeps primary queue with only one value. Adds to end, then pulls
            #   front off.
            #   Primary queue stores the most recent value
            #   Second most recent value(previous primary head) will be at
            #   the back of the secondary queue now.
            self.primary.enqueue(value)
            primaryHead = self.primary.dequeue()
            self.secondary.enqueue(primaryHead)
        self.size += 1

    def pop(self):
        # Steps:
        #   Get most recent value from primary queue.
        #   Cycle secondary queue through the stack, which leaves back of
        #     secondary queue(second most recent val) in the primary queue
        #   Reduce size by 1
        toReturn = self.primary.dequeue()
        if not self.secondary.isEmpty():
            for _ in range(self.secondary.getSize()):
                value = self.secondary.dequeue()
                self.push(value)
        self.size -= 1
        return toReturn

    def peek(self):
        value = self.primary.dequeue()
        self.primary.enqueue(value)
        return value

    def getSize(self):
        return self.size

    def isEmpty(self):
        if self.size == 0:
            return True
        return False
