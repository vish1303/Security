class Node(object):

    def __init__(self, data = None, prev = None, next = None):
        self.data = data
        self.prev = prev
        self.next = next

class DLL(object):

    head = tail = None

    # Showing elements of the list

    def show(self):

        cur = self.head

        print "Elements of the list include:"

        while cur is not None:
            
            #print cur.prev.data if hasattr(cur.prev, "data") else None
            print cur.data, "->",
            #print cur.next.data if hasattr(cur.next, "data") else None

            cur = cur.next

        print None

    # Appending elements to the list

    def append(self, data):

        new_node = Node(data)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

    # Removing elements of the list

    def remove(self, data):

        cur = self.head

        while cur is not None:
            if cur.data == data:
                if cur.prev is None:
                    self.head = cur.next
                    cur.next.prev = None  # self.head.prev = None
                    break
                else:
                    cur.prev.next = cur.next
                    cur.next.prev = cur.prev
                    break

            cur = cur.next
        if cur is None:
            print "Element not found"

n = DLL()

n.append(1)
n.append(2)
n.append(3)
n.append(4)
n.append(5)

n.show()

n.remove(3)

n.show()

n.remove(6)
