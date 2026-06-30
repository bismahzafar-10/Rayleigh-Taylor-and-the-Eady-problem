import os
import numpy as np
import matplotlib.pyplot as plt
from src.profiles import get_profile_values
from src.discretization import build_stability_matrices
from src.solvers import solve_generalized_eigenproblem
from src.diagnostics import compute_2d_flow_fields

def main():
    # Setup directories
    os.makedirs('figures', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    print("====================================================")
    print("  TWOPLES FLUID DYNAMICS & STABILITY ANALYSIS PILE  ")
    print("====================================================")
    print("Available Test Cases to Copy/Paste:")
    print(" -> 1 - y**2")
    print(" -> np.exp(-y**2)")
    print(" -> np.tanh(y/0.5)")
    print(" -> np.cos(2*y)\n")

    # Ask user for velocity profile function U(y) matching notebook prompt
    U_str = input("Enter U(y) as a function of y: ").strip()

    # Fixed Grid Initialization Parameters
    N = 200
    y = np.linspace(-1, 1, N)
    dy = y[1] - y[0]
    k = 1  

    try:
        # 1. Evaluate Profile Characteristics
        U_values, d2U_dy2 = get_profile_values(U_str, y, dy)
        
        # 2. Setup Spatial Matrix Arrays
        A, B = build_stability_matrices(N, dy, k, U_values, d2U_dy2)
        
        # 3. Compute System Spectrum
        omega, count, c, max_growth_idx, psi_unstable = solve_generalized_eigenproblem(A, B)
        print(f'\n[SUCCESS] Number of unstable modes extracted: {count}')
        
        # 4. Generate & Save Visualizations
        filename_suffix = U_str.replace("np.", "").replace("*", "").replace("/", "_").replace("-", "m")
        
        # Plot 1: Velocity Profile
        plt.figure(figsize=(6, 4))
        plt.plot(y, U_values, 'b', linewidth=1.5)
        plt.title(f'Velocity Profile U(y) = {U_str}')
        plt.xlabel('y')
        plt.ylabel('U(y)')
        plt.grid(True)
        plt.savefig(f'figures/profile_{filename_suffix}.png', dpi=150)
        plt.close()

        # Plot 2: Eigenvalue Spectrum
        plt.figure(figsize=(6, 4))
        plt.scatter(np.real(omega), np.imag(omega), color='b', label="Eigenvalues")
        if c is not None:
            plt.scatter(np.real(c), np.imag(c), color='r', zorder=5, label="Most Unstable Mode")
        plt.xlabel(r'Re($\omega$)')
        plt.ylabel(r'Im($\omega$)')
        plt.title('Eigenvalue Spectrum')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'figures/spectrum_{filename_suffix}.png', dpi=150)
        plt.close()

        # Unstable Field Perturbation Render Diagnostics
        if psi_unstable is not None:
            # Map structural components to 2D
            X, Y, psi_field, u, v = compute_2d_flow_fields(y, dy, k, psi_unstable)
            
            # Plot 3: Most Unstable Eigenmode 
            plt.figure(figsize=(6, 4))
            plt.plot(y, psi_unstable, 'r', linewidth=1.5)
            plt.title(r'Most Unstable Eigenmode $\hat{\psi}(y)$')
            plt.xlabel('y')
            plt.ylabel(r'$\hat{\psi}(y)$')
            plt.grid(True)
            plt.savefig(f'figures/eigenmode_{filename_suffix}.png', dpi=150)
            plt.close()

            # Plot 4: Flow Field Contours
            plt.figure(figsize=(6, 4))
            plt.contourf(X, Y, psi_field, cmap='coolwarm', levels=50)
            plt.colorbar(label="Streamfunction perturbation")
            plt.title('Flow Field (Streamfunction Contours)')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig(f'figures/flow_field_{filename_suffix}.png', dpi=150)
            plt.close()

            # Plot 5: Quiver Plots
            plt.figure(figsize=(6, 4))
            plt.quiver(X, Y, u, v, scale=5, color='black')
            plt.title('Velocity Field (u-v Components)')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig(f'figures/velocity_quiver_{filename_suffix}.png', dpi=150)
            plt.close()
            
            print(f"[EXPORT] Diagnostic diagnostics saved to /figures folder successfully.")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to execute solver configuration: {e}")

if __name__ == '__main__':
    main()
