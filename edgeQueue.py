class EdgeQueue:
    def __init__(self, capacity):
        self.capacity = capacity  # Max capacity of the queue
        self.queue = []  # List to hold messages in the queue

    def addMessage(self, message, current_time):

        if self.checkCapacity():
            message.wait_time = current_time  # Assuming wait time is calculated as current_time
            message.departure_time = current_time + message.processing_time  # Set departure time based on processing time
            self.queue.append(message)
            return True  # Mess age added successfully
        else:
            global dropout
            dropout += 1  # Increase global dropout counter if queue is full
            return False  # Message not added due to full capacity

    def checkCapacity(self):
        return len(self.queue) < self.capacity

    def removeMessage(self, current_time):
        departing = []
        for i in range(0, len(self.queue)):
            next_departure = self.queue[0]
            if next_departure.cloud_departure_time <= current_time:
                depart = heapq.heappop(self.queue)
                departing.append(depart)
            else:
                break
        return departing
