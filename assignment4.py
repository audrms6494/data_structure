### PROBLEM II #####################################################################################################
import datetime

class File:
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name
        self.date = datetime.datetime.now()

    def __repr__(self):
        return f"Filename : {self.name}\nContent : {self.content}\nGenerated at {self.date:%Y-%m-%d %H:%M:%S}"


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    @property
    def data(self):
        return self._data

    @property
    def next(self):
        return self._next

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @next.setter
    def next(self, new_next):
        self._next = new_next
        
class UnorderedList:
    def __init__(self):
        self.head = None
        self.metric = None
            
    def append(self, item):
        current = self.head
        temp = Node(item)
        if current == None:
            self.head = temp
        else:
            while current.next != None:
                current = current.next

            current.next = temp
    
    def merge_sort_helper(self, new_head):
        ### CODE HERE ###
        if new_head.next != None: # 모든 노드가 나뉠 때 까지
            left = new_head # left 와 right을 나눈다
            right = self.get_middle(new_head)
            left = self.merge_sort_helper(left) # recursion
            right = self.merge_sort_helper(right)
            temp_left = left
            temp_right = right
            # 헤드 결정
            if self.metric == 'name': # 이름 순 정렬일 때에
                if temp_left.data.name < temp_right.data.name:
                    current = temp_left # 현재 위치
                    new_head = current # 새로운 헤드 결정
                    temp_left = temp_left.next
                else:
                    current = temp_right # 현재 위치
                    new_head = current # 새로운 헤드 결정
                    temp_right = temp_right.next
            if self.metric == 'date': # 날짜 순 정렬일 때에
                if temp_left.data.date < temp_right.data.date:
                    current = temp_left # 현재 위치
                    new_head = current # 새로운 헤드 결정
                    temp_left = temp_left.next
                else:
                    current = temp_right # 현재 위치
                    new_head = current # 새로운 헤드 결정
                    temp_right = temp_right.next
            while temp_left != None and temp_right != None: # 헤드 결정 뒤 merge sort
                if self.metric == 'name': # 이름 순 일 때
                    if temp_left.data.name < temp_right.data.name:
                        current.next = temp_left
                        temp_left = temp_left.next
                    else:
                        current.next = temp_right
                        temp_right = temp_right.next
                elif self.metric == 'date': # 날짜 순 일 때
                    if temp_left.data.date < temp_right.data.date:
                        current.next = temp_left
                        temp_left = temp_left.next
                    else:
                        current.next = temp_right
                        temp_right = temp_right.next
                current = current.next
            while temp_left != None: # right node가 끝났을 때
                current.next = temp_left
                temp_left = temp_left.next
                current = current.next
            while temp_right != None: # left node가 끝났을 때
                current.next = temp_right
                temp_right = temp_right.next
                current = current.next
        return  new_head
        #################
    
    
    def get_middle(self, new_head):
        ### CODE HERE ###
        length = self.get_length(new_head) # 길이 확인
        for _ in range(length//2 - 1): # 길이중간까지 이동
            new_head = new_head.next
        temp = new_head.next # 오른쪽 노드의 헤드 정의
        new_head.next = None # 왼쪽과 오른쪽 분리
        return temp # 오른쪽 노드 헤드 반환
        #################
    
    def merge_sort(self, metric):
        assert isinstance(metric, str)
        self.metric = metric
        head = self.merge_sort_helper(self.head)
        self.head = head

    def __repr__(self):
        result = "["
        current = self.head
        if current != None:
            result += current.data.name
            current = current.next
            while current != None:
                result += ", " + current.data.name
                current = current.next
        result += "]"
        return result
    # node의 길이를 쉽게 가져오기 위해 새로 정의
    def get_length(self, new_head):
        temp = new_head
        length = 1
        while temp.next != None: # 노드의 끝이 닿을 때 까지
            temp = temp.next
            length += 1 # 길이 += 1
        return length

####################################################################################################################


### PROBLEM III ####################################################################################################
class HashTable_Chain:
    def __init__(self, size):
        self.size = size
        self.slots = [[] for _ in range(size)]
        self.data = [[] for _ in range(size)]
        self.num_collision = 0
        self.num_element = 0
          
    def hash_func(self, key):
        ### CODE HERE ###
        return key % self.size ## 사이즈를 나눈 나머지를 hash_func으로 정의
        #################
    
    def _resize(self):
        ### CODE HERE ###
        temp_slots = self.slots  # backup before resizing
        temp_data = self.data
        self.size *= 2 # doubling the size of hashtable
        self.slots = [[] for _ in range(self.size)] 
        self.data = [[] for _ in range(self.size)]
        self.num_element = 0 # recouning num of elements
        for index1 in range(len(temp_slots)): # hashing keys and data in temp
            for index2 in range(len(temp_slots[index1])):
                self.put(temp_slots[index1][index2], temp_data[index1][index2])
        #################
        
    def put(self, key, data):
        ### CODE HERE ###
        self.num_element += 1 # element += 1
        if self.num_element == self.size: # 만약 load factor = 1이면
            self._resize() # 리사이즈 진행
        index = self.hash_func(key)
        if self.slots[index] != []:
            self.num_collision += len(self.slots[index])
        self.slots[index].append(key)
        self.data[index].append(data)
        #################
        
    def get(self, key):
        ### CODE HERE ###
        hash_val = self.hash_func(key)
        exist = False
        for i in range(len(self.slots[hash_val])):
            if key == self.slots[hash_val][i]:
                exist = True # 찾음
                index = i
                break
        if exist: # 찾았다면 반환
            return self.data[hash_val][index]
        else: # 못 찾았다면 오류메세지 출력
            print('There is no corresponding key')
        #################
            
    def remove(self, key):
        ### CODE HERE ###
        hash_val = self.hash_func(key)
        exist = False
        for i in range(len(self.slots[hash_val])):
            if key == self.slots[hash_val][i]:
                exist = True
                index = i
                break
        if exist: # 찾았다면 제거
            del self.slots[hash_val][index]
            del self.data[hash_val][index]
            self.num_element -= 1 # 요소 개수 -= 1
            if self.slots[hash_val] != []: # collision 횟수 정리
                self.num_collision -= len(self.slots[hash_val])
        else: # 못 찾았다면 오류메세지 출력
            print('There is no corresponding key')
        #################
    
    
    def __getitem__(self, key):
        ### CODE HERE ###
        return self.get(key)
        #################
    
    def __setitem__(self, key, data):
        ### CODE HERE ###
        self.put(key, data)
        #################
        
    def __delitem__(self, key):
        ### CODE HERE ###
        self.remove(key)
        #################
        
    def __len__(self):
        ### CODE HERE ###
        return self.num_element
        #################
    
    def __contains__(self, key):
        ### CODE HERE ###
        for i in range(self.size):
            if key in self.slots[i]:
                return True
        return False
        #################
    
    def keys(self):
        ### CODE HERE ###
        temp = []
        for i in range(self.size):
            for key in self.slots[i]:
                temp.append(key)
        return temp
        #################
    def values(self):
        ### CODE HERE ###
        temp = []
        for i in range(self.size):
            for data in self.data[i]:
                temp.append(data)
        return temp
        #################
    
class HashTable_DoubleHash:
    def __init__(self, size):
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.num_collision = 0
        self.num_element = 0
    
    def hash_function1(self, key):
        ### CODE HERE ###
        return key % self.size # size로 나눈 나머지
        #################
    
    def hash_function2(self, key):
        ### CODE HERE ###
        return (key % (self.size - 1)) + 1 # size-1로 나눈 나머지 + 1
        #################

    def _resize(self):
        ### CODE HERE ###
        temp_slots = self.slots  # backup before resizing
        temp_data = self.data
        self.size *= 2 # doubling the size of hashtable
        self.slots = [None] * self.size
        self.data = [None] * self.size 
        self.num_element = 0 # recouning num of elements
        for i in range(len(temp_slots)):
            if temp_slots[i] != None and temp_slots[i] != 'Delete':
                self.put(temp_slots[i], temp_data[i])
        #################
                
    def put(self, key, data):
        ### CODE HERE ###
        self.num_element += 1
        if self.num_element > self.size * 0.75: # load factor을 초과하면
            self._resize()
            self.num_element += 1
        possible = False # put할 수 있는지
        for i in range(self.size):
            index = (self.hash_function1(key) + i * self.hash_function2(key)) % self.size
            if self.slots[index] == None or self.slots[index] == 'Delete':
                self.slots[index] = key
                self.data[index] = data
                possible = True
                break
            self.num_collision += 1
        if not possible: # 만약 put에 실패하면
            self._resize() # resize한 뒤
            self.put(key,data) # put 재실행
        #################
                   
    def get(self, key):
        ### CODE HERE ###
        exist = False # 존재 여부
        for i in range(self.size): # hash_fucn2 만큼 움직이면서 probe
            current = (self.hash_function1(key) + i * self.hash_function2(key)) % self.size
            if key == self.slots[current]:
                exist = True
                index = current
                break
            elif self.slots[current] == None:
                break
        if exist: # 있으면 반환
            return self.data[index]
        else: # 없으면 오류메세지 출력
            print('There is no corresponding key')
        #################
    
    def remove(self, key):
        ### CODE HERE ###
        exist = False # 존재 여부
        for i in range(self.size): # hash_fucn2 만큼 움직이면서 probe
            current = (self.hash_function1(key) + i * self.hash_function2(key)) % self.size
            if key == self.slots[current]:
                exist = True
                index = current
                collision = i
                break
            elif self.slots[current] == None:
                break
        if exist: #있으면 반환
            self.data[index] = 'Delete'
            self.slots[index] = 'Delete'
            self.num_element -= 1
            self.num_collision -= collision
        else: # 없으면 오류메세지 출력
            print('There is no corresponding key')
        #################
    

    def __getitem__(self, key): 
        ### CODE HERE ###
        return self.get(key)
        #################
    
    def __setitem__(self, key, data): 
        ### CODE HERE ###
        self.put(key, data)
        #################
    
    def __delitem__(self, key):
        ### CODE HERE ###
        self.remove(key)
        #################
        
    def __len__(self):
        ### CODE HERE ###
        return self.num_element
        #################
    
    def __contains__(self, key):
        ### CODE HERE ###
        if key in self.slots:
            return True
        return False
        #################
    
    def keys(self):
        ### CODE HERE ###
        temp = []
        for key in self.slots:
            if key != None and key != 'Delete':
                temp.append(key)
        return temp
        #################
    
    def values(self):
        ### CODE HERE ###
        temp = []
        for data in self.data:
            if data != None and data != 'Delete':
                temp.append(data)
        return temp
        #################

def plot_collision(): 
    import random
    import matplotlib.pyplot as plt
    ### CODE HERE ###
    x_axis = [num for num in range(694)]
    collision_chain = []
    collision_double = []
    sample = random.sample([num for num in range(10000)], 694) # 10000개 중 무작위로 694개 선택
    hash_table_1 = HashTable_Chain(size = 347)
    hash_table_2 = HashTable_DoubleHash(size = 347)
    for key in sample:
        hash_table_1.put(key, 'null')
        hash_table_2.put(key, 'null')
        collision_chain.append(hash_table_1.num_collision)
        collision_double.append(hash_table_2.num_collision)
    plt.figure(figsize=(10, 10))
    plt.plot(x_axis, collision_chain)
    plt.plot(x_axis, collision_double)
    plt.xlabel('# of elements', fontsize=10)
    plt.ylabel('# of collisions', fontsize=10)
    plt.legend(['Chaining', 'Double Hash'], loc='best', fontsize=15)
    plt.show()
    #################


def plot_chain_length():
    import random
    import matplotlib.pyplot as plt
    ### CODE HERE ###
    chain_hist = []
    hash_table_3 = HashTable_Chain(size = 983) 
    sample = random.sample([num for num in range(10000)], 983) # 10000 중 무작위로 983개 선택
    for key in sample:
        hash_table_3.put(key, 'null')
    for slot in hash_table_3.slots:
        chain_hist.append(len(slot))
    plt.figure(figsize=(10, 10))
    plt.hist(chain_hist)
    plt.xlabel('Length of chains', fontsize=10)
    plt.ylabel('Number', fontsize=10)
    #################
    
###################################################################################################################
