# chroma-coords-lattice

Python script designed to generate a user-defined number of equidistant chromaticity coordinates and save them to a CSV file. The primary use case is to supply these values to an RGB light panel for profiling the colour response of a camera or film stock.
## How to Use
1. **Install dependencies** - This script requires matplotlib, numpy, and colour-science.
2. **Input light panel primaries** - Input the chromaticity coordinates for a given light panel's RGB primaries.
3. **Set CSV output path** - Specify the name and path to where you would like the CSV saved.
4. **Run script** - Run the script to initiate the matplotlib window. Use the left and right arrow keys to select the number of points you want.
7. **Save CSV** - Once you are satisfied with the number of points, press the enter/return key to save the CSV and close the window. Exiting the window will not save the CSV.

<img width="697" alt="xy" src="https://github.com/user-attachments/assets/db5025e3-4e17-4a74-a6a0-42020011caff">
