from abc import ABC,abstractmethod
import uuid
import threading
from datetime import datetime

#####-----Vehicle Hierarcy-----#####

class Vehicle(ABC):

    def __init__(self,licence_plate):
        self.licence_plate=licence_plate

    @abstractmethod
    def get_size(self):
        pass

class MotorCycle(Vehicle):

    def get_size(self):
        return 1

class Car(Vehicle):

    def get_size(self):
        return 1

class Truck(Vehicle):
    def get_size(self):
        return 2

#####-----Slot-----#####

class Slot:

    def __inint__(self,floor,size):
        self.UId=str(uuid.uuid4())
        self.floor=floor
        self.size=size
        self.isOccupied=False
        self._lock=threading.Lock()

    def can_fit(self,vehicle):

        if vehicle.get_size()==2:
            return self.size==2
        return True

    def assign(self,vehicle):

        with self._lock:
            if not self.isOccupied:
                self.isOccupied=True
                return True
            else:
                return False

    def free(self):
        with self._lock:
            self.isOccupied=False

#####-----ticket-----#####

class Ticket:

    def __init__(self,vehicle,spot):
        self.UId=str(uuid.uuid4())
        self.vehicle=vehicle
        self.spot=spot
        self.entry_time=datetime.now()

#####-----PricingStartegies-----#####

class PricingStrategy(ABC):

    @abstractmethod
    def calculate_fee(self,ticket):
        pass

class hourly_fee(PricingStrategy):

    def __init__(self,ticket,rate):
        self.ticket=ticket
        self.rate=rate

    def calculate_fee(self):
        entry_time=self.ticket.entry_time
        exit_time=datetime.now()
        seconds=(exit_time-entry_time).total_seconds()
        amount=max(1,seconds//3600)*self.rate

        return round(amount,2)

#####-----Receipt-----#####

class Receipt:

    def __init__(self,ticket,pricing):
        self.ticket=ticket
        self.pricing=pricing
        self.amount=pricing.calculate_fee()



        

        

    
