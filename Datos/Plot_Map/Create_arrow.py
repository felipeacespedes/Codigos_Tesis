#%%
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

fig, ax = plt.subplots(figsize=(2, 2.6), dpi=300)
ax.set_aspect("equal")
ax.axis("off")

# Left half (Bottom tip x adjusted from 0.20 to 0.26 to narrow width by 20%)
left_half = Polygon(
    [[0.5, 0.72], [0.26, 0.15], [0.5, 0.28]],
    closed=True,
    facecolor="white",
    edgecolor="black",
    linewidth=2.5,
    joinstyle="round",
)

# Right half (Bottom tip x adjusted from 0.80 to 0.74 to narrow width by 20%)
right_half = Polygon(
    [[0.5, 0.72], [0.5, 0.28], [0.74, 0.15]],
    closed=True,
    facecolor="black",
    edgecolor="black",
    linewidth=2.5,
    joinstyle="round",
)

ax.add_patch(left_half)
ax.add_patch(right_half)

# North label
ax.text(
    0.5,
    0.78,
    "N",
    fontsize=30,
    fontweight="bold",
    ha="center",
    va="bottom",
    color="black",
)

ax.set_xlim(0.1, 0.9)
ax.set_ylim(0.1, 1.0)

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/'
plt.savefig(
    path + "north_arrow.png", transparent=True, bbox_inches="tight", pad_inches=0.05
)
plt.show()
plt.close()
# %%
