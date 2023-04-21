import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import os
import matplotlib
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)

# Number of trucks in the US in 2021
# From https://www.trucking.org/economics-and-industry-data
N_TRUCKS_2021 = 4.06e6
N_YEARS_TO_RAMP = 10
N_EVS_PER_YEAR = N_TRUCKS_2021 / N_YEARS_TO_RAMP
TESLA_SEMI_BATTERY_MASS = 5 # Tons


def get_top_dir():
    '''
    Gets the path to the top level of the git repo (one level up from the source directory)
        
    Parameters
    ----------
    None

    Returns
    -------
    top_dir (string): Path to the top level of the git repo
        
    NOTE: None
    '''
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    top_dir = os.path.dirname(source_dir)
    return top_dir
    
def main():
    top_dir = get_top_dir()
    
    # Read in battery compositions
    batt_comp_df = pd.read_csv(f'{top_dir}/data/battery_composition/battery_composition.csv')
    
    comp_demand_df = batt_comp_df.copy(deep=True)
    
    for column in batt_comp_df.columns:
        if column == 'Component': continue
        
        # Convert the masses from kg to fractional composition
        batt_comp_df[column] = batt_comp_df[column] / batt_comp_df[column].sum()
        
        # Calculate the total annual demand for each component in each
        # battery, in millions of tons per year
        comp_demand_df[column] = batt_comp_df[column] * TESLA_SEMI_BATTERY_MASS * N_EVS_PER_YEAR / 1e6
        
    # Save the demand by component
    comp_demand_df.to_csv(f'{top_dir}/data/demand_by_component.csv')
    
    # Plot the annual demand as a stacked bar plot for each battery type
    fig = plt.figure(figsize = (12, 7))
    ax = plt.subplot(111)
    comp_demand_df_T = comp_demand_df.set_index('Component').T
    comp_demand_df_T.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Annual demand for truck battery materials', fontsize=18)
    plt.ylabel('Demand (millions of tons)', fontsize=18)
    plt.xlabel('Battery Chemistry', fontsize=18)
    plt.xticks(rotation = 0)
    plt.legend(fontsize=16, bbox_to_anchor=(1,0.5))
    plt.tight_layout()
    plt.savefig(f'{top_dir}/plots/annual_demand.pdf')
    plt.savefig(f'{top_dir}/plots/annual_demand.png')
    
    # Plot the annual demand as a stacked bar plot for only NMC811
    fig = plt.figure(figsize = (10, 7))
    ax = plt.subplot(111)
    plot_df = comp_demand_df_T[comp_demand_df_T.index == 'NMC811']
    plot_df.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Annual demand for truck battery materials (NMC811)', fontsize=18)
    plt.ylabel('Demand (millions of tons)', fontsize=18)
    #plt.xlabel('Battery Chemistry', fontsize=18)
    plt.xticks([])
    plt.legend(fontsize=16, bbox_to_anchor=(1,0.5))
    plt.tight_layout()
    plt.savefig(f'{top_dir}/plots/annual_demand_NMC811.pdf')
    plt.savefig(f'{top_dir}/plots/annual_demand_NMC811.png')
    
    # For NMC811, plot the anticipated demand of each component next to the current demand
    df_NMC = comp_demand_df_T[comp_demand_df_T.index == 'NMC811']
    df_2022_demand = pd.read_csv(f'{top_dir}/data/material_demand/material_demand.csv').set_index('Component').T
    merged_df = pd.concat([df_NMC, df_2022_demand])
    merged_df.rename(columns={'NMC811': 'BEV Trucks', 'Consumption (millions of tons)': 'Current Demand'})
    
    merged_df_plot = merged_df.T.rename(columns={'NMC811': 'BEV Trucks', 'Consumption (millions of tons)': 'Current Demand'})
        
#    fig = plt.figure(figsize = (10, 7))
#    ax = plt.subplot(111)
#    merged_df_plot.plot(kind='bar', ax=ax)
#    plt.title('Comparison of annual demand for minerals for BEV trucks\nwith current demand from all sectors', fontsize=18)
#    plt.ylabel('Demand (millions of tons)', fontsize=18)
#    plt.xlabel('')
#    plt.legend(fontsize=16, bbox_to_anchor=(1,0.5))
#    plt.tight_layout()
#    plt.savefig(f'{top_dir}/plots/annual_demand_comparison.pdf')
#    plt.savefig(f'{top_dir}/plots/annual_demand_comparison.png')
    
    for component in merged_df.columns:
        fig = plt.figure(figsize = (10, 7))
        ax = plt.subplot(111)
        merged_df_plot.loc[component]
        merged_df_plot.loc[[component]].plot(kind='bar', ax=ax)
        plt.title(f'Comparison of annual demand for {component} for BEV trucks\nwith current demand from all sectors', fontsize=18)
        plt.ylabel('Demand (millions of tons)', fontsize=18)
        plt.xlabel('')
        plt.xticks([])
        plt.xticks(rotation = 0)
        plt.legend(fontsize=16, bbox_to_anchor=(1,0.5))
        plt.tight_layout()
        plt.savefig(f'{top_dir}/plots/annual_demand_comparison_{component}.pdf')
        plt.savefig(f'{top_dir}/plots/annual_demand_comparison_{component}.png')
    
main()


