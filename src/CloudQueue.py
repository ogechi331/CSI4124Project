import numpy as np
import heapq
import Message


class CloudQueue():
    """
    A class that creates an M/M/n/inf queue with exponentially distributed service time
    """
    n_servers: int  # number of servers accepting customers from the queue
    service_time: np.random.default_rng  # specifies the numpy method used to generate the random numbers
    service_time_mean: float  # the mean of the exponential distribution used to calculate the service time
    processed: list  # a list of all customers in the queue system - sorted with a min heap
    event_list: list

    def __init__(self, n_servers: int, service_time_mean: float, service_time=np.random.default_rng(), processed=[],
                 event_list=[]):
        self.n_servers = n_servers
        self.service_time = service_time
        self.service_time_mean = service_time_mean
        self.processed = processed
        self.event_list = event_list

    def addMessage(self, message: Message) -> None:
        # calculates the message's service time using an exponential distribution with the queue's mean service time
        message.cloud_service_time = self.service_time.exponential(self.service_time_mean)

        #########Calculation of Wait Time ###########
        # checks the event list, if the event list is full then remove, the next to leave
        next_departure = None if len(self.event_list) < self.n_servers else heapq.heappop(self.event_list)

        # checks if more messages are in the system than are being served (meaning they are in the queue), if there is a queue, the wait time is calculated from the next customer to depart the system
        message.cloud_wait_time = 0 if next_departure is None else max(0,
                                                                       next_departure.cloud_departure_time - message.cloud_arrival_time)
        # calculates the departure time from the message's arrival time, service time, and wait time (arrival time is calculated in main based on the message's departure time from the previous queue + lag time)
        message.cloud_departure_time = message.cloud_arrival_time + message.cloud_service_time + message.cloud_wait_time
        # sets the message's sorting criteria to the cloud departure_time
        message.current_departure_time = message.cloud_departure_time

        # sorts the event list
        heapq.heappush(self.event_list, message)
        # adds the message that left the eventlist into the processed list
        if next_departure is not None:
            self.processed.append(next_departure)

        return None

    def removeMessage(self, current_time: int) -> Message:
        departing = []  # a list that contains all messages that left the system between the previous and current time interval

        for i in range(0, self.n_servers):
            if self.event_list[0].cloud_departure_time <= current_time:
                self.processed.append(heapq.heappop(self.event_list))

        for i in range(0, len(self.processed)):
            if self.processed[0].cloud_departure_time >= current_time:
                departing.append(self.processed.pop(0))
            # next_departure = self.queue[0] #peeks at the item at the top of the queue
            # if next_departure.cloud_departure_time <= current_time: #if the fog departure time is less or equal to current time, message leaves the system
            #    depart = heapq.heappop(self.queue)
            #    departing.append(depart)

        return departing
