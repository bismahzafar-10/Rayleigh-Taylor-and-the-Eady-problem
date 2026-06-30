import numpy as np

def compute_2d_flow_fields(y, dy, k, psi_unstable):
    """
    Extrapolates 1D perturbation eigenfunctions into 2D meshgrid spatial structures.
    """
    x = np.linspace(-5, 5, 100) 
    X, Y = np.meshgrid(x, y)
    
    # Reconstruct perturbation structures
    psi_field = np.real(np.exp(1j * k * X) * psi_unstable[:, np.newaxis])
    u = np.real(1j * k * np.exp(1j * k * X) * psi_unstable[:, np.newaxis])
    v = np.real(np.exp(1j * k * X) * np.gradient(psi_unstable, dy)[:, np.newaxis])
    
    return X, Y, psi_field, u, v
