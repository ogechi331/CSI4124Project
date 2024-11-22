import math

import Message
import fogQueue


class LoadBalencing:
    def __init__(self, prev):
        self.prev = prev

    def roundRobin(self, queuelist: list[fogQueue.fogQueue], message):
        queuelist[self.prev].addMessage(message)
        if self.prev == (len(queuelist) - 1):
            self.prev = 0
        else:
            self.prev += 1
        print(queuelist)

    @staticmethod
    def leastConnections(queuelist: list[fogQueue.fogQueue], message: Message.Message):
        len_lst = []
        index = 0
        for i in range(len(queuelist)):
            len_lst.append(len(queuelist[i]))

        least = len_lst[0]
        for i in range(len(len_lst)):
            if len_lst[i] < least:
                least = len_lst[i]
                index = i

        queuelist[index].addMessage(message)
        print(queuelist)

    # list is array of queue
    # messages is array of message
    @staticmethod
    def geolocation(queuelist: list[fogQueue.fogQueue], messages):
        for m in messages:

            # variables used to determine which queue message should be added to
            prevCapacity = 0
            quickest = 0

            # each priority has own dedicated section of list
            # higher priorities have more reserved list
            # Priority 5 has 40%
            if m.priority == 5:
                prevCapacity = len(queuelist[0])
                for i in range(math.floor(len(queuelist) * 0.4)):
                    if prevCapacity >= len(queuelist[i]):
                        quickest = i
                        prevCapacity = len(queuelist[i])
                queuelist[quickest].addMessage(m)
            # Priority 4 has 20%
            elif m.priority == 4:
                prevCapacity = len(queuelist[math.floor(len(queuelist) * 0.4)])
                for i in range(math.floor(len(queuelist) * 0.4), math.floor(len(queuelist) * 0.6)):
                    if prevCapacity >= len(queuelist[i]):
                        quickest = i
                        prevCapacity = len(queuelist[i])
                queuelist[quickest].addMessage(m)
            # Priority 3 has 20%
            elif m.priority == 3:
                prevCapacity = len(queuelist[math.floor(len(queuelist) * 0.6)])
                for i in range(math.floor(len(queuelist) * 0.6), math.floor(len(queuelist) * 0.8)):
                    if prevCapacity >= len(queuelist[i]):
                        quickest = i
                        prevCapacity = len(queuelist[i])
                queuelist[quickest].addMessage(m)
            # Priority 2 has 10%
            elif m.priority == 2:
                prevCapacity = len(queuelist[math.floor(len(queuelist) * 0.8)])
                for i in range(math.floor(len(queuelist) * 0.8), math.floor(len(queuelist) * 0.9)):
                    if prevCapacity >= len(queuelist[i]):
                        quickest = i
                        prevCapacity = len(queuelist[i])
                queuelist[quickest].addMessage(m)
            # Priority 1 has 10%
            else:
                prevCapacity = len(queuelist[math.floor(len(queuelist) * 0.9)])
                for i in range(math.floor(len(queuelist) * 0.9), math.floor(len(queuelist))):
                    if prevCapacity >= len(queuelist[i]):
                        quickest = i
                        prevCapacity = len(queuelist[i])
                queuelist[quickest].addMessage(m)
        return None
