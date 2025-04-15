import numpy as np
import matplotlib.pyplot as plt

def f(x): #funkcija x^2 koja se integrira
    return x**2
def p(x): #funkcija raspodjele vjerojatnosti
    return np.exp(-(x**2)/2)

N = 100000 #moguci broj dogadaja
burn = 0 #pocetni broj koraka koji cemo zanemariti jer najvjerojatnije nisu dobri
delta = 5.0
accept = 0 #broj prihvacenih dogadaja

with open('exp2_Metropolis.txt', 'w') as wr:
    x0 =[] #pocetni polozaji
    for i in range(100):
        x0.append(-10.0+20*np.random.rand())
    I = 0.0
    for j in range(1, int(N+burn+1)):
        for i in range(100):
            xn = x0[i] + np.random.uniform(-delta, delta)
            if np.abs(xn) > 10.0: #rub intervala integracije
                xn = x0[i]
            w = p(xn)/p(x0[i])
            if w >= 1.0:
                I += f(xn)
                x0[i] = xn
                accept += 1
            else:
                if np.random.rand() <= w:
                    I += f(xn)
                    x0[i] = xn
                    accept += 1
        if j > burn and j%100 == 0: #odbacivanje pocetnog broja koraka
            wr.write(f"%7d %6.2f\n" %(j, I))
    wr.close()
print(accept/N)

  
'''
# Metropolis algorithm
def metropolis_sampling(n_samples, x0=0.0, step_size=1.0):
    samples = []
    x = x0
    for _ in range(n_samples):
        x_new = x + np.random.uniform(-step_size, step_size)
        # Reflect at boundaries
        if np.abs(x_new) > 15.0:
            x_new = x  # reject move outside interval

        # Acceptance probability
        accept_ratio = p(x_new) / p(x)
        if np.random.rand() < accept_ratio:
            x = x_new
        samples.append(x)
    return np.array(samples)

# Parameters
n_samples = 100000
burn_in = 1000
step_size = 1.0

# Run sampler
samples = metropolis_sampling(n_samples + burn_in, step_size=step_size)
samples = samples[burn_in:]  # remove burn-in

# Estimate integral using importance sampling
integral_estimate = np.mean(f(samples))
normalization = np.mean(p(samples))  # approximate normalization factor (for completeness)

# For Gaussian with std=1, normalization is sqrt(2*pi), so we scale accordingly
integral_estimate *= np.sqrt(2 * np.pi)

print(f"Estimated integral of x^2 * exp(-x^2/2): {integral_estimate:.4f}")

# Plot the sampled distribution
plt.hist(samples, bins=100, density=True, alpha=0.6, label='Sampled Distribution')
x_vals = np.linspace(-15, 15, 500)
plt.plot(x_vals, p(x_vals) / np.sqrt(2 * np.pi), 'r', label='True Distribution (normalized)')
plt.legend()
plt.title("Metropolis Sampling")
plt.xlabel("x")
plt.ylabel("Density")
plt.show()'''