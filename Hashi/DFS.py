import time

class Block:
    def __init__(self, *arg): # (n, i, j) or (Block)
        if (len(arg) == 3):
            # These attribute is used to calculate
            self.isNode = True if arg[0] > 0 else False
            self.branchValue = [0, 0, 0, 0] # up, right, down, left
            self.bridge = arg[0]
            self.restBridge = arg[0]
            self.i = arg[1]
            self.j = arg[2]
            # These attribute is used to draw
            self.bridgeDraw = [0, 0, 0, 0]
        else:
            self.isNode = arg[0].isNode
            self.branchValue = [x for x in arg[0].branchValue]
            self.bridge = arg[0].bridge
            self.restBridge = arg[0].restBridge
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
            self.lineDraw = []
            for x in arg.lineDraw:
                self.lineDraw.append(x)
            self.drawOrder = []
            for x in arg.drawOrder:
                self.drawOrder.append(x)
            self.tempCase = None
            self.mark = []
            self.markDraw = []
            self.checkedList = []
            self.generateList = []
            self.setGenerateList()
        else:
            # These attribute is used to save the grid
            self.size = 0
            self.grid = []
            self.stack = [] # list of grid
            self.lineDraw = [] # list of tuple (x1, y1, x2, y2, n)
            self.drawOrder = [] # order to draw (include draw and delete line)
            # These attribute is used as temporary variable to calculate
            self.tempCase = None
            self.mark = []
            self.markDraw = [] # mark lines to delete when cases are wrong
            self.checkedList = []
            self.generateList = []
            self.setGenerateList()
            # Read input
            self.readInput(arg)
        
    def play(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.grid[i][j].isNode):
                    for k in range(0, 4):
                        self.calcBranchValue(i, j, k)
        startPos = self.getStartNode()
        i = startPos[0]
        j = startPos[1]
        # print("---Begin---")
        step = 0
        # self.showTable()
        while not self.isComplete() and step < 10000:
            validList = self.genListValid(i, j)
            if len(validList) == 0:
                # print("THIS CASE IS FALSE!!!")
                self.selectOtherCase()
            elif len(validList) == 1:
                self.solveNode(i, j, validList[0])
            else:
                self.mark.append(len(self.stack))
                self.markDraw.append(len(self.lineDraw))
                self.appendToStack(validList, i, j)
                self.grid = self.stack[-1].grid
                self.lineDraw = self.stack[-1].lineDraw
                self.drawOrder.append(self.stack[-1].drawOrder[-1])
            # Draw
            step += 1
            print("---Step " + str(step) + "---")
            # self.showTable()
            # self.showResult()
            if (self.isComplete()):
                res = self.checkIsolation()
                if res:
                    # print("THIS CASE IS FALSE!!!")
                    self.selectOtherCase()
                    startPos = self.getStartNode()
                    i = startPos[0]
                    j = startPos[1]
            else:
                startPos = self.getStartNode()
                i = startPos[0]
                j = startPos[1]
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

    def showTable(self):
        print("-----Table-----")
        for i in range(0, self.size):
            s1 = ""
            s2 = ""
            s3 = ""
            for j in range(0, self.size):
                if (self.grid[i][j].isNode):
                    s1 += " " + str(self.grid[i][j].branchValue[0]) + " "
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
        # print("-----Connected order-----")
        # for x in self.drawOrder:
        #     print(x)
        # print("-----Clearly connected order-----")
        # for x in self.lineDraw:
        #     print(x)

    def setGenerateList(self):
        for a in range(0, 3):
            for b in range(0, 3):
                for c in range(0, 3):
                    for d in range(0, 3):
                        self.generateList.append([a, b, c, d])

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

    def getStartNode(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.grid[i][j].restBridge > 0):
                    return (i, j)
        return ()

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
        for e in validList:
            gridNode = Grid(self)
            gridNode.solveNode(i, j, e)
            self.stack.append(gridNode)

    def solveNode(self, i, j, valid):
        for k in range(0, 4):
            branchTemp = self.grid[i][j].branchValue[k]
            if (branchTemp > 0):
                self.connectBridge(i, j, k, valid[k])
                self.grid[i][j].branchValue[k] = 0
                self.updateAdjacentBridge(i, j, k, valid[k])
                adjacentNode = self.findAdjacentNode(i, j, k)
                adjacentNode.restBridge -= valid[k]
                adjacentNode.branchValue[k - 2] = 0
                self.updateAdjacentNode(adjacentNode.i, adjacentNode.j)

    def connectBridge(self, i, j, direction, n):
        if (n > 0):
            self.drawBridge(i, j, i, j, direction, n, False)
            self.grid[i][j].branchValue[direction] -= n
            self.grid[i][j].restBridge -= n
    
    def drawBridge(self, iStart, jStart, i, j, direction, n, isStart):
        if (self.grid[i][j].isNode):
            if (isStart):
                self.grid[i][j].bridgeDraw[direction - 2] += n
                self.drawLine(iStart, jStart, i, j, n)
                isStart = False
            else:
                self.grid[i][j].bridgeDraw[direction] += n
                isStart = True
        else:
            self.grid[i][j].bridgeDraw[direction] += n
            self.grid[i][j].bridgeDraw[direction - 2] += n
        if (isStart):
            if (direction == 0):
                self.drawBridge(iStart, jStart, i - 1, j, direction, n, isStart)
            elif (direction == 1):
                self.drawBridge(iStart, jStart, i, j + 1, direction, n, isStart)
            elif (direction == 2):
                self.drawBridge(iStart, jStart, i + 1, j, direction, n, isStart)
            else:
                self.drawBridge(iStart, jStart, i, j - 1, direction, n, isStart)

    def drawLine(self, x1, y1, x2, y2, n):
        self.drawOrder.append((x1, y1, x2, y2, n, True))
        self.lineDraw.append((x1, y1, x2, y2, n))

    def updateAdjacentBridge(self, i, j, direction, n):
        if (n > 0):
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
                    adjacentNode2.branchValue[x] = 0
                if direction == 0:
                    i -= 1
                elif direction == 1:
                    j += 1
                elif direction == 2:
                    i += 1
                else:
                    j -= 1

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

    def isComplete(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.grid[i][j].restBridge > 0:
                    return False
        return True

    def checkIsolation(self):
        nNode = 0
        iStart = -1
        jStart = -1
        self.checkedList = []
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
            while (not self.grid[x][y].isNode):
                x += 1
            self.checkingList(x, y)
        if (self.grid[i][j].bridgeDraw[3] > 0):
            x = i
            y = j - 1
            while (not self.grid[x][y].isNode):
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
        self.deleteLines(self.markDraw[-1])
        self.tempCase = self.stack[-1]
        if len(self.stack) == self.mark[-1] + 1:
            self.stack.pop()
            self.mark.pop()
            self.markDraw.pop()
        self.grid = self.tempCase.grid
        self.lineDraw = self.tempCase.lineDraw

    def deleteLines(self, start):
        for i in range(start, len(self.lineDraw)):
            x1 = self.lineDraw[i][0]
            y1 = self.lineDraw[i][1]
            x2 = self.lineDraw[i][2]
            y2 = self.lineDraw[i][3]
            n = self.lineDraw[i][4]
            self.drawOrder.append((x1, y1, x2, y2, n, False))

# main
start_time = time.time()
data = open("large_input_hashi.txt", "r")
grid = Grid(data)
grid.play()
data.close()
print("--- Running time: %s seconds ---" % (time.time() - start_time))