def minimise_volatility(target_return, er, cov):
    '''
    Minimise volatility function will give a SINGLE array of weights for the assets
    for a given return value
    '''
    n = er.shape[0] #n would give the number of assets
    
    #Create a numpy array that repeats 1/n, n number of times
    # Put it into an initial guess where the weights are all equal
    initial_guess = np.repeat(1/n,n) 
    
    bounds = ((0.0,0.2),)*n  #Create a tuple of n number of tuples with 0 and 1 as the values within each tuple
    
    #Create our constraints which must be in a dictionary form
    return_is_target = {
        'type':"eq", #Equality type means that whatever formula is provided in the 'fun' line will be equal to zero
        'args': (er,), #arguments=> Over here it means that expected returns er is the variable argument
                       #and weights is the value we want
        'fun': lambda weights, er: target_return - portfolio_returns(weights, er)
    }
    weights_sum_to_1 = {
        'type':'eq',
        'fun': lambda weights: np.sum(weights) - 1
    }
    
    max_asset_weight = {
        'type':'ineq',
        'fun':lambda weights: weights
    }
    
    weights_ = minimize(portfolio_variance, initial_guess,
                        #Note that the portfolio variance is another formula here(i.e this is a nested formula, with inputs 
                        #Covariance and weights, BUT we put the cov as an arg in the next line, ie. its a known variable)
                        args = (cov,), method = "SLSQP",
                        constraints = (return_is_target, weights_sum_to_1),
                        bounds = bounds)
    return weights_.x


def portfolio_variance(weights, covariance):
    '''
    To calculate the portfolio variance with the weights and covariance matrix
    We use the portfolio variance formula:
    Weights transpose -> Matrix multiply by covar matrix -> Matrix multiply by weights
    '''
    return (weights.T@ covariance @ weights)**0.5



def pf_returns(weights,df):
    rets = (df-df.shift(1))/df
    allocationWeights.columns = rets.columns
    rets = rets*allocationWeights.astype(float)
    return rets.sum(axis = 1)

def plot_backtest(weights,df):
    (1+pf_returns(weights, df)).cumprod().plot(figsize = (6,5))
    
def semideviation(r):
    semidev = r[r<0].std(ddof = 0)
    return semidev

def portfolio_returns(weights, returns):
    '''
    To calulate the returns from the weights of each asset.
    weights would be a numpy array which is then transposed to form a matrix
    returns is a series consisting of the returns(data) of different assets(index)
    Transpose weights - > Matrix multiplication with returns
    
    '''
    return weights.T @ returns


def resize_data(dataframe,rebal_freq = 5):
    Resizeddf = {}
    counter = 0
    for i in dataframe.index:
        counter +=1
        if counter ==rebal_freq:
            Resizeddf[i]=dataframe.loc[i]
            counter =0
    Resizeddata = pd.DataFrame(Resizeddf.values(), index = Resizeddf.keys(),
                               columns = dataframe.columns)        
    return Resizeddata