
# Numerical Stability Analysis of Barotropic and Baroclinic Fluid Instabilities

A computational fluid dynamics (CFD) suite implementing generalized eigenvalue problem solvers, finite difference discretizations, and data-driven modal analysis techniques to study the linear stability of parallel shear flows. This work was conducted during the **Twoples Mentorship Programme (Spring 2025)** under the mentorship of Dr. Mansi Singh (KU Eichstätt-Ingolstadt).

---

## 🔬 Mathematical & Physical Framework

### 1. Barotropic Instability & The Rayleigh Equation
Starting from the 2D incompressible Euler equations linearized around a parallel shear flow $U = (U(y), 0)$, we eliminate pressure by taking the curl to yield the linearized vorticity equation:

$$\left( \frac{\partial}{\partial t} + U \frac{\partial}{\partial x} \right) \nabla^2 \psi - \frac{d^2 U}{dy^2} \frac{\partial \psi}{\partial x} = 0$$

Applying the normal mode ansatz $\psi(x,y,t) = \hat{\psi}(y)e^{i(kx - \omega t)}$, where $c = \frac{\omega}{k}$ represents the complex phase speed, we isolate the governing **Rayleigh Equation**:

$$(U - c) \left( \frac{d^2 \hat{\psi}}{dy^2} - k^2 \hat{\psi} \right) - \frac{d^2 U}{dy^2} \hat{\psi} = 0$$

The system becomes unstable if there exists an eigenvalue where $\text{Im}(c) > 0$. According to **Rayleigh's Inflection Point Theorem**, a necessary condition for inviscid instability is the presence of an inflection point $U''(y) = 0$ somewhere in the domain.

### 2. Baroclinic Instability & The Eady Problem
The Eady problem targets baroclinic growth within a stratified, uniformly sheared fluid on an $f$-plane ($\beta=0$) bounded by rigid horizontal surfaces mimicking the atmosphere/ocean. The interior potential vorticity dynamics are governed by:

$$( \Lambda z - c ) \left[ \frac{\partial^2 \tilde{\psi}}{\partial y^2} + \frac{H^2}{L_d^2} \frac{\partial^2 \tilde{\psi}}{\partial z^2} \right] = 0$$

Subject to vertical velocity constraints ($w=0$) at $z=0, H$, non-trivial solutions satisfy the complex dispersion relation:

$$c^2 - Uc + U^2 \left( \mu^{-1}\coth\mu - \mu^{-2} \right) = 0$$

Where $\mu$ represents the scaled horizontal wavenumber. An instability manifests strictly below the short-wave cutoff scale $\mu < \mu_c \approx 2.399$.

---

## 💻 Numerical Implementation & Discretization

### Central Finite Difference Discretization
To simulate general profiles where analytical approaches fail, the 1D spatial domain $y \in [-1, 1]$ is discretized into $N$ grid points with space step $\Delta y$. Second-order spatial derivatives are mapped via a 3-point central finite difference stencil:

$$\frac{d^2\hat{\psi}}{dy^2} \approx \frac{\hat{\psi}_{i+1} - 2\hat{\psi}_i + \hat{\psi}_{i-1}}{(\Delta y)^2}$$

Enforcing the Dirichlet boundaries $\hat{\psi}(-1) = \hat{\psi}(1) = 0$ onto the interior grid points transforms the Rayleigh equation into a **Sparse Tridiagonal Generalized Eigenvalue Problem**:

$$\mathbf{A}\hat{\psi} = c\mathbf{B}\hat{\psi}$$

Where the entries of the non-constant matrix $\mathbf{A}$ and constant matrix $\mathbf{B}$ are configured dynamically:

$$a_{i} = -\left(\frac{2(1-y_i^2)}{(\Delta y)^2} + k^2(1-y_i^2) - U''(y_i)\right), \quad b_{i} = \frac{1-y_i^2}{(\Delta y)^2}$$
$$b_{ii} = -\left(\frac{2}{(\Delta y)^2} + k^2\right), \quad b_{i,i\pm1} = \frac{1}{(\Delta y)^2}$$

The code solves this linear algebraic system using `scipy.linalg.eig` to obtain the complete spectrum of discrete phase speeds.

### Data-Driven Feature Extraction
* **Singular Value Decomposition (SVD):** Leveraged to unpack linear state matrices and perform geometric optimal-growth alignment mapping.
* **Dynamic Mode Decomposition (DMD):** Implemented to process spatial snapshots of the evolving unstable flow field, decoupling complex multi-frequency growth rates into dominant, distinct coherent spatial structures.

---

## 📊 Analyzed Base Flow Profiles

The implementation explicitly tests and evaluates four critical velocity profiles:
1. **Parabolic (Plane Poiseuille Flow):** $U(y) = 1 - y^2$. Stable ($U''(y) = -2 \neq 0$).
2. **Gaussian Jet:** $U(y) = e^{-y^2}$. Unstable (Inflection points at $y = \pm 1/\sqrt{2}$).
3. **Hyperbolic Tangent (Mixing Layer):** $U(y) = \tanh(y/0.5)$. Unstable (Inflection point at $y = 0$).
4. **Sinusoidal Shear Flow:** $U(y) = \cos(2y)$. Unstable (Periodic inflection points).

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed along with the required libraries:
```bash
pip install -r requirements.txt
```
## Execution
Run the main script to loop through the test cases, execute the eigenvalue solver, apply data-driven structural decomposition, and export visual field results:
```bash
python main.py
```
---

## 📈 Sample Results & Visualization

The pipeline automatically outputs several diagnostics into the figures/ directory:
1. Eigenvalue Spectrums: Isolating unstable growing modes ($\text{Im}(\omega) > 0$).
2. Flow Fields: Iso-contours mapping the perturbation streamfunction $\psi(x,y)$.
3. Velocity Vectors: Quiver vector layouts capturing spatial $(u, v)$ velocity perturbations.


---

### 💡 Quick Tips for Maximum Impact

1. **Populate your `figures/` folder:** Since your research code explicitly generates eigenvalue spectrum graphs, streamfunction contour maps, and $(u,v)$ velocity component fields[cite: 306, 307], make sure to include high-quality images of them in your repository. GitHub profiles look substantially more mature when visual analytics accompany numerical descriptions.
2. **Upload the PDF Report:** Keeping `Twoples.pdf` directly in the root directory acts as a built-in whitepaper for your repository, immediately linking your clean codebase to its academic-grade derivation[cite: 1, 124].
