# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from utils.data_operations import custom_sort
from django.conf import settings

unfavorable_gain_ppties = settings.UNFAVORABLE_GAIN_PPTIES
affinity_ppties = settings.AFFINITY_PPTIES

matplotlib.use('Agg') # important coz plt is not thread safe, thus causing infinite loops
sns.set_context("paper", font_scale=2.5)

def get_bbs_boxPlot(df, x_ppty, y_ppty, series, x_lim=29.5, y_lim=None):
    df[x_ppty] = df[x_ppty].apply(custom_sort)
    df = df.sort_values(by=x_ppty)
    df = df.reset_index(drop=True)
    
    if y_ppty in affinity_ppties: # for EC50 when too high
        y_lim = 500
    
    plt.rcParams["figure.figsize"] = [16, 6]
    fig = sns.boxplot(x=x_ppty, y=y_ppty, data=df, color='#3e931f')
    fig.set(xlim=(-0.5, x_lim))
    fig.set(ylim=(0, y_lim))
    plt.xticks(rotation=60)

    counts = df[x_ppty].value_counts().reset_index()
    counts.columns = [x_ppty, 'Count']
    counts = counts.sort_values(by=x_ppty)
    n_bbs = len(counts)
    if y_ppty == 'HLM':
        fig.axhline(y=300, color='#33931f', linestyle='--', linewidth=1)
        fig.fill_between(x=[-1,n_bbs], y1=0, y2=300, color='#7edf5e', alpha=0.3)
    elif y_ppty == 'MDR1_efflux':
        fig.axhline(y=10, color='#33931f', linestyle='--', linewidth=1)
        fig.fill_between(x=[-1,n_bbs], y1=0, y2=10, color='#7edf5e', alpha=0.3)
    elif y_ppty == 'MDR1_PappAB':
        fig.axhline(y=10, color='#33931f', linestyle='--', linewidth=1)
        fig.fill_between(x=[-1,n_bbs], y1=10, y2=35, color='#7edf5e', alpha=0.3)
    elif y_ppty == 'sol_FaSSIF':
        fig.axhline(y=100, color='#33931f', linestyle='--', linewidth=1)
        fig.fill_between(x=[-1,n_bbs], y1=100, y2=900, color='#7edf5e', alpha=0.3)
    elif y_ppty == 'CYP_testo':
        fig.axhline(y=4, color='#33931f', linestyle='--', linewidth=1)
        fig.fill_between(x=[-1,n_bbs], y1=4, y2=50, color='#7edf5e', alpha=0.3)
    elif y_ppty == 'PXR_EC50':
        fig.axhline(y=4, color='#33931f', linestyle='--', linewidth=1)
        fig.fill_between(x=[-1,n_bbs], y1=4, y2=30, color='#7edf5e', alpha=0.3)

    for i, count in enumerate(counts['Count']):
        y_position = df[df[x_ppty] == counts.iloc[i][x_ppty]][y_ppty].max() + 0.5
        
        # Ensure the annotation stays within the y-axis limit
        #TODO: add y limit as input
        if y_ppty in affinity_ppties:
            if (y_position > y_lim):
                y_position = y_lim - 0.5  # Adjust to fit within the plot
        
            fig.text(i, y_position, str(count), ha='center', va='bottom', fontsize=12, color='#33931f')
        else:
            fig.text(i, df[df[x_ppty] == counts.iloc[i][x_ppty]][y_ppty].max() + 0.5, str(count), ha='center', va='bottom', fontsize=12, color='#33931f')

    p = fig.get_figure()
    p.savefig("media/plots/boxplot_"+series+".svg", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

    return None

def get_duo_swarmPlot(df, y_ppty, bb_id, bb_duo_tag):
    #TODO: add limit on displayed combos (at least n=3) to remove singletons which clutter the plot
    bb_tag = bb_id[0]
    plt.figure(figsize=(4, 5))
    fig = sns.swarmplot(data=df, x=bb_tag+'_id', y=y_ppty, hue=bb_duo_tag+"_id", s=15)
    fig.set_xlabel('')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=16, markerscale=1, ncol=1)
    p = fig.get_figure()
    p.savefig("media/plots/swarmplot_duo_"+bb_duo_tag+".svg", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return None

def plot_mmps_ppty_relPlot(df, bb_tag, ppty):
    palette = ['#541471', '#D90373']
    fig = sns.relplot(x="combo", y=ppty, hue=bb_tag, data=df, height=6, aspect=16/8,s=125,  palette=palette)
    if ppty == 'EC50_main': #TODO: add parm so user can change ylim
        plt.ylim(0, 400)
        plt.ylabel(r'IC$_{50}$ (nM)') #TODO: add IC50 to proj setting for ec50_main
    plt.xticks(rotation=75)
    fig.savefig("media/plots/relplot.svg", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_mmps_pptyFold_barPlot(df, ppty, property_bb1_id, property_bb2_id):
    if ppty in unfavorable_gain_ppties:
        df['Fold_Change'] = (df[property_bb1_id] / df[property_bb2_id]).round(2)
    else:
        df['Fold_Change'] = (df[property_bb2_id] / df[property_bb1_id]).round(2)
    df['Fold_Change'] = df['Fold_Change'].replace([np.inf, -np.inf], np.nan).fillna(1)  # Replace inf/-inf with 1
    df['Fold_Change_Norm'] = df['Fold_Change'].apply(lambda x: np.log2(x + 1e-9)).round(2)

    sns.set_style("white")
    plt.figure(figsize=(16,6))
    plt.bar(df['combo'], df['Fold_Change_Norm'], color=df['Fold_Change_Norm'].apply(lambda x: '#33931f' if x > 0 else '#ff3300'))

    plt.axhline(y=0, color='grey', linewidth=0.8)
    plt.ylabel('Normalized Fold Change')
    plt.xlabel('combo')
    plt.xticks(rotation=75)

    # Save the figure using plt.savefig
    plt.savefig("media/plots/barplot.svg", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()