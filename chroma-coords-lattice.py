import matplotlib.pyplot as plt
from matplotlib.backend_bases import KeyEvent
from matplotlib.patches import Polygon
import numpy as np
import colour

def rbf(dist, r=0.18):
    """Radial basis function for smoother blending."""
    return np.exp(-(dist**2) / (2*r**2))

def linear_to_sRGB(linear):
    """Convert a linear RGB colour to an sRGB colour."""
    a = 0.055
    return np.where(linear <= 0.0031308, linear * 12.92, (1 + a) * np.power(linear, 1 / 2.4) - a)

def generate_chromaticity_diagram_colours(samples=500, alpha=0.9):
    """Generate colours for the chromaticity diagram."""
    ii, jj = np.meshgrid(
        np.linspace(x_min, x_max, samples), np.linspace(y_min, y_max, samples)
    )
    
    refs = [
        {"colour": [0, 0, 1], "point": [0.2, 0], "alpha": 1},
        {"colour": [1, 0, 1], "point": [0.45, 0.1], "alpha": 0.2},
        {"colour": [1, 0, 0], "point": [0.7, 0.25], "alpha": 1},
        {"colour": [0, 1, 1], "point": [0, 0.4], "alpha": 0.2},
        {"colour": [0, 1, 0], "point": [0.1, 0.85], "alpha": 1},
        {"colour": [1, 1, 0], "point": [0.4, 0.6], "alpha": 0.2},
    ]
    
    blended_RGB = np.zeros((samples, samples, 3))
    weights_sum = np.zeros((samples, samples, 1))
    
    for ref in refs:
        dist_from_ref = np.sqrt((ii - ref["point"][0])**2 + (jj - ref["point"][1])**2)
        weight = rbf(dist_from_ref) * ref["alpha"]
        weight = np.expand_dims(weight, axis=-1)
        blended_RGB += weight * ref["colour"]
        weights_sum += weight

    # adjust weights_sum to push values towards white
    max_weight = np.max(weights_sum)
    weights_sum = weights_sum / max_weight

    # blend the result by the adjusted weights
    blended_RGB = blended_RGB / np.clip(weights_sum, 1e-6, None)

    # convert to sRGB and clip 0-1
    blended_RGB = linear_to_sRGB(blended_RGB)
    blended_RGB = np.clip(blended_RGB * alpha + (1 - alpha), 0, 1)
    
    return blended_RGB

def generate_triangular_grid_coordinates(num_grid_points):
    coordinates = []
    # ensure the range of generated coordinates match the chromaticity plot
    max_weight = num_grid_points - 1
    for i in range(num_grid_points):
        for j in range(num_grid_points - i):
            # weight calculation with normalisation
            x = (i * primary_chromaticities['red'][0] + j * primary_chromaticities['green'][0] +
                 (max_weight - i - j) * primary_chromaticities['blue'][0]) / max_weight
            y = (i * primary_chromaticities['red'][1] + j * primary_chromaticities['green'][1] +
                 (max_weight - i - j) * primary_chromaticities['blue'][1]) / max_weight
            coordinates.append((x, y))
    return coordinates

def save_coordinates_to_csv(coordinates, filename):
    with open(filename, 'w', newline='') as csvfile:
        for coord in coordinates:
            csvfile.write(f"{round(coord[0], 4)},{round(coord[1], 4)}\n")

def update_plot(ax, num_grid_points):
    ax.clear()  
    ax.plot(spectral_locus_closed[:, 0], spectral_locus_closed[:, 1], color='black', lw=1) # spectral locus outline

    # clip the diagram colours to spectral locus
    polygon = Polygon(spectral_locus_closed, facecolor='none', edgecolor='none')
    ax.add_patch(polygon)
    image = ax.imshow(
        generate_chromaticity_diagram_colours(),
        interpolation="bilinear",
        extent=(x_min, x_max, y_min, y_max),
        origin='lower'
    )
    image.set_clip_path(polygon)

    # plot triangular coordinates
    coordinates = generate_triangular_grid_coordinates(num_grid_points)
    x, y = zip(*coordinates)
    ax.scatter(x, y, c='black', s=5)

    ax.grid(True, alpha=0.3)

    ax.set_title(f"Total Points: {len(coordinates)}")
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # re-apply limits to ensure they are respected
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.9)

    fig.canvas.draw_idle()

def on_key(event: KeyEvent):
    global num_grid_points
    if event.key == 'left':
        num_grid_points = max(3, num_grid_points - 1)  # prevent from going below 3 points
    elif event.key == 'right':
        num_grid_points += 1
    elif event.key in ['enter', 'return']:
        coordinates = generate_triangular_grid_coordinates(num_grid_points)
        save_coordinates_to_csv(coordinates, savecsv)
        plt.close(fig)
        return
    else:
        return
    update_plot(ax, num_grid_points)
    
# input chromaticity coordinates for the light panel primaries
primary_chromaticities = {
    'red': (0.650, 0.320),
    'green': (0.175, 0.690),
    'blue': (0.150, 0.040)
}

# save CSV file to your chosen path
savecsv = "xycoords.csv"

# create spectral locus
wavelengths = np.linspace(380, 750, 500)
spectral_locus = colour.XYZ_to_xy(colour.wavelength_to_XYZ(wavelengths))
spectral_locus_closed = np.vstack([spectral_locus, spectral_locus[0]])

# determine the bounding box of the spectral locus
x_min, x_max = np.min(spectral_locus[:, 0]), np.max(spectral_locus[:, 0])
y_min, y_max = np.min(spectral_locus[:, 1]), np.max(spectral_locus[:, 1])

# initial setup
num_grid_points = 5
fig, ax = plt.subplots(figsize=(8, 8))

# first update to plot
update_plot(ax, num_grid_points)

# connect the event handler to the figure canvas
fig.canvas.mpl_connect('key_press_event', on_key)

fig.patch.set_alpha(0.8)
ax.set_xlim(0, 0.8)
ax.set_ylim(0, 0.9)
fig.tight_layout()
plt.show()