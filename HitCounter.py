class HitCounter:
    def __init__(self):
        self.hits=[]

    def hit(self,timeStamp):

        if self.hits and self.hits[-1]==timeStamp:
            self.hits[-1][1]+=1
            return
        
        self.hits.append([timeStamp,1])

    def getHits(self,timeStamp):

        count=0

        for i in range(len(self.hits)):
            if self.hits[i][0]>timeStamp-300:
                count+=self.hits[i][1]
        return count


from collections import deque

class HitCounter:
    def __init__(self):
        self.hits=deque()

    def hit(self,timeStamp):

        while self.hits and self.hits[0][0]<timeStamp-300:
            self.hits.popleft()

        if self.hits and self.hits[-1][0]==timeStamp:
            self.hits[-1][1]+=1
            return

        self.hits.append([timeStamp,1])
 
    def getHits(self,timeStamp):

        while self.hits and self.hits[0][0]<timeStamp-300:
            self.hits.popleft()

        count=0

        for _,h in self.hits:
            count+=h
        return count


    

