import numpy as np
import matplotlib.pyplot as plt

print("Hello World!")
print("Let's start...")

z = np.zeros(10)
print(z)

plt.style.use('seaborn-whitegrid')

x = np.linspace(-4, 4, 1000)
yPar = x ** 2
y2 = 10 / (x ** 2 + 1)
ySin = 5 * np.cos( 2 * x )
fig, ax = plt.subplots()

ax.plot(x, yPar, x, y2, x, ySin)

yParSin = np.maximum(yPar, ySin)
ax.fill_between(x, y2, yParSin, where=y2>yParSin, color='orange', alpha=0.1)
lgnd = ax.legend(['Parabola', 'Hueta', 'Sinus'])

plt.show()