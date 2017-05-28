class Node(object):
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next

class SLL(object):
    head = tail = None

    # Showing all the elemnets in the list
    def show(self):
        
        print "The current elements of the list are:"
        
        cur = self.head
        
        while cur is not None:
            print cur.data, "->",
            cur = cur.next
        
        print None

    # Appending elements to the list
    def append(self, data):

        new_node = Node(data)
        
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    # Removing an element from the list
    def remove(self, data):
        
        cur = self.head
        prev = None
        
        while cur is not None:
            if cur.data == data:
                if prev is None:
                    self.head = cur.next
                    break
                else:
                    prev.next = cur.next
                    break

            prev = cur
            cur = cur.next

        if cur is None:
            print "Element not found"

n = SLL()

n.append(1)
n.append(2)
n.append(3)

n.show()

n.remove(2)

n.show()

n.remove(4)




