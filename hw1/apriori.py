
'''
makeItemSet(TransactionList):
TransactinList로부터 item의 집합을 추출
'''
def makeItemSet(TransactionList):
    itemSet = []
    for Transaction in TransactionList:
        for item in Transaction:
            if not item in itemSet:
                itemSet.append(item)
    itemSet.sort()
    return itemSet


'''
makeL1(TransactionList,itemSet,min_sup):
L1 집합을 만듬
'''
def makeL1(TransactionList, itemSet, min_sup):
    item_count = [0] * len(itemSet)  # 각 item의 개수를 저장하는 리스트
    for item in itemSet:
        for transaction in TransactionList:
            if {item}.issubset(transaction):  # item이 해당 transaction에 들어있는지 체크
                item_count[itemSet.index(item)] += 1  # item이 들어있으면 카운트를 1 증가시킴

    L1 = []  # L1을 저장할 set을 선언
    Total_trnsa = len(TransactionList)  # transaction의 총 개수를 구함
    for index in range(len(item_count)):
        sup = item_count[index] / float(Total_trnsa)
        if sup * 100 >= min_sup:
            L1.append([itemSet[index]])
    return L1


'''
makeC_k(L_k_1,k):
각 level k의 후보 itemset C_k를 생성
'''
def makeC_k(L_k_1, k):
    C_k = []
    for i in range(len(L_k_1) - 1):
        for j in range(i + 1, len(L_k_1)):
            if L_k_1[i][0:k - 2] == L_k_1[j][0:k - 2]:
               li = set(L_k_1[i])
               lj = set(L_k_1[j])
               C_k.append(list(li.union(lj)))

    return C_k


'''
apriori(TransactionList,L_list,min_sup,itemNum):
frequent itemset을 찾아서 반환하는 함수
'''
def apriori(TransactionList, L_list, min_sup, itemNum):

    for k in range(2, itemNum + 1):

        #generate Candidate_k
        C_k = makeC_k(L_list[k - 1], k)
        if C_k == []:
            return L_list

        #pruning
        C_k_pruned = pruning(C_k,k,L_list)        
        if (C_k_pruned) == []:         
           return L_list
       
        #generate L_k       
        L_k = checkMinSup(C_k_pruned,k,TransactionList,min_sup) 
        if L_k == []:
            return L_list
        
            
        L_list.append(L_k)
    
    return L_list

'''
pruning(C_k,k,L_List): 
C_k에 있는 itemset 후보들의 부분집합이 L_1~L_k-1에 존재하는지 확인 한 뒤
없으면 그 itemset을 버림
'''
def pruning(C_k,k,L_List):   
    # pruning 
    for Candidate in C_k: 
        for Subset in getSubset(Candidate)[1:]: 
            exist = 0
            i=len(Subset)
            if i >= k:
                return C_k
            for Li in L_List[i]:
                if Subset == Li:
                    exist = 1
                    break

            if exist == 0:
                del C_k[C_k.index(Candidate)]
                return C_k

'''
checkMinSup(C_k_pruned,k,TransactionList,min_sup):
Pruning 과정을 거친 itemset 후보들의 min_sup을 체크 뒤 만족 못하면 버림
'''
def checkMinSup(C_k_pruned,k,TransactionList,min_sup):
    C_k_count = [0]*len(C_k_pruned)
    for C_k in C_k_pruned:
        for transaction in TransactionList:
            if set(C_k).issubset(transaction):
                C_k_count[C_k_pruned.index(C_k)]+=1

    L_k = []
    Total_trnsa = len(TransactionList)
    for index in range(len(C_k_count)):
        sup = C_k_count[index] / float(Total_trnsa)
       
        if sup*100 >= min_sup:
            L_k.append(C_k_pruned[index])

    return L_k             



'''
getSup(Ck_subset,TransactionList):
특정 itemset의 support를 구하는 함수
'''
def getSup(Lk_subset,TransactionList):
    Total_trnsa = len(TransactionList)
    cnt = 0
    for transaction in TransactionList:
           if set(Lk_subset).issubset(transaction):
                cnt+=1
    
    sup = cnt / float(Total_trnsa)
    return sup*100


'''
getSubset(Candidate,prev=[]):
itemset의 부분집합을 구해서 반환하는 함수
'''
def getSubset(Candidate,prev=[]):
    if Candidate:
        cur=Candidate[0]
        return getSubset(Candidate[1:],prev)+getSubset(Candidate[1:],prev+[cur])
    return [prev]

def getConfidence(item_p,item_q,TransactionList):
    union = item_p | item_q
    p_q = getSup(list(union),TransactionList)/getSup(list(item_p),TransactionList)
    q_p = getSup(list(union),TransactionList)/getSup(list(item_q),TransactionList)

    return p_q*100,q_p*100

'''
getAllAssociation(L_list,TransationList):
[a,b,support,confidence]의 list를 반환
'''
def getAllAssociation(L_list,TransationList):
    Association_list = []
    for index in range(2,len(L_list)):
        for Li in L_list[index]:
            subset_list = getSubset(Li)[1:]
            subset_list.pop()       
            for subset in subset_list:
                sup = getSup(Li,TransactionList)
                itemset_whole = set(Li)
                itemset_p = set(subset)
                itemset_q = itemset_whole - itemset_p
                conf_p_q,conf_q_p = getConfidence(itemset_p,itemset_q,TransactionList)

                temp = []
                temp.append(itemset_p)
                temp.append(itemset_q)
                temp.append(sup)
                temp.append(conf_p_q)
                Association_list.append(temp)

    return Association_list



if __name__ =="__main__":
    #TransactionList =[[1,2,3],[1,2,7],[1,4],[2,3,4]]
    TransactionList =[[1,2,5],[1,2,4],[2,3],[4,5,6],[1,3,2]]
    #TransactionList =[[4],[4],[3],[2]]
    itemSet = makeItemSet(TransactionList)
    #min_sup=2/9.0*100
    min_sup = 50
    L1 = makeL1(TransactionList,itemSet,min_sup)
    L_list = [0]
    L_list.append(L1)

    L_list = apriori(TransactionList,L_list,min_sup,len(itemSet))

    Association = getAllAssociation(L_list,TransactionList)
    print(Association)
    # print(L_list)
    # a=getSubset([5,6])
    # print(a)
    # a=a[1:]
    # a.pop()
    # print(a)
  
   