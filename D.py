import sys


def dif(a: int, b: int):
    if a > b:
        return a - b
    return b - a


def Finder(start: int, finish: int, count: int, Name: list):
    i_f = count - 1
    i_l = min(len(Name[start][1]), len(Name[finish][1]))
    while i_l - i_f > 1:
        i_mid = (i_l + i_f) // 2
        if Name[start][1][i_mid] == Name[finish][1][i_mid]:
            i_f = i_mid
        else:
            i_l = i_mid
    if i_l < min(len(Name[start][1]), len(Name[finish][1])):
        return i_l + 1
    else:
        if len(Name[start][1]) <= len(Name[finish][1]):
            return i_l + 1
        return -1


class Graph:
    def __init__(self, n: int):
        self.Elements = list()
        self.size = n
        for i_ in range(n):
            self.Elements.append([-1] * n)

    def add(self, i_: int, j_: int, a: int):
        self.Elements[i_][j_] = a

    def length(self, i_: int, j_: int):
        return self.Elements[i_][j_] - 1

    def dijkstra(self, start: int, finish: int):
        N = self.size
        Answer = [-1] * N
        for i_ in range(N):
            Answer[i_] = [-1, -1]
        Left = set()
        for i_ in range(N):
            Left.add(i_)
        s = start
        Answer[s][0] = 0
        while s != finish:
            ans_s = Answer[s][0]
            for j_ in Left:
                ans_j = Answer[j_][0]
                a = self.Elements[s][j_]
                if a >= 1 and (ans_j == -1 or ans_j > ans_s + a):
                    Answer[j_] = [ans_s + a, s]
            if s == 0:
                j_1 = N - 1
                j_2 = 1
            elif s == N - 1:
                j_1 = N - 2
                j_2 = 0
            else:
                j_1 = s - 1
                j_2 = s + 1
            if Answer[j_1][0] == -1 or Answer[j_1][0] > ans_s + 1:
                Answer[j_1] = [ans_s + 1, s]
            if Answer[j_2][0] == -1 or Answer[j_2][0] > ans_s + 1:
                Answer[j_2] = [ans_s + 1, s]
            Left.discard(s)
            minimum = -1
            s = -1
            for k in Left:
                b = Answer[k][0]
                if b != -1 and (b < minimum or minimum == -1):
                    (s, minimum) = (k, b)
            if Answer[finish][0] == minimum:
                return Answer
        return Answer

    def Done(self, A: list):
        N = len(A)
        Names = [1] * N
        for i_ in range(N):
            Names[i_] = [1, 1]
        for i_ in range(N):
            Names[i_][0] = A[i_]
        for i_ in range(N):
            Now = ''
            Names[i_][1] = []
            for j_ in Names[i_][0]:
                Now += j_
                Names[i_][1].append(hash(Now))
        for i_ in range(N):
            count = 1
            hash_base = Names[i_][1][count - 1]
            j_ = i_ - 1
            state = True
            while j_ >= 0:
                if len(Names[j_][1]) < count:
                    self.Elements[j_][i_] = count + 1
                    j_ -= 1
                    continue
                hash_now = Names[j_][1][count - 1]
                if hash_now != hash_base:
                    self.Elements[j_][i_] = count + 1
                else:
                    a = Finder(j_, i_, count, Names)
                    if a >= 0:
                        count = a
                        hash_base = Names[i_][1][count - 1]
                        self.Elements[j_][i_] = count + 1
                    else:
                        state = False
                        break
                j_ -= 1
            if not state:
                continue
            j_ = N - 1
            while j_ > i_:
                if len(Names[j_][1]) < count:
                    self.Elements[j_][i_] = count + 1
                    j_ -= 1
                    continue
                hash_now = Names[j_][1][count - 1]
                if hash_now != hash_base:
                    self.Elements[j_][i_] = count + 1
                else:
                    a = Finder(j_, i_, count, Names)
                    if a >= 0:
                        count = a
                        hash_base = Names[i_][1][count - 1]
                        self.Elements[j_][i_] = count + 1
                    else:
                        state = False
                        break
                j_ -= 1


def my_print(A: Graph, Names: list, i_: int, j_: int):
    Answer = ''
    if dif(i_, j_) == 1:
        if i_ > j_:
            Answer = 'up'
        else:
            Answer = 'down'
    elif dif(i_, j_) == N - 1:
        if i_ > j_:
            Answer = 'down'
        else:
            Answer = 'up'
    else:
        Answer += 'Alt\n'
        size = A.length(i_, j_)
        for num_ in range(size):
            Answer += Names[j_][num_]
            if num_ != size - 1:
                Answer += '\n'

    return Answer


N = int(sys.stdin.readline())
Names = [1] * N
for i_ in range(N):
    Names[i_] = sys.stdin.readline().rstrip()
My_Graph = Graph(N)
My_Graph.Done(Names)
for i_ in range(N):
    My_Graph.add(i_, i_, 0)
K = int(sys.stdin.readline())
A = [1]
A += list(map(int, sys.stdin.readline().split()))
for i_ in range(len(A)):
    A[i_] -= 1
for i_ in range(K):
    Answer = My_Graph.dijkstra(A[i_], A[i_ + 1])
    print(Answer[A[i_ + 1]][0])
    My_answer = []
    now = A[i_ + 1]
    prev = Answer[now][1]
    while prev != -1:
        My_answer.append(my_print(My_Graph, Names, prev, now))
        now = prev
        prev = Answer[now][1]
    My_answer.reverse()
    for i_ in My_answer:
        print(i_)
