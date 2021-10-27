import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
from scipy.stats import norm

STEPS = 10000


def make_data(m1: float = 1, v1: float = 1, m2: float = 1, v2: float = 1):
    norm_1 = np.random.normal(m1, v1, STEPS)
    norm_2 = np.random.normal(m2, v2, STEPS)
    df = pd.DataFrame()

    df["norm_1_1"] = np.sort(norm_1)
    df["norm_2_1"] = np.sort(norm_2)

    df_div = pd.DataFrame()

    div = norm_2 / norm_1
    div = np.sort(div)

    times = norm_2 * norm_1
    times = np.sort(times)

    df_div["div"] = div
    df_div["times"] = times

    return df, df_div


plt.style.use("ggplot")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)


df_dist, df_div = make_data(5, 1, 15, 2)


ax1.hist(
    df_dist["norm_1_1"],
    bins=STEPS // 50,
    label=f"Mean={df_dist['norm_1_1'].mean(): 2.2f}, SD={df_dist['norm_1_1'].std(): 2.2f} ({df_dist['norm_1_1'].quantile(0.05): 2.2f}, {df_dist['norm_1_1'].quantile(0.95): 2.2f})",
)
ax2.hist(
    df_dist["norm_2_1"],
    bins=STEPS // 50,
    label=f"Mean={df_dist['norm_2_1'].mean(): 2.2f}, SD={df_dist['norm_2_1'].std(): 2.2f} ({df_dist['norm_2_1'].quantile(0.05): 2.2f}, {df_dist['norm_2_1'].quantile(0.95): 2.2f})",
)
ax3.hist(
    df_div["div"],
    bins=STEPS // 50,
    label=f"Mean={df_div['div'].mean(): 2.2f}, SD={df_div['div'].std(): 2.2f} ({df_div['div'].quantile(0.05): 2.2f}, {df_div['div'].quantile(0.5): 2.2f}, {df_div['div'].quantile(0.95): 2.2f})",
)
ax4.hist(
    df_div["times"],
    bins=STEPS // 50,
    label=f"Mean={df_div['times'].mean(): 2.2f}, SD={df_div['times'].std(): 2.2f} ({df_div['times'].quantile(0.05): 2.2f}, {df_div['times'].quantile(0.5): 2.2f}, {df_div['times'].quantile(0.95): 2.2f})",
)


for ax in (ax1, ax2, ax3, ax4):
    ax.legend(loc="best")
plt.show()
