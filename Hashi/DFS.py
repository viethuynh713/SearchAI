

import re
from typing import List
from venv import main
from xml.dom.minidom import Element
from Data import data


class Node:
    def __init__(self, x,y,value):
        self.x = x
        self.y = y
        self.value = value
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y# and self.value == other.value
    
    def GetNeighbor(self,tempdata):
        self.neighbors = [] # type: List[Node] [Phải, trái , trên , dưới] 
        # tìm node phía phải
        for i in range(self.y + 1,len(tempdata)):
            newNode = Node(self.x,i,tempdata[self.x][i])
            if newNode.value > 0  : 
                self.neighbors.append(newNode)
                break
        if len(self.neighbors) == 0:
            self.neighbors.append(0)
        # tìm node phía trái   
        for i in range(self.y - 1,-1,-1):
            newNode = Node(self.x,i,tempdata[self.x][i])
            if newNode.value > 0 : 
                self.neighbors.append(newNode)
                break
        if len(self.neighbors) == 1:
            self.neighbors.append(0)
        # tìm node phía trên
        for i in range(self.x-1,-1,-1):
            newNode = Node(i,self.y,tempdata[i][self.y])
            if newNode.value > 0:
                self.neighbors.append(newNode)
                break
        if len(self.neighbors) == 2:
            self.neighbors.append(0)
        # tìm node phía dưới
        for i in range(self.x +1,len(tempdata)):
            newNode = Node(i,self.y,tempdata[i][self.y])
            if newNode.value > 0 :
                self.neighbors.append(newNode)
                break
        if len(self.neighbors) == 3:
            self.neighbors.append(0)
        
        

class Hashi():
    def __init__(self,d):
        self.hashiData = NewList(d)
        self.mark = []
        self.path =[]
        self.stack = []
        self.updateData = False
        self.GetRoot(self.hashiData)

    def GetRoot(self,d):
        for i in range(len(d)):
            for j in range(len(d[i])):
                if data[j][i] != 0:
                    self.stack.append([Node(j,i,d[i][j]),0])
                    return                 
        
    def DFS(self,path,tempdata):
        # print(self.stack)
        if self.stack == []:
            return
        ele = self.stack.pop()
        node = ele[0]
        if node.value == 0:
            return
        
        tempdata[node.x][node.y] -= node.value

        if TerminalDFS(self.hashiData) == 0:
            print("success")
            print(path) 
            return
        
        node.GetNeighbor(tempdata)
        checkNeighbor = 0
        for i in node.neighbors:
            if type(i) == Node:
                checkNeighbor += 1
        if checkNeighbor == 0:
            return
        arrayDivide = DivideValue(node.value,4)
        
        for i in arrayDivide:
            checkValue = True
            # Kiểm tra cặp số có phù hợp không
            for j in range(4):
                if i[j] != 0 and type(node.neighbors[j]) != Node:
                    checkValue = False
                    break
            if checkValue == False:
                continue
            
            resPath = []
            dataRecursive = NewList(tempdata)
            lenOfStack = len(self.stack)
            self.mark.append(lenOfStack)
            for nei in range(4):
                if type(node.neighbors[nei]) == Node:
                    if node.neighbors[nei].value - i[nei] < 0:
                        checkValue = False
                        break
                    
                    node.neighbors[nei].value -= i[nei]
                    self.stack.append([node.neighbors[nei], lenOfStack])
                    dataRecursive[node.neighbors[nei].x][node.neighbors[nei].y] -= i[nei]
                    resPath.append([(node.x,node.y),(node.neighbors[nei].x,node.neighbors[nei].y),i[nei]])
            goodCase = True
            for neighb in node.neighbors:
                if type(neighb) == Node and neighb.value != 0 and checkValue == True:
                    goodCase = False
                    break
            if goodCase:
                print("goodCase")
                self.hashiData = dataRecursive  
                self.path = path + resPath  
                # for i in self.stack:
                #     if i[1] < lenOfStack:
                #         self.stack.remove(i)       
            for i in range(4):
                if(type(node.neighbors[i]) == Node) and checkValue == True:
                    self.DFS(path + resPath,dataRecursive)
                    # for node in self.stack:
                    #     if node[1] > lenOfStack:
                    #         self.stack.remove(node)     
        # for node in self.stack:
        #     if ele[1] == node[1]:
        #         self.stack.remove(node)  
                               

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
    Hashi.DFS(ha,ha.path,ha.hashiData)

    