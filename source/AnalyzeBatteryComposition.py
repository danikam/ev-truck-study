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
    
main()


