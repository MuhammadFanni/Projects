import numpy as np
import sys
import symnmf
from sklearn.metrics import silhouette_score
from kmeans import kmeans

np.random.seed(1234)

def read_input(file_name):
    vectors = []
    with open(file_name, 'r') as file:
        for line in file:
            values = line.split(',')
            vector = list(map(float, values))
            vectors.append(vector)
    return np.array(vectors)

def init_H(W, n, k):
    mean=np.mean(W)
    H=np.random.uniform(0, 2* np.sqrt(mean/k), (n,k))
    return H

def main():
    max_iter=300
    epsilon= 1e-4
    if len(sys.argv)!=3:
        print("An Error Has Occurred") 
        sys.exit(1)
    try:
        k= int(sys.argv[1])
        if k<=0:
            raise ValueError("An Error Has Occurred")
    except ValueError as e: 
        print(f"An Error Has Occurred: {e}")
        sys.exit(1)
    file_name=sys.argv[2]
    X = read_input(file_name)
    n,d=X.shape
    Xlist=X.tolist()
    centroids =kmeans(Xlist, max_iter, k, epsilon)
    centroids=np.array(centroids)
    kmeans_labels = [np.argmin([np.linalg.norm(x - c) for c in centroids]) for x in X]
    A=symnmf.sym(Xlist, n, d)
    D=symnmf.ddg(A, n)
    W=symnmf.norm(A, D, n)
    H_init= init_H(W, n, k).tolist()
    H_final=symnmf.symnmf(W, H_init, n, k, max_iter, epsilon)
    if H_final is not None:
        H_labels = np.argmax(np.array(H_final), axis=1)
        unique_labels = np.unique(H_labels)
        if len(unique_labels) > 1 and len(np.unique(kmeans_labels)) > 1:
            symnmf_score = silhouette_score(X, H_labels)
            print(f"nmf: {symnmf_score:.4f}")
            kmeans_score = silhouette_score(X, kmeans_labels)
            print(f"kmeans: {kmeans_score:.4f}")
        else:
            print("An Error Has Occurred") 
            sys.exit(1)
    else:
        print("An Error Has Occurred") 
        sys.exit(1)
    

if __name__ == "__main__":
    main()



