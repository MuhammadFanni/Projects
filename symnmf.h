#define _GNU_SOURCE
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "symnmf.h"
#include <time.h>
#include <stdlib.h>
#include <string.h>
#define INITIAL_CAPACITY 10

double Squared_euclidean_distance(double* p, double* q, int dim){
    double EC_sum=0;
    int i;
    for (i=0; i<dim; i++){
        EC_sum+= (p[i]-q[i])*(p[i]-q[i]);
    }
    return EC_sum;
}

void sym(double** X, double** A, int n, int dim){
    int i1,i2;
    for(i1=0; i1<n; i1++){
        for(i2=0; i2<n; i2++){
            if (i1==i2){
                A[i1][i2]=0.0;
            }
            else{
                double squared_dis=Squared_euclidean_distance(X[i1], X[i2], dim);
                A[i1][i2]=exp(-squared_dis/2.0);
            }
        }
    }
}

void ddg(double** A, double** D, int n){
    int i; 
    int j;
    for(i=0; i<n; i++) 
    {
        double sum = 0;
        for (j=0; j<n; j++)
        {
            sum += A[i][j];
            D[i][j]=0.0;
        }
        D[i][i] = sum;
    }

}

void norm(double** A, double** D, double** W, int n){
    int i;
    int j; 
    for(i=0;i<n;i++){
        for(j = 0; j<n; j ++){
            if (D[i][i] != 0 && D[j][j] != 0) { 
                W[i][j] = (1 / sqrt(D[i][i])) * (1 / sqrt(D[j][j])) * A[i][j];
            } else {
                W[i][j] = 0; 
            }
        }
    }
}

int convergence(double** oldH, double** cur_H, int k, int n, double epsilon){
    double sum = 0; 
    int i;
    int j;
    for(i=0; i<n;i++){
        for(j=0;j<k;j++){
            sum += (cur_H[i][j]-oldH[i][j])*(cur_H[i][j]-oldH[i][j]);
        }
    }
    if (sum< epsilon){
        return 1;
    } 
    return 0;
}
void mat_multiplication(double** mat1, double** mat2, double** res, int mat1rows, int mat1cols,  int mat2cols){
    int i,k,j;
    for(i=0; i<mat1rows; i++){
        for(j=0; j<mat2cols; j++){
            res[i][j]=0.0;
            for(k=0; k<mat1cols; k++){
                res[i][j]+=mat1[i][k]*mat2[k][j];
            }
        }
    }
}
void transpose_matrix(double** H, int k, int n, double** Ht){
    int i,j;
    for(i=0; i<n; i++){
        for(j=0; j<k; j++){
            Ht[j][i]=H[i][j];
        }
    }
}

void update_H(double** H, double** W, int n, int k){
    double** WH= (double**) malloc(n*sizeof(double*));
    double** HHtH= (double**) malloc(n*sizeof(double*));
    double** HHt= (double**) malloc(n*sizeof(double*));
    double** Ht=(double**) malloc(k*sizeof(double*));
    int i,j; 
    for(i=0; i<n; i++){
        WH[i]= (double*) malloc (k*sizeof(double));
        HHtH[i]= (double*) malloc (k*sizeof(double));
        HHt[i]= (double*) malloc (n*sizeof(double));
    }
    for(i=0; i<k; i++){Ht[i]=(double*) malloc(n*sizeof(double)); }
    transpose_matrix(H, k, n, Ht);
    mat_multiplication(H, Ht, HHt, n, k, n);
    mat_multiplication(HHt, H, HHtH, n, n, k);
    mat_multiplication(W, H, WH, n, n, k);
    
    for(i=0; i<n; i++){
        for(j=0; j<k; j++){
            if(HHtH[i][j]!=0){
                H[i][j]*= (1- 0.5 + 0.5 * WH[i][j]/HHtH[i][j]);
            }
        }
    }
    for (i = 0; i< n; i++) {free(WH[i]);
        free(HHtH[i]);
        free(HHt[i]);
    }
    for(i=0; i<k; i++){
        free(Ht[i]);
    }

    free(Ht);free(WH);free(HHtH); free(HHt);   
}


void symnmf(double** W, double **H, int n, int k, int max_iter, double epsilon){
    int i,j;
    int iter=0;
    double** oldH= (double**) malloc (n*sizeof(double*));
    for(i=0; i<n; i++){
        oldH[i]= (double*) malloc (k*sizeof(double));
    }
    while(iter<max_iter){
        for(i=0; i<n; i++){
            for(j=0; j<k; j++){
                oldH[i][j]=H[i][j];
            }
        }
        update_H(H, W, n, k);
        if(convergence(oldH, H, k, n, epsilon)){break;}
        iter++;
    }

   
    for(i=0; i<n; i++){
        free(oldH[i]);
    }
    free(oldH);
}

void print_output(double** mat, int n){
    int i,j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            if (j > 0) {
                printf(",");
            }
            printf("%.4f", mat[i][j]);
        }
        printf("\n");
    }
}


