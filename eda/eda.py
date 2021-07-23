import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import emoji

##### EDA STEPS #####
# Column names and definition

# Column datatypes and possible values

# Sample (head) of the data

# Statistical summaries
## Number of categorical and continuous features
## Number of dtypes: DONE

# Categorical Data
## Missing values: DONE
## Relative frequencies
## Correlations

# Continuous Data
## Missing values
## Histograms for distribution
## Means, standard deviation, medians, etc
## Correlations

# Text Data
## Pre-processing
### Convert emojis into text
### Remove tagged users "@"
### Remove URLs 
## wordclouds
## text length
## word counts
## top unigrams (individual words)
### before and after removing words
## top bigrams
### before and after removing words
## Topic Modeling
### TF-IDF
    '''
    pass
    '''
    def __init__(self, data, categorical=None, continuous=None, text=None):
        '''
        data: a pandas dataframes with the data types already set to be the correct ones
        categorical: a list columns that are categorical
        continuous: a list of columns that are continuous
        '''
        self.data = data
        self.dtypes = ['O', 'float', 'int', 'datetime64[ns]', 'bool', 'other']
        self.categorical = categorical
        self.continuous = continuous
        self.text = text
        self._util()

    def _util(self):
        self.num_categorical = len(self.categorical) if self.categorical != None else 0
        self.num_continuous = len(self.continuous) if self.continuous != None else 0
        self.num_text = len(self.text) if self.text != None else 0
    
    def _remove_url(self):
        pattern=r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
        for col_i in self.text:
            self.data[col_i] = self.data[col_i].str.replace(pattern,'')

    def _replace_emojis(self):
        for col_i in self.text:
            self.data[col_i] = self.data[col_i].apply(emoji.demojize, delimiters=("", " "))

    def _remove_tags(self):
        pattern = r"\@\w+[,]|\@\w+|[,]\@\w+"
        for col_i in self.text:
            self.data[col_i] = self.data[col_i].str.replace(pattern,'')

    def len_of_text(self, column):
        if column not in self.text:
            raise Exception("No Text columns to analyze, please add them to text")

        return self.data[column].apply(lambda x: len(x))

    def number_of_words(self,column):
        if column not in self.text:
            raise Exception("No Text columns to analyze, please add them to text")

        return self.data[column].str.count('\w+')

    def _calc_number_of_dtypes(self):
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
            self.num_dtypes[dtypes_lookup[value]] += 1
    
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
        
    
