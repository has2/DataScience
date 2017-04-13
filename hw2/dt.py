import math
import operator
import sys
import copy
# def getGiniD(D):
#     ClassCount = {}
#     total = len(D)
#     GiniD = 1.0
#     for data in D:
#         Class = data['class']
#         if Class not in ClassCount.keys():
#             ClassCount[Class]=0
#         ClassCount[Class] += 1
    
#     for Class in ClassCount:
#         p_class = float(ClassCount[Class])/total
#         GiniD -= p_class*p_class
#     return GiniD
# def getGiniDiff(D,Attr):
#     values = getValuesInAttr(D,Attr)
#     total = len(D)
#     GiniD = getGiniD(D)
#     GiniaD = 0.0
#     for value_j in values:
#         data_j = getD_j(D,Attr,value_j)
#         len_j = len(data_j)
#         GiniaD += float(len_j)/total * getGiniD(data_j)
#     return GiniD - GiniaD
# def getBestAttrGini(D,Attrs):
    # attrGain = {}
    # for attr in Attrs:
    #     attrGain[attr]=getGiniDiff(D,attr)
    # attrGain = sorted(attrGain.items(), key=operator.itemgetter(1),reverse=True)
    # return attrGain[0][0]
def getInfo(D):
    ClassCount = {}             # ClassCount stores number of tuples for each class
    total = len(D)              # total number of tuples in D
    entropy = 0.0               # store entropy
    for data in D:              # for each data tuple in D
        Class = data['class']   
        if Class not in ClassCount.keys():
            ClassCount[Class]=0
        ClassCount[Class] += 1
    
    for Class in ClassCount:
        p_class = float(ClassCount[Class])/total
        entropy -= p_class*math.log(p_class,2)
    return entropy
def getValuesInAttr(D,Attr):
    values = set()
    for data in D:
        values.add(data[Attr])
    return values
def getD_j(D,Attr,value_j):
    
    D_j = []
    for data in D:
        if(data[Attr]==value_j):
            D_j.append(data)
    
    return D_j
def getGain(D,Attr):
    values = getValuesInAttr(D,Attr)
    total = len(D)
    infoD = getInfo(D)
    info_attr_D = 0.0
    for value_j in values:
        data_j = getD_j(D,Attr,value_j)
        len_j = len(data_j)
        info_attr_D += float(len_j)/total * getInfo(data_j)
    
    return (infoD - info_attr_D)
def getBestAttr(D,Attrs):
    attrGain = {}
    for attr in Attrs:                     # 남은 모든 attribute에 대해 gain값을 구함
        attrGain[attr]=getGain(D,attr)                   
    attrGain = sorted(attrGain.items(), key=operator.itemgetter(1),reverse=True)
    return attrGain[0][0]
def getMajority(D):
    ClassCount = {}
    for data in D:
        Class = data['class']
        if Class not in ClassCount.keys():
              ClassCount[Class]=0
        ClassCount[Class] += 1
    ClassCount = sorted(ClassCount.items(),key=operator.itemgetter(1),reverse=True)
    return ClassCount[0][0]
def make_dt(D_total,D,Attrs):
    
    Attr_cpy = Attrs[:]
    
    ClassforData = [data['class'] for data in D]
    
    if ClassforData.count(ClassforData[0]) == len(ClassforData):
        return ClassforData[0]
    if len(Attr_cpy) == 0:
        return getMajority(D)
    
    bestAttr = getBestAttr(D,Attr_cpy)
    #bestAttr = getBestAttrGini(D,Attr_cpy) <- gini
    del Attr_cpy[Attr_cpy.index(bestAttr)]
    dt = {bestAttr:{}}
    values = getValuesInAttr(D_total,bestAttr)
    for value_j in values:
        D_j = getD_j(D,bestAttr,value_j)
   
        if len(D_j) == 0:
            dt[bestAttr][value_j] = getMajority(D)
        else:
            dt[bestAttr][value_j] = make_dt(D_total,D_j,Attr_cpy)
    return dt 
        
def classifier(decision_tree,data):
    dt = copy.deepcopy(decision_tree)
    cur_attr = list(dt)[0]
 
    while True:
        dt = dt[cur_attr]
       
        value = data[cur_attr]   
        if not isinstance(dt[value],dict):
            return dt[value]
        dt = dt[value]
        cur_attr = list(dt)[0] 
       
if __name__ =="__main__":
    TrainingData = []
    Attribute = []
    Attrcpy = []
    #Training 
    with open('dt_train1.txt') as f:    # open "input.txt"
        Attribute = f.readline()
        Attrcpy = copy.deepcopy(Attribute)
        Attribute = Attribute.split()
        Attribute = Attribute[:-1]
        
        for line in f:              # for all line in input.txt
            eachline = line.split()
            temp = {}
            for i in range(len(Attribute)):
                temp[Attribute[i]]=eachline[i];
            temp['class'] = eachline[-1]
            TrainingData.append(temp)
    TrainingData_total = copy.deepcopy(TrainingData)  
    DecisionTree = make_dt(TrainingData_total,TrainingData,Attribute)
    #Test
    result = open('dt_result1.txt','w')   
    with open('dt_test1.txt') as test:    
            test.readline()  
            result.write(Attrcpy)
            Attrcpy = Attrcpy.split()
        
            for line in test:
                eachline = line.split()
                data = {}
                for i in range(len(Attrcpy)-1):
                    data[Attrcpy[i]]=eachline[i];
                data['class'] = classifier(DecisionTree,data) 
                result_data = []
                for key in data:
                    result_data.append(data[key])
                
                result_data = "\t".join(result_data)
                result_data +="\n"
                result.write(result_data)
    
    result.close()