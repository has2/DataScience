import sys

def DBSCAN(DataSet,isVisited,hasCluster,eps,MinPts): 
    ClusterList = []
    for id in range(len(DataSet)):
        if isVisited[id] == 0:
            isVisited[id] = 1
            N = regionQuery(id,eps,DataSet)
            if len(N) < MinPts:
                isVisited[id] = 2
            else:
                ClusterList.append(expandCluster(DataSet,id,N,isVisited,hasCluster,eps,MinPts))   
    return ClusterList
                
def expandCluster(DataSet,start_id,N,isVisited,hasCluster,eps,MinPts):
     newCluster = [start_id]     
     hasCluster[start_id] = 1
     for n_id in N:
         if isVisited[n_id] == 0:
             isVisited[n_id] = 1
             n_N = regionQuery(n_id,eps,DataSet)
             if len(n_N) >= MinPts:
                 for n_N_id in n_N:
                    N.append(n_N_id)       
         if hasCluster[n_id] == 0:
             newCluster.append(n_id)
             hasCluster[n_id] = 1 
     return newCluster

def regionQuery(cur_id,eps,DataSet):
    N = []
    cur_x = DataSet[cur_id][0]
    cur_y = DataSet[cur_id][1]
    for id in range(len(DataSet)):
        x = DataSet[id][0]
        y = DataSet[id][1]
        if (cur_x-x)**2+(cur_y-y)**2 <= eps**2:
            N.append(id)
    return N

if __name__ =="__main__":

    filename = sys.argv[1]
    filename = filename.split('.')[0]    
    n = int(sys.argv[2])
    eps = float(sys.argv[3])
    MinPts = int(sys.argv[4])

    DataSet = []
    isVisited = [] # unvisited:0 visited:1 noise:2
    hasCluster = [] # has : 1

    with open(filename+".txt") as f:
        for line in f:
            temp = line.split()
            x = float(temp[1])
            y = float(temp[2])
            DataSet.append([x,y])
            isVisited.append(0)
            hasCluster.append(0)
    
    ClusterList = DBSCAN(DataSet,isVisited,hasCluster,eps,MinPts)
    ClusterList.sort(key=len,reverse=True)

    for cluster_id in range(n):
        with open(filename+"_cluster_"+str(cluster_id)+".txt","w") as f:
            for member_id in ClusterList[cluster_id]:
                f.write("%d\n" % member_id)
            