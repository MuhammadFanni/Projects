#ifndef SYMNMF_H
#define SYMNMF_H

void sym(double** X, double** A, int n, int dim);
void ddg(double** A, double** D, int n);
void norm(double** A, double** D, double** W, int n);
void symnmf(double** W, double **H, int n, int k, int max_iter, double epsilon);

#endif