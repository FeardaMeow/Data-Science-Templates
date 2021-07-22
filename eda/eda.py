import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create an EDA class that contains all of these steps outlined below
class EDA():
    '''
    pass
    '''
    def __init__(self, data, categorical, continuous):
        '''
        data: a pandas dataframes with the data types already set to be the correct ones
        categorical: a list columns that are categorical
        continuous: a list of columns that are continuous
        '''
        self.data = data
        self.dtypes = ['O', 'float', 'int', 'datetime64[ns]', 'bool', 'other']
        self.categorical = categorical
        self.continuous = continuous
        
    def _calc_number_of_feature_types(self):
        unique_dtypes = set(self.data.dtypes.to_dict().values())
        dtypes_lookup = {}
        for i in unique_dtypes:
            dtype_bool = False
            for j in self.dtypes:
                if i==j:
                    dtypes_lookup[i] = j 
                    dtype_bool=True
                    break
            if not dtype_bool:
                dtypes_lookup[i] = 'other'

        self.num_dtypes = {key:0 for key in self.dtypes}
        for key, value in self.data.dtypes.to_dict().items():
            # Look up value and add it
            self.num_dtypes[value] += 1
    
    def head(self, *args, **kwargs):
        # Show head of data, pass arguements through
        return self.data.head(*args, **kwargs)
    
    def _calculate_number_of_missing_values(self, percentage=False, plot=False, **kwargs):
        if percentage:
            results = self.data.isna().sum()/self.data.shape[0]
        else:
            results = self.data.isna().sum()
        
        if plot:
            results = results.plot.bar(**kwargs)
        
        return results
    
    def _plot_categories_pct_of_total(self, column_to_groupby:str, column_to_agg:str, column_to_agg_value_order: list, figsize= (10,8)):
        '''
        TODO: write docstrings
        '''
        figure = (self.data.groupby(column_to_groupby)[column_to_agg]
        .value_counts(normalize = True)
        .mul(100)
        .rename('percent')
        .reset_index())

        fig, ax = plt.subplots(figsize = figsize)
        
        sns.barplot(x=column_to_groupby, 
                    y="percent", 
                    hue=column_to_agg, 
                    data= figure, 
                    ax = ax, 
                    order = column_to_agg_value_order,
                    hue_order = column_to_agg_value_order)

        ax.xaxis.set_tick_params(rotation=90)
        ax.legend(title = column_to_agg, loc = 'best')
        plt.show()
        
    
