import numpy as np

def derivative(f_values, dy, order=1):
    """
    Compute derivatives numerically using central differences matching the original notebook layout.
    """
    df = np.gradient(f_values, dy, edge_order=2)
    if order == 2:
        df = np.gradient(df, dy, edge_order=2)
    return df

def get_profile_values(U_str, y, dy):
    """
    Dynamically evaluates the user profile string and computes its derivatives.
    """
    # Safe evaluation environment for standard mathematical inputs
    safe_dict = {
        'np': np, 'numpy': np, 'pi': np.pi,
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'tanh': np.tanh, 'cosh': np.cosh, 'sinh': np.sinh
    }
    
    # Evaluate the function based on the input string layout
    U_values = eval(U_str, safe_dict, {'y': y})
    
    # Generate numerical derivatives using finite differences
    dU_dy = np.gradient(U_values, dy, edge_order=2)
    d2U_dy2 = np.gradient(dU_dy, dy, edge_order=2)
    
    return U_values, d2U_dy2
