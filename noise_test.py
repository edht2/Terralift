import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=5, seed=10)
xpix = 100
pic = [[noise([j/xpix]) for j in range(xpix)]]

plt.imshow(pic, cmap='gray')
plt.show()