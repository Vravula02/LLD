from enum import Enum
from abc import ABC, abstractmethod

class NotificationType(Enum):

    EMAIL=1
    SMS=2

class User:

    def __init__(self,name,mail,phn):
        self.name=name
        self.mail=mail
        self.phn=phn

class Notification:

    def __init__(self,user,type,message):
        self.user=user
        self.type=type
        self.message=message

class NotificationSender(ABC):

    @abstractmethod
    def sendNotification(self,notification):
        pass

class EmailSender(NotificationSender):

    def sendNotification(self,notification):
        print("sending "+notification.message+" to "+notification.user.name+" through "+ notification.user.mail)

class SMSSender(NotificationSender):


    def sendNotification(self,notification):
        print("sending "+notification.message+" to "+notification.user.name+" through "+ notification.user.phn)

class NotificationService:

    def __init__(self):

        self.senders={
            NotificationType.EMAIL: EmailSender(),
            NotificationType.SMS: SMSSender()

        }

    def send(self,notification):

        sender=self.senders[notification.type]

        sender.sendNotification(notification)
    

        
        