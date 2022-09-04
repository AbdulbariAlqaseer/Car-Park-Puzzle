from queue import PriorityQueue as PQ
import numpy as np
import copy
def test():
    lst = [ 
        [1,2,3],
        [4,5,6,7],
        [8,9],
        [10,20,30,40],
        []
    ]
    max_size_tubes = 4
    num_of_tupes = 5
    for i in range(max_size_tubes):
        for j in range(num_of_tupes):
            try:
                print(lst[j][max_size_tubes-1 - i], end = "")
            except:
                print(0, end = "")
            print("\t", end = "")
        print("")

class Car():
    def __init__(self, dir, lstPos, num, leng = 2):
        assert len(lstPos) == leng and (dir == 0 or dir == 1),"invalid inter for car object"
        self._length = leng
        self._dir = dir
        self._pos = lstPos
        self._num = num
    def __setattr__(self, key, value):
        if key in ['_num','_length','_dir','_pos']:
            if key == '_pos':
                self.__dict__[key] = value
            elif not hasattr(self,key):
                self.__dict__[key] = value
            else:
                raise 'not allow change it'
        else:
            raise 'not allow adding new attribute'
    @property
    def length(self):
        return self._length
    @property
    def num(self):
        return self._num
    @property
    def dir(self):
        return self._dir
    @property
    def pos(self):
        return self._pos
    @property
    def num(self):
        return self._num
    def __str__(self):
        direction =""
        if self.dir == 0 :
            direction = "vertical"
        else:
            direction = "horizontal"
        return f"\tposition : point 1:{self.pos[0]}, point 2: {self.pos[1]}\n\tAnd is direction: {direction}"

class State():
    def __init__(self , n , m , lstOfCar):
        self.parent = None
        self.allParents = ""
        self.cars = lstOfCar
        self.curent_state = np.zeros((n,m),int)
        for i in self.cars:
            if i.pos[0][0]< 0 or i.pos[0][1] < 0 or i.pos[0][0] >= n or i.pos[0][1] >= m:
                raise f"Car position({i.pos[0][0]},{i.pos[0][1]}) is out of patch({n},{m})"
            if i.pos[1][0]< 0 or i.pos[1][1] < 0 or i.pos[1][0] >= n or i.pos[1][1] >= m:
                raise f"Car position({i.pos[1][0]},{i.pos[1][1]}) is out of patch({n},{m})"
            for j in i.pos:
                self.curent_state[j[0],j[1]] = i.num
        self.id = self.hash()
        #print(self.id)
    def can_move(self,car):
        x,y = (0,1) if car.dir else (1,0)
        lst = []
        for j in car.pos:   #j is (j[0],j[1])
            x1,y1 = (j[0]+x,j[1]+y)
            x2,y2 = (j[0]-x,j[1]-y) 
            if not (x1,y1) in car.pos:
                if (x1 >= 0 and x1 < self.curent_state.shape[0]) and (y1 >= 0 and y1 < self.curent_state.shape[1]):
                    if self.curent_state[x1,y1] == 0:
                        lst.append((x1,y1))
            if not (x2,y2) in car.pos:
                if (x2 >= 0 and x2 < self.curent_state.shape[0]) and (y2 >= 0 and y2 < self.curent_state.shape[1]):
                    if self.curent_state[x2,y2] == 0:
                        lst.append((x2,y2))
        return lst
    def move(self,car,lst):
        x,y = (0,1) if car.dir else (1,0)
        lstOfState = []
        for j in car.pos:
            if (j[0]+x,j[1]+y) in lst:
                nextStip = copy.deepcopy(self)
                nextStip.curent_state[j[0]+x,j[1]+y] = car.num
                if car.length == 2:
                    nextStip.curent_state[j[0]-x,j[1]-y] = 0
                else:
                    nextStip.curent_state[j[0],j[1]-1-y] = 0
                b = False
                for nextstipCar in nextStip.cars:
                    if nextstipCar.num == car.num:
                        b = True
                        nextstipCar._pos = [j,(j[0]+x,j[1]+y)]
                        break
                if not b:
                    raise "error not found car in new state"
                #nextStip.id = nextStip.hash()
                lstOfState.append(nextStip)
                continue
            if (j[0]-x,j[1]-y) in lst:
                nextStip = copy.deepcopy(self)
                nextStip.curent_state[j[0]-x,j[1]-y] = car.num
                if car.length == 2:
                    nextStip.curent_state[j[0]+x,j[1]+y] = 0
                else:
                    nextStip.curent_state[j[0]+x,j[1]+1+y] = 0
                b = False
                for nextstipCar in nextStip.cars:
                    if nextstipCar.num == car.num:
                        b = True
                        nextstipCar._pos = [j,(j[0]-x,j[1]-y)]
                        break
                if not b:
                    raise "error not found car in new state"
                #nextStip.id = nextStip.hash()
                lstOfState.append(nextStip)
        return lstOfState
    def next_state(self):
        states =[]
        for car in self.cars:
            z = self.can_move(car)
            if z :
                statesForCar = self.move(car,z)
                for i in statesForCar:
                    states.append(i)
        return states
    def is_goal(self):
        numCar = -1
        if numCar == self.curent_state[int(self.curent_state.shape[0]/2),self.curent_state.shape[1]-1]:
            if numCar == self.curent_state[int(self.curent_state.shape[0]/2),self.curent_state.shape[1]-2]:
                if numCar == self.curent_state[int(self.curent_state.shape[0]/2),self.curent_state.shape[1]-3]:
                    return True
        return False
    def print_state(self):
        print("(***(******)***)")
        for i in self.curent_state:
            for j in i:
                print(j,end="\t")
            print("\n")
    def hash(self):
        _str = ""
        shape = self.curent_state.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                _str += str(self.curent_state[i][j])
        return _str
    def heri(self):
        i = 1
        count = 0
        while i <= self.curent_state.shape[1]:
            num = self.curent_state[int(self.curent_state.shape[0]/2),self.curent_state.shape[1]-i]
            if num == -1:
                break
            if num == 0:
                count += 1
            else:
                count += 1000
            i += 1
        return count

