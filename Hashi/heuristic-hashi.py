class Block:
    def __init__(self, *arg): # (n, i, j) or (Block)
        if (len(arg) == 3):
            # These attribute is used to calculate
            self.isNode = True if arg[0] > 0 else False
            self.branchValue = [0, 0, 0, 0] # up, right, down, left
            self.bridge = arg[0]
            self.restBridge = arg[0]
            self.weight = 10
            self.i = arg[1]
            self.j = arg[2]
            # These attribute is used to draw
            self.bridgeDraw = [0, 0, 0, 0]
        else:
            self.isNode = arg[0].isNode
            self.branchValue = [x for x in arg[0].branchValue]
            self.bridge = arg[0].bridge
            self.restBridge = arg[0].restBridge
            self.weight = arg[0].weight
            self.i = arg[0].i
            self.j = arg[0].j
            self.bridgeDraw = [x for x in arg[0].bridgeDraw]

class Grid:
    def __init__(self, arg):
        if type(arg) == Grid:
            self.size = arg.size
            self.grid = []
            for i in range(0, self.size):
                row = []
                for j in range(0, self.size):
                    row.append(Block(arg.grid[i][j]))
                self.grid.append(row)
            self.stack = []
            self.tempCase = None
            self.mark = []
            self.checkedList = []
            self.generateList = []
            self.setGenerateList()
        else:
            # These attribute is used to save the grid
            self.size = 0
            self.grid = []
            self.stack = [] # (grid, sum)
            # These attribute is used as temporary variable to calculate
            self.tempCase = None
            self.mark = []
            self.checkedList = []
            self.generateList = []
            self.setGenerateList()
            # Read input
            self.readInput(arg)

    # Main method
    def play(self):
        # Step 1 to 3
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.grid[i][j].isNode):
                    # Step 1
                    for k in range(0, 4):
                        self.calcBranchValue(i, j, k)
                    # Step 2
                    self.calcWeight(i, j)
        # Step 3
        minWeight = self.findMinWeight() # [i, j, weight]
        # Step 5
        step = 0
        # print("---Step 0---")
        # self.showTable()
        while (minWeight[2] < 9):
            # Step 6
            if (minWeight[2] < 0):
                self.selectOtherCase()
            # Step 7
            elif (minWeight[2] == 0):
                self.solveNode(minWeight[0], minWeight[1], 0)
            # Step 8
            elif (minWeight[2] > 0.4 and minWeight[2] < 0.6):
                self.solveNode(minWeight[0], minWeight[1], 1)
            # Step 9
            else:
                validList = self.genListValid(minWeight[0], minWeight[1])
                self.mark.append(len(self.stack))
                self.appendToStack(validList, minWeight[0], minWeight[1])
                self.grid = self.stack[-1][0].grid
            step += 1
            print("---Step " + str(step) + "---")
            self.showResult()
            # self.showTable()
            minWeight = self.findMinWeight()
            if (minWeight == 9 and len(self.stack) > 0):
                res = self.checkIsolation()
                if res:
                    self.selectOtherCase()
        print("The puzzle is solved after ", step, " steps!")
        self.showResult()

    def readInput(self, input):
        while True:
            line = input.readline()
            if not line:
                break
            rowData = line.replace('\n', '').split(" ")
            row = []
            for i in range(0, len(rowData)):
                row.append(Block(int(rowData[i]), self.size, i))
            self.grid.append(row)
            self.size += 1

    def setGenerateList(self):
        for a in range(0, 3):
            for b in range(0, 3):
                for c in range(0, 3):
                    for d in range(0, 3):
                        self.generateList.append([a, b, c, d])

    def showTable(self):
        print("-----Table-----")
        for i in range(0, self.size):
            s1 = ""
            s2 = ""
            s3 = ""
            for j in range(0, self.size):
                if (self.grid[i][j].isNode):
                    if (self.grid[i][j].weight < 0):
                        weight = '-'
                    else:
                        weight = '/' if self.grid[i][j].weight > 0.4 and self.grid[i][j].weight < 0.6 else str(self.grid[i][j].weight)
                    s1 += " " + str(self.grid[i][j].branchValue[0]) + weight
                    s2 += str(self.grid[i][j].branchValue[3]) + str(self.grid[i][j].restBridge) + str(self.grid[i][j].branchValue[1])
                    s3 += " " + str(self.grid[i][j].branchValue[2]) + str(self.grid[i][j].bridge)
                else:
                    s1 += "   "
                    s2 += "   "
                    s3 += "   "
            print(s1)
            print(s2)
            print(s3)

    def showResult(self):
        print("-----Result-----")
        for i in range(0, self.size):
            s1 = ""
            s2 = ""
            s3 = ""
            for j in range(0, self.size):
                # up
                if (self.grid[i][j].bridgeDraw[0] == 0):
                    s1 += "   "
                elif (self.grid[i][j].bridgeDraw[0] == 1):
                    s1 += " \' "
                else:
                    s1 += " \" "
                # left
                if (self.grid[i][j].bridgeDraw[3] == 0):
                    s2 += " "
                elif (self.grid[i][j].bridgeDraw[3] == 1):
                    s2 += "-"
                else:
                    s2 += "="
                # center
                if (self.grid[i][j].bridge == 0):
                    if (self.grid[i][j].bridgeDraw[0] == 0 and self.grid[i][j].bridgeDraw[1] == 0):
                        s2 += " "
                    elif (self.grid[i][j].bridgeDraw[0] == 1):
                        s2 += "\'"
                    elif (self.grid[i][j].bridgeDraw[0] == 2):
                        s2 += "\""
                    elif (self.grid[i][j].bridgeDraw[1] == 1):
                        s2 += "-"
                    elif (self.grid[i][j].bridgeDraw[1] == 2):
                        s2 += "="
                else:
                    s2 += str(self.grid[i][j].bridge)
                # right
                if (self.grid[i][j].bridgeDraw[1] == 0):
                    s2 += " "
                elif (self.grid[i][j].bridgeDraw[1] == 1):
                    s2 += "-"
                else:
                    s2 += "="
                # down
                if (self.grid[i][j].bridgeDraw[2] == 0):
                    s3 += "   "
                elif (self.grid[i][j].bridgeDraw[2] == 1):
                    s3 += " \' "
                else:
                    s3 += " \" "
            print(s1)
            print(s2)
            print(s3)

    def calcBranchValue(self, i, j, direction):
        # Get information of adjacent node
        adjacentNode = self.findAdjacentNode(i, j, direction)
        restBridgeAdjaNode = None
        if (adjacentNode != None):
            restBridgeAdjaNode = adjacentNode.restBridge
        if (self.grid[i][j].restBridge == 0 or adjacentNode == None or restBridgeAdjaNode == 0):
            self.grid[i][j].branchValue[direction] = 0
        elif (self.grid[i][j].restBridge == 1 or restBridgeAdjaNode == 1):
            self.grid[i][j].branchValue[direction] = 1
        else:
            self.grid[i][j].branchValue[direction] = 2

    def findAdjacentNode(self, i, j, direction):
        if (direction == 0):
            if (i > 0):
                return self.grid[i - 1][j] if self.grid[i - 1][j].isNode else self.findAdjacentNode(i - 1, j, direction)
            return None
        if (direction == 1):
            if (j < self.size - 1):
                return self.grid[i][j + 1] if self.grid[i][j + 1].isNode else self.findAdjacentNode(i, j + 1, direction)
            return None
        if (direction == 2):
            if (i < self.size - 1):
                return self.grid[i + 1][j] if self.grid[i + 1][j].isNode else self.findAdjacentNode(i + 1, j, direction)
            return None
        if (j > 0):
            return self.grid[i][j - 1] if self.grid[i][j - 1].isNode else self.findAdjacentNode(i, j - 1, direction)
        return None

    def calcWeight(self, i, j):
        if self.grid[i][j].restBridge == 0:
            self.grid[i][j].weight = 9
        else:
            weight = 0
            nBranch1 = 0
            nBranch2 = 0
            for k in range(0, 4):
                if self.grid[i][j].branchValue[k] == 1:
                    nBranch1 += 1
                elif self.grid[i][j].branchValue[k] == 2:
                    nBranch2 += 1
                weight += self.grid[i][j].branchValue[k]
            weight -= self.grid[i][j].restBridge
            if (weight > 0 and nBranch2 > 0 and int((self.grid[i][j].restBridge - nBranch1 + 1) / 2) == nBranch2):
                weight = 0.5
            self.grid[i][j].weight = weight

    def findMinWeight(self):
        iMinWeight = -1
        jMinWeight = -1
        minWeight = 10
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.grid[i][j].weight < minWeight):
                    iMinWeight = i
                    jMinWeight = j
                    minWeight = self.grid[i][j].weight
        return [iMinWeight, jMinWeight, minWeight]

    def solveNode(self, i, j, mode, valid = [0, 0, 0, 0]): # mode 0 is step 7, mode 1 is step 8
        if mode == 0:
            for k in range(0, 4):
                branchTemp = self.grid[i][j].branchValue[k]
                if (branchTemp > 0):
                    self.connectBridge(i, j, k, branchTemp)
                    self.updateAdjacentBridge(i, j, k)
                    adjacentNode = self.findAdjacentNode(i, j, k)
                    adjacentNode.restBridge -= branchTemp
                    adjacentNode.branchValue[k - 2] -= branchTemp
                    self.updateAdjacentNode(adjacentNode.i, adjacentNode.j)
        elif mode == 1:
            for k in range(0, 4):
                if (self.grid[i][j].branchValue[k] == 2):
                    self.connectBridge(i, j, k, 1)
                    self.updateAdjacentBridge(i, j, k)
                    adjacentNode = self.findAdjacentNode(i, j, k)
                    adjacentNode.restBridge -= 1
                    adjacentNode.branchValue[k - 2] -= 1
                    self.updateAdjacentNode(adjacentNode.i, adjacentNode.j)
        else:
            for k in range(0, 4):
                branchTemp = self.grid[i][j].branchValue[k]
                if (branchTemp > 0):
                    self.connectBridge(i, j, k, valid[k])
                    self.grid[i][j].branchValue[k] = 0
                    self.updateAdjacentBridge(i, j, k)
                    adjacentNode = self.findAdjacentNode(i, j, k)
                    adjacentNode.restBridge -= valid[k]
                    adjacentNode.branchValue[k - 2] = 0
                    self.updateAdjacentNode(adjacentNode.i, adjacentNode.j)
        self.calcWeight(i, j)

    def connectBridge(self, i, j, direction, n):
        if (n > 0):
            self.drawBridge(i, j, direction, n, False)
            self.grid[i][j].branchValue[direction] -= n
            self.grid[i][j].restBridge -= n
    
    def drawBridge(self, i, j, direction, n, isStart):
        if (self.grid[i][j].isNode):
            if (isStart):
                self.grid[i][j].bridgeDraw[direction - 2] += n
                isStart = False
            else:
                self.grid[i][j].bridgeDraw[direction] += n
                isStart = True
        else:
            self.grid[i][j].bridgeDraw[direction] += n
            self.grid[i][j].bridgeDraw[direction - 2] += n
        if (isStart):
            if (direction == 0):
                self.drawBridge(i - 1, j, direction, n, isStart)
            elif (direction == 1):
                self.drawBridge(i, j + 1, direction, n, isStart)
            elif (direction == 2):
                self.drawBridge(i + 1, j, direction, n, isStart)
            else:
                self.drawBridge(i, j - 1, direction, n, isStart)

    def updateAdjacentNode(self, i, j):
        if (self.grid[i][j].restBridge == 0):
            for k in range(0, 4):
                if self.grid[i][j].branchValue[k] > 0:
                    self.grid[i][j].branchValue[k] = 0
                    adjacentNode = self.findAdjacentNode(i, j, k)
                    adjacentNode.branchValue[k - 2] = 0
                    self.updateAdjacentNode(adjacentNode.i, adjacentNode.j)
        elif (self.grid[i][j].restBridge == 1):
            for k in range(0, 4):
                if self.grid[i][j].branchValue[k] == 2:
                    self.grid[i][j].branchValue[k] = 1
                    adjacentNode = self.findAdjacentNode(i, j, k)
                    adjacentNode.branchValue[k - 2] = 1
                    self.updateAdjacentNode(adjacentNode.i, adjacentNode.j)
        self.calcWeight(i, j)

    def checkIsolation(self):
        nNode = 0
        iStart = -1
        jStart = -1
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.grid[i][j].bridge > 0):
                    if (nNode == 0):
                        iStart = i
                        jStart = j
                    nNode += 1
        self.travel(iStart, jStart)
        if (len(self.checkedList) == nNode):
            return False
        return True
        
    def travel(self, i, j):
        if (self.grid[i][j].bridgeDraw[0] > 0):
            x = i - 1
            y = j
            while (not self.grid[x][y].isNode):
                x -= 1
            self.checkingList(x, y)
        if (self.grid[i][j].bridgeDraw[1] > 0):
            x = i
            y = j + 1
            while (not self.grid[x][y].isNode):
                y += 1
            self.checkingList(x, y)
        if (self.grid[i][j].bridgeDraw[2] > 0):
            x = i + 1
            y = j
            while (not self.grid[i][j].isNode):
                x += 1
            self.checkingList(x, y)
        if (self.grid[i][j].bridgeDraw[3] > 0):
            x = i
            y = j - 1
            while (not self.grid[i][j].isNode):
                y -= 1
            self.checkingList(x, y)
    
    def checkingList(self, i, j):
        isExist = False
        for x in self.checkedList:
            if x == [i, j]:
                isExist = True
                break
        if (not isExist):
            self.checkedList.append([i, j])
            self.travel(i, j)

    def selectOtherCase(self):
        self.stack.pop()
        self.tempCase = self.stack[-1][0].grid
        if len(self.stack) == self.mark[-1] + 1:
            self.stack.pop()
            self.mark.pop()
        self.grid = self.tempCase

    def updateAdjacentBridge(self, i, j, direction):
        x = 0; y = 0
        if direction == 0:
            i -= 1
            x = 1; y = 3
        elif direction == 1:
            j += 1
            x = 0; y = 2
        elif direction == 2:
            i += 1
            x = 1; y = 3
        else:
            j -= 1
            x = 0; y = 2
        while not self.grid[i][j].isNode:
            adjacentNode1 = self.findAdjacentNode(i, j, x)
            adjacentNode2 = self.findAdjacentNode(i, j, y)
            if adjacentNode1 != None and adjacentNode2 != None:
                adjacentNode1.branchValue[y] = 0
                self.calcWeight(adjacentNode1.i, adjacentNode1.j)
                adjacentNode2.branchValue[x] = 0
                self.calcWeight(adjacentNode2.i, adjacentNode2.j)
            if direction == 0:
                i -= 1
            elif direction == 1:
                j += 1
            elif direction == 2:
                i += 1
            else:
                j -= 1

    def genListValid(self, i, j):
        ans = []
        for x in self.generateList:
            sum = 0
            for y in x:
                sum += y
            if sum == self.grid[i][j].restBridge:
                valid = True
                for k in range(0, 4):
                    if (x[k] > self.grid[i][j].branchValue[k]):
                        valid = False
                        break
                if valid:
                    ans.append(x)
        return ans

    def appendToStack(self, validList, i, j):
        arr = []
        for e in validList:
            gridNode = Grid(self)
            gridNode.solveNode(i, j, 2, e)
            sum = 0
            for x in range(0, 4):
                adjacentNode = gridNode.findAdjacentNode(i, j, x)
                if adjacentNode != None:
                    if adjacentNode.bridge < 9:
                        sum += abs(adjacentNode.bridge - gridNode.grid[i][j].bridge) * e[x]
            arr = self.insert(gridNode, sum, arr)
        for k in range(0, len(arr)):
            self.stack.append(arr[k])
            
    def insert(self, gridNode, sum, arr):
        idx = len(arr)
        arr.append((gridNode, sum))
        while idx > 0 and sum < arr[idx - 1][1]:
            temp = arr[idx]
            arr[idx] = arr[idx - 1]
            arr[idx - 1] = temp
            idx -= 1
        return arr


# main
data = open("input_hashi.txt", "r")
g = Grid(data)
g.play()
data.close()
