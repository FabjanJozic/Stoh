import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

L = 256

filename = f"T_x_Cv_M_{L}x{L}.dat"
T_range = (1.00, 1.20)
nu = 0.7 # kriticni eksponent za najbolji fit
T_KT_val = np.linspace(0.86, 0.92, 300) # potencijalne vrijednost T_KT

T, x_vec = np.loadtxt(filename, usecols=(0, 2), unpack=True, comments="#")

mask = (T >= T_range[0]) & (T <= T_range[1]) # odabir temperatura
T_fit = T[mask]
chi_fit = x_vec[mask]
ln_chi = np.log(chi_fit)

def ln_chi_fit(eps_inv, ln_A, b): #funkcija za fit: ln(χ) = ln(A) + b / ε^ν
    return ln_A + b * eps_inv

best_std = np.inf
best_fit = {}

for T_KT in T_KT_val: # petlja za fit
    epsilon = (T_fit - T_KT) / T_KT
    if np.any(epsilon <= 0):  # valjano samo za T > T_KT
        continue
    eps_inv_nu = epsilon ** (-nu)
    
    try:
        p_opt, p_cov = curve_fit(ln_chi_fit, eps_inv_nu, ln_chi)
        ln_A, b = p_opt
        p_err = np.sqrt(np.diag(p_cov))  # standardna devijacija
        residuals = ln_chi - ln_chi_fit(eps_inv_nu, *p_opt)
        std_res = np.std(residuals)
        
        if std_res < best_std:
            best_std = std_res
            best_fit = {
                "T_KT": T_KT,
                "ln_A": ln_A,
                "b": b,
                "A": np.exp(ln_A),
                "σ_ln_A": p_err[0],
                "σ_b": p_err[1],
                "std_residual": std_res,
                "fit_x": eps_inv_nu,
                "fit_y": ln_chi_fit(eps_inv_nu, *p_opt),
                "ln_chi": ln_chi
            }
    except Exception:
        continue

# ispis najboljih parametara
output = f"best_fit_results_{L}x{L}_vec.dat"

with open(output, "w", encoding="utf-8") as f:
    f.write("Best KT Fit Results:\n")
    f.write(f"T_KT        = {best_fit['T_KT']:.6f}\n")
    f.write(f"ln(A)       = {best_fit['ln_A']:.6f} ± {best_fit['σ_ln_A']:.6f}\n")
    f.write(f"A           = {best_fit['A']:.6f}\n")
    f.write(f"b           = {best_fit['b']:.6f} ± {best_fit['σ_b']:.6f}\n")
    f.write(f"Residual σ  = {best_fit['std_residual']:.6f}\n")

plt.plot(best_fit["fit_x"], best_fit["ln_chi"], 'o', label='data')
plt.plot(best_fit["fit_x"], best_fit["fit_y"], '-', label='Fit')
plt.xlabel(r"$\epsilon^{-\nu}$")
plt.ylabel(r"$\ln \chi$")
plt.title(f"KT Fit (T_KT = {best_fit['T_KT']:.4f}, ν = {nu}, L = {L})")
plt.grid(lw=0.3, linestyle=':')
plt.legend()
plt.tight_layout()
plt.show()
