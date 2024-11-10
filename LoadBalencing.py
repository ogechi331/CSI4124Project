import math
class loadBalencing:
    def __init__(self, prev):
        self.prev = prev

    def roundRobin(self, list, message):
        list[self.prev].addMessage(message)
        if self.prev == (len(list) - 1):
            self.prev = 0
        else:
            self.prev+=1
        print(list)

    def leastConnections(self, list, message):
        len_lst = []
        index = 0
        for i in range(len(list)):
            len_lst.append(len(list[i]))

        least = len_lst[0]
        for i in range(len(len_lst)):
            if len_lst[i]< least:
                least = len_lst[i]
                index = i

        list[index].addMessage(message)
        print(list)

    #list is array of queue
    #messages is array of message
    def geolocation(self, list, messages):
        for m in messages:
    
            #variables used to determine which queue message should be added to
            prevCapacity = 0
            quickest = 0
    
            #each priority has own dedicated section of list
            #higher priorities have more reserved list
            #Priority 5 has 40%
            if m.priority == 5:
                prevCapacity = len(list[0])
                for i in range(math.floor(len(list)*0.4)):
                    if prevCapacity >= len(list[i]):
                        quickest = i
                        prevCapacity = len(list[i])
                list[quickest].addMessage(m)
            #Priority 4 has 20%
            elif m.priority == 4:
                prevCapacity = len(list[math.floor(len(list)*0.4)])
                for i in range(math.floor(len(list)*0.4), math.floor(len(list)*0.6)):
                    if prevCapacity >= len(list[i]):
                        quickest = i
                        prevCapacity = len(list[i])
                list[quickest].addMessage(m)
            #Priority 3 has 20%
            elif m.priority == 3:
                prevCapacity = len(list[math.floor(len(list)*0.6)])
                for i in range(math.floor(len(list)*0.6), math.floor(len(list)*0.8)):
                    if prevCapacity >= len(list[i]):
                        quickest = i
                        prevCapacity = len(list[i])
                list[quickest].addMessage(m)
            #Priority 2 has 10%
            elif m.priority == 2:
                prevCapacity = len(list[math.floor(len(list)*0.8)])
                for i in range(math.floor(len(list)*0.8), math.floor(len(list)*0.9)):
                    if prevCapacity >= len(list[i]):
                        quickest = i
                        prevCapacity = len(list[i])
                list[quickest].addMessage(m)
            #Priority 1 has 10%
            else:
                prevCapacity = len(list[math.floor(len(list)*0.9)])
                for i in range(math.floor(len(list)*0.9), math.floor(len(list))):
                    if prevCapacity >= len(list[i]):
                        quickest = i
                        prevCapacity = len(list[i])
                list[quickest].addMessage(m)
        return None


