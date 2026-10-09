import time
from abc import ABC, abstractmethod
from collections import deque

class RateLimitingStrategy(ABC):

    @abstractmethod
    def allowReq(self):
        pass

class TokenBucket(RateLimitingStrategy):

    def __init__(self,capacity,refillingRate):
        self.capacity=capacity
        self.rate=refillingRate

        self.tokens=capacity
        self.lastRefill=time.monotonic()

    def allowReq(self):

        now=time.monotonic()

        timeElapised=now-self.lastRefill
        newTokens=self.rate*timeElapised

        self.tokens=min(self.capacity,self.tokens+newTokens)
        self.lastRefill=now

        if self.tokens>=1:
            self.tokens-=1
            return True
        return False

class SlidingWindow(RateLimitingStrategy):

    def __init__(self,windowLength,maxReq):
        self.windowLen=windowLength
        self.maxReq=maxReq

        self.requests=deque()

    def allowReq(self):

        currentTime=time.monotonic()

        while self.requests and self.requests[0]<=currentTime-self.windowLen:
            self.requests.popleft()

        if len(self.requests)>=self.maxReq:
            return False

        self.requests.append(currentTime)
        return True

class RateLimiter:

    def __init__(self,strategy):
        self.startegy=strategy

    def allowReq(self):
        return self.startegy.allowReq()
