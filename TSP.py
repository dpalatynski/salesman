import time
import sys
import os
import imageio
import googlemaps
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import itertools
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'
from datetime import datetime

with open('apikey.txt') as f:
    api_key = f.readline()
    f.close

class Queue:

    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def enqueue(self,item):
        self.items.append(item)
    def dequeue(self):
        return self.items.pop(0)
    def size(self):
        return len(self.items)
    def show(self):
        return self.items


class Stack(object):
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)


class Vertex:

    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white'
        self.fontColor = 'black'
        self.dist = sys.maxsize
        self.pred = None
        self.disc = 0
        self.fin = 0

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ":color " + self.color + ":disc " + str(self.disc) + ":fin " + str(self.fin) +":dist " + str(self.dist) + ":pred \n\t[" + str(self.pred)+ "]\n"

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def setColor(self,color):
        self.color = color

    def setDistance(self,d):
        self.dist = d

    def setPred(self,p):
        self.pred = p

    def setDiscovery(self,dtime):
        self.disc = dtime

    def setFinish(self,ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getFontColor(self):
        return self.fontColor

    def setFontColor(self, color):
        self.fontColor = color




def gm_distance(string1,string2):
    gmaps = googlemaps.Client(key = api_key)
    now = datetime.now()
    directions_result = gmaps.directions(string1,string2,mode = 'driving',avoid = 'ferries',departure_time = now)
    dist = directions_result[0]['legs'][0]['distance']['text']
    return float(dist[0:-2])


def TSP_brute_force(textfile):
    f = open(textfile, 'r')

    addresses = f.readlines()

    vertexes = []

    for i in addresses:
        v = Vertex(i)
        vertexes.append(v)

    for i in vertexes:
        for j in vertexes:
            if (i != j):
                i.addNeighbor(j, gm_distance(i.id,j.id))

    permutations = itertools.permutations(vertexes)
    all_perms = list()
    all_distance = list()

    for perm in permutations:
        all_perms.append(perm)

    for perm in all_perms:
        distance = 0
        for i in range(len(vertexes)-1):
            distance += perm[i].connectedTo[perm[i+1]]
        all_distance.append(distance)

    min_distance = min(all_distance)
    index_dist = all_distance.index(min_distance)
    result = all_perms[index_dist]

    g = open("results.txt", "w+")

    for city in result:
        g.write(city.id)
        print(city.id)

    print(str(min_distance) + " km")

    if os.path.isfile("distance.txt"):
        with open("distance.txt", "w") as f:
            f.truncate()

    f = open("distance.txt", 'a+')
    f.write(str(min_distance)  + " km")


def TSP_rnn(textfile):

    f = open(textfile,'r')

    addresses = f.readlines()

    vertexes = []

    for i in addresses:
        v = Vertex(i)
        vertexes.append(v)

    for i in vertexes:
        for j in vertexes:
            if (i != j):
                i.addNeighbor(j, gm_distance(i.id,j.id))

    rnn_distance = list()
    rnn_route = list()

    for vertex in vertexes:
        start = vertex
        current = start
        start.color = 'black'
        distance = 0
        route = [current]

        for j in range(len(current.connectedTo.items())):
            i = sys.maxsize
            for key, value in current.connectedTo.items():
                if value < i and key.color == 'white':
                    i = value
                    final = key
            final.color = 'black'
            current = final
            distance += i
            route.append(current)
        rnn_route.append(route)
        rnn_distance.append(distance)
        for vertex in vertexes:
            vertex.color = 'white'

    min_distance = min(rnn_distance)
    index_dist = rnn_distance.index(min_distance)
    result = rnn_route[index_dist]

    g = open("results.txt", "w+")

    for city in result:
        g.write(city.id)
        print(city.id)

    print(str(min_distance) + " km")

    if os.path.isfile("distance.txt"):
        with open("distance.txt", "w") as f:
            f.truncate()

    f = open("distance.txt", 'a+')
    f.write(str(min_distance)  + " km")


def TSP_held_karp(textfile):

    f = open(textfile, 'r')
    addresses = f.readlines()
    n = len(addresses)

    dists = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dists[i][j] = dists[j][i] = gm_distance(addresses[i], addresses[j])
    n = len(dists)

    C = {}

    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    bits = (2 ** n - 1) - 1

    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)

    min_distance = opt
    result = list(reversed(path))

    g = open("results.txt", "w+")

    for index in result:
        g.write(addresses[index])
        print(addresses[index])

    print(str(min_distance) + " km")

    if os.path.isfile("distance.txt"):
        with open("distance.txt", "w") as f:
            f.truncate()

    f = open("distance.txt", 'a+')
    f.write(str(min_distance) + " km")

    return opt, list(reversed(path))