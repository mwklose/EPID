import pandas as pd
import matplotlib.pyplot as plt

from sierra_plot_alpha import sierra_plot, norm_rd, norm_rr

##########################
# Setup data
# Reading in data
data = pd.read_csv("data_twister.csv")  # .csv read in and managed using pandas

##########################
# Example: Difference
ax = sierra_plot(
    data,
    xvar="RD",
    lcl="RD_LCL",
    ucl="RD_UCL",
    yvar="t",
    treat_labs=["Vaccine", "Placebo"],
    interval_func=norm_rd,
)

# Formatting the axes and labels
ax.legend(loc="lower right")  # Added legend to the lower right corner of the plot
ax.set_yticks([i for i in range(0, 113, 7)])  # Sets the y-axes tick marks

plt.tight_layout()  # Sets spacing of the border of the plot
plt.savefig(
    "sierra_plot_python.png", format="png", dpi=600
)  # Saves the generated figure as .png
plt.show()  # displays the generated image

# ##########################
# # Example: Ratio
ax = sierra_plot(
    data,
    xvar="RR",
    lcl="RR_LCL",
    ucl="RR_UCL",
    yvar="t",
    reference_line=1.0,
    log_scale=True,
    treat_labs=["Vaccine", "Placebo"],
    interval_func=norm_rr,
)

# Formatting the axes and labels
ax.legend(loc="lower right")  # Added legend to the lower right corner of the plot
ax.set_yticks([i for i in range(0, 113, 7)])  # Sets the y-axes tick marks
ax.set_xticks([0.1, 0.25, 1, 5, 10])  # Sets the x-axes tick marks
ax.set_xticklabels(["0.10", "0.25", "1", "5", "10"])

plt.tight_layout()  # Sets spacing of the border of the plot
# plt.savefig("twister_plot_python.png", format='png', dpi=600)  # Saves the generated figure as .png
plt.show()  # displays the generated image
