import heapq
import numpy as np

import Message
import copy


class EdgeQueue:
    def __init__(self, capacity, serviceRate):
        self.capacity = capacity  # Max capacity of the queue
        self.eventList = []
        self.queue = []  # List to hold messages in the
        self.serviceRate = serviceRate
        self.server_time = 0

    def addMessage(self, time: float):
        message = Message.Message(time)
        
        if self.checkCapacity():
            if len(self.eventList) > 0:
                message.edge_wait_time = (self.eventList[0].edge_departure_time - message.edge_arrival_time) 
                self.queue.append(heapq.heappop(self.eventList))
            else:
                message.edge_wait_time = 0
            # message.wait_time = current_time  # Assuming wait time is calculated as current_time

            message.edge_service_time = np.random.exponential(self.serviceRate)
            message.edge_departure_time = message.edge_arrival_time + message.edge_service_time + message.edge_wait_time  # Set departure time based on processing time
            # ensure the messages are ordered from lowest to greatest departure when adding messages
            message.current_departure_time = copy.deepcopy(message.edge_departure_time)
            heapq.heappush(self.eventList, message)
            return True  # Mess age added successfully
        else:  # Increase global dropout counter if queue is full
            return False  # Message not added due to full capacity

    def checkCapacity(self) -> bool:
        """Returns true if the Edge Queue is not full
        """
        return len(self.queue) < self.capacity

    def removeMessage(self, current_time: int) -> list:
        departing = []
        for i in range(0, len(self.eventList)):
            if self.eventList[0].edge_departure_time <= current_time:
                self.queue.append(heapq.heappop(self.eventList))
        for i in range(0, len(self.queue)):
            if self.queue[0].edge_departure_time <= current_time:
                self.server_time += self.queue[0].edge_service_time
                departing.append(self.queue.pop(0))
        return departing
    
    def getServerTime(self, current_time):
        current_item = self.eventList.pop(0)
        self.server_time += max(0,(current_item.edge_service_time - (current_item.edge_departure_time - current_time)))
        return self.server_time

    def __gt__(self, other):
        """Compare two EdgeQueue objects based on the next message's departure time."""
        if not other.queue:
            return True
        elif not self.queue:
            return False

        return self.queue[0] > other.queue[0]

    def __lt__(self, other):
        """Compare two EdgeQueue objects based on the next message's departure time."""
        if not other.queue:
            return True
        elif not self.queue:
            return False
        return self.queue[0] < other.queue[0]

    def __ge__(self, other):
        """Compare two EdgeQueue objects based on the next message's departure time."""
        if not other.queue:
            return True
        elif not self.queue:
            return False
        return self.queue[0] >= other.queue[0]

    def __le__(self, other):
        """Compare two EdgeQueue objects based on the next message's departure time."""
        if not other.queue:
            return True
        elif not self.queue:
            return False
        return self.queue[0] <= other.queue[0]

        '''
    def removeMessage(self, current_time):
        if self.queue and self.queue[0].departure_time <= current_time:
            return self.queue.pop(0)
        return None

    def getNextDepartureTime(self):
        """Return the departure time of the message with the earliest departure time."""
        if len(self.queue) > 0:
            return self.queue[0].current_departure_time
        else:
            print("Attempting to obtain Departure time for an empty edge.queue")

    def __gt__(self, other):
        """Compare two EdgeQueue objects based on the next message's departure time."""
        return self.queue[0] > other.queue[0]
        '''
