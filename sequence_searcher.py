import matplotlib.pyplot as plt
import numpy as np
import re


def find_matches(genome_seq: str, subseq: str) -> dict:
    matches = [m.start() for m in re.finditer('(?=' + subseq + ')', genome_seq)]
    return {pos: genome_seq[pos:pos + len(subseq)] for pos in matches}


def make_line_plot_of_matches(genome_seq: str, matches: dict):
    # # Modified From https://matplotlib.org/stable/gallery/lines_bars_and_markers/timeline.html#sphx-glr-gallery
    # -lines-bars-and-markers-timeline-py

    levels = np.tile([-5, 5, -3, 3, -1, 1],
                     int(np.ceil(len(matches.keys()) / 6)))[:len(matches.keys())]

    fig, ax = plt.subplots(figsize=(8.8, 4), layout='constrained')
    ax.set(title='Target Sequence Locations')

    ax.vlines(matches.keys(), 0, levels, color="tab:red")  # The vertical stems.
    ax.plot(np.array(list(matches.keys())), np.zeros_like(list(matches.keys())), "-o",
            color="k", markerfacecolor="w")  # Baseline and markers on it.

    # annotate lines
    for d, l, r in zip(matches.keys(), levels, matches.values()):
        ax.annotate(r, xy=(d, l),
                    xytext=(-3, np.sign(l) * 3), textcoords="offset points",
                    horizontalalignment="right",
                    verticalalignment="bottom" if l > 0 else "top")

    # remove y-axis and spines
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)
    plt.xlim([0, len(genome_seq)])
    return plt
