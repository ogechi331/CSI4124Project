import enum
import heapq
import numpy as np
import CloudQueue
import LoadBalencing
import edgeQueue as edge
import fogQueue


class LoadBalancingType(enum.Enum):
    RoundRobin = 1
    LeastConnections = 2
    GeoLocation = 3


def main():
    # User parameters Begins
    time_step = 1
    end_time = 10000
    n_edgeServers = 3
    edgeArrivalRates = [5, 5, 5]
    edgeCapacities = [10, 10, 10]
    edgeServiceRates = [10, 10, 10]
    edgeDelay = [.05, .05, .05]
    fogDelayTime = 0.05
    n_fogServers = [3, 3, 3]
    n_fogQueues = 3
    fogServiceRates = [10, 10, 10]
    n_cloudServers = 4
    cloudServiceRate = 10
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

        # poisson or exponential?
        nextEdgeArrival.append((np.random.exponential(1 / edgeArrivalRates[i]), i))

    for i in range(0, n_fogQueues):
        fogQueueList.append(fogQueue.fogQueue(n_fogServers[i], fogServiceRates[i]))

    heapq.heapify(edgeQueuesList)
    heapq.heapify(nextEdgeArrival)

    while simulation_time < end_time:
        # message is class we call

        # handle message arriving at current simulation time
        if nextEdgeArrival[0][0] >= simulation_time:
            server_id = nextEdgeArrival[0][1]

            # find where the corresponding edge Queue for the message currently is in the min heap
            for i in range(0, len(edgeQueuesList)):
                if edgeQueuesList[i][1] == server_id:
                    if not edgeQueuesList[i][0].addMessage(simulation_time):
                        dropout += 1
                    # replace the min arrival with the next generated arrival time. Heap will auto balance itself
                    heapq.heapreplace(nextEdgeArrival,
                                      (np.random.exponential(1 / edgeArrivalRates[server_id]), server_id))

        # handle message departing at current simulation time
        for item in edgeQueuesList:
            messages = item[0].removeMessage(simulation_time)
            if messages:
                for i in range(0, len(messages)):
                    messages[i].incrementDeparture(edgeDelay[item[1]])
                    edgeDelayQueue[item[1]].append(messages[i])

        # handle Messages leaving edge Delay Queue and use Load Balancing to add them to fog
        for messages in edgeDelayQueue:
            if messages:
                # use Load Balancing to add to fog queue
                if loadbalancingtype == LoadBalancingType.RoundRobin:
                    for i in range(0, len(messages)):
                        balance.roundRobin(fogQueueList, messages[i])
                elif loadbalancingtype == LoadBalancingType.LeastConnections:
                    for i in range(0, len(messages)):
                        balance.leastConnections(fogQueueList, messages[i])
                elif loadbalancingtype == LoadBalancingType.GeoLocation:
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


main()
