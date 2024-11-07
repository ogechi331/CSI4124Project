import numpy as np
import heapq
import Message

class fogQueue():
    n_servers: int
    service_time: np.random.default_rng
    service_time_mean: float
    queue: list
    def __init__(self, n_servers: int, service_time: np.random.default_rng, service_time_mean: float, queue = []):
        self.n_servers = n_servers
        self.service_time = service_time
        self.service_time = service_time_mean
        self.queue = queue 


    def addMessage(self, message: Message) -> None: 
        ##do calculate wait time, service time, and departure time
        next_departure = 0 if len(self.queue) == 0 else self.queue[0]
        message.fog_service_time = self.service_time.exponential(self.service_time_mean)
        message.fog_wait_time = 0 if len(self.queue) < self.n_servers else max(0, next_departure.edge_departure_time - message.fog_arrival_time)
        message.fog_departure_time = message.fog_arrival_time + message.fog_service_time + message.fog_wait_time
        ##need to determine how to have a queue that uses different comparators depending on which queue it is
        heapq.heappush(self.queue, message)
        return None



    def removeMessage(self, current_time: int) -> Message:
        departing = []
        for i in range(0, len(self.queue)):
            next_departure = self.queue[0]
            if next_departure.fog_departure_time <= current_time:
                depart = heapq.heappop(self.queue)
                departing.append(depart)
        
        return departing
