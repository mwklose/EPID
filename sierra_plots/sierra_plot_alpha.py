########################################################################################################################
# Twister Plots
#
# Paul Zivich (2021/5/19)
########################################################################################################################

# Importing required dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import norm
import seaborn as sns

from typing import Union, Tuple  # Import union, tuple type hinting


def normal_ppf_rd(location: pd.Series, scale: pd.Series, query: float) -> pd.Series:
    # Something up here: maybe has to do with input values?

    n = norm.ppf(location, scale, query)
    return n


##########################
def sierra_plot(
    data,
    xvar,
    lcl,
    ucl,
    yvar,
    xlab="Risk Difference",
    ylab="Days",
    log_scale=False,
    reference_line=0.0,
    treat_labs=("Treatment", "Placebo"),
    treat_labs_top=True,
    treat_labs_spacing="\t\t\t",
):
    """Function to generate a twister plot from input data. Returns matplotlib axes which can have xlims and ylims
    set to the desired levels.

    Parameters
    ----------
    data : pandas DataFrame
        Pandas dataframe with the risk difference, upper and lower confidence limits, and times
    xvar : str
        The variable/column name for the risk difference.
    lcl : str
        The variable/column name for the lower confidence limit of the risk difference.
    ucl : str
        The variable name for the upper confidence limit of the risk difference.
    yvar : str
        The variable name for time.
    xlab : str, optional
        The x-axis label. Defaults to "Risk Difference".
    ylab : str, optional
        The y-axis label. Defaults to "Days".
    treat_labs : list, set, optional
        List of strings containing the names of the treatment groups. Only the first two elements are used in the
        labels. Defaults to 'Favors Treatment' and 'Favors Placebo'.
    treat_labs_top : bool, optional
        Whether to place the `treat_labs` at the top (True) or bottom (False). Defaults to True.
    treat_labs_spacing : str, optional
        Spacing to use between the treatment group names.

    Returns
    -------
    Matplotlib axes object

    Examples
    --------

    Example of plotting functionality

    >>> ax = twister_plot(data, xvar="RD", lcl="RD_LCL", ucl="RD_UCL", yvar="t")
    >>> ax.legend(loc='lower right')  # Added legend to the lower right corner of the plot
    >>> plt.tight_layout()  # Sets spacing of the border of the plot
    >>> plt.show()  # displays the generated image

    """
    max_t = data[yvar].max()  # Extract max y value for the plot

    # Initializing plot
    fig, ax = plt.subplots(figsize=(6, 8))  # fig_size is width by height
    # Place reference line at end
    # Prep data for plotting; p
    df = pd.DataFrame()
    df[yvar] = data[yvar]
    df[xvar] = data[xvar]
    # Get standard deviation of each column
    df["sd"] = (data[ucl] - data[xvar]) / 1.96

    # loop through as many steps as needed

    # # # Functionally not needed, but helps Shaded step function for Risk Difference confidence intervals
    ax.fill_betweenx(
        data[yvar],  # time column (no shift needed here)
        data[ucl],  # upper confidence limit
        data[lcl],  # lower confidence limit
        label="95% CI",  # Sets the label in the legend
        facecolor="k",  # Sets the color of the shaded region (k=black)
        alpha=0.2,  # Sets the transparency of the shaded region
        step="post",
    )

    for a in np.arange(0.05, 0.5, 0.01):
        df[a] = df.apply(
            lambda x: normal_ppf_rd(location=x[xvar], scale=x["sd"], query=a), axis=1
        )
        df[a] = df[a].fillna(0)
        df[1 - a] = df.apply(
            lambda x: normal_ppf_rd(location=x[xvar], scale=x["sd"], query=(1 - a)),
            axis=1,
        )
        df[1 - a] = df[1 - a].fillna(0)
        ax.fill_betweenx(
            df[yvar], df[1 - a], df[a], facecolor="k", alpha=0.02, step="post"
        )

    # Step function for Risk Difference
    ax.step(
        data[xvar],  # Risk Difference column
        data[yvar]
        .shift(-1)
        .ffill(),  # time column (shift is to make sure steps occur at correct t
        # label="RD",  # Sets the label in the legend
        color="k",  # Sets the color of the line (k=black)
        where="post",
    )

    # Draw reference
    ax.vlines(
        reference_line,
        0,
        max_t,
        colors="black",  # Sets color to gray for the reference line
        linestyles="--",  # Sets the reference line as dashed
        label=None,
    )  # drawing dashed reference line at RD=0

    ax2 = ax.twiny()  # Duplicate the x-axis to create a separate label
    ax2.set_xlabel(
        "Favors "
        + treat_labs[0]
        + treat_labs_spacing.expandtabs()
        + "Favors "  # Manually create some custom spacing
        + treat_labs[1],  # Top x-axes label for 'favors'
        fontdict={"size": 10},
    )
    ax2.set_xticks([])  # Removes top x-axes tick marks
    # Option to add the 'favors' label below the first x-axes label
    if not treat_labs_top:
        ax2.xaxis.set_ticks_position("bottom")
        ax2.xaxis.set_label_position("bottom")
        ax2.spines["bottom"].set_position(("outward", 36))

    ax.set_ylim([0, max_t])  # Sets the min and max of the y-axis
    ax.set_ylabel(ylab)  # Sets the y-label
    if log_scale:
        ax.set_xscale("log")
        xlimit = np.max(
            [np.abs(np.log(data[lcl])), np.abs(np.log(data[ucl]))]
        )  # Extract the x-limits to use
        spacing = xlimit * 2 / 20  # Sets a spacing factor. 20 seems to work well enough
        ax.set_xlim(
            [np.exp(-xlimit - spacing), np.exp(xlimit + spacing)]
        )  # Sets the min and max of the x-axis
    else:
        xlimit = np.max(
            [np.abs(data[lcl]), np.abs(data[ucl])]
        )  # Extract the x-limits to use
        spacing = xlimit * 2 / 20  # Sets a spacing factor. 20 seems to work well enough
        ax.set_xlim(
            [-xlimit - spacing, xlimit + spacing]
        )  # Sets the min and max of the x-axis

    ax.set_xlabel(
        xlab,  # Sets the x-axis main label (bottom label)
        fontdict={
            "size": 11,  # "weight": "bold"
        },
    )
    return ax
