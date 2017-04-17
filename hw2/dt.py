import math
import operator
import sys
import copy

def getInfo(D):
    """ 
    param D : dataset D
    returns : dateset D's entropy Info(D) 
    """
    ClassCount = {}             # 'ClassCount' stores number of tuples for each class
    total = len(D)              # total number of tuples in D
    entropy = 0.0               # store entropy
    for data in D:              # for each data tuple in D
        Class = data['class']   # temp variable stores data's class label
        if Class not in ClassCount.keys(): 
            ClassCount[Class]=0
        ClassCount[Class] += 1  # increase count
    
    for Class in ClassCount:    # get entropy
        p_class = float(ClassCount[Class])/total
        entropy -= p_class*math.log(p_class,2)
    return entropy

def getValuesInAttr(D,Attr):   
    """
    param D    : dataset 
    parem Attr : specific attribute name
    return     : all attribute values in specific atrribute 'Attr' for dataset 'D' 
    """    
    values = set()              
    for data in D:             # for all data tuples in D  
        values.add(data[Attr]) 
    return values

def getD_j(D,Attr,value_j):    
    """
    param D       : dataset
    param Attr    : specific attribute
    param value_j : specific value in 'Attr'
    return        : dataset D_j having attribute value 'value_j' in attribute 'Attr' 
    """
    D_j = []                   # stores dataset D_j
    for data in D:             # for each data tuple in D
        if(data[Attr]==value_j):
            D_j.append(data)
    
    return D_j

def getGain(D,Attr):             
    """ 
    param D     : dataset
    param Attr  : specific attribute
    return      : get Gain(Attr) 
    """
    values = getValuesInAttr(D,Attr)    # store all values in attribute 'Attr'
    total = len(D)                      # total number of tuples in D
    infoD = getInfo(D)                  # info(D)
    info_attr_D = 0.0                   # info_attr(D) 
    for value_j in values:              # for all values 
        data_j = getD_j(D,Attr,value_j) # get dataset D_j
        len_j = len(data_j)             # number of tuples in D_j
        info_attr_D += float(len_j)/total * getInfo(data_j) #get info_attr(D) 
    return (infoD - info_attr_D)

def getBestAttr(D,Attrs):    
    """ 
    param D     : dataset
    param Attrs : remaining attribute in process of making decision tree
    return      : Best Attribute of 'Attrs' using Information Gain 
    """               
    attrGain = {}                       # store each atrribute's Gain value

    # for all remaining attribute in 'Attrs'
    for attr in Attrs:                  
        attrGain[attr]=getGain(D,attr)  # get Gain(attr)                

    # sort to pick biggest Gain value 
    attrGain = sorted(attrGain.items(), key=operator.itemgetter(1),reverse=True) 
    return attrGain[0][0]               # return best attribute

def getMajority(D):           
    """
    param D : dataset
    return  : Majority class label
    """            
    ClassCount = {}                         # 'ClassCount' stores number of tuples for each class

    # for each data tuple in D
    for data in D:                          
        Class = data['class']               # temp variable stores data's class label
        if Class not in ClassCount.keys():
              ClassCount[Class]=0
        ClassCount[Class] += 1              # increase count
    
    # sort to pick Majority class label
    ClassCount = sorted(ClassCount.items(),key=operator.itemgetter(1),reverse=True) 
    return ClassCount[0][0]                 # return Majority class label


def make_dt(D_total,D,Attrs):     
    """
    param D_total : total training dataset
    param D       : portion of total dataset in internal node  
    return        : decision tree for total Training dataset 'D_total' 
    """
    Attr_cpy = Attrs[:]                          # copy 'Attrs' because recursive call below will references 'Attrs'
    ClassforData = [data['class'] for data in D] # list all class labels in each data tuple in D
    
    # if there is only one class label in 'D'
    if ClassforData.count(ClassforData[0]) == len(ClassforData):
        return ClassforData[0]

    # if there is no remaining attribute in 'Attrs'
    if len(Attr_cpy) == 0:
        return getMajority(D)
    
    bestAttr = getBestAttr(D,Attr_cpy)           # get best attribute in 'Attrs'
    del Attr_cpy[Attr_cpy.index(bestAttr)]       # delete 'bestAttr' in 'Attrs'
    dt = {bestAttr:{}}                           # make sub decision tree 
    values = getValuesInAttr(D_total,bestAttr)   # set of values inf 'bestAttr'

    # for all value_j in values
    for value_j in values:
        D_j = getD_j(D,bestAttr,value_j)
        
        # if there is no data tutple in D_j
        if len(D_j) == 0:
            dt[bestAttr][value_j] = getMajority(D)
        
        # if there is remaining data tuple in D_j
        else:
            dt[bestAttr][value_j] = make_dt(D_total,D_j,Attr_cpy)

    return dt 
        
def classifier(decision_tree,data):
    """ classify data into specific class
    param decision_tree : decision tree made by training data
    param data          : one data tuple 
    """
    dt = copy.deepcopy(decision_tree)   # copy to maintain original decision tree
    cur_attr = list(dt)[0]              # 'cur_attr' is first selected attribute
 
    while True:
        dt = dt[cur_attr]               # 'dt' is sub decision tree  
        value = data[cur_attr]          # 'value' is data's attribute value

        # if there is no dictionary type instance, dt[value] is class label
        if not isinstance(dt[value],dict):    
            return dt[value]

        dt = dt[value]                  # 'dt' is branches of value
        cur_attr = list(dt)[0]          # update cur_attr
       
if __name__ =="__main__":
    TrainingData = []                   # list of storing Training dataset
    Attribute = []                      # list of all attributes in Training dataset
    Attrcpy = []                        # copy of Attribute to use output

    """ 
    Training part
    """
    # open "dt_train.txt"
    with open(sys.argv[1]) as f:   

        # read all attributes in Training dataset
        Attribute = f.readline()
        Attrcpy = copy.deepcopy(Attribute)
        Attribute = Attribute.split()
        Attribute = Attribute[:-1]
        
        # for all dataset
        for line in f:              
            eachline = line.split()
            temp = {}                               # dictionary type for one tuple
            # for all attributes
            for i in range(len(Attribute)):     
                temp[Attribute[i]]=eachline[i];     # temp[attr] = value
            temp['class'] = eachline[-1]            # last element of line is class label
            TrainingData.append(temp)           
            
    DecisionTree = make_dt(TrainingData,TrainingData,Attribute) # make decision tree
    
    """
    Testing part
    """
    # open "dt_result.txt"
    result = open(sys.argv[3],'w')   
    # open "dt_test.txt"
    with open(sys.argv[2]) as test:    
            test.readline()  
            result.write(Attrcpy)       # Write the attributes on the first line
            Attrcpy = Attrcpy.split()

            # for all test dataset
            for line in test:
                eachline = line.split()
                data = {}       # temp data tuple

                # for all attribute except for class
                for i in range(len(Attrcpy)-1):
                    data[Attrcpy[i]]=eachline[i];

                # decision data tuple's class label
                data['class'] = classifier(DecisionTree,data) 
                result_data = [] # temp data tuple
                for key in data:
                    result_data.append(data[key])
                
                # make one data tuple string and write to result file
                result_data = "\t".join(result_data)
                result_data +="\n"
                result.write(result_data)
    
    result.close()