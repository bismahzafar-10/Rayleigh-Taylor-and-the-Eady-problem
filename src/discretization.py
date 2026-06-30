import numpy as np

def build_stability_matrices(N, dy, k, U_values, d2U_dy2):
    """
    Discretizes second derivatives via 3-point central finite differences 
    and applies Dirichlet Boundary Conditions to output system matrices A and B.
    """
    # Construct second derivative operator matrix
    D2 = np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1) - 2 * np.eye(N)
    D2 /= dy**2 

    # Enforce rigid boundary criteria (Dirichlet BC)
    D2[0, :] = 0
    D2[-1, :] = 0

    # Frame the Laplacian operator (D2 - k^2*I)
    L_operator = D2 - (k**2) * np.eye(N)
    
    # Assemble general algebraic matrix equations
    A = np.diag(U_values) @ L_operator - np.diag(d2U_dy2)
    B = L_operator
    
    return A, B
