import edgeQueue as edge
import Message as mess
import heapq
import numpy as np


def main():
    global dropout
    dropout = 0
    simulation_time = 0
    end_time = 10000
    n_edgeServers = 3
    edgeArrivalRates = [5, 5, 5]
    edgeCapacities = [10, 10, 10]
    edgeServiceRates = [10, 10, 10]
    edgeDelay = [.05, .05, .05]
    edgeQueuesList = []
    edgeDelayQueue = []*n_edgeServers
    # List of scheduled arrivals for Edge queues stored in tuple
    # tuple of form : (nextEdgeArrivalTime, edgeServer_id)
    nextEdgeArrival = []
    # construct a list of edge server queues and determine the message arrival based on inter-arrival generated from
    # exponential distribution
    for i in range(0, n_edgeServers):
        edgeQueuesList.append((edge.EdgeQueue(edgeCapacities[i], edgeServiceRates[i]), i))
        edgeDelayQueue.append([])

        # poisson or exponential?
        nextEdgeArrival.append((np.random.exponential(1 / edgeArrivalRates[i]), i))

    heapq.heapify(edgeQueuesList)
    heapq.heapify(nextEdgeArrival)

    while simulation_time < end_time:
        # message is class we call

        # handle message arriving at current simulation time
        if nextEdgeArrival[0][0] >= simulation_time:
            server_id = edgeQueuesList[0][1]

            # find where the corresponding edge Queue for the message currently is in the min heap
            for i in range(0, len(edgeQueuesList)):
                if edgeQueuesList[i][1] == server_id:
                    if edgeQueuesList[i][0].addMessage(simulation_time):
                        dropout += 1
                    # replace the min arrival with the next generated arrival time. Heap will auto balance itself
                    heapq.heapreplace(nextEdgeArrival, (np.random.exponential(1 / edgeArrivalRates[server_id]), server_id))

        # handle message departing at current simulation time
        flag1 = False
        for item in edgeQueuesList:
            message = item[0].removeMessage(simulation_time)
            if flag1 and (message is None):
                # the minimum departure is greater than the simulation, so we exit the for loop
                break
            else:
                # add the message to the correct delay queue
                message.incrementDeparture(edgeDelay[item[1]])
                edgeDelayQueue[item[1]].append(message)

            # continue to remove messages from a given edge Queue while allowed since messages could have the same
            # departure time
            while True:
                message = item[0].removeMessage(simulation_time)
                if message is None:
                    break
                message.incrementDeparture(edgeDelay[item[1]])
                edgeDelayQueue[item[1]].append(message)
                flag1 = True



        simulation_time += 1
