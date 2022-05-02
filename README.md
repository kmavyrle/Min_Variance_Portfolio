# Min_Variance_Portfolio
Testing out the minimum variance portfolio using Markowitz Mean Variance portfolio theory
## Introduction
This project aims to apply the Markowitz Mean Variance portfolio theory using the global minimum variance portfolio. Asset prices are extracted from yahoo finance using the yfinance api.
The investment universe used consists of different indices from various asset classes as shown below:
1. SPDR Gold Shares: Gold proxy
2. STI Index
3. S&P500 Index
4. FTSE Index
5. Nikkei Index
6. Hang Seng Index
7. Russell 2000
8. VIX: Volatility Proxy
9. Dow Jones
10. Nasdaq
11. Kospi Index
12. TLT: 30+ Year US Treasury Proxy
13. TLH: 10 Year US Treasury Proxy
14. SHY: 3 year US Treasury Proxy

## Built With
Mainly built with Python and Jupyter notebook. Libraries used include scipy.optimize, matplotlib, yfinance api, datetime, pandas and numpy. The NTU QAM club's quant risk package was also used for
performing more advanced statistical analysis

## Step I: Import relevant python libraries such as pandas, numpy, sklearn, scipy.optimize and NTU QAM's quant risk package
1. Pandas: Used for dataframe manipulation
2. Numpy: Used for mathematical calculations
3. sklearn: Used for linear regression
4. scipy.optimize: Optimization of minimum variance portfolio
5. quant_risk: Used to calculate portfolio statisical measures

![image](https://user-images.githubusercontent.com/85161103/166206535-ad832904-0557-43bd-bc66-060ab46b0cf2.png)

## Step II: Pull daily closing prices for the various indices and asset class proxies using yahoo finance API.
In this step, we will be utilising the yahoo finance API to retrieve daily closing prices for the assets mentioned above. The period in which we would be interested in would be from 2007 onwards. The data retrieved will be stored in a pandas dataframe. Pulling the data as it is from yahoo finance will produced a fairly clean datasets with only NaN values to handle. The NaN values are usually a reult of the particular asset class not trading on a specific day. We will be using the pandas.fillna(method = 'bfill') function to backfill these empty data points. 

![image](https://user-images.githubusercontent.com/85161103/166206973-6e555c84-2ea4-42b2-8b9a-1040c35a5c1e.png)

## Step III: Create functions to perform statistical measures of portfolio returns and risk
Required statistical measures to construct a Markowitz Minimum Variance Portfolio are as such:
1. Portfolio returns will be measured using annualised returns
2. Portfolio risk will be measured using annualised portfolio variance
3. Annualised covariance Matrix
4. Minimise volatility function 
Functions are coded out in the functions.py file while annualised returns and annualised variance functions are imported from the quant_risk package.

### Portfolio Returns and Portfolio Variance Functions(Not Annualised)
![image](https://user-images.githubusercontent.com/85161103/166207462-54260c65-0874-4638-8ff4-d4042a3e98e3.png)
### Minimise volatility Function Produces the Weights of the Minimum Variance Portfolio given a target return.
![image](https://user-images.githubusercontent.com/85161103/166207611-42006eaf-8404-4ca6-92a2-7622ccf4ec34.png)

## Step IV: Plot out the Efficient Frontier
For this step, we will plot out the efficient frontier for the asset class in our investment universe. The efficient frontier has 2 axes whereby the y-axis corresponds to portfolio returns while the x-axis corresponds to portfolio variance. To plot out the efficient frontier, we first require the following:
1. Target returns list for our various efficient portfolios
2. The optimal asset weights in our portfolio which would give us the target returns specified above
3. The variance of the resulting portfolio.
We then generate an array of target returns starting from 0.2% with increments of 0.3%. as shown.
![image](https://user-images.githubusercontent.com/85161103/166208066-6b08053d-4df3-48ea-8c62-ed57224a9af3.png)

We then calculate the annualised returns and annualised covariance matrix of all the different assets from the period between 2007 to 2022 using the quant_risk package. These 2 measures will serve as inputs, along with our target return to find the weights of the minimum variance portfolio.
Next, we iterate through our target returns array to calculate the respective portfolio returns and variances which will be appended to two separate lists.
![image](https://user-images.githubusercontent.com/85161103/166208649-8b27cfc3-d5ac-4410-b2c9-3c055d01b95f.png)

After which we can plot these portfolio returns and variances on a plot to generate the efficient frontier.
![image](https://user-images.githubusercontent.com/85161103/166208733-d2162c8d-6516-4577-af68-a06f8fa9a69a.png)

From the plot shown, we can see that the minimum variance portfolio has a target return of about 0.10 amounting to 10% returns per year. This 10% target return will be used in constructing a minimum variance portfolio to backtest.

## Step V: Apply the Minimum Variance Portfolio Strategy
One limitation of using a single set of asset weights between 2007 and 2022 to allocate to our portfolio is that it does not have any regime awareness. Between 2007 and 2022, economic conditions are always changing. The optimal asset weights in 2007, is unlikekly to be the optimal asset weights in 2022. Hence we need to continuously re-perform the minimum variance analysis and constantly update these weights as time goes by. To establish this, we will be using a 240 day window, i.e the minimum variance portfolio weights will be constructed using past 240 days data and the portfolio will be rebalanced weekly. This is done using the min_vol_strategy function as shown:
![image](https://user-images.githubusercontent.com/85161103/166209495-0c246c27-31ca-45be-be9a-d9262a359d69.png)

The output for the above function will generate the expected optimal weights for our portfolio on a weekly basis and then applied to our portfolio. The weights will then be stored in a dataframe:
![image](https://user-images.githubusercontent.com/85161103/166209711-ea59831d-f11d-40b3-9731-b445f6b76213.png)

We will be using the above asset weights dataframe to calculate the returns of the portfolio, and plot the time-series returns to visualise it's performance.

![image](https://user-images.githubusercontent.com/85161103/166209909-5eea47f4-7435-421f-9fd3-a4d5d533ee89.png)

## Conclusion
From the comparison between the Global Minimum Variance portfolio (Green) with the performance of the S&P500 (Blue), we can tell that it was significantly less volatile with lesser price swings. In 2008 the min vol strategy protected the portfolio fairly well, i.e it protected against the large drawdown from stock market crash. Minimum Variance portfolio also outperformed S&P500 (the best performing asset in our selected universe of assets).
