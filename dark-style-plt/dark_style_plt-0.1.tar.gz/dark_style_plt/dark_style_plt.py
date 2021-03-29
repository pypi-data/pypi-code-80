
import matplotlib.pyplot as plt

def dark_style():
    axis = '#34383F'
    figure = '#34383F'
    text = '#DFDFE0'
    title = '#DFDFE0'
    label = '#DFDFE0'
    ytick = '#DFDFE0'
    xtick = '#DFDFE0'
    edge = '#DFDFE0'

    plt.style.use('seaborn')
    plt.rcParams.update({'axes.facecolor': axis,
                     'figure.facecolor': figure,
                     'text.color': text,
                     'axes.titlecolor': title,
                     'axes.labelcolor': label,
                     'ytick.color': ytick,
                     'xtick.color': xtick,
                     'axes.edgecolor': edge,
                     'axes.grid': True,
                     'grid.linewidth': 0.20,
                     'axes.linewidth': 0.40,
                     'axes.titlesize': 16,
                     'figure.figsize': (7,4)})