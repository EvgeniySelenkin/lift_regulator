from collections import deque
import numpy as np

states = {0: 'стоит', 1: 'едет вверх', -1: 'едет вниз'}

class Lift():
  def __init__(self, location, name):
    self.location = location
    self.state = 0
    self.queue = deque()
    self.name = name
    self.destination = location
    self.commands = []
    self.num_movements = 0
    self.movements = []

  def add_floor_deque(self, floor):
    self.queue.append(floor)
    self.setDestination()

  def setStateValue(self, s):
    self.state = s

  def setState(self):
    if self.queue[0] - self.location > 0:
      self.state = 1
    elif self.queue[0] - self.location < 0:
      self.state = -1
    elif len(self.queue) == 0 or self.queue[0] - self.location == 0 or self.checkStop():
      self.state = 0

  def move(self):
    self.location += self.state
    print('Лифт', self.name, 'находится на', self.location, 'этаже и', states[self.state])
    self.addCommand()

  def checkStop(self):
    check = self.destination == self.location
    if check: print('Лифт', self.name, f'остановка на {self.location} этаже')
    return check

  def delFirstElem(self):
    return self.queue.popleft()
  
  def checkLocation(self):
    return self.location

  def checkState(self):
    return self.state
  
  def addCommand(self):
    self.commands.append(self.state)
    self.checkMovements()
  
  def checkCommands(self):
    return self.commands

  def addkMovement(self):
    self.movements.append(self.num_movements)

  def checkMovements(self):
    if self.state != 0:
      self.num_movements +=1
    else:
      self.addkMovement()
      self.num_movements = 0
  
  def isQueueEmpty(self):
    return self.queueLen() == 0

  def queueLen(self):
    return len(self.queue)

  def setDestination(self): 
    self.destination = self.queue[0]

  def getDestination(self):
    return self.destination

  def startLift(self):
    while not self.isQueueEmpty():
      self.setDestination()
      self.setState()
      if self.checkStop():
        self.addCommand()
        self.setState()
        self.delFirstElem()
      else:
        self.move()

# Задаем этажность дома, стартовые состояния лифтов и список пар (номер этажа вызова, номер этажа, куда нужно попасть).
number_of_floor = 12
lift_loc1, lift_loc2 = 5, 1
lift_1 = Lift(lift_loc1, '1')
lift_2 = Lift(lift_loc2, '2')
main_deq = [(1,2), (1,5), (5,3), (7,2), (12,7), (5,1)]
main_deq.sort(key = lambda x: x[0], reverse=False)
print(main_deq)

while len(main_deq) > 0:
  if len(main_deq) > 0:
    task = main_deq.pop(0)

    if (task[0] == lift_1.checkLocation()):
      s1 = -1 if task[0] > task[1]  else 1
      if lift_1.isQueueEmpty():
        lift_1.setStateValue(s1)
        lift_1.add_floor_deque(task[0])
      if s1 == lift_1.checkState():
        lift_1.add_floor_deque(task[1])
        
    elif (task[0] == lift_2.checkLocation()):
      s2 = -1 if task[0] > task[1]  else 1
      if lift_2.isQueueEmpty():
        lift_2.setStateValue(s2)
        lift_2.add_floor_deque(task[0])
      if s2 == lift_2.checkState():
        lift_2.add_floor_deque(task[1])
    
    else:
      if lift_1.queueLen() == lift_2.queueLen():
        if abs(lift_1.getDestination() - task[0]) <= abs(lift_2.getDestination() - task[0]):
          lift_1.add_floor_deque(task[0])
          lift_1.add_floor_deque(task[1])
        else:
          lift_2.add_floor_deque(task[0])
          lift_2.add_floor_deque(task[1])
        
      elif lift_1.queueLen() < lift_2.queueLen():
        lift_1.add_floor_deque(task[0])
        lift_1.add_floor_deque(task[1])
      
      else: 
        lift_2.add_floor_deque(task[0])
        lift_2.add_floor_deque(task[1])

print('Очередность команд для 1 лифта', lift_1.queue)
print('Очередность команд для 2 лифта', lift_2.queue)

lift_1.startLift()

lift_2.startLift()

# Команды для лифтов:
# 0: остановиться, открыть двери и закрыть двери;
# 1: проехать этаж вверх;
# -1: проехать этаж вниз.

print('Последовательность команд для первого лифта:')
print(np.array(lift_1.checkCommands()))

print('Количество перемещений первого лифта:')
print(np.array(lift_1.movements))

print('Последовательность команд для первого лифта:')
print(np.array(lift_2.checkCommands()))

print('Количество перемещений первого лифта:')
print(np.array(lift_2.movements))