
class Node:

    def __init__(self,key,val,next=None,prev=None):
        self.key=key
        self.val=val
        self.next=next
        self.prev=prev

class LRUCache:

    def __init__(self,capacity):

        self.cap=capacity
        self.map={}
        self.head=Node(-1,-1)
        self.tail=Node(-1,-1)

        self.head.next=self.tail
        self.tail.prev=self.head

    def insert_at_front(self,node):

        prevFirst=self.head.next

        self.head.next=node
        node.prev=self.head

        node.next=prevFirst
        prevFirst.prev=node

    def remove(self,node):

        front=node.next
        back=node.prev

        front.prev=back
        back.next=front

    def put(self,key,val):

        if key in self.map:
            self.map[key].val=val
            self.remove(self.map[key])
            self.insert_at_front(self.map[key])
            return

        node=Node(key,val)
        self.map[key]=node
        self.insert_at_front(node)

        if len(self.map)>self.cap:
            del self.map[self.tail.prev.key]
            self.remove(self.tail.prev)

    def get(self,key):

        if key not in self.map:
            return "Key not found"

        self.remove(self.map[key])
        self.insert_at_front(self.map[key])

        return self.map[key].val

lru=LRUCache(3)

lru.put(3,"3")
lru.put(2,'2')
print(lru.get(2))
print(lru.get(1))
lru.put(5,"5")
lru.put(7,'7')
print(lru.get(3))

