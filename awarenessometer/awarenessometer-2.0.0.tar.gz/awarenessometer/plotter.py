# -*- coding: utf-8 -*-

import gettext
import os
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series

LANGUAGE = os.environ['LANG'].split('.')[0]
LOCALE_PATH = os.path.join(os.path.dirname(__file__), 'locale')
TRANSLATION = gettext.translation('plotter', LOCALE_PATH, languages=[LANGUAGE], fallback=True)
_ = TRANSLATION.gettext


class Plotter:
    @staticmethod
    def distplot(values: List[float], plt_path: str) -> None:
        color = 'dimgrey'
        axes = plt.subplots()[1]
        series = pd.Series(values)
        try:
            series.plot.kde()
        except np.linalg.LinAlgError:
            print(f'No variance in correlations for plot {plt_path}, can not create KDE')
            return
        except ValueError:
            print(f'Not enough values for plot {plt_path} to create KDE')
            return
        line = axes.lines[0]
        line.set_color(color)
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        axes.fill_between(xdata, ydata, color=color, alpha=0.45)
        axes.set_xlabel(_('Correlation'))
        axes.set_ylabel(_('Density'))
        axes.spines['right'].set_color('none')
        axes.spines['top'].set_color('none')
        axes.hist([series], bins=40, alpha=1.0, histtype='bar', color=color, rwidth=0.9)
        for rectangle in axes.patches:
            rectangle.set_height(rectangle.get_height() / len(series))
        plt.tight_layout()
        plt.savefig(plt_path)
        plt.clf()

    @staticmethod
    def reactions_by_artifact_relative(artifacts: List[str],
                                       no_reactions: Dict[str, List[int]],
                                       phase1_artifact_amount: int,
                                       plt_path: str) -> None:
        fig = plt.figure(figsize=((6, 2.3)))  # This changes aspect ratio
        axes = fig.add_subplot(111)

        axes.bar(np.arange(len(artifacts)),
                 no_reactions['bad'],
                 color=('white'),
                 edgecolor='black',
                 width=2 / 3)
        axes.bar(np.arange(len(artifacts)),
                 no_reactions['good'],
                 color=('white'),
                 edgecolor='black',
                 width=2 / 3)
        bar_good_bad = axes.bar(np.arange(len(artifacts)),
                                no_reactions['good_and_bad'],
                                color=('white'),
                                edgecolor='black',
                                width=2 / 3)
        axes.bar(np.arange(len(artifacts)),
                 [-x for x in no_reactions['good_and_bad']],
                 color=('white'),
                 edgecolor='black',
                 width=2 / 3)
        bars = axes.patches
        patterns = ['', '', 'xx', 'xx']
        hatches = [p for p in patterns for i in range(len(artifacts))]
        for bar, hatch in zip(bars, hatches):
            bar.set_hatch(hatch)

        labels = [label.replace('-', '-\n') for label in artifacts]
        plt.xticks(np.arange(len(labels)), labels, rotation=90, fontsize=8)
        axes.set_ylabel(_('ratio of participants with\n'
                          r'positive reaction $\bf{⟵}$ $\bf{⟶}$ negative reaction'))
        y_offset = (1 / (abs(axes.get_ylim()[0]) + axes.get_ylim()[1]) *
                    abs(min(no_reactions['good'])))
        y_label_pos = [-0.12, 0.06 + y_offset]
        axes.yaxis.set_label_coords(*y_label_pos)

        axes.legend(
            [bar_good_bad],
            [_(r'positive $\bf{and}$' '\nnegative reaction')],
            loc='upper left',
            bbox_to_anchor=(0, 1.4)
        )
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        if phase1_artifact_amount > 0:
            axes.annotate(
                _(r'Phase 1 $\bf{⟵}$ $\bf{⟶}$ Phase 2'),
                xy=(phase1_artifact_amount - 0.75 * bars[-1].get_width(), axes.get_ylim()[0]),
                xycoords='data',
                xytext=(phase1_artifact_amount - 0.75 * bars[-1].get_width(), axes.get_ylim()[1]),
                textcoords='data',
                arrowprops=dict(arrowstyle='-'),
                ha='center'
            )
        axes.grid(axis='both', color='lightgray', linestyle='dashed')
        axes.set_axisbelow(True)
        # tight layout interferes with proper legend position
        # for unknown data, the legend MUST be placed outside of the plot
        # plt.tight_layout()
        plt.savefig(plt_path, bbox_inches='tight', pad_inches=0)
        plt.clf()

    # pylint: disable=too-many-locals
    @staticmethod
    def iitsa_kde(iitsas: List[Series],
                  iitsa_iv: Series,
                  iitsa_noiv: Series,
                  plt_path: str,
                  phase: int) -> None:
        group_names = [_('Group A (intervention)'), _(r'Group B ($\neg$ intervention)')]
        colors = ['lightgrey', 'dimgray']
        axes = plt.subplots()[1]
        linear_err = []

        for i, iitsa in enumerate(iitsas):
            try:
                iitsa.plot.kde(bw_method=1.55)
            except np.linalg.LinAlgError:
                print(f'No variance in IITSA of group: `{group_names[i]}`.',
                      'Can not create KDE of this group!')
                linear_err.append(group_names[i])
                continue
            line = axes.lines[i - len(linear_err)]
            line.set_color(colors[i])
            xdata = line.get_xydata()[:, 0]
            ydata = line.get_xydata()[:, 1]
            axes.fill_between(xdata, ydata, color=colors[i], alpha=0.45)

        axes.set_xlim(left=0.0, right=1.0)
        axes.set_ylim(bottom=0.0, top=0.9)
        xlabel = _('Average Individual IT-Security Awareness')
        if phase > 0:
            xlabel = xlabel + _(' on Artifacts of Phase {}').format(phase)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(_('Density'))
        for name in linear_err:
            group_names.remove(name)
        axes.legend(group_names, loc=2, fancybox=True, framealpha=0)
        axes.set_aspect(aspect=0.3)
        axes.spines['right'].set_color('none')
        axes.spines['top'].set_color('none')

        Plotter._overlay_histogram(axes, iitsa_iv, iitsa_noiv, colors)

        plt.savefig(plt_path, bbox_inches='tight', pad_inches=0)
        plt.clf()

    @staticmethod
    def _overlay_histogram(axes: plt.Axes,
                           iitsa_iv: Series,
                           iitsa_noiv: Series,
                           colors: List[str]) -> None:
        axes.hist([iitsa_iv, iitsa_noiv],
                  bins=40,
                  alpha=1.0,
                  histtype='bar',
                  color=colors,
                  rwidth=0.9)
        for i, rectangle in enumerate(axes.patches):
            if i < 40:
                rectangle.set_height(rectangle.get_height() / len(iitsa_iv))
            else:
                rectangle.set_height(rectangle.get_height() / len(iitsa_noiv))
