Homework 3: Numerical Methods 515

Problem #3
import numpy as np

# Problem dimensions and setup
n = 50
A = 4 * np.eye(n) - np.diag(np.ones(n - 1), 1) - np.diag(np.ones(n - 1), -1)

b = 2 * np.ones((n, 1))
b[0] = 3
b[-1] = 3

x0 = np.zeros((n, 1))
tol = 1e-5
max_iter = 10000

def steepest_descent_v2(A, b, x0, tol, max_iter):
    x = x0.copy()
    r = b - A @ x
    for k in range(max_iter):
        if np.linalg.norm(r) < tol:
            return x, k
        q = A @ r
        alpha = (r.T @ r) / (r.T @ q)
        x = x + alpha * r
        r = r - alpha * q
    return x, max_iter

sd_sol, sd_iters = steepest_descent_v2(A, b, x0, tol, max_iter)
print(f"Steepest Descent - Converged: {np.linalg.norm(b - A @ sd_sol) < tol}")
print(f"Iterations: {sd_iters}")

Problem #4
def conjugate_gradient_v2(A, b, x0, tol, max_iter):
    x = x0.copy()
    r = b - A @ x
    p = r.copy()
    
    for k in range(max_iter):
        if np.linalg.norm(r) < tol:
            return x, k
        
        q = A @ p
        z = r.T @ r
        alpha = z / (p.T @ q)
        
        x = x + alpha * p
        r_new = r - alpha * q
        
        if np.linalg.norm(r_new) < tol:
            return x, k + 1
            
        beta = (r_new.T @ r_new) / z
        p = r_new + beta * p
        r = r_new
        
    return x, max_iter

cg_sol, cg_iters = conjugate_gradient_v2(A, b, x0, tol, max_iter)
print(f"Conjugate Gradient - Converged: {np.linalg.norm(b - A @ cg_sol) < tol}")
print(f"Iterations: {cg_iters}")

Problem #7
from scipy.linalg import hessenberg, qr

# Part a: Hessenberg QR Algorithm without shifts
def hessenberg_qr_basic(A, iterations=30):
    H = hessenberg(A)
    n = H.shape[0]
    for _ in range(iterations):
        Q, R = qr(H)
        H = R @ Q
    return np.diag(H)

# Part b: Hessenberg QR Algorithm with single shift
def hessenberg_qr_shifted(A, iterations=30):
    H = hessenberg(A)
    n = H.shape[0]
    for _ in range(iterations):
        mu = H[-1, -1]
        Q, R = qr(H - mu * np.eye(n))
        H = R @ Q + mu * np.eye(n)
    return np.diag(H)

# Part c: Deflated Hessenberg QR with stopping criterion
def hessenberg_qr_deflated(A, tol=1e-9, max_iter=100):
    H = hessenberg(A)
    n = H.shape[0]
    eigenvalues = np.zeros(n, dtype=complex)
    
    current_n = n
    while current_n > 0:
        sub_H = H[:current_n, :current_n]
        for _ in range(max_iter):
            if current_n > 1 and abs(sub_H[current_n-1, current_n-2]) < tol:
                break
            mu = sub_H[-1, -1]
            Q, R = qr(sub_H - mu * np.eye(current_n))
            sub_H = R @ Q + mu * np.eye(current_n)
            
        eigenvalues[current_n - 1] = sub_H[-1, -1]
        current_n -= 1
        
    return eigenvalues

if __name__ == "__main__":
    print("=== RUNNING PROBLEM 3: Steepest Descent ===")
    sd_sol, sd_iters = steepest_descent_v2(A, b, x0, tol, max_iter)
    print(f"Method converged. Total iterations: {sd_iters}\n")
    
    print("=== RUNNING PROBLEM 4: Conjugate Gradient ===")
    cg_sol, cg_iters = conjugate_gradient_v2(A, b, x0, tol, max_iter)
    print(f"Method converged. Total iterations: {cg_iters}\n")
    
    print("=== RUNNING PROBLEM 7: Hessenberg QR ===")
    # Add your call for Problem 7 here, for example:
    # evals = hessenberg_qr_deflated(A_matrix)
    # print("Computed Eigenvalues:", evals)
    