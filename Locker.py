from enum import Enum
from datetime import datetime,timedelta
import uuid


class Item:

    def __init__(self,size):
        self.size=size

    def getSize(self):
        return self.size
    
class Token:

    def __init__(self,code,expiration,compartment):
        self.code=code
        self.expiration=expiration
        self.compartment=compartment

    def isExpired(self):
        return self.expiration<datetime.now()

    def getCode(self):
        return self.code

class Compartment:

    def __init__(self,size):
        self.size=size
        self.isOccupied=False

    def getSize(self):
        return self.size

    def canFit(self,item):
        return item.getSize()<=self.getSize()

    def isFree(self):
        return not self.isOccupied

    def open(self):
        pass

    def makeFree(self):
        self.isOccupied=False

    def makeunAvailable(self):
        self.isOccupied=True

class Locker:

    def __init__(self):
        self.compartments=[]
        self.activeTokens={}

    def addCompartments(self,compartment):
        self.compartments.append(compartment)

    def placeItem(self,item):

        for compartment in self.compartments:
            if compartment.isFree() and compartment.canFit(item):

                compartment.open()
                compartment.makeunAvailable()

                code=str(uuid.uuid4())
                token=Token(code,datetime.now()+timedelta(7),compartment)
                self.activeTokens[code]=token

                return code
        return False

    def takeItem(self,code):

        if code not in self.activeTokens:
            return False

        token=self.activeTokens[code]

        if token.isExpired():
            return False

        compartment=token.compartment
        compartment.open()
        compartment.makeFree()

        del self.activeTokens[code]
        return True

    def removeExpired(self):

        expired=[]

        for code,token in self.activeTokens.items():
            if token.isExpired():
                compartment=token.compartment
                compartment.open()
                compartment.makeFree()
                expired.append(code)

        for code in expired:
            del self.activeTokens[code]


# ---------------- DRIVER CODE ----------------

locker = Locker()

# Add compartments
smallCompartment = Compartment(1)
mediumCompartment = Compartment(2)
bigCompartment = Compartment(3)

locker.addCompartments(smallCompartment)
locker.addCompartments(mediumCompartment)
locker.addCompartments(bigCompartment)


# Create items
smallItem = Item(1)
mediumItem = Item(2)
bigItem = Item(3)


# Place small item
token1 = locker.placeItem(smallItem)

print("Small item token:", token1)
print("Small compartment occupied:", smallCompartment.isOccupied)


# Place medium item
token2 = locker.placeItem(mediumItem)

print("Medium item token:", token2)
print("Medium compartment occupied:", mediumCompartment.isOccupied)


# Take small item
print("Take small item:", locker.takeItem(token1))
print("Small compartment occupied:", smallCompartment.isOccupied)


# Place big item
token3 = locker.placeItem(bigItem)

print("Big item token:", token3)
print("Big compartment occupied:", bigCompartment.isOccupied)


# Try using an invalid token
print("Invalid token:", locker.takeItem("invalid-token"))


# Check active tokens
print("Active tokens:", len(locker.activeTokens))