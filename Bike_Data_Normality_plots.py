"""
This file manages checks for normality and plotting the relevant subsets.

The bike share data provides 16 features. We are particularly interested in
the peak usage data. As peak usage has no precise definition, we iterate
through the subset conditions, plotting the histograms for each subset.

This stops any mistakes by assuming that peak data is not what we think it
is.
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

from BikeData import BikeData


def sw_normality(data: BikeData) -> None:
    """
    Wrapper for the scipy.stats shapiro wilks test.
    Prints readable version of P value on binned values of the
    total "cnt" column. The bin widths are determined by the length of
    the array.

    Number of bins = no_datapoints**0.5//1

    Args:
        data: BikeData instance.

    Returns:

    """
    seasons = ["Spring", "Summer"]

    print(f"{seasons[data.data['seasons'][0]]} SW P value:{p_val}")


if __name__ == "__main__":
    data = BikeData("hour.csv")
    summer = data.subset(eq={"season": 2})
    spring = data.subset(eq={"season": 1})
    summer_max = np.max(summer.data["cnt"])
    spring_max = np.max(spring.data["cnt"])
    subsets = {"eq":{"workingday": 1, "holiday": 0,}, "geq":