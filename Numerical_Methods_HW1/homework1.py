import numpy as np

print("========================================")
print("       HOMEWORK 1 - NUMERICAL METHODS   ")
print("========================================")

# ========================================
# PROBLEM #3: Analysis of Matrix A
# ========================================
print("\n--- [PROBLEM 3] SVD and Rank Analysis of A ---")
A = np.array([[1, 2, 3], [2, 4, 6]], dtype=float)

# Compute SVD and rank
U, s, Vt = np.linalg.svd(A)
rank_A = np.linalg.matrix_rank(A)
AtA = A.T @ A
eigenvalues_AtA = np.linalg.eigvalsh(AtA)

print(f"Matrix A:\n{A}")
print(f"Rank of A (r): {rank_A}")
print(f"Singular values (s): {s}")
print(f"Eigenvalues of A^T * A: {eigenvalues_AtA}")
print(f"Verification (s^2 == lambda): {s**2}")


# ========================================
# PROBLEM #4: Numerical Rank with Random Matrices
# ========================================
print("\n--- [PROBLEM 4] Numerical Rank (Random Matrices) ---")
np.random.seed(42)
A_rand = np.random.rand(8, 4) @ np.random.rand(4, 6)
_, s_rand, _ = np.linalg.svd(A_rand)

np.set_printoptions(formatter={"float_kind": "{:10.4e}".format})
print(f"Singular values of the random matrix:\n{s_rand}")
np.set_printoptions()

numerical_rank = np.linalg.matrix_rank(A_rand)
print(f"Numerical rank of the random matrix: {numerical_rank}")


# ========================================
# PROBLEM #8: LU Factorization with Partial Pivoting
# ========================================
print("\n--- [PROBLEM 8] LU Factorization with Pivoting (PA = LU) ---")


def lu_with_pivoting(A):
  n = A.shape[0]
  L = np.eye(n)
  U = A.copy()
  P = np.eye(n)

  for k in range(n - 1):
    # Partial pivoting: find the maximum absolute value in the current column
    max_idx = np.argmax(np.abs(U[k:, k])) + k

    if max_idx != k:
      # Swap rows in U
      U[[k, max_idx], :] = U[[max_idx, k], :]
      # Swap rows in the permutation matrix P
      P[[k, max_idx], :] = P[[max_idx, k], :]
      # Swap rows in L (for previously computed columns)
      if k > 0:
        L[[k, max_idx], :k] = L[[max_idx, k], :k]

    # Standard Gaussian elimination steps
    for i in range(k + 1, n):
      L[i, k] = U[i, k] / U[k, k]
      U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]

  return P, L, U


# Test matrix for LU factorization
A_lu = np.array([[2, 1, 1], [4, 3, 3], [8, 7, 9]], dtype=float)
P, L, U = lu_with_pivoting(A_lu)

print(f"Original Matrix A:\n{A_lu}")
print(f"Permutation Matrix (P):\n{P}")
print(f"Lower Triangular Matrix (L):\n{L}")
print(f"Upper Triangular Matrix (U):\n{U}")

# Verification: PA should equal L @ U
is_correct = np.allclose(P @ A_lu, L @ U)
print(f"Verification that P * A == L * U: {is_correct}")