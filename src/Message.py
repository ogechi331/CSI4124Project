class Message:
    def __init__(self, current_departure_time, priority=None,
                 edge_arrival_time=None, edge_service_time=None, edge_wait_time=None, edge_departure_time=None,
                 fog_arrival_time=None, fog_service_time=None, fog_wait_time=None, fog_departure_time=None,
                 cloud_arrival_time=None, cloud_service_time=None,
                 cloud_wait_time=None, cloud_departure_time=None):
        # Need to add the rest of the parameters

        self.current_departure_time = current_departure_time
        self.priority = priority

        self.edge_arrival_time = edge_arrival_time
        self.edge_service_time = edge_service_time
        self.edge_departure_time = edge_departure_time
        self.edge_wait_time = edge_wait_time

        self.fog_arrival_time = fog_arrival_time
        self.fog_service_time = fog_service_time
        self.fog_wait_time = fog_wait_time
        self.fog_departure_time = fog_departure_time

        self.cloud_arrival_time = cloud_arrival_time
        self.cloud_service_time = cloud_service_time
        self.cloud_wait_time = cloud_wait_time
        self.cloud_departure_time = cloud_departure_time

    def __gt__(self, other):
        return self.current_departure_time > other.current_departure_time  # this should work for message

    def incrementDeparture(self, deltaTime):
        self.current_departure_time += deltaTime
        return

    def setCurrentDepartureTime(self, time):
        self.current_departure_time = time
        return
