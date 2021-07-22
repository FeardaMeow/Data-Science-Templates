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
        self.dtypes = ['O', 'float', 'int', 'datetime64[ns]', 'bool']
        self.categorical = categorical
        self.continuous = continuous
        
    def _calc_number_of_feature_types(self):
        self.num_dtypes = {key:0 for key in self.dtypes}
        for key, value in self.data.dtypes.to_dict():
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
    
    