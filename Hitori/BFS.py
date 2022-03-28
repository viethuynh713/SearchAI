# class State:
#     def __init__(self, score = 0, costSofar = 0):
#         self.score = score
#         self.costSofar = costSofar
#         self.blackedOut = []
        
# class Hitori:
#     def __init__(self, data):
#         self.data = data
#         self.size = len(data)
#         self.state = State()
#         self.state.blackedOut = [[False for i in range(self.size)] for j in range(self.size)]
#         self.state.costSofar = 0
#         self.state.score = 0
#         self.state.score = self.calculateScore(self.state)
#         self.state.costSofar = self.calculateCostSofar(self.state)
#     def BFS(self):
#         if self.state.score == 0:
#             return self.state
#         else:
#             queue = []
#             queue.append(self.state)
#             while len(queue) > 0:
#                 Curstate = queue.pop(0)
#                 if Curstate.score == 0:
#                     return Curstate
#                 else:
#                     for i in range(self.size):
#                         for j in range(self.size):
#                             if Curstate.blackedOut[i][j] == False:
#                                 if self.data[i][j] == 0:
#                                     Curstate.blackedOut[i][j] = True
#                                     Curstate.costSofar += 1
#                                     Curstate.score = self.calculateScore(Curstate)
#                                     if Curstate.score == 0:
#                                         return Curstate
#                                     else:
#                                         queue.append(Curstate)
#                                     Curstate.blackedOut[i][j] = False
#                                     Curstate.costSofar -= 1
#                                     Curstate.score = self.calculateScore(Curstate)
#     def calculateScore(self, state):
#         score = 0
#         for i in range(self.size):
#             for j in range(self.size):
#                 if state.blackedOut[i][j] == False:
#                     if self.data[i][j] == 0:
#                         score += 1
#         return score
#     def calculateCostSofar(self, state):
#         costSofar = 0
#         for i in range(self.size):
#             for j in range(self.size):
#                 if state.blackedOut[i][j] == False:
#                     if self.data[i][j] == 0:
#                         costSofar += 1
#         return costSofar

