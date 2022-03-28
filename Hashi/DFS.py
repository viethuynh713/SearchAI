

from typing import List
from venv import main
from Data import data


class Node:
    def __init__(self, x,y,value):
        self.x = x
        self.y = y
        self.value = value
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y# and self.value == other.value
    
    def GetNeighbor(self,tempdata):
        self.neighbors = []
        for i in range(self.y + 1,len(tempdata)):
            newNode = Node(self.x,i,tempdata[self.x][i])
            if newNode.value > 0  : 
                self.neighbors.append(newNode)
                break
        for i in range(self.y - 1,-1,-1):
            newNode = Node(self.x,i,tempdata[self.x][i])
            if newNode.value > 0 : 
                self.neighbors.append(newNode)
                break
        for i in range(self.x +1,len(tempdata)):
            newNode = Node(i,self.y,tempdata[i][self.y])
            if newNode.value > 0 :
                self.neighbors.append(newNode)
                break
        for i in range(self.x-1,-1,-1):
            newNode = Node(i,self.y,tempdata[i][self.y])
            if newNode.value > 0:
                self.neighbors.append(newNode)
                break
        

class Hashi():
    def __init__(self,d):
        self.hashiData = NewList(d)
        self.path =[]
        self.queue = []
        self.updateData = False
        self.GetRoot(self.hashiData)
    # def GetTotalLine(self,d):
    #     self.totalLine = 0
    #     for row in d:
    #         for item in row:
    #             if item != 0:
    #                 self.totalLine += item
    def GetRoot(self,d):
        for i in range(len(d)):
            for j in range(len(d[i])):
                if data[j][i] != 0:
                    self.queue.append(Node(j,i,d[i][j]))
                    return                 
        
    def DFS(self,path,totalLine,tempdata):
        print("z")
        if self.queue == []:
            return
        node = self.queue.pop()
        tempdata[node.x][node.y] -= node.value

        if TerminalDFS(self.hashiData) == 0:
            print(path) 
            return
        # totalLine -= node.value 
        node.GetNeighbor(tempdata)

        if len(node.neighbors) == 1:

            path.append([(node.x,node.y),(node.neighbors[0].x,node.neighbors[0].y),node.value])    
            
            newNode1 = Node(node.neighbors[0].x,node.neighbors[0].y,node.neighbors[0].value - node.value)
    
            tempdata[newNode1.x][newNode1.y] = newNode1.value
            
            if newNode1.value != 0:
                self.queue.append(newNode1)
                self.DFS(path,totalLine,tempdata)
            if newNode1.value == 0:
                self.updateData = True
                self.path += path
                self.hashiData = NewList(tempdata)
                return
            
                                
        if len(node.neighbors) == 2:
            
            arrayDivide = DivideValue(node.value,2)
            
            for i in arrayDivide:
            
                if node.neighbors[0].value - i[0] < 0 or node.neighbors[1].value - i[1] < 0:
                    continue
                resPath = []
                resPath.append([(node.x,node.y),(node.neighbors[0].x,node.neighbors[0].y),i[0]])
                resPath.append([(node.x,node.y),(node.neighbors[1].x,node.neighbors[1].y),i[1]])
                
                newNode1 = Node(node.neighbors[0].x,node.neighbors[0].y,node.neighbors[0].value - i[0])
                newNode2 = Node(node.neighbors[1].x,node.neighbors[1].y,node.neighbors[1].value - i[1])
                
                dataRecur = NewList(tempdata)
                dataRecur[newNode1.x][newNode1.y] -= i[0]
                dataRecur[newNode2.x][newNode2.y] -= i[1]
                temp = 0
                if newNode1.value != 0: 
                    if newNode1 not in self.queue:
                        self.queue.append(newNode1)
                        temp += 1
                    else:
                        for no in self.queue:
                            if no == newNode1:
                                no.value -= i[0]
                                
                    temp+=1
                if newNode2.value != 0 and newNode2 not in self.queue:
                    if newNode2 not in self.queue:
                        self.queue.append(newNode2)
                        temp+=1
                    else:
                        for no in self.queue:
                            if no == newNode2:
                                no.value -= i[1]

                for j in range(temp):
                    if self.updateData == True:
                        dataRecur = NewList(self.hashiData)
                        self.updateData = False
                    self.DFS(path+resPath,totalLine,dataRecur)
                if newNode1.value == 0 and newNode2.value == 0:
                    tempdata[newNode1.x][newNode1.y] -= newNode1.value
                    tempdata[newNode2.x][newNode2.y] -= newNode2.value
                    self.updateData = True
                    self.path = path + resPath
                    self.hashiData = NewList(tempdata)
                    
                
                # if i == arrayDivide[len(arrayDivide)-1]:
                #     break

                # dataRecur[newNode1.x][newNode1.y] += newNode1.value
                # dataRecur[newNode2.x][newNode2.y] += newNode2.value
              
        if len(node.neighbors) == 3:
            # print("3")
            arrayDivide = DivideValue(node.value,3)
            for i in arrayDivide:
                if node.neighbors[0].value - i[0] < 0 or node.neighbors[1].value - i[1] < 0 or node.neighbors[2].value - i[2] < 0:
                    continue
                resPath = []
                resPath.append([(node.x,node.y),(node.neighbors[0].x,node.neighbors[0].y),i[0]])
                resPath.append([(node.x,node.y),(node.neighbors[1].x,node.neighbors[1].y),i[1]])
                resPath.append([(node.x,node.y),(node.neighbors[1].x,node.neighbors[1].y),i[2]])
                
                newNode1 = Node(node.neighbors[0].x,node.neighbors[0].y,node.neighbors[0].value - i[0])
                newNode2 = Node(node.neighbors[1].x,node.neighbors[1].y,node.neighbors[1].value - i[1])
                newNode3 = Node(node.neighbors[2].x,node.neighbors[2].y,node.neighbors[2].value - i[2])
                
                dataRecur = NewList(tempdata)
                dataRecur[newNode1.x][newNode1.y] -= i[0]
                dataRecur[newNode2.x][newNode2.y] -= i[1]
                dataRecur[newNode3.x][newNode3.y] -= i[2]

                temp = 0
                if newNode1.value != 0 and newNode1 not in self.queue:
                    self.queue.append(newNode1)
                    temp+=1
                elif newNode2.value != 0 and newNode2 not in self.queue:
                    self.queue.append(newNode2)
                    temp+=1
                elif newNode3.value != 0 and newNode3 not in self.queue:
                    self.queue.append(newNode3)
                    temp+=1
                for j in range(temp):
                    if self.updateData == True:
                        dataRecur = NewList(self.hashiData)
                        self.updateData = False
                    self.DFS(path+resPath,totalLine,dataRecur)
                if newNode1.value == 0 and newNode2.value == 0 and newNode3.value == 0:
                    self.updateData = True
                    self.path = path + resPath
                    self.hashiData = NewList(tempdata)
                # if i == arrayDivide[len(arrayDivide)-1]:
                #     break
                
                # dataRecur[newNode1.x][newNode1.y] += newNode1.value
                # dataRecur[newNode2.x][newNode2.y] += newNode2.value
                # dataRecur[newNode3.x][newNode3.y] += newNode3.value
                
        if len(node.neighbors) == 4:
            arrayDivide = DivideValue(node.value,4)
            for i in arrayDivide:
                if node.neighbors[0].value - i[0] < 0 or node.neighbors[1].value - i[1] < 0 or node.neighbors[2].value - i[2] < 0 or node.neighbors[3].value - i[3] < 0:
                    continue
                resPath = []
                resPath.append([(node.x,node.y),(node.neighbors[0].x,node.neighbors[0].y),i[0]])
                resPath.append([(node.x,node.y),(node.neighbors[1].x,node.neighbors[1].y),i[1]])
                resPath.append([(node.x,node.y),(node.neighbors[1].x,node.neighbors[1].y),i[2]])
                resPath.append([(node.x,node.y),(node.neighbors[1].x,node.neighbors[1].y),i[3]])
                
                newNode1 = Node(node.neighbors[0].x,node.neighbors[0].y,node.neighbors[0].value - i[0])
                newNode2 = Node(node.neighbors[1].x,node.neighbors[1].y,node.neighbors[1].value - i[1])
                newNode3 = Node(node.neighbors[2].x,node.neighbors[2].y,node.neighbors[2].value - i[2])
                newNode4 = Node(node.neighbors[3].x,node.neighbors[3].y,node.neighbors[3].value - i[3])
                
                dataRecur = NewList(tempdata)
                dataRecur[newNode1.x][newNode1.y] -= i[0]
                dataRecur[newNode2.x][newNode2.y] -= i[1]
                dataRecur[newNode3.x][newNode3.y] -= i[2]
                dataRecur[newNode4.x][newNode4.y] -= i[3]
                temp = 0     
                if newNode1.value != 0 and newNode1 not in self.queue:
                    self.queue.append(newNode1)
                    temp+=1
                if newNode2.value != 0 and newNode2 not in self.queue:
                    self.queue.append(newNode2)
                    temp+=1
                if newNode3.value != 0 and newNode3 not in self.queue:
                    self.queue.append(newNode3)
                    temp+=1
                if newNode4.value != 0 and newNode4 not in self.queue:
                    self.queue.append(newNode4)
                    temp+=1
                for i in range(temp):
                    if self.updateData == True:
                        dataRecur = NewList(self.hashiData)
                        self.updateData = False
                    self.DFS(path+resPath,totalLine,dataRecur)
                if i == arrayDivide[len(arrayDivide)-1]:
                    break            
                dataRecur[newNode1.x][newNode1.y] += newNode1.value
                dataRecur[newNode2.x][newNode2.y] += newNode2.value
                dataRecur[newNode3.x][newNode3.y] += newNode3.value
                dataRecur[newNode4.x][newNode4.y] += newNode4.value
                if newNode1.value == 0 and newNode2.value == 0 and newNode3.value == 0 and newNode4.value == 0:
                    self.updateData = True
                    self.path = path + resPath
                    self.hashiData = NewList(tempdata)
            

def NewList(olddata):
    newData = []
    for i in olddata:
        newData.append(i.copy())
    return newData           
def TerminalDFS(tempdata):
    sum = 0
    for i in tempdata:
        for j in i:
            sum += j
    return sum
def DivideValue(value,NumNeighbor):
     # print(data, "DivideValue", NumNeighbor)
    result =[]
    if NumNeighbor == 2:
        for i in range(3):
            for j in range(3):
                if i + j == value:
                    result.append([i,j])
    if NumNeighbor == 3:
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i + j + k == value:
                        result.append([i,j,k])
    if NumNeighbor == 4:
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if i + j + k + l == value:
                            result.append([i,j,k,l])
    return result
if __name__ == "__main__":
    ha = Hashi(data)
    Hashi.DFS(ha,ha.path,0,ha.hashiData)

    