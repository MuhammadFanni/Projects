import math
import sys


def kmeans(Nlist, iter, k, e):
    Klist=Nlist[:k]
    NlistTuple=[[xi,-1] for xi in Nlist]
    for i in range(k):
        NlistTuple[i][1]=i
    KlistPrev=[[xi,1] for xi in Klist]
    KlistCurr=[[xi[0][:], xi[1]] for xi in KlistPrev]
    curr_iter=0
    while(curr_iter<iter):
        for i in range(len(Nlist)):
            xi=Nlist[i]
            curr_cluster= NlistTuple[i][1]
            new_cluster=argmin(xi, KlistPrev)
            if (new_cluster!=curr_cluster):
                cur_mean=KlistCurr[new_cluster][0]
                prev_points_new_cluster=KlistCurr[new_cluster][1]
                new_points_new_cluster= prev_points_new_cluster+1
                new_mean= division(addition(multiplication(cur_mean, prev_points_new_cluster), xi),new_points_new_cluster)
                KlistCurr[new_cluster][0]=new_mean
                KlistCurr[new_cluster][1]=new_points_new_cluster
                if (curr_iter!=0):
                    prev_mean=KlistCurr[curr_cluster][0]
                    prev_points_prev_cluster=KlistCurr[curr_cluster][1]
                    new_points_prev_cluster=prev_points_prev_cluster-1
                    updated_prev_mean= division(reduction(multiplication(prev_mean, prev_points_prev_cluster), xi),new_points_prev_cluster)
                    KlistCurr[curr_cluster][0]=updated_prev_mean
                    KlistCurr[curr_cluster][1]=new_points_prev_cluster
                NlistTuple[i][1]=new_cluster
        if (curr_iter!=0 and convergence(e, KlistPrev, KlistCurr)):
            KlistPrev= [[xi[0][:], xi[1]] for xi in KlistCurr]
            break
        else:
            KlistPrev= [[xi[0][:], xi[1]] for xi in KlistCurr]
            curr_iter+=1
    return [ki[0] for ki in KlistPrev]


def Euclidean_Distance(p,q):
    ec_sum=0
    for i in range(len(p)):
        ec_sum+=pow((p[i]-q[i]),2)
    return math.sqrt(ec_sum)

def convergence(e, KlistPrev, KlistCurr):
    for i in range(len(KlistCurr)):
        if (Euclidean_Distance(KlistPrev[i][0], KlistCurr[i][0])>=e):
            return False
    return True

def argmin(xi, KlistPrev):
    curr_k=0
    curr_min=float('inf') 
    for i in range(len(KlistPrev)):
        curr_dist=Euclidean_Distance(xi, KlistPrev[i][0])
        if (curr_dist<curr_min):
            curr_min=curr_dist
            curr_k=i
    return curr_k

def addition(p,q):
    res=p[:]
    for i in range(len(q)):
        res[i]+=q[i]
    return res

def reduction(p,q):
    res=p[:]
    for i in range(len(q)):
        res[i]-=q[i]
    return res

def multiplication(p,num):
    res=p[:]
    for i in range(len(p)):
        res[i]*=num
    return res

def division(p,num):
    res=p[:]
    for i in range(len(p)):
        res[i]/=num
    return res


def main():
    e=0.001
    if len(sys.argv) < 3:
        print("Usage: python kmeans.py <K> <iter> <input_file>")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("Usage: python kmeans.py <K> <iter> <input_file>")
        sys.exit(1)
    if len(sys.argv) == 4:
        K = float(sys.argv[1])
        iter = float(sys.argv[2])
        input_file = sys.argv[3]
    if len(sys.argv) == 3:
        K = float(sys.argv[1])
        iter = 200
        input_file = sys.argv[2]
    if not (1 < iter < 1000 and iter % 1 == 0):
        print("Error: Invalid maximum iteration!")
        sys.exit(1)
    try:
        Nlist = []
        with open(input_file, 'r') as file:
            for line in file:
                values = line.split(',')
                vector = list(map(float, values))
                Nlist.append(vector)
                n=len(Nlist)
        if not (1 < K < n and K % 1 == 0):
            print("Error: Invalid number of clusters!")
            sys.exit(1)
        centroids = kmeans(Nlist, iter, int(K), e)
    except ZeroDivisionError as exp:
        print("An Error Has Occurred")
        sys.exit(1)
    for centroid in centroids:
        formatted_centroid = ','.join(['%.4f' % val for val in centroid])
        print(formatted_centroid)


if __name__ == "__main__":
    main()
