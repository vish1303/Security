class Node(object):
    def __init__(self, data = None, next = next):
        self.data = data
        self.next = next


class CLL(object):
    
    head = None
    tail = None

    # Displaying elements of the list
    def show(self):

        cur = self.head.next

        print "Elements of the list are:"

        #print self.head.data, "->",

        while cur is not self.head:
            print cur.data, "->",
            cur = cur.next


    # Appending elements to the list

    def append(self, data):

        new_node = Node(data)
        cur = self.head
        new_node.next = self.head


        if self.head is None:
            new_node.next = new_node
        else:
            while cur.next != self.head:
                cur = cur.next
            cur.next = new_node

        self.head = new_node

    # Removing elements from the list

    def remove(self, data):
        
        cur = self.head.next

        if self.head.data == data:
            self.head = self.head.next




n = CLL()

n.append(1)
n.append(2)
n.append(3)
n.append(4)

n.show()




