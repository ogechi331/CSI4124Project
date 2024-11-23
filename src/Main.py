import enum
import heapq
import numpy as np
import CloudQueue
import LoadBalencing
import edgeQueue as edge
import fogQueue

import matplotlib.pyplot as plt


class LoadBalancingType(enum.Enum):
    RoundRobin = 1
    LeastConnections = 2
    GeoLocation = 3


def main():
    # User parameters Begins
    time_step = 0.01 #ms
    end_time = 5000 #ms (will check if reached steady state)
    n_edgeServers = 6
    edgeArrivalRates = [0.01,0.01,0.01,0.01,0.01,0.01] #this is the value that will change with each test
    edgeCapacities = [50,50,50,50,50,50]
    edgeServiceRates = [5,5,5,5,5,5]
    edgeDelay = [.05, .05, .05, 0.05, 0.05]
    fogDelayTime = 0.05
    n_fogServers = [2,2]
    n_fogQueues = 1 #other parameter that was changed
    fogServiceRates = [30,30]
    n_cloudServers = 4 #what about number of queues? assumes 1 queue (which is right according to the paper)
    cloudServiceRate = 50
    loadbalancingtype = 1
    # End User Parameters
    balance = LoadBalencing.LoadBalencing(0)
    dropout = 0
    simulation_time = 0
    edgeQueuesList = []
    edgeDelayQueue = [] * n_edgeServers
    fogDelayQueue = []
    fogQueueList = []
    cloudExitMessageList = []
    cloudQueue = CloudQueue.CloudQueue(n_cloudServers, cloudServiceRate)

    # List of scheduled arrivals for Edge queues stored in tuple
    #  of form : (nextEdgeArrivalTime, edgeServer_id)
    nextEdgeArrival = []
    # construct a list of edge server queues and determine the message arrival based on inter-arrival generated from
    # exponential distribution
    for i in range(0, n_edgeServers):
        edgeQueuesList.append((edge.EdgeQueue(edgeCapacities[i], edgeServiceRates[i]), i))
        edgeDelayQueue.append([])

        # assumes that the initial arrival time is exponentially distributed after 0
        nextEdgeArrival.append([np.random.exponential(edgeArrivalRates[i]), i]) #this calculates the interarrival time, not the arrival time

    for i in range(0, n_fogQueues):
        fogQueueList.append(fogQueue.fogQueue(n_fogServers[i], fogServiceRates[i]))

    heapq.heapify(edgeQueuesList)
    heapq.heapify(nextEdgeArrival)

    while simulation_time < end_time:
        # message is class we call

        # handle message arriving at current simulation time
        for i in range(len(nextEdgeArrival)):
            if nextEdgeArrival[i][0] <= simulation_time:
                server_id = nextEdgeArrival[0][1]

                # find where the corresponding edge Queue for the message currently is in the min heap
                for i in range(0, len(edgeQueuesList)):
                    if edgeQueuesList[i][1] == server_id:
                        if not edgeQueuesList[i][0].addMessage(simulation_time):
                            dropout += 1
                        # replace the min arrival with the next generated arrival time. Heap will auto balance itself
                        prev = heapq.heappop(nextEdgeArrival)
                        value = prev[0] + np.random.exponential(edgeArrivalRates[server_id])
                        heapq.heappush(nextEdgeArrival, [value, server_id])
                        #heapq.heapreplace(nextEdgeArrival,
                        #                (nextEdgeArrival[0] + np.random.exponential(edgeArrivalRates[server_id]), server_id))

        # handle message departing at current simulation time
        for item in edgeQueuesList:
            messages = item[0].removeMessage(simulation_time)
            if messages:
                for i in range(0, len(messages)):
                    messages[i].incrementDeparture(edgeDelay[item[1]-1])
                    edgeDelayQueue[item[1]].append(messages[i])

        # handle Messages leaving edge Delay Queue and use Load Balancing to add them to fog
        for messages in edgeDelayQueue:
            if messages:
                # use Load Balancing to add to fog queue
                if loadbalancingtype == LoadBalancingType.RoundRobin.value:
                    for i in range(0, len(messages)):
                        balance.roundRobin(fogQueueList, messages.pop(0))
                elif loadbalancingtype == LoadBalancingType.LeastConnections.value:
                    for i in range(0, len(messages)):
                        balance.leastConnections(fogQueueList, messages[i])
                elif loadbalancingtype == LoadBalancingType.GeoLocation.value:
                    balance.geolocation(fogQueueList, messages)
            else:
                continue

        # handle Messages departing fog Queue and add them to fog Delay Queue

        for item in fogQueueList:
            messages = item.removeMessage(simulation_time)
            if messages:
                for i in range(0, len(messages)):
                    messages[i].incrementDeparture(fogDelayTime)
                    heapq.heappush(fogDelayQueue, messages[i])

        # handle messages departing fog Delay
        while True:
            if fogDelayQueue and fogDelayQueue[0].current_departure_time >= simulation_time:
                cloudQueue.addMessage(heapq.heappop(fogDelayQueue))
            else:
                # no more messages that can leave (departure time of remaining messages > current simulation time), break out of while loop
                break

        # Return list of all messages exiting cloud
        messages = cloudQueue.removeMessage(simulation_time)
        if messages:
            for i in range(0, len(messages)):
                cloudExitMessageList.append(messages[i])

        
        simulation_time += time_step

    return cloudExitMessageList


messages = main()

print(len(messages))

system_time = []

edge_arrival_time = []
edge_service_time = []
edge_wait_time = []
edge_departure_time = []

fog_arrival_time = []
fog_service_time = []
fog_wait_time = []
fog_departure_time = []

cloud_arrival_time = []
cloud_service_time = []
cloud_wait_time = []
cloud_departure_time = []

for message in messages:
    edge_arrival_time.append(message.edge_arrival_time)
    edge_service_time.append(message.edge_service_time)
    edge_wait_time.append(message.edge_wait_time)
    edge_departure_time.append(message.edge_departure_time)

    fog_arrival_time.append(message.fog_arrival_time)
    fog_service_time.append(message.fog_service_time)
    fog_wait_time.append(message.fog_wait_time)
    fog_departure_time.append(message.fog_departure_time)

    cloud_arrival_time.append(message.cloud_arrival_time)
    cloud_service_time.append(message.cloud_service_time)
    cloud_wait_time.append(message.cloud_wait_time)
    cloud_departure_time.append(message.cloud_departure_time)

    system_time.append(message.cloud_departure_time - message.edge_arrival_time)

#now calculate all the statistics
"""
What to calculate:
    1. determine system time (look for when this stabilizes)
    1. determine when cloud departure time stabilizes (plot cloud departure time as histogram?)
    2. average cloud departure time (graph)
"""

#cloud departure stabilization - plot the cloud departure by time
plt.hist(system_time)
plt.show()


