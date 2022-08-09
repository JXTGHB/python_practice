import csv
import math
import numpy as np
import pandas as pd
nd = np.genfromtxt('validationData.csv', delimiter=',', skip_header=True)
nd2 = np.genfromtxt('trainingData.csv', delimiter=',', skip_header=True)
validation_list = nd.tolist()
training_list = nd2.tolist()
n_observation = len(training_list)
d_observation = len(validation_list)
total=0
n_feature = 520
d_feature = 520
distance = [[0 for i in range(n_observation)] for j in range(d_observation)]
print(len(distance))
print(n_observation)
aa = []
ii = []
#weight = []
for a in range(0,d_observation):
    for i in range(0,n_observation):
        total=0
        for j in range(0,n_feature):
            total+=math.pow((training_list[i][j]-validation_list[a][j]),2)
        distance[a][i] = math.sqrt(total) 
        

near = distance
for a in range(0,d_observation):
    near[a].sort()
k = 1
weight_sum = []
temp = 0

weight = [[0 for i in range(k)] for j in range(d_observation)]
for a in range(0,d_observation):
    temp = 0
    for i in range(0,k):
        weight[a][i] = (1/near[a][i])
        temp += (1/near[a][i])
    weight_sum.append(temp)


for a in range(0,d_observation):
    for i in range(0,k):
        weight[a][i] = weight[a][i]/weight_sum[a]

estlongtitude = []
estlatitude = []
tempo = 0
tempa = 0
for a in range(0,d_observation):
    tempa = 0
    tempo = 0
    for i in range(0,k):
        #重量權重*該重量的longitude
        tempo+=weight[a][i]*(training_list[distance[a].index(near[a][i])][520])
        tempa+=weight[a][i]*(training_list[distance[a].index(near[a][i])][521])
    estlongtitude.append(tempo)
    estlatitude.append(tempa)
print(estlongtitude[0],estlongtitude[33],estlongtitude[16])
print(estlatitude[0],estlatitude[33],estlatitude[16])

error = []
for a in range(0,d_observation):
    error.append(math.sqrt(math.pow((validation_list[a][520]-estlongtitude[a]),2)+math.pow((validation_list[a][521]-estlatitude[a]),2)))

for i in range(0,d_observation):
    print(error[i])
    #print(validation_list[a][520],estlongtitude[a])
    #print(validation_list[a][521],estlatitude[a])