class logic():
    def initState(self):
        cars = []
        cars.append(Car(dir=0,lstPos=[(0,0),(1,0)],num = 1))
        cars.append(Car(dir=0,lstPos=[(4,0),(3,0)],num = 2))
        cars.append(Car(dir=0,lstPos=[(3,3),(2,3)],num = 3))
        cars.append(Car(dir=0,lstPos=[(3,5),(2,5)],num = 5))
        cars.append(Car(dir=0,lstPos=[(4,6),(3,6)],num = 6))
        cars.append(Car(dir=0,lstPos=[(2,6),(1,6)],num = 7))

        cars.append(Car(dir=1,lstPos=[(0,1),(0,2)],num = 8))
        cars.append(Car(dir=1,lstPos=[(4,3),(4,2)],num = 4))
        cars.append(Car(dir=1,lstPos=[(0,5),(0,6)],num = 9))
        cars.append(Car(dir=1,lstPos=[(1,2),(1,3)],num = 10))
        cars.append(Car(dir=1,lstPos=[(3,1),(3,2)],num = 11))
        cars.append(Car(dir=1,lstPos=[(4,4),(4,5)],num = 12)) 

        cars.append(Car(dir=1,lstPos=[(2,0),(2,1),(2,2)],num = -1,leng=3))

        return State(5,7,cars)
    def cmd(self):
        currentState = self.initState()
        previous_states = [] 
        while True:
            print("CURRENT STATE :")
            currentState.print_state()

            states = currentState.next_state()
            if not states:
                print("the game hasn't solved")
                break
            
            print("----------------------below-------------------------")
            '''for i in range(len(states)):
                for j in previous_states:
                    if (states[i].curent_state==j.curent_state).all():
                        states[i] = None
                        break'''
            for i in range(len(states)):
                if states[i] :
                    print(f"\n*****************NO. of state:{i}*****************")
                    states[i].print_state()
            print("----------------------above-------------------------")
            while True:
                try:
                    i = int(input("please enter No. of state : "))
                    if not states[i]:
                        raise
                    break
                except:
                    print("Item NOT Found Or invalid enter\nEnter another time : ")

            previous_states.append(currentState)
            currentState = states[i]
            if currentState.is_goal():
                print("\n***************************************************")
                print("*********************** WON ***********************\t\n")
                currentState.print_state()
                break
            print(previous_states)
    def DFS(self):
        currentState = self.initState()
        stack = []
        visited = dict()
        visited[currentState.hash()] = 1
        count = 1
        while True:
            #print(count)
            if currentState.is_goal():
                break
            next = currentState.next_state()
            for i in next:
                if visited.get(i.hash(),None):
                    continue
                visited[i.hash()] = 1
                i.parent = currentState
                stack.append(i)
            currentState = stack.pop()
            visited[currentState.hash()] = 1
            count += 1
        count2 = 0
        while True:
            count2 += 1
            currentState.print_state()
            currentState = currentState.parent
            if currentState.parent is None:
                break
        print("count of eniter loop :",count)
        print("************************************")
        print("count of parents for goal :",count2)
    def BFS(self):
        currentState = self.initState()
        queue = []
        visited = dict()
        visited[currentState.hash()] = 1
        count = 1
        while not currentState.is_goal():
            #currentState.print_state()
            next = currentState.next_state()
            for i in next:
                if visited.get(i.hash(),None):
                    continue
                visited[i.hash()] = 1
                i.parent = currentState
                queue.append(i)
            currentState = queue.pop(0)
            count += 1
        count2 = 0
        while True:
            count2 += 1
            currentState.print_state()
            currentState = currentState.parent
            if currentState.parent is None:
                break
        print("count of eniter loop :",count)
        print("************************************")
        print("count of parents for goal :",count2)
    def UCS(self):
        currentState = self.initState()
        queue = PQ()
        visited = dict()
        visited[currentState.hash()] = 0
        count = 1
        cost = 0
        while not currentState.is_goal():
            next = currentState.next_state()
            for i in next:
                tmp = visited.get(i.hash(),None)
                if tmp and tmp <= cost + 1:
                    continue
                i.parent = currentState
                queue.put((cost + 1 ,id(i), i))
                visited[i.hash()] = cost + 1
            cost ,_id, currentState = queue.get()
            count += 1
        count2 = 0
        while True:
            if currentState.parent is None:
                break
            count2 += 1
            currentState.print_state()
            currentState = currentState.parent
            
        print("************************************")
        #العقد المطورة
        print("devlopemnt nodes :",count)
        print("************************************")
        #عدد عقد المسار الأمثل
        print("count of parents for goal :",count2)
    def A_Star(self):
        currentState = self.initState()
        queue = PQ()
        visited = dict()
        visited[currentState.hash()] = 0
        count = 1
        cost = 0
        while not currentState.is_goal():
            next = currentState.next_state()
            for i in next:
                tmp = visited.get(i.hash(),None)
                if tmp and tmp <= cost + 1 + i.heri():
                    continue
                i.parent = currentState
                queue.put((cost + 1 + i.heri() ,cost + 1, id(i), i))
                visited[i.hash()] = cost + 1 +i.heri()
            total,  cost, _id, currentState = queue.get()
            count += 1
        count2 = 0
        while True:
            if currentState.parent is None:
                break
            count2 += 1
            currentState.print_state()
            print(f"hyristic value for this state is {currentState.heri()}\n")
            currentState = currentState.parent
        print("************************************")
        #العقد المطورة
        print("devlopemnt nodes :",count)
        print("************************************")
        #عدد عقد المسار الأمثل
        print("count of parents for goal :",count2)




l = logic()
l.A_Star()