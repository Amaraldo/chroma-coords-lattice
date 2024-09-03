import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import KeyEvent
from matplotlib.patches import Polygon
import colour

# replace these chromaticity coordinates with the
# chromaticities of the LEDs of your RGB light panel
xy_primaries = {
    'red': (0.688126, 0.311812),
    'green': (0.169687, 0.728162),
    'blue': (0.148101, 0.033792)
}

# save CSV file to your chosen path
xycsv = "xycoords.csv"

def chromaticity_colours():
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    ii, jj = np.meshgrid(x, y)

    params = [
        {"colour": [1, 0, 0], "pos": [0.9, 0.3]},  # red
        {"colour": [0, 1, 0], "pos": [0.1, 0.9]},  # green
        {"colour": [0, 0, 1], "pos": [0.2, 0.1]},  # blue
    ]

    blended = np.zeros((100, 100, 3))
    total = np.zeros((100, 100, 1))

    for param in params:
        dx = ii - param["pos"][0]
        dy = jj - param["pos"][1]
        sq_dist = dx**2 + dy**2

        gaussian_rbf = np.exp(-sq_dist / (2 * 0.3**2))
        weight = gaussian_rbf[..., np.newaxis]

        # accumulate weighted colour and total weight
        blended += weight * np.array(param["colour"])
        total += weight

    return np.power(blended / total, 1/2.2)

def barycentric_lattice(n_pts):
    coordinates = []
    
    rx, ry = xy_primaries['red']
    gx, gy = xy_primaries['green']
    bx, by = xy_primaries['blue']
    
    for i in range(n_pts):
        for j in range(n_pts - i):
            k = n_pts - 1 - i - j

            x = (i * rx + j * gx + k * bx) / (n_pts - 1)
            y = (i * ry + j * gy + k * by) / (n_pts - 1)
            
            coordinates.append((x, y))
    
    return coordinates

def save_coords(coords, name):
    with open(name, 'w', newline='') as csvfile:
        for xy in coords:
            csvfile.write(f"{xy[0]:.4f},{xy[1]:.4f}\n")

def update_plot(ax, n_pts):
    ax.clear()  

    polygon = Polygon(
    spectral_locus,
    facecolor='none',
    edgecolor='black',
    linewidth=1
    )
    ax.add_patch(polygon)
    
    image = ax.imshow(
    chromaticity_colours(),
    interpolation="bilinear",
    extent=(0, 0.8, 0, 0.9),
    origin='lower',
    alpha=0.7
    )
    image.set_clip_path(polygon)

    x, y = zip(*barycentric_lattice(n_pts))
    ax.scatter(x, y, c='black', s=3)
    ax.grid(True, alpha=0.25, linewidth=0.5)
    ax.set_title(f"Total Points: {len(barycentric_lattice(n_pts))}")
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # re-apply limits to ensure they are respected
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.9)

    fig.canvas.draw_idle()

def on_key(event: KeyEvent):
    global n_pts
    if event.key == 'left':
        n_pts = max(3, n_pts - 1)  # prevent from going below 3 points
    elif event.key == 'right':
        n_pts += 1
    elif event.key in ['enter', 'return']:
        xycoords = barycentric_lattice(n_pts)
        save_coords(xycoords, xycsv)
        plt.close(fig)
        return
    else:
        return
    update_plot(ax, n_pts)

wavelengths = np.linspace(380, 750, 500)
spectral_locus = colour.XYZ_to_xy(colour.wavelength_to_XYZ(wavelengths))
spectral_locus = np.vstack([spectral_locus, spectral_locus[0]])

# initial setup
fig, ax = plt.subplots(figsize=(7, 8))
n_pts = 5
update_plot(ax, n_pts)

ax.set_facecolor('#999999')
fig.patch.set_facecolor('#d7d6c6')
fig.canvas.mpl_connect('key_press_event', on_key)
fig.patch.set_alpha(0.8)
ax.set_xlim(0, 0.8)
ax.set_ylim(0, 0.9)
fig.tight_layout()
plt.show()
