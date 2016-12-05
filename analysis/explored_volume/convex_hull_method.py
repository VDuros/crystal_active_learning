import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

analysis_path = os.path.join(HERE_PATH, '..')
sys.path.append(analysis_path)

import json
import random
import numpy as np

from utils.csv_helpers import read_data
from utils.plot_helpers import save_and_close_figure

from tools import N_INIT_POINTS
from tools import CRYSTAL_CLASS

from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay


import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


# design figure
fontsize = 22
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
matplotlib.rcParams.update({'font.size': fontsize})


def compute_volume_convex_hull(filename, test_range=range(0, 101, 10)):

    X, y = read_data(filename)

    scores = []
    for t in test_range:
        ind = N_INIT_POINTS - 1 + t

        X_train = X[0:ind]
        y_train = y[0:ind]

        points = X_train[y_train == CRYSTAL_CLASS, :]
        hull = ConvexHull(points)
        scores.append(hull.volume)

    return test_range, scores


if __name__ == '__main__':

    import filetools
    PLOT_FOLDER = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(PLOT_FOLDER)

    from tools import FILENAMES

    fig = plt.figure(figsize=(12, 8))
    for xp_name, filename in FILENAMES.items():
        test_range, volumes = compute_volume_convex_hull(filename)
        plt.plot(test_range, volumes)

    plt.legend(FILENAMES.keys(), fontsize=fontsize, loc=2)
    plt.xlim([0, 100])
    # plt.ylim([0.5, 1])
    plt.xlabel('Number of experiments', fontsize=fontsize)
    plt.ylabel('Volume of convex hull', fontsize=fontsize)

    plot_filename = os.path.join(PLOT_FOLDER, 'volume_convex_hull')
    save_and_close_figure(fig, plot_filename, exts=['.png'])
