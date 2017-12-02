# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 18:10:19 2017

@author: Ben
"""


import math
import time
import copy
#import winsound

#import plotly
import plotly.plotly as py
import plotly.graph_objs as go

start_time = time.time()

#test = [k, feature height, feature width, overlap (0-no overlap, 1-overlap), number of classes, data height (row), data width(col), val 0, val 1, val 2,   ]

#Part 1 Tests
# 1x1 Feature K set
#test = [0.2, 1, 1, 0, 10, 28, 28, ' ', '+', '#' ]
# 2x2 Feature with no overlap K set
#test = [0.3, 2, 2, 0, 10, 28, 28, ' ', '+', '#' ]
# 2x4 Feature with no overlap K set
#test = [0.1, 2, 4, 0, 10, 28, 28, ' ', '+', '#' ]
# 4x2 Feature with no overlap k set
#test = [0.1, 4, 2, 0, 10, 28, 28, ' ', '+', '#' ]
# 4x4 Feature with no overlap kset
#test = [0.1, 4, 4, 0, 10, 28, 28, ' ', '+', '#' ]
# Overlapping Features
# 2x2 Feature with Overlap
#test = [0.1, 2, 2, 1, 10, 28, 28, ' ', '+', '#' ]
# 2x4 Feature with overlap
#test = [0.1, 2, 4, 1, 10, 28, 28, ' ', '+', '#' ]
# 4x2 Feature with overlap
#test = [0.1, 4, 2, 1, 10, 28, 28, ' ', '+', '#' ]
# 4x4 Feature with overlap
test = [0.1, 4, 4, 1, 10, 28, 28, ' ', '+', '#' ]
# 2x3 Feature with overlap
#test = [0.1, 2, 3, 1, 10, 28, 28, ' ', '+', '#' ]
# 3x2 Feature with overlap
#test = [0.1, 3, 2, 1, 10, 28, 28, ' ', '+', '#' ]
# 3x3 Feature with overlap
#test = [0.2, 3, 3, 1, 10, 28, 28, ' ', '+', '#' ]

#%%

k_smooth = test[0]
V = pow(2,test[1]*test[2])


temp_image = []
count_data = []
count_class = []
test_count_class = []
prob_mat = []
class_prob = []

test_data = []
test_image_data = []

conf_mat_data = []
conf_mat = []

odds_mat_data = []

class1_mat_data = []
class2_mat_data = []


z=[]

for j in range(test[4]):
    count_class.append(0)
    test_count_class.append(0)
    class_prob.append([])

for j in range(0,test[5],1): #row
    count_data.append([])
    test_data.append([])
    prob_mat.append([])
    temp_image.append([])
    test_image_data.append([])
    odds_mat_data.append([])
    class1_mat_data.append([])
    class2_mat_data.append([])
    z.append([])
for k in range(0,test[6],1): #col
    for j in range(0,test[5],1):
        count_data[j].append([])
        test_data[j].append([])
        prob_mat[j].append([])
        temp_image[j].append([])
        test_image_data[j].append([])
        odds_mat_data[j].append([])
        class1_mat_data[j].append([])
        class2_mat_data[j].append([])
        z[j].append([])
        
for k in range(0,test[6],1): 
    for j in range(0,test[5],1):
        for l in range(test[4]):#class
#            count_data[j][k].append([])
            count_data[j][k].append({})
#            prob_mat[j][k].append([])
#for k in range(0,test[6],1): 
#    for j in range(0, test[5], 1):
#        for l in range(test[4]):
#            for m in range(V):#features
##                count_data[j][k][l].append({})
##                prob_mat[j][k][l].append([])
#                break
   
for j in range(test[4]): #row
    conf_mat_data.append([])
    conf_mat.append([])
for k in range(test[4]): #col
    for j in range(test[4]):
        conf_mat_data[j].append(0)
        conf_mat[j].append([])

for k in range(0,test[6],1): 
    for j in range(0,test[5],1):
        for l in range(4):
            odds_mat_data[j][k].append([])
            class1_mat_data[j][k].append([])
            class2_mat_data[j][k].append([])

if test[3] == 0:
    row_adv = test[1]
    col_adv = test[2]
else:
    row_adv = 1
    col_adv = 1    
        
"""
Read in all the training data, count the occurences and place that data in the matrix
"""        
train_label = open("digitdata/traininglabels","r")
train_image = open("digitdata/trainingimages","r")

count = 0
while(True):
    count += 1
#    print(count)
    char = train_label.read(1)
    if not char:
        break #Label file has been fully read

    class_label = int(char)
    count_class[class_label] += 1
    train_label.read(1) #This reads the \n to get to the next label
    for row in range(0, test[5], 1):
        for col in range(0, test[6] + 1, 1):  # + 1 to include "\n" which is discarded
            char = train_image.read(1)
            if char != '\n':
                if char == test[7]:
                    temp_image[row][col] = 0
                if char == test[8]:
                    temp_image[row][col] = 1
                if char == test[9]:
                    temp_image[row][col] = 1
                    
    
    #Assmble the data based on the read
    
    if test[3] == 1:
        row_buff = test[1]
        col_buff = test[2]
    else:
        row_buff = 0
        col_buff = 0 
    
    for row in range(0, test[5] - row_buff, row_adv):
        for col in range(0, test[6] - col_buff, col_adv):  # + 1 to include "\n" which is discarded
            feature = 0
            #print("Feature: ",[row,col])
            for f_row in range(test[1]):
                for f_col in range(test[2]):
                   # print([row + f_row, col + f_col])
                    feature |= temp_image[row + f_row][col + f_col] << f_row * test[2] + f_col
#            print(feature)
            value = count_data[row][col][class_label].get(feature, -1)
#            count_data[row][col][class_label].append(feature)
            if value == -1:
                count_data[row][col][class_label][feature] = 1
            else:
                count_data[row][col][class_label][feature] = value + 1
            
train_label.close()
train_image.close()


#%%
"""
Create the probability matrices based on the training data
"""   
                
train_size = sum(count_class)

for c in range(test[4]):
    class_prob[c] = count_class[c]/train_size

#%%
"""
Read in all the test data, make decisions
"""   
test_label = open("digitdata/testlabels","r")
test_image = open("digitdata/testimages","r")

success = 0
fail = 0
high = -100000
low = 0
while(True):

    char = test_label.read(1)
    if not char:
        break #Label file has been fully read
    test_class_label = int(char)
    test_count_class[test_class_label] += 1
    test_label.read(1) #This reads the "\n" to get to the next label
    for row in range(test[5]):
        for col in range(test[6] + 1): # + 1 to include "\n" which is discarded
            char = test_image.read(1)
            if char != '\n':
                if char == test[7]:
                    test_image_data[row][col] = 0
                if char == test[8]:
                    test_image_data[row][col] = 1
                if char == test[9]:
                    test_image_data[row][col] = 1     
                    
                    
        #Assmble the data based on the read
    
    for row in range(0, test[5] - row_buff, row_adv):
        for col in range(0, test[6]  - col_buff, col_adv):  # + 1 to include "\n" which is discarded
            feature = 0
            for f_row in range(test[1]):
                for f_col in range(test[2]):
                    feature |= test_image_data[row + f_row][col + f_col] << f_row * test[2] +f_col
            test_data[row][col] = feature
    best = -100000
    best_class = -1                  
    for c in range(test[4]):
        total = math.log(class_prob[c])
        for row in range(0,test[5] - row_buff, row_adv):
            for col in range(0, test[6] - col_buff, col_adv):
#                print([row,col])
                value = count_data[row][col][c].get(test_data[row][col], -1)
                if value == -1:
                    total += math.log((0 + k_smooth)/(count_class[c] + V*k_smooth))
                else:
                    total += math.log((value + k_smooth)/(count_class[c] + V*k_smooth))
        if total > best:
            best = total
            best_class = c
    if best > high:
        high = best
        high_prob = copy.deepcopy(test_image_data)

    if best < low:
        low = best
        low_prob = copy.deepcopy(test_image_data)

    conf_mat_data[test_class_label][best_class] += 1
    if best_class == test_class_label:
        success += 1
    else:
        fail += 1
        
      
                
                    
test_label.close()
test_image.close()


print("For K: ", test[0])
print([test[1],test[2]])
print("Accuracy: ", 100*(success/(fail + success)))
print("Total Time: ", time.time() - start_time)

#%%

print("Confusion Matrix:")
print("", end='\t')
for a in range(test[4]):
    print(a, end='\t')
print("")
for row in range(test[4]):
    print(row, end='\t')
    for col in range(test[4]):
        conf_mat[row][col] = 100*(conf_mat_data[row][col]/test_count_class[row])
        print("%.1f" % conf_mat[row][col], end='\t')
        if col == test[4] - 1:
            print("")



#%%
if test[1]==1: #Only done for part 1.1  
    print("Highest Probability Image")
    for row in range(28):
        for col in range(28):
            print(high_prob[row][col], end='')
            if col == 27:
                print("")
            
    print("Lowest Probability Image")
    for row in range(28):
        for col in range(28):
            print(low_prob[row][col], end='')
            if col == 27:
                print("")
            
    most = [0,0,0,0]
    most_index = [0,0,0,0]
    
    for row in range(test[4]):
        for col in range(test[4]):
            if row != col:
                if conf_mat[row][col] > most[3]:
                    for c in range(4):
                        if conf_mat[row][col] > most[c]:
                            most.insert(c,conf_mat[row][col])
                            del most[4]
                            most_index.insert(c,[row,col])
                            del most_index[4]
                            break
    

    
    for row in range(test[5]):
        for col in range(test[6]):
            for c in range(4):
                value = count_data[row][col][most_index[c][0]].get(1, -1)
                if value == -1:
                    total1 = (0 + k_smooth)/(count_class[most_index[c][0]] + V*k_smooth)
                else:
                    total1 = (value + k_smooth)/(count_class[most_index[c][0]] + V*k_smooth)
                value = count_data[row][col][most_index[c][1]].get(1, -1)
                if value == -1:
                    total2 = (0 + k_smooth)/(count_class[most_index[c][1]] + V*k_smooth)
                else:
                    total2 = (value + k_smooth)/(count_class[most_index[c][1]] + V*k_smooth)
                odds_mat_data[row][col][c] = math.log(total1/total2)
                class1_mat_data[row][col][c] = math.log(total1)
                class2_mat_data[row][col][c] = math.log(total2)
#
#    
#    for c in range(4):
#        print("Class 1 Matrix: ", most_index[c][0])
#        for row in range(test[5]):
#            for col in range(test[6]):
#                if class1_mat_data[row][col][c] < -0.1:
#                    print("-", end='')
#                elif class1_mat_data[row][col][c] > 0.1:
#                    print("+", end='')
#                else:
#                    print(" ", end='')
#            print("")
#        print("")
#        print("Class 2 Matrix: ", most_index[c][1])
#        for row in range(test[5]):
#            for col in range(test[6]):
#                if class2_mat_data[row][col][c] < -0.1:
#                    print("-", end='')
#                elif class2_mat_data[row][col][c] > 0.1:
#                    print("+", end='')
#                else:
#                    print(" ", end='')
#            print("")
#        print("")
#        print("Odds Matrix:")
#        print(most_index[c])
#        for row in range(test[5]):
#            for col in range(test[6]):
#                if odds_mat_data[row][col][c] < -0.1:
#                    print("-", end='')
#                elif odds_mat_data[row][col][c] > 0.1:
#                    print("+", end='')
#                else:
#                    print(" ", end='')
#            print("")
#        print("")
  


    # layout = go.Layout(
    #     width=800,
    #     height=800
    # )
    # for c in range(4):
    #     for row in range(28):
    #         for col in range(28):
    #             z[row][col] = class1_mat_data[27 - row][col][c]
    #     title = "class1_" + str(c) 
    #     trace = go.Heatmap(z=z)
    #     data=[trace]
    #     fig = go.Figure(data=data, layout=layout)
    #     py.plot(fig, filename=title)
    
    #     for row in range(28):
    #         for col in range(28):
    #             z[row][col] = class2_mat_data[27 - row][col][c]
    #     title = "class2_" + str(c) 
    #     trace = go.Heatmap(z=z)
    #     data=[trace]
    #     fig = go.Figure(data=data, layout=layout)
    #     py.plot(fig, filename=title)

    #     for row in range(28):
    #         for col in range(28):
    #             z[row][col] = odds_mat_data[27 - row][col][c]
    #     title = "odds_" + str(c) 
    #     trace = go.Heatmap(z=z)
    #     fig = go.Figure(data=data, layout=layout)
    #     py.plot(fig, filename=title)

        





#duration = 500  # millisecond
#freq = 440  # Hz
#winsound.Beep(freq, duration)

