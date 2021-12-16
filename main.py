import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from function import find_extrema, plot_window, find_patterns


if __name__ == '__main__':

    data = pd.read_csv('PFE.csv', ',')
    #data.set_index('Date', inplace=True)

    ######################################################
    # Smoothing the Noise and Find the Minama and Maxima #
    ######################################################

    extrema, prices, smooth_extrema, smooth_prices = find_extrema(data['Close'], bw=[1.5])

    #plot_window(prices, extrema, smooth_prices, smooth_extrema, ax=None)

    ##########################
    # Pattern Identification #
    ##########################

    patterns = find_patterns(extrema)

    for name, pattern_periods in patterns.items():
        print(f"{name}: {len(pattern_periods)} occurences")

    for name, pattern_periods in patterns.items():

        print(name)

        rows = int(np.ceil(len(pattern_periods)/2))
        f, axes = plt.subplots(rows, 2, figsize=(20, 5*rows))
        axes = axes.flatten()

        i = 0
        for start, end in pattern_periods:
            s = prices.index[start-1]
            e = prices.index[end+1]

            plot_window(prices[s:e], extrema.loc[s:e],
                        smooth_prices[s:e],
                        smooth_extrema.loc[s:e], ax=axes[i])
            i+=1
        plt.show()