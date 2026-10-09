class Node:
    def __init__(self,key,val,freq=None,next=None,prev=None):
        self.key=key
        self.val=val
        self.freq=freq
        self.next=next
        self.prev=prev

class DoublyLinkedList:

    def __init__(self):
        self.head=Node(-1,-1)
        self.tail=Node(-1,-1)

        self.head.next=self.tail
        self.tail.prev=self.head

    def insert_at_front(self,node):

        front=self.head.next

        self.head.next=node
        node.prev=self.head

        node.next=front
        front.prev=node

    def remove(self,node):

        front=node.next
        back=node.prev

        back.next=front
        front.prev=back

class LFU:

    def __init__(self,capacity):

        self.cap=capacity
        self.key_map={}
        self.freq_map={}
        self.min_freq=0


    def get_list(self,freq):

        if freq not in self.freq_map:
            self.freq_map[freq]=DoublyLinkedList()

        return self.freq_map[freq]

    def increase_freq(self,node):

        old_freq=node.freq
        old_list=self.get_list(old_freq)

        old_list.remove(node)

        if old_list.head.next==old_list.tail and self.min_freq==old_freq:
            self.min_freq+=1

        new_freq=old_freq+1
        new_list=self.get_list(new_freq)

        node.freq+=1
        new_list.insert_at_front(node)

    def get(self,key):

        if key in self.key_map:

            node=self.key_map[key]
            self.increase_freq(node)

            return node.val
        return -1

    def put(self,key,value):

        if self.cap==0:
            return 

        if key in self.key_map:
            node=self.key_map[key]
            node.val=value

            self.increase_freq(node)
            return

        if len(self.key_map)==self.cap:

            lfu_list=self.freq_map[self.min_freq]
            lru_node=lfu_list.tail.prev

            lfu_list.remove(lru_node)
            del self.key_map[lru_node.key]

        node=Node(key,value,1)
        freq_list=self.get_list(1)
        freq_list.insert_at_front(node)
        self.key_map[key]=node
        self.min_freq=1



lfu = LFU(2)

print("put(1, 1)")
lfu.put(1, 1)

print("put(2, 2)")
lfu.put(2, 2)

print("get(1):", lfu.get(1))  # Expected: 1
# Frequency of key 1 becomes 2

print("put(3, 3)")
lfu.put(3, 3)
# Key 2 should be removed because it has the lowest frequency

print("get(2):", lfu.get(2))  # Expected: -1
print("get(3):", lfu.get(3))  # Expected: 3
# Frequency of key 3 becomes 2

print("put(4, 4)")
lfu.put(4, 4)
# Key 1 should be removed because keys 1 and 3 have frequency 2,
# but key 1 is the least recently used among them

print("get(1):", lfu.get(1))  # Expected: -1
print("get(3):", lfu.get(3))  # Expected: 3
print("get(4):", lfu.get(4))  # Expected: 4



    
    