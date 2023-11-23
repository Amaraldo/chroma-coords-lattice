# chroma-coords-lattice

`chroma-coords-lattice` is a Python script for generating a user-tunable number of equidistant chromaticity coordinates and saving them to a CSV file. The primary use case is for passing the values to an RGB light panel should you want to profile the colour response of a camera/film stock.

## How to Use
1. **Install dependencies** - This script requires matplotlib, numpy, and colour-science.
2. **Input light panel primaries** - Input the chromaticity coordinates for a given light panel's RGB primaries.
3. **Set CSV output path** - Specify the name and path to where you would like the CSV saved.
4. **Run script and select number of points** - Running the script initialises the matplotlib window. Use the left and right arrow keys to select the number of points.
5. **Save CSV** - Once you are satisfied with the number of points, press the enter/return key to save the CSV and close the window. Exiting the window will not save the CSV.

<img width="868" alt="chroma-coords-lattice" src="https://github.com/Amaraldo/chroma-coords-lattice/assets/51723444/b61b627c-a293-4180-be43-486506b5ead3">
