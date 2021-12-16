import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm

import os.path
from os import path

from function import find_extrema, plot_window, find_patterns


if __name__ == '__main__':

    data = pd.read_csv('testdata.csv', ';')
    data.set_index('Date', inplace=True)

    ######################################################
    # Smoothing the Noise and Find the Minama and Maxima #
    ######################################################

    name_ticker = list(data.columns)
    stat_pattern = pd.DataFrame(columns=['Pattern', 'Count'])

    for ticker in tqdm(name_ticker):
        extrema, prices, smooth_extrema, smooth_prices = find_extrema(data[ticker], bw=[1.5])

    #plot_window(prices, extrema, smooth_prices, smooth_extrema, ax=None)

        ##########################
        # Pattern Identification #
        ##########################

        patterns = find_patterns(extrema)

        result = pd.DataFrame(columns=['Pattern', 'Start_bar', 'End_bar'])

        for name, pattern_periods in patterns.items():
            stat_pattern = stat_pattern.append({'Pattern':name, 'Count':int(len(pattern_periods))}, ignore_index=True)

            rows = int(np.ceil(len(pattern_periods)/2))
            f, axes = plt.subplots(rows, 2, figsize=(20, 5*rows))
            axes = axes.flatten()

            i = 0
            for start, end in pattern_periods:
                result = result.append({'Pattern':name, 'Start_bar':start, 'End_bar':end}, ignore_index=True)
        
                s = prices.index[start-1]
                e = prices.index[end+6]

                plot_window(ticker, name, prices[s:e], extrema.loc[s:e-5],
                            smooth_prices[s:e-5],
                            smooth_extrema.loc[s:e-5], ax=axes[i])
                i+=1
            
            folder = '/Users/Maxou/Documents/Cours/PROGRAMMATION/FINANCE/Algorithmic_Chart_Pattern_Detection/Resultat/'+str(ticker)
            if path.exists(folder) == False:
                os.mkdir(folder)
            
            plt.savefig('/Users/Maxou/Documents/Cours/PROGRAMMATION/FINANCE/Algorithmic_Chart_Pattern_Detection/Resultat/'+str(ticker)+'/'+str(name)+'.png')
            result.to_csv('/Users/Maxou/Documents/Cours/PROGRAMMATION/FINANCE/Algorithmic_Chart_Pattern_Detection/Patterns/Pattern_'+str(ticker)+'.csv')
    
    list_pattern = (np.unique(stat_pattern['Pattern']))
    stat = pd.DataFrame(columns=list_pattern)

    for pat in list_pattern:
        stat[pat] = stat_pattern[stat_pattern['Pattern']==pat].sum()
    
    stat = stat.drop(index='Pattern')

    print(stat)
    print('Done...')

