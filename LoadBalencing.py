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
        least = self.maxLen
        index = 0
        for i in range(len(list)):
            if len(list[i])< least:
                least = len(list[index])
                index = i

        if len(list[index]) < self.maxLen:
            list[index].append(message)
            print(list)

lst3 = [7,4,9,0]
lst2 = [3,4,8]
lst = [1,2]
lstM = [lst, lst2,lst3]
LB =loadBalencing(5, 0)
i=0
while i < 10:
    LB.leastConnections(lstM, i)
    i+=1
