import heapq
import numpy as np


class EdgeQueue:
    def __init__(self, capacity, serviceRate):
        self.capacity = capacity  # Max capacity of the queue
        self.queue = []  # List to hold messages in the
        self.serviceRate = serviceRate

    def addMessage(self, message, current_time):

        if self.checkCapacity():
            message.wait_time = current_time  # Assuming wait time is calculated as current_time

            service_time = np.random.exponential(1 / self.serviceRate)
            message.current_departure_time = current_time + service_time  # Set departure time based on processing time
            # ensure the messages are ordered from lowest to greatest departure when adding messages
            heapq.heappush(self.queue, message)
            return True  # Mess age added successfully
        else:  # Increase global dropout counter if queue is full
            return False  # Message not added due to full capacity

    def checkCapacity(self) -> bool:
        """Returns true if the Edge Queue is not full
        """
        return len(self.queue) < self.capacity

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
