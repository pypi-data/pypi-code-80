from matplotlib.ticker import AutoMinorLocator, MultipleLocator


def setStandardFrame(
    ax,
    fontsize=17,
    xMajorTD=0,
    xMinorTD=0,
    yMajorTD=0,
    yMinorTD=0,
    xlim=0,
    ylim=0,
    lw=2,
    majorA=0.9,
    minorA=0.7,
):
    # Remove ticks
    ax.yaxis.set_tick_params(which="both", length=0)
    ax.xaxis.set_tick_params(which="both", length=0)

    # Customize domain limit if wanted
    if xlim != 0:
        ax.set_xlim(xlim)
    if ylim != 0:
        ax.set_ylim(ylim)

    # Customize minor and major ticks if wanted
    # Minor = majorTickDistance/minorTickDistance
    if xMajorTD != 0:
        ax.xaxis.set_major_locator(MultipleLocator(xMajorTD))
    if xMinorTD != 0:
        ax.xaxis.set_minor_locator(AutoMinorLocator(xMinorTD))
    if yMajorTD != 0:
        ax.yaxis.set_major_locator(MultipleLocator(yMajorTD))
    if yMinorTD != 0:
        ax.yaxis.set_minor_locator(AutoMinorLocator(yMinorTD))

    # Turn grid on for both major and minor ticks and style minor slightly
    # differently.
    ax.grid(which="major", color="#CCCCCC", linestyle="--", lw=lw, alpha=majorA)
    ax.grid(which="minor", color="#CCCCCC", linestyle=":", lw=lw, alpha=minorA)

    # Remove box around figure
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)


def setLabelsAndTitles(
    ax, title, xlabel, ylabel, tickSize=20, labelSize=20, titleSize=22
):

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(tickSize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(tickSize)

    ax.set_xlabel(xlabel, fontsize=labelSize)
    ax.set_ylabel(ylabel, fontsize=labelSize)
    ax.set_title(title, fontsize=titleSize)


def setLegend(ax, loc=0, lrLoc=1.05, udLoc=1, size=16):
    if loc == 0:
        ax.legend(bbox_to_anchor=(lrLoc, udLoc), prop={"size": size})
    else:
        ax.legend(loc=loc, prop={"size": size})
