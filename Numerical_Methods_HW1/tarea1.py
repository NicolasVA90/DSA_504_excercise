import numpy as np

print("========================================")
print("       TAREA 1 - MÉTODOS NUMÉRICOS      ")
print("========================================")

# ========================================
# PUNTO #3: Análisis de la matriz A
# ========================================
print("\n--- [PUNTO 3] Análisis SVD y Rango de A ---")
A = np.array([[1, 2, 3], [2, 4, 6]], dtype=float)

# Calcular SVD y rango
U, s, Vt = np.linalg.svd(A)
rank_A = np.linalg.matrix_rank(A)
AtA = A.T @ A
eigenvalues_AtA = np.linalg.eigvalsh(AtA)

print(f"Matriz A:\n{A}")
print(f"Rango de A (r): {rank_A}")
print(f"Valores singulares (s): {s}")
print(f"Valores propios de A^T * A: {eigenvalues_AtA}")
print(f"Verificación (s^2 == lambda): {s**2}")


# ========================================
# PUNTO #4: Rango numérico con matrices aleatorias
# ========================================
print("\n--- [PUNTO 4] Rango Numérico (Matrices Aleatorias) ---")
np.random.seed(42)
A_rand = np.random.rand(8, 4) @ np.random.rand(4, 6)
_, s_rand, _ = np.linalg.svd(A_rand)

np.set_printoptions(formatter={"float_kind": "{:10.4e}".format})
print(f"Valores singulares de la matriz aleatoria:\n{s_rand}")
np.set_printoptions()

numerical_rank = np.linalg.matrix_rank(A_rand)
print(f"Rango numérico de la matriz aleatoria: {numerical_rank}")


# ========================================
# PUNTO #8: Factorización LU con Pivoteo Parcial
# ========================================
print("\n--- [PUNTO 8] Factorización LU con Pivoteo (PA = LU) ---")


def lu_with_pivoting(A):
  n = A.shape[0]
  L = np.eye(n)
  U = A.copy()
  P = np.eye(n)

  for k in range(n - 1):
    max_idx = np.argmax(np.abs(U[k:, k])) + k

    if max_idx != k:
      U[[k, max_idx], :] = U[[max_idx, k], :]
      P[[k, max_idx], :] = P[[max_idx, k], :]
      if k > 0:
        L[[k, max_idx], :k] = L[[max_idx, k], :k]

    for i in range(k + 1, n):
      L[i, k] = U[i, k] / U[k, k]
      U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]

  return P, L, U


A_lu = np.array([[2, 1, 1], [4, 3, 3], [8, 7, 9]], dtype=float)
P, L, U = lu_with_pivoting(A_lu)

print(f"Matriz Original A:\n{A_lu}")
print(f"Matriz de Permutación (P):\n{P}")
print(f"Matriz Triangular Inferior (L):\n{L}")
print(f"Matriz Triangular Superior (U):\n{U}")

is_correct = np.allclose(P @ A_lu, L @ U)
print(f"Verificación de que P * A == L * U: {is_correct}")