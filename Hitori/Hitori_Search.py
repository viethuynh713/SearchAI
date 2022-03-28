from ast import Delete
import pygame
import sys
import time
import random
from Data import data

drawGird = []
class Block:
    def __init__(self, arg):
        if type(arg) == int:
            self.value = arg
            self.weight = -2
        else:
            self.value = arg.value
            self.weight = arg.weight
        
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
            self.colorList = []
            for x in arg.colorList:
                self.colorList.append(x)
            self.stack = []
            self.checkedList = []
            self.tempCase = None
            self.colorMark = []
        else:
            # These attribute is used to save the grid
            self.size = 0
            self.grid = []
            self.colorList = []
            # These attribute is used as temporary variable
            self.stack = [] # grid
            self.checkedList = []
            self.tempCase = None
            self.colorMark = []
            # Read input
            self.readInput(arg)

    def play(self):
        # initial
        for i in range(0, self.size):
            for j in range(0, self.size):
                self.calcWeight(i, j)
        maxWeight = self.findMaxWeight()
        # play
        step = 0
        print("-----Begin-----")
        # self.showTable()
        while maxWeight[2] > 0:
            if maxWeight[2] == self.size * 2:
                self.setFalseBlock(maxWeight[0], maxWeight[1])
            else:
                print("WE HAVE TWO CASES HERE!!!")
                self.colorMark.append(len(self.colorList))
                self.guessing(maxWeight[0], maxWeight[1])
            # Draw
            step += 1
            print("---Step " + str(step) + "---")
            self.showResult()
            # self.showTable()
            maxWeight = self.findMaxWeight()
            if maxWeight[2] == 0 and len(self.stack) > 0:
                res = self.checkIsolation()
                if res:
                    print("THIS CASE IS FALSE!!!")
                    self.selectOtherCase()
                    maxWeight = self.findMaxWeight()
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
                row.append(Block(int(rowData[i])))
            self.grid.append(row)
            self.size += 1

    def showTable(self):
        print("-----Table-----")
        for i in range(0, self.size):
            s = ""
            for j in range(0, self.size):
                weight = "-" if self.grid[i][j].weight == -1 else str(self.grid[i][j].weight)
                s += weight + "\t"
            print(s)

    def showResult(self):
        print("-----Result-----")
        for i in range(0, self.size):
            s = ""
            for j in range(0, self.size):
                res = "-" if self.grid[i][j].weight == -1 else str(self.grid[i][j].value)
                s += res + "\t"
            print(s)
        print("-----Colored order-----")
        step = []
        for x in self.colorList:
            step.append(x)
            print(x)
        drawGird.append(step)

    def isEqual(self, i1, j1, i2, j2):
        if (self.grid[i1][j1].value == self.grid[i2][j2].value):
            return True
        return False

    def calcWeight(self, i, j):
        # Step 1.1 - 1.3
        # row
        if self.grid[i][j].weight == -2:
            if i > 0 and self.isEqual(i, j, i - 1, j):
                if i > 1 and self.isEqual(i, j, i - 2, j):
                    self.setTrueBlock(i - 1, j)
                else:
                    for x in range(0, self.size):
                        if x != i and x != i - 1 and self.isEqual(i, j, x, j):
                            self.grid[x][j].weight = self.size * 2
            elif i > 1 and self.isEqual(i, j, i - 2, j):
                self.setTrueBlock(i - 1, j)
            # column
            if j > 0 and self.isEqual(i, j, i, j - 1):
                if j > 1 and self.isEqual(i, j, i, j - 2):
                    self.setTrueBlock(i, j - 1)
                else:
                    for x in range(0, self.size):
                        if x != j and x != j - 1 and self.isEqual(i, j, i, x):
                            self.grid[i][x].weight = self.size * 2
            elif j > 1 and self.isEqual(i, j, i, j - 2):
                self.setTrueBlock(i, j - 1)
        # Step 1.4
        if self.grid[i][j].weight == -2:
            weight = 0
            for x in range(0, self.size):
                if self.isEqual(i, j, x, j) and x != i:
                    weight += 1
                if self.isEqual(i, j, i, x) and x != j:
                    weight += 1
            self.grid[i][j].weight = weight

    def findMaxWeight(self):
        iMaxWeight = -1
        jMaxWeight = -1
        maxWeight = -2
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.grid[i][j].weight > maxWeight):
                    iMaxWeight = i
                    jMaxWeight = j
                    maxWeight = self.grid[i][j].weight
        return [iMaxWeight, jMaxWeight, maxWeight]

    def setFalseBlock(self, i, j):
        self.grid[i][j].weight = -1
        self.colorFalseBlock(i, j)
        for x in range(0, self.size):
            if self.isEqual(i, j, x, j) and self.grid[x][j].weight > 0 and self.grid[x][j].weight < self.size * 2:
                self.grid[x][j].weight -= 1
            if self.isEqual(i, j, i, x) and self.grid[i][x].weight > 0 and self.grid[i][x].weight < self.size * 2:
                self.grid[i][x].weight -= 1
        if i > 0:
            self.setTrueBlock(i - 1, j)
        if j < self.size - 1:
            self.setTrueBlock(i, j + 1)
        if i < self.size - 1:
            self.setTrueBlock(i + 1, j)
        if j > 0:
            self.setTrueBlock(i, j - 1)

    def colorFalseBlock(self, i, j):
        # Color the False Block at (i, j) by black
        # We will color block[i][j] by black
        self.colorList.append((i, j))

    def setTrueBlock(self, i, j):
        self.grid[i][j].weight = 0
        for x in range(0, self.size):
            if self.isEqual(i, j, x, j) and (self.grid[x][j].weight == -2 or self.grid[x][j].weight > 0):
                self.grid[x][j].weight = self.size * 2
            if self.isEqual(i, j, i, x) and (self.grid[i][x].weight == -2 or self.grid[i][x].weight > 0):
                self.grid[i][x].weight = self.size * 2

    def guessing(self, i, j):
        trueBlockCase = Grid(self)
        trueBlockCase.setTrueBlock(i, j)
        self.stack.append(trueBlockCase)
        self.setFalseBlock(i, j)

    def checkIsolation(self):
        nWhiteBlock = self.calcNumOfWhiteBlock() # [nWhiteBlock, iStart, jStart]
        self.checkedList = []
        self.travel(nWhiteBlock[1], nWhiteBlock[2])
        if (len(self.checkedList) == nWhiteBlock[0]):
            return False
        return True

    def calcNumOfWhiteBlock(self):
        ans = 0
        iStart = -1
        jStart = -1
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.grid[i][j].weight == 0):
                    if ans == 0:
                        iStart = i
                        jStart = j
                    ans += 1
        return [ans, iStart, jStart]

    def travel(self, i, j):
        if i > 0 and self.grid[i - 1][j].weight == 0:
            self.checkingList(i - 1, j)
        if j < self.size - 1 and self.grid[i][j + 1].weight == 0:
            self.checkingList(i, j + 1)
        if i < self.size - 1 and self.grid[i + 1][j].weight == 0:
            self.checkingList(i + 1, j)
        if j > 0 and self.grid[i][j - 1].weight == 0:
            self.checkingList(i, j - 1)

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
        self.tempCase = self.stack[-1]
        self.undoColorFalseBlock(self.colorMark[-1])
        self.stack.pop()
        self.colorMark.pop()
        self.grid = self.tempCase.grid
        self.colorList = self.tempCase.colorList

    def undoColorFalseBlock(self, start):
        for i in range(start, len(self.colorList)):
            # Color each block at (self.colorList[i][0], self.colorList[i][1]) by white
            # We will color each block[self.colorList[i][0]][self.colorList[i][1]] by white
            pass
            



pygame.init()
pygame.display.set_caption("Hitori_Search")

screen = pygame.display.set_mode((500, 500))


myfont = pygame.font.SysFont(None, 48)

done = False
d = open("input_hitori.txt", "r")
g = Grid(d)
g.play()
d.close()
# print(drawGird)
while not done:

    screen.fill((255, 255, 255))
    for i in range(0,500,100):
        pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, 700), 2)
        pygame.draw.line(screen, (0, 0, 0), (0, i), (700, i), 2)
        
        
    for i in range(0,5):
        for j in range(0,5):
            screen.blit(myfont.render(str(data[j][i]), True, (255, 0, 0)), (i*100+50-10, j*100+50-15))  
    
    pygame.display.update()
    step = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                for i in drawGird[step]:
                    print(drawGird[step])
                    print(i)
                    pygame.draw.circle(screen, (0, 0, 0), (i[1] * 100 + 55, i[0] * 100 + 50), 40)
                    # pygame.display.flip()
                    pygame.display.update()
                    time.sleep(2)
            step += 1
                    
    # for i in range(0,500,100):
    #     pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, 700), 2)
    #     pygame.draw.line(screen, (0, 0, 0), (0, i), (700, i), 2)
        
        
    # for i in range(0,5):
    #     for j in range(0,5):
    #         screen.blit(myfont.render(str(data[j][i]), True, (255, 0, 0)), (i*100+50-10, j*100+50-15))  
    
    # pygame.display.update()