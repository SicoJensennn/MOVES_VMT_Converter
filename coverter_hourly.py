"""
author: shuying.zhao@utah.edu
date: 10-24-2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def hourly_data(vtype, AADVMT, year):
    # calculate ajusted daily VMT
    default_ref = pd.read_csv('/uufs/chpc.utah.edu/common/home/u1474799/szhao/RoadSalt/AADVMT/MOVES_converter/default_factors_nofdays.csv', index_col=0)
    certain_type_df = default_ref.loc[default_ref['HPMSVTypeID']==vtype]
    certain_type_df = certain_type_df.sort_values('monthID')
    ty_mon_factors = certain_type_df['MOVES3 Default Monthly Adjustment Factor']  
    certain_type_df['day VMT'] = ty_mon_factors * AADVMT

    # apply hourly adjustor
    hour_dic = {'weekday':[], 'weekend':[]}
    hourf = pd.read_csv('/uufs/chpc.utah.edu/common/home/u1474799/szhao/RoadSalt/AADVMT/MOVES_converter/hour_fraction.csv', index_col = 0)

    for i in range(1, 13):  # i is month
        for k in range(1, 25):  # hour
            each_h_frac_wnd = hourf[(hourf.index == vtype) & (hourf.dayID == 2) &(hourf['hourID'] == k)]['hourVMTFraction'].values[0]
            each_h_frac_wee = hourf[(hourf.index == vtype) & (hourf.dayID == 5) &(hourf['hourID'] == k)]['hourVMTFraction'].values[0]
            hour_VMT_wnd = each_h_frac_wnd * certain_type_df[certain_type_df.monthID == i]['day VMT'].values[0]
            hour_VMT_wee = each_h_frac_wee * certain_type_df[certain_type_df.monthID == i]['day VMT'].values[0]
            hour_dic['weekend'].append(hour_VMT_wnd)
            hour_dic['weekday'].append(hour_VMT_wee)
    print(f'{year} hourly VMT has been calculated!')
    # (weekday, weekend), each with lenth of 288 = 12 * 24
    return hour_dic

def vis_hour_trend(dic):
    weekend = dic['weekend']
    week = dic['weekday']
    fig, ax = plt.subplots(1,3, figsize = (15,6), dpi = 300, gridspec_kw={'width_ratios': [3, 3, 0.2]})
    cmap = plt.get_cmap('tab20b')
    for i in range(1,13):
        ax[0].plot(np.arange(0,24), week[(i-1)*24:i*24], color = cmap(i/12), label = f'month {i}')
        ax[1].plot(np.arange(0,24), weekend[(i-1)*24:i*24], color = cmap(i/12), label = f'month {i}')
    ax[0].set_xlabel('Hour')
    ax[0].set_ylabel('VMT')
    ax[0].set_xticks(np.arange(0,24,2))
    ax[0].set_title('Hourly VMT on weekdays')
    ax[1].set_xlabel('Hour')
    ax[1].set_ylabel('VMT')
    ax[1].set_xticks(np.arange(0,24,2))
    ax[1].set_title('Hourly VMT on weekends')
    ax[2].axis('off')
    # Place the legend in the third axis
    ax[2].legend(*ax[0].get_legend_handles_labels(), frameon=False, loc='center')
    # plt.legend(frameon = False)
    plt.tight_layout()
    plt.show()



# # Define values here, input (vtype, y_scale, AADVMT, year)
# hour_VMT_25 = hourly_data(25, 1, 20000, 2017)
# vis_hour_trend(hour_VMT_25)
# latch_data = pd.read_csv('../data/latch_2017_base.csv')