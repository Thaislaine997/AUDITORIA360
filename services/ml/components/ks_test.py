from scipy.stats import ks_2samp
import numpy as np


def ks_test_by_group(data: np.ndarray, group_labels: np.ndarray):
    unique_groups = np.unique(group_labels)
    results = {}
    for i, g1 in enumerate(unique_groups):
        for g2 in unique_groups[i + 1 :]:
            stat, pval = ks_2samp(data[group_labels == g1], data[group_labels == g2])
            results[f"{g1} vs {g2}"] = {"statistic": stat, "pvalue": pval}
    return results
