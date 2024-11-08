import math
class loadBalencing:
    def __init__(self, length, prev):
        self.maxLen = length
        self.prev = prev

    def roundRobin(self, list, message):
        if len(list[self.prev]) >= self.maxLen:
            if self.prev == (len(list) - 1):
                self.prev = 0
            else:
                self.prev+=1
            return
        else:
            list[self.prev].append(message)
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
            if len(list[i])< least:
                least = len(list[index])
                index = i

        list[index].append(message)
        print(list)

    #list is array of queue
    #messages is array of message
    def geolocation(self, list, messages):
        for m in messages:
    
            #variables used to determine which queue message should be added to
            prevCapacity = len(list[0])
            quickest = 0
    
            #each priority has own dedicated section of list
            #higher priorities have more reserved list
            #Priority 5 has 40%
            if m.priority == 5:
                for i in range(math.floor(len(list)*0.4)):
                    if prevCapacity >= list[i].size:
                        quickest = i
                        prevCapacity = list[i].size
                list[quickest].addMessage(m)
            #Priority 4 has 20%
            elif m.priority == 4:
                for i in range(math.floor(len(list)*0.4), math.floor(len(list)*0.6)):
                    if prevCapacity >= list[i].size:
                        quickest = i
                        prevCapacity = list[i].size
                list[quickest].addMessage(m)
            #Priority 3 has 20%
            elif m.priority == 3:
                for i in range(math.floor(len(list)*0.6), math.floor(len(list)*0.8)):
                    if prevCapacity >= list[i].size:
                        quickest = i
                        prevCapacity = list[i].size
                list[quickest].addMessage(m)
            #Priority 2 has 10%
            elif m.priority == 2:
                for i in range(math.floor(len(list)*0.8), math.floor(len(list)*0.9)):
                    if prevCapacity >= list[i].size:
                        quickest = i
                        prevCapacity = list[i].size
                list[quickest].addMessage(m)
            #Priority 1 has 10%
            else:
                for i in range(math.floor(len(list)*0.9), math.floor(len(list))):
                    if prevCapacity >= list[i].size:
                        quickest = i
                        prevCapacity = list[i].size
                list[quickest].addMessage(m)
        return None

#lst3 = [7,4,9,0]
#lst2 = [3,4,8]
#lst = [1,2]
#lstM = [lst, lst2,lst3]
#LB =loadBalencing(5, 0)
#i=0
#while i < 10:
#    LB.leastConnections(lstM, i)
#    i+=1
