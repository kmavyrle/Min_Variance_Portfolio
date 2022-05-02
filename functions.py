# This file contains all the required functions to perform our analysis. File will be imported into our jupyter notebook to utilise the functions
from quant_risk.statistics import financial_ratios as ratios
from quant_risk.portfolio import portfolio as port
from quant_risk.portfolio.portfolio import MeanVariance
from quant_risk.utils import plot
from quant_risk.utils import fetch_data as fetch_data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression



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

def minimise_volatility_full(target_return, er, cov):
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
    return weights_

def min_vol_strategy(start_dt,data,lags = 252,rebals_per_year=52,target_return = 0.1):
    '''
    This function will run the minimise volatility function shown above iteratively over time.
    Intuitively, we feed in more data day by day to optimise the our given function, in this case minimise the volatility of our portfolio.
    This function will perform the iterative function while performing the backtest and provide optimal weights for the portfolio on an iterative basis
    We set the target return as 0.06
    '''
    data.index = pd.to_datetime(data.index, format = '%Y%m%d')
    data = data[start_dt:]
    
    data = resize_data(data,rebal_freq = int(252/rebals_per_year))
        
    
    returns = ((data-data.shift(1))/data.shift(1)).fillna(0)
    A_weights ={}

    counter = 0
    for i in data.index:
        counter+=1
        start = i-dt.timedelta(days = lags)
        
        if counter >=2 and counter < lags:
            ann_ret = ratios.annualised_returns(returns[start_dt:i],rebals_per_year)
            covv = returns[start:i].cov()
            w = minimise_volatility(target_return,ann_ret,covv)
            A_weights[i]=w
            
        elif counter >= lags:
            try:
                ann_ret = ratios.annualised_returns(returns[start:i],rebals_per_year)
                covv = returns[start:i].cov()
                w = minimise_volatility(target_return,ann_ret,covv)
                A_weights[i]=w
            except:
                adj_start = i-dt.timedelta(days = (lags+4))
                ann_ret = ratios.annualised_returns(returns[adj_start:i],rebals_per_year)
                covv = returns[adj_start:i].cov()
                w = minimise_volatility(target_return,ann_ret,covv)
                A_weights[i]=w
            
    weights = pd.DataFrame(A_weights.values(),index = A_weights.keys(),columns = data.columns)
    return weights

def portfolio_variance(weights, covariance):
    '''
    To calculate the portfolio variance with the weights and covariance matrix
    We use the portfolio variance formula:
    Weights transpose -> Matrix multiply by covar matrix -> Matrix multiply by weights
    '''
    return (weights.T@ covariance @ weights)**0.5



def pf_returns(weights,df):
    rets = df.fillna(method = 'bfill').pct_change()
    rets = rets*weights
    rets = 1+(rets.sum(axis = 1))
    return rets.prod()

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


def backtest_plot(prices_ts, weights_ts):
    '''
    This function will help us plot the backtested data and show the returns over time
    '''
    prices_ts = prices_ts.loc[weights_ts.index]
    
    returns = ((prices_ts-prices_ts.shift())/prices_ts.shift()).fillna(0)
    returns = 1+returns
    return (returns*weights_ts).sum(axis=1).cumprod().plot(figsize = (14,8), title = 'Minimum Variance Portfolio Returns')