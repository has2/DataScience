def makeItemSet(TransactionList):
    itemSet =[]
    for Transaction in TransactionList:
        for item in Transaction:
            if not item in itemSet:
                itemSet.append(item)
    itemSet.sort()
    return itemSet

def makeL1(TransactionList,itemSet,min_sup):
    item_count = [0]*len(itemSet)                      #각 item의 개수를 저장하는 리스트 
    for item in itemSet:
        for transaction in TransactionList:
            if {item}.issubset(transaction):           #item이 해당 transaction에 들어있는지 체크
                item_count[itemSet.index(item)]+=1     #item이 들어있으면 카운트를 1 증가시킴

    L1 = set()                                         #L1을 저장할 set을 선언
    Total_trnsa = len(TransactionList)                 #transaction의 총 개수를 구함
    for index in range(len(item_count)):               
        sup = item_count[index] / float(Total_trnsa)  
        if sup*100 >= min_sup:
            L1.add(itemSet[index])

    return L1


if __name__ =="__main__":
    TransactionList =[[1,2,3],[1,3,7],[10,11,12,2,8]]
    itemSet = makeItemSet(TransactionList)
    
    result = makeL1(TransactionList,itemSet,50)
    print(itemSet)
    print(result)

