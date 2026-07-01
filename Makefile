import numpy as np
import sys
import symnmf
np.random.seed(1234)


def goals(goal,X, n, d , k, max_iter, epsilon):
    if goal== 'sym':
        A=symnmf.sym(X, n, d)
        np.savetxt(sys.stdout, np.array(A), delimiter=',', fmt='%.4f')
    elif goal == 'ddg':
        A=symnmf.sym(X, n, d)
        D=symnmf.ddg(A, n)
        np.savetxt(sys.stdout, np.array(D), delimiter=',', fmt='%.4f')
    elif goal=='norm':
        A=symnmf.sym(X, n, d)
        D=symnmf.ddg(A, n)
        W=symnmf.norm(A, D, n)
        np.savetxt(sys.stdout, np.array(W), delimiter=',', fmt='%.4f')
    elif goal == 'symnmf':
        A=symnmf.sym(X, n, d)
        D=symnmf.ddg(A, n)
        W=symnmf.norm(A, D, n)
        H_init= init_H(W, n, k).tolist()
        H_final=symnmf.symnmf(W, H_init, n, k, max_iter, epsilon)
        if H_final is not None:
            np.savetxt(sys.stdout, np.array(H_final), delimiter=',', fmt='%.4f')
        else: 
            print("An Error Has Occured")
            sys.exit(1)
    else: 
        print("An Error Has Occured")
        sys.exit(1)


def init_H(W, n, k):
    mean=np.mean(W)
    H=np.random.uniform(0, 2* np.sqrt(mean/k), (n,k))
    return H

def main():
    max_iter=300
    epsilon= 1e-4
    if len(sys.argv)!=4:
        print("An Error Has Occurred") 
        sys.exit(1)
    try:
        k= int(sys.argv[1])
        if k<=0:
            raise ValueError("An Error Has Occurred")
    except ValueError as e: 
        print(f"An Error Has Occurred: {e}")
        sys.exit(1)
    goal= sys.argv[2]
    file_name=sys.argv[3]
    try:
        X=np.loadtxt(file_name, delimiter=',')
        if X.ndim==1:
            X=X.reshape(-1, 1)
    except Exception as e:
        print("An Error Has Occurred") 
        sys.exit(1)
    n,d=X.shape
    X=X.tolist()
    goals(goal,X, n, d, k, max_iter, epsilon)
    

if __name__ == "__main__":
    main()



