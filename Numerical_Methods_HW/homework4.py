import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# PROBLEM 1: FINITE DIFFERENCE METHODS
# ==============================================================================

# [a] Discretize the domain [-3, 3] into N = 10 uniform subintervals
N = 10
h = (3 + 3) / N
# Column vector storing all grid points x_i without a for loop
x_col = np.linspace(-3, 3, N + 1).reshape(-1, 1)
print("--- Problem 1[a]: Column vector x_i (N=10) ---")
print(x_col)


# [c] Function to generate matrix A for the finite difference system
def generate_fd_matrix(N):
    h = 6.0 / N
    A = np.zeros((N + 1, N + 1))

    # Boundary conditions
    A[0, 0] = 1.0
    A[N, N] = 1.0

    # Interior nodes (1 <= i <= N-1)
    for i in range(1, N):
        A[i, i - 1] = -1.0 / (h**2) - 1.0 / h
        A[i, i] = 2.0 / (h**2) + 1.0 / h + 1.0
        A[i, i + 1] = -1.0 / (h**2)

    return A


# [d] & [e] Exact solution y(x) = x^3, RHS f(x) = -6x + 3x^2 + x^3, N = 10
def f_rhs(x):
    return -6.0 * x + 3.0 * (x**2) + (x**3)


def y_exact_func(x):
    return x**3


N_10 = 10
x_10 = np.linspace(-3, 3, N_10 + 1)
A_10 = generate_fd_matrix(N_10)

b_10 = np.zeros(N_10 + 1)
b_10[0] = -27.0  # alpha = (-3)^3
b_10[N_10] = 27.0  # beta = (3)^3
b_10[1:N_10] = f_rhs(x_10[1:N_10])

# Solve the linear system
y_fd_10 = np.linalg.solve(A_10, b_10)

