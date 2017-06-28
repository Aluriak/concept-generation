"""Use matplotlib to draw in 2d the stats in stats/stats CSV file.

Will draw edge reduction function to number of nodes,
and edge reduction function to graph density,
one time for each case (made by powergrasp/powergraph and fullcomress),
then will show the exact same graphs, but with the diff between the two methods.


Accept one CLI argument : the name of the file containing the data.


If you get this error, it's because matplotlib is not up to date:

    AttributeError: module 'matplotlib.cm' has no attribute 'plasma'


"""

import sys
import pandas
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

import methods


DEFAULT_IN_DATA = 'output.csv'
COLORS = [cm.plasma, cm.rainbow]
# COLORS = [cm.seismic, cm.spring, cm.summer]


def plot_multiple_x(xss:iter, ys, xlabels:iter, ylabel):
    # fig = plt.figure()

    # Plot the surface.

    for xs, cmap, xlabel in zip(xss, COLORS, xlabels):
        fig = plt.figure()
        fig.plot(xs, ys)
        ax = fig.gca()
        surf = ax.plot_surface(xs, ys, cmap=cmap,
                               linewidth=10, antialiased=True,
                               ymin=ys.min(), ymax=ys.max())

        # Customize the z axis.
        ax.set_ylim(ys.min(), ys.max())

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        # Add a color bar which maps values to colors.
        # plt.pcolor(xs, ys, zs, vmin=0.2)
        fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


import csv
import pandas as pd

file_to_open = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IN_DATA
print('INFILE:', file_to_open)
df = pd.read_csv(file_to_open, index_col=False)
print(df)

ax = None
for density in (0.4,):
    dfd = df.loc[df['context density'] == density]
    method_fields = (name + ' time' for name in methods.METHOD_NAMES)
    # plt.rcParams['axes.labelsize'] = 20
    for method_field in method_fields:
        ax = dfd.plot(x='context size', y=method_field, ax=ax)
    ax.set_xlabel('context size', fontsize=30)
    ax.set_ylabel('runtime', fontsize=30)
plt.show()
