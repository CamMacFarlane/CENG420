import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# tunable parameter
sector_count = 8;

# init sector list
sectors = [list() for x in range(0, sector_count)]

# define step size
angle_step =(2*np.pi)/sector_count;
angle_sum = 0

# generate angle ranges for each sector
for i in range(0, sector_count):
    sectors[i] = [angle_sum, angle_sum + angle_step]
    angle_sum += angle_step

# unused
x = list()
y = list()

for i in range(0, sector_count):
    x.append(np.cos(sectors[i][1]))
    y.append(np.sin(sectors[i][1]))

# Colormapping of threat level
#threat = list()
#for k in range(0, 10):
#    threat.append(k)
#cmap = mpl.cm.Reds
#threat_map = mpl.colors.BoundaryNorm(threat, cmap)


radii = [1 for k in range(0, sector_count)]
theta = np.linspace(0.0, 2*np.pi, sector_count, endpoint=False)

width = list()
for k in range(0, sector_count):
    width.append(sectors[k][1] - sectors[k][0])

ax = plt.subplot(111, projection='polar')
bars = ax.bar(theta, radii, width=width, bottom=0.0, fill=False)

plt.show()