# Plot numerical vs exact solution for N = 10
plt.figure(figsize=(8, 5))
plt.plot(x_10, y_fd_10, "ro-", label="Finite Difference Solution ($N=10$)")
plt.plot(x_10, y_exact_func(x_10), "b--", label="Exact Solution ($y = x^3$)")
plt.xlabel("$x$")
plt.ylabel("$y(x)$")
plt.title("Problem 1[e]: Finite Difference Method vs Exact Solution ($N=10$)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("problem1_fd_N10.png", dpi=300)
plt.show()

# [f] Infinity-norm errors and convergence rates for N = 10, 20, 40, 80, 160
print("\n--- Problem 1[f]: Finite Difference Convergence Table ---")
print(f"{'N':<8} {'||y_h - y||_inf':<22} {'Convergence Rate':<18}")
print("-" * 48)

N_values = [10, 20, 40, 80, 160]
prev_error = None

for N_val in N_values:
    x_grid = np.linspace(-3, 3, N_val + 1)
    A_mat = generate_fd_matrix(N_val)

    b_vec = np.zeros(N_val + 1)
    b_vec[0] = -27.0
    b_vec[N_val] = 27.0
    b_vec[1:N_val] = f_rhs(x_grid[1:N_val])

    y_num = np.linalg.solve(A_mat, b_vec)
    err = np.max(np.abs(y_num - y_exact_func(x_grid)))

    if prev_error is not None:
        rate = np.log2(prev_error / err)
        print(f"{N_val:<8} {err:<22.6e} {rate:<18.4f}")
    else:
        print(f"{N_val:<8} {err:<22.6e} {'-':<18}")
    prev_error = err


# [g] Explore singularly perturbed problem: -0.01 y'' + y' + y = f(x), y(-3)=0, y(3)=0
# Using f(x) = 1 to observe the boundary layer behavior near x = 3
def generate_perturbed_fd_matrix(N, eps=0.01):
    h = 6.0 / N
    A = np.zeros((N + 1, N + 1))
    A[0, 0] = 1.0
    A[N, N] = 1.0
    for i in range(1, N):
        # Using central difference for y'' and backward difference (upwind) for y'
        A[i, i - 1] = -eps / (h**2) - 1.0 / h
        A[i, i] = 2.0 * eps / (h**2) + 1.0 / h + 1.0
        A[i, i + 1] = -eps / (h**2)
    return A


plt.figure(figsize=(8, 5))
for N_val in [10, 40, 160]:
    x_grid = np.linspace(-3, 3, N_val + 1)
    A_pert = generate_perturbed_fd_matrix(N_val, eps=0.01)
    b_pert = np.ones(N_val + 1)
    b_pert[0] = 0.0
    b_pert[N_val] = 0.0
    y_pert = np.linalg.solve(A_pert, b_pert)
    plt.plot(x_grid, y_pert, marker=".", label=f"Upwind FD ($N={N_val}$)")

plt.xlabel("$x$")
plt.ylabel("$y(x)$")
plt.title(r"Problem 1[g]: Singularly Perturbed Problem ($\epsilon = 0.01$, $f(x)=1$)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("problem1_perturbed.png", dpi=300)
plt.show()


# ==============================================================================
# PROBLEM 2: FINITE ELEMENT METHODS (FEM)
# ==============================================================================


# [e] & [f] Build Stiffness (A), Convection (L), Mass (M), and solve FEM system
def build_fem_matrices(N):
    h = 6.0 / N
    n_int = N - 1  # Number of interior nodes

    # Interior Stiffness Matrix A (size (N-1) x (N-1))
    A_int = np.zeros((n_int, n_int))
    # Interior Convection Matrix L with entries L_ij = (\phi_i', \phi_j)
    L_int = np.zeros((n_int, n_int))
    # Interior Mass Matrix M with entries M_ij = (\phi_i, \phi_j)
    M_int = np.zeros((n_int, n_int))

    for i in range(n_int):
        A_int[i, i] = 2.0 / h
        M_int[i, i] = 2.0 * h / 3.0
        if i > 0:
            A_int[i, i - 1] = -1.0 / h
            L_int[i, i - 1] = 0.5
            M_int[i, i - 1] = h / 6.0
        if i < n_int - 1:
            A_int[i, i + 1] = -1.0 / h
            L_int[i, i + 1] = -0.5
            M_int[i, i + 1] = h / 6.0

    return A_int, L_int, M_int


def solve_fem(N, alpha=-27.0, beta=27.0):
    h = 6.0 / N
    x = np.linspace(-3, 3, N + 1)

    A_int, L_int, M_int = build_fem_matrices(N)

    # Note: In weak form \int y'_h \phi_i dx, the matrix acting on coefficients is L_int.T
    K_int = A_int + L_int.T + M_int

    # Assemble right-hand side load vector F_i = \int f(x) \phi_i(x) dx
    # Using 2-point Gauss-Legendre quadrature on each subinterval (exact for polynomials up to degree 3)
    F_int = np.zeros(N - 1)
    gp = np.array([-1.0 / np.sqrt(3.0), 1.0 / np.sqrt(3.0)])

    for idx in range(N - 1):
        i = idx + 1  # Global node index 1 .. N-1

        # Left subinterval [x_{i-1}, x_i]
        xm_L = 0.5 * (x[i - 1] + x[i])
        xq_L = xm_L + 0.5 * h * gp
        phi_L = (xq_L - x[i - 1]) / h
        int_L = 0.5 * h * np.sum(f_rhs(xq_L) * phi_L)

        # Right subinterval [x_i, x_{i+1}]
        xm_R = 0.5 * (x[i] + x[i + 1])
        xq_R = xm_R + 0.5 * h * gp
        phi_R = (x[i + 1] - xq_R) / h
        int_R = 0.5 * h * np.sum(f_rhs(xq_R) * phi_R)

        F_int[idx] = int_L + int_R

    # Adjust RHS for non-homogeneous Dirichlet boundary conditions c_0 = alpha, c_N = beta
    # Contribution from c_0 * \phi_0 on node i = 1: (-1/h - 1/2 + h/6) * alpha
    F_int[0] -= (-1.0 / h - 0.5 + h / 6.0) * alpha
    # Contribution from c_N * \phi_N on node i = N-1: (-1/h + 1/2 + h/6) * beta
    F_int[-1] -= (-1.0 / h + 0.5 + h / 6.0) * beta

    # Solve for interior coefficients
    c_int = np.linalg.solve(K_int, F_int)

    # Combine boundary and interior values
    y_fem = np.zeros(N + 1)
    y_fem[0] = alpha
    y_fem[1:N] = c_int
    y_fem[N] = beta

    return x, y_fem


# Plot FEM vs Exact solution for N = 10
x_fem_10, y_fem_10 = solve_fem(10)

plt.figure(figsize=(8, 5))
plt.plot(x_fem_10, y_fem_10, "go-", label="FEM Solution ($N=10$)")
plt.plot(
    x_fem_10, y_exact_func(x_fem_10), "b--", label="Exact Solution ($y = x^3$)"
)
plt.xlabel("$x$")
plt.ylabel("$y(x)$")
plt.title("Problem 2[f]: Finite Element Method vs Exact Solution ($N=10$)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("problem2_fem_N10.png", dpi=300)
plt.show()

# Infinity-norm errors and convergence rates for FEM (N = 10, 20, 40, 80, 160)
print("\n--- Problem 2[f]: Finite Element Method Convergence Table ---")
print(f"{'N':<8} {'||y_h - y||_inf':<22} {'Convergence Rate':<18}")
print("-" * 48)

prev_error_fem = None
for N_val in N_values:
    x_f, y_f = solve_fem(N_val)
    err_fem = np.max(np.abs(y_f - y_exact_func(x_f)))

    if prev_error_fem is not None:
        rate_fem = np.log2(prev_error_fem / err_fem)
        print(f"{N_val:<8} {err_fem:<22.6e} {rate_fem:<18.4f}")
    else:
        print(f"{N_val:<8} {err_fem:<22.6e} {'-':<18}")
    prev_error_fem = err_fem