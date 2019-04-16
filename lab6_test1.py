# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:30:14 2019

@author: Joey Roe
CS 2302
Instructor: Fuentes
TA's: Anindita Nath, Maliheh Zargaran
Assignment: Lab 6
Purpose: The purpose of this lab is to create a maze using disjoint set forest
by removing random walls that didn't have the same set and joining the two cells 
together
Date: 04/15/2019
"""


import matplotlib.pyplot as plt
import numpy as np
import random
import time

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def findCompressed(S, i):
    if S[i] < 0:
        return i
    root = findCompressed(S, S[i])   #the compressed version of find
    S[i] = root
    return root


def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j) 
    if ri!=rj: # Do nothing if i and j belong to the same set 
        S[rj] = ri  # Make j's root point to i's root
        
def union2(S, i, j):
    ri = findCompressed(S, i)
    rj = findCompressed(S, j)       #the compressed version of union
    if ri != rj:
        S[rj] = ri
      

def numOfSets(S):
    sets = 0
    for i in range(len(S)):
        if S[i] < 0:
            sets += 1
    return sets



def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w




plt.close("all") 
maze_rows = 10
maze_cols = 15

walls = wall_list(maze_rows,maze_cols)
#print(walls)
#print()
disjointSet = DisjointSetForest(maze_rows * maze_cols)
#print(disjointSet)
#print()
#print(len(walls))
#print(len(disjointSet))
#print()
start = time.time()
while numOfSets(disjointSet) > 1:                #as long as the number of sets is greater than 1
    randomIndex = random.randint(0, len(walls) - 1)      
    randomWall = walls[randomIndex]
    if find(disjointSet, randomWall[0]) != find(disjointSet, randomWall[1]):     #if the two cells belong to different sets
        walls.pop(randomIndex)                           #remove the wall
        union(disjointSet, randomWall[0], randomWall[1])       #join the two sets
        #union2(disjointSet, randomWall[0], randomWall[1])
draw_maze(walls, maze_rows, maze_cols)
end = time.time()
print()
print((end - start) * 1000)  

#draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 