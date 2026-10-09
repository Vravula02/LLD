"""
    Design a parking lot where there are two types of parking slots, small and big where a small can fit into big but not the other way round.
    """

from abc import ABC, abstractmethod
import uuid
import threading
from datetime import datetime


#####----Vehicle Class-----#####

class Vehicle(ABC):

    def __init__(self,licenceNumber):
        self.licenceNumber=licenceNumber

    @abstractmethod
    def get_size(self):
        pass

class car(Vehicle):
    def get_size(self):
        return "small"

class MotorCycle(Vehicle):
    def get_size(self):
        return "small"

class truck(Vehicle):
    def get_size(self):
        return "big"

########----ParkingSlot----########

class ParkingSlot:

    def __init__(self,size,floor):
        self.spotId=str(uuid.uuid4())
        self.size=size
        self.floor=floor
        self.isOccupied=False
        self._lock=threading.Lock()

    def canFit(self,vehicle):

        if vehicle.get_size()=="big":
            return self.size=="big"
        return True

    def assign(self):
        with self._lock:
            if self.isOccupied:
                return False
            self.isOccupied=True
            return True

    def free(self):

        with self._lock:
            self.isOccupied=False

######---Ticket---####

class Ticket:

    def __init__(self,vehicle,parkingSpot):
        self.ticketID=str(uuid.uuid4())
        self.vehicle=vehicle
        self.parkingspot=parkingSpot
        self.entryTime=datetime.now()

class Receipt:

    def __init__(self,ticketID,entryTime,pricing):
        self.ticketID=ticketID
        self.entryTime=entryTime
        self.exitTime=datetime.now()
        self.amount=pricing.calculateFee(
            self.entryTime,
            self.exitTime
        )



class PricingStrategy(ABC):

    @abstractmethod
    def calculateFee(self,entryTime,exitTime):
        pass

class hourly(PricingStrategy):
    rate=2.5

    def calculateFee(self, entryTime, exitTime):
        hours = max(1, (exitTime - entryTime).total_seconds() / 3600)
        return round(hours * self.rate, 2)


#####---ParkingLot----######

class ParkingLot:

    def __init__(self,pricingStrategy):
        self.slots=[]
        self.activeTickets={}
        self.pricingStrategy=pricingStrategy


    def add_slots(self,slot):
        self.slots.append(slot)

    def enterVehicle(self,vehicle):

        if vehicle.get_size()=="small":
            slots=sorted(self.slots,key= lambda x:0 if x.size=="small" else 1)
        else:
            slots=self.slots

        for slot in slots:
            if slot.canFit(vehicle) and slot.assign():
                ticket=Ticket(vehicle,slot)
                self.activeTickets[ticket.ticketID]=ticket
                return ticket
        return "No available slots"

    def exitVehicle(self,ticketId):

        ticket=self.activeTickets.get(ticketId)

        if not ticket:
            return "Invalid ticket"

        receipt = Receipt(
            ticket.ticketID,
            ticket.entryTime,
            self.pricingStrategy
        )

        ticket.parkingspot.free()


        del self.activeTickets[ticket.ticketID]

        return receipt

from datetime import datetime


# =========================
# Driver Code
# =========================

if __name__ == "__main__":

    # Create parking lot with hourly pricing
    parkingLot = ParkingLot(hourly())

    # --------------------------------
    # Add parking slots
    # --------------------------------

    parkingLot.add_slots(ParkingSlot("small", 1))
    parkingLot.add_slots(ParkingSlot("small", 1))
    parkingLot.add_slots(ParkingSlot("big", 1))

    parkingLot.add_slots(ParkingSlot("small", 2))
    parkingLot.add_slots(ParkingSlot("big", 2))

    # --------------------------------
    # Create vehicles
    # --------------------------------

    car1 = car("CAR-101")
    motorcycle1 = MotorCycle("BIKE-202")
    truck1 = truck("TRUCK-303")

    # --------------------------------
    # Park Car
    # --------------------------------

    ticket1 = parkingLot.enterVehicle(car1)

    print("\n===== CAR PARKING =====")

    if isinstance(ticket1, Ticket):
        print("Car parked successfully")
        print("Ticket ID:", ticket1.ticketID)
        print("Vehicle:", ticket1.vehicle.licenceNumber)
        print("Vehicle Size:", ticket1.vehicle.get_size())
        print("Spot ID:", ticket1.parkingspot.spotId)
        print("Floor:", ticket1.parkingspot.floor)
        print("Entry Time:", ticket1.entryTime)
    else:
        print(ticket1)

    # --------------------------------
    # Park Motorcycle
    # --------------------------------

    ticket2 = parkingLot.enterVehicle(motorcycle1)

    print("\n===== MOTORCYCLE PARKING =====")

    if isinstance(ticket2, Ticket):
        print("Motorcycle parked successfully")
        print("Ticket ID:", ticket2.ticketID)
        print("Vehicle:", ticket2.vehicle.licenceNumber)
        print("Vehicle Size:", ticket2.vehicle.get_size())
        print("Spot ID:", ticket2.parkingspot.spotId)
        print("Floor:", ticket2.parkingspot.floor)
        print("Entry Time:", ticket2.entryTime)
    else:
        print(ticket2)

    # --------------------------------
    # Park Truck
    # --------------------------------

    ticket3 = parkingLot.enterVehicle(truck1)

    print("\n===== TRUCK PARKING =====")

    if isinstance(ticket3, Ticket):
        print("Truck parked successfully")
        print("Ticket ID:", ticket3.ticketID)
        print("Vehicle:", ticket3.vehicle.licenceNumber)
        print("Vehicle Size:", ticket3.vehicle.get_size())
        print("Spot ID:", ticket3.parkingspot.spotId)
        print("Floor:", ticket3.parkingspot.floor)
        print("Entry Time:", ticket3.entryTime)
    else:
        print(ticket3)

    # --------------------------------
    # Show active tickets
    # --------------------------------

    print("\n===== ACTIVE TICKETS =====")

    for ticket_id, ticket in parkingLot.activeTickets.items():

        print(
            f"Ticket: {ticket_id} | "
            f"Vehicle: {ticket.vehicle.licenceNumber} | "
            f"Spot: {ticket.parkingspot.spotId}"
        )

    # --------------------------------
    # Car exits
    # --------------------------------

    print("\n===== CAR EXIT =====")

    receipt = parkingLot.exitVehicle(ticket1.ticketID)

    if isinstance(receipt, Receipt):

        print("Car exited successfully")
        print("Ticket ID:", receipt.ticketID)
        print("Entry Time:", receipt.entryTime)
        print("Exit Time:", receipt.exitTime)
        print("Parking Fee: $", receipt.amount)

    else:
        print(receipt)

    # --------------------------------
    # Show remaining active tickets
    # --------------------------------

    print("\n===== REMAINING ACTIVE TICKETS =====")

    for ticket_id, ticket in parkingLot.activeTickets.items():

        print(
            f"Ticket: {ticket_id} | "
            f"Vehicle: {ticket.vehicle.licenceNumber} | "
            f"Spot: {ticket.parkingspot.spotId}"
        )