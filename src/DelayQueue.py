import enum
import heapq

import Message


class DelayType(enum.Enum):
    edgeToFog = 1
    fogToCloud = 2


class DelayQueue:
    """
    A class that creates an M/M/n/inf queue with exponentially distributed service time
    """

    n_servers: int  # number of servers accepting customers from the queue
    delay_time: float  # specifies the numpy method used to generate the random numbers
    service_time_mean: float  # the mean of the exponential distribution used to calculate the service time
    processed: list  # a list of all customers that have been processed by the servers
    event_list: list  # a list that corresponds to the number of customers being served

    def __init__(self, n_servers: int, service_time_mean: float, delayTime: float, processed=[],
                 event_list=[]):
        self.n_servers = n_servers
        self.service_time = delayTime
        self.service_time_mean = service_time_mean
        self.processed = processed
        self.event_list = event_list
        self.type = type

    def addMessage(self, message: Message) -> None:
        # calculates the message's service time which is the
        message.fog_service_time = self.service_time

        ########Calculation of Wait Time ##########

        # checks the event list, if the event list is full then remove, the next to leave
        next_departure = None if len(self.event_list) < self.n_servers else heapq.heappop(self.event_list)
        # add next message that should be dealt with to the eventlist
        message.fog_wait_time = 0 if next_departure is None else max(0,
                                                                     next_departure.fog_departure_time - message.fog_arrival_time)
        # calculates the departure time from the message's arrival time, service time, and wait time (arrival time is
        # calculated in main based on the message's departure time from the previous queue + lag time)
        message.fog_departure_time = message.fog_arrival_time + message.fog_service_time + message.fog_wait_time
        # sets the message's sorting criteria to the fog departure_time
        message.current_departure_time = message.fog_departure_time
        # sorts the event list
        heapq.heappush(self.event_list, message)
        # adds the message that left the eventlist into the processed list
        if next_departure is not None:
            self.processed.append(next_departure)

        return None

    def removeMessage(self, current_time: int) -> list:
        departing = []  # a list that contains all messages that left the system between the previous and current time interval

        for i in range(0, self.n_servers):
            if self.event_list[0].fog_departure_time <= current_time:
                self.processed.append(heapq.heappop(self.event_list))

        for i in range(0, len(self.processed)):
            if self.processed[0].fog_departure_time >= current_time:
                departing.append(self.processed.pop(0))

        return departing