char** read_lines_from_file(FILE *file, size_t *num_lines) {
    char buffer[1024];
    size_t line_count = 0;
    size_t capacity = INITIAL_CAPACITY;
    char **lines = malloc(capacity * sizeof(char *));
    char **temp;
    size_t len, i;
    if (lines == NULL) {
        perror("An Error Has Occurred");
        return NULL;}
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        if (line_count >= capacity) {
            capacity *= 2;
            temp = realloc(lines, capacity * sizeof(char *));
            if (temp == NULL) {
                perror("An Error Has Occurred");
                for (i = 0; i < line_count; i++) {
                    free(lines[i]);
                }
                free(lines);
                return NULL;
            }lines = temp;}
        len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {buffer[len - 1] = '\0';}
        lines[line_count] = malloc((strlen(buffer) + 1) * sizeof(char));
        if (lines[line_count] == NULL) {
            perror("An Error Has Occurred");
            for (i = 0; i < line_count; i++) {
                free(lines[i]);
            }
            free(lines);
            return NULL; }
        strcpy(lines[line_count], buffer);
        line_count++; }
    *num_lines = line_count;
    return lines;
    }


char** read_file_lines(const char *filename, size_t *num_lines) {
    FILE *file = fopen(filename, "r");
    char **lines;

    if (file == NULL) {
        perror("An Error Has Occurred");
        return NULL;
    }

    lines = read_lines_from_file(file, num_lines);
    fclose(file);

    return lines;
}


void print_lines(char **lines, size_t num_lines) {
    size_t i;
    for ( i = 0; i < num_lines; i++) {
        printf("%s", lines[i]);
        if (i < num_lines - 1) {
            printf("\n"); 
        }
    }
}

size_t count_columns(const char *line) {
    size_t num_columns = 0;
    char *line_copy = strdup(line);
    if (line_copy) {
        char *token = strtok(line_copy, ",");
        while (token != NULL) {
            num_columns++;
            token = strtok(NULL, ",");
        }
        free(line_copy);
    }
    return num_columns;
}

void goals(const char *goal, double **X,double **A,double **D,double **W, size_t n, size_t d){
    sym(X, A, n, d);
    ddg(A, D, n);
    norm(A, D, W, n);
    if (strcmp(goal, "sym") == 0) {
        print_output(A, n);
    }
    else if (strcmp(goal, "ddg") == 0){
        print_output(D, n);
    }
    else if (strcmp(goal, "norm") == 0){
        print_output(W, n);
    }
}


double** readinput(const char *filename, size_t *ndlist){
    size_t n,d = 0;
    size_t i, j;
    double *jx;
    double **X;
    char *token, **lines;
    lines = read_file_lines(filename, &n);
    if (lines == NULL) {
        return NULL;
    }
    if (n > 0) {
        d = count_columns(lines[0]);
    }
    jx = (double*)malloc(n * d * sizeof(double));
    for (i = 0; i < n; i++) {
        token = strtok(lines[i], ",");
        for (j = 0; j < d; j++) {
            if (token != NULL) {
                jx[i * d + j] = atof(token);
                token = strtok(NULL, ",");
            } else {
                jx[i * d + j] = 0.0; 
            }
        }
    }
    X= (double**) malloc (n*sizeof(double*));
    for(i=0; i<n; i++){
        X[i]=(double*) malloc (d*sizeof(double));
        for (j=0; j<d; j++){
            X[i][j]=jx[i*d+j];
        }
    }
    ndlist[0]=n;ndlist[1] = d;
    free(jx);
    for (i=0; i<n; i++){free(lines[i]);}
    free(lines);
    return X;
}


int main(int argc, char *argv[]) {
    size_t i, *ndlist, n,d;
    double **X, **A, **D,**W;
    const char *goal, *filename;
    
    if (argc!=3){
        printf("An Error Has Occured");
        return EXIT_FAILURE;}
    goal = argv[1];
    filename = argv[2];
    ndlist = (size_t*) malloc(2*sizeof(size_t));
    X = readinput(filename, ndlist);
    if (X == NULL){
        free(ndlist);
        return EXIT_FAILURE;
    }
    n = ndlist[0];
    d = ndlist[1]; free(ndlist);
    A = (double**) malloc(n*sizeof(double*));
    D = (double**) malloc(n*sizeof(double*));
    W = (double**) malloc(n*sizeof(double*));
    for(i=0; i<n; i++){
        A[i] = (double*) malloc(n*sizeof(double));
        D[i] = (double*) malloc(n*sizeof(double));
        W[i]= (double*) malloc(n*sizeof(double));}
    goals(goal,X,A,D,W,n,d);
    for (i = 0; i< n; i++) {
        free(A[i]);
        free(D[i]);
        free(W[i]);
        free(X[i]);
    }
    free(A);free(D);free(W);free(X);
    return EXIT_SUCCESS;
}


