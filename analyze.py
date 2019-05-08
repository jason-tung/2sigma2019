import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import locale
from locale import atof

def printdf(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

data = pd.read_csv("master.csv").drop(["HDI for year"], axis=1).dropna()


data['age_adj'] = data['age'].map({'5-14 years': (5+14)/2, '15-24 years': (15+25)/2, '25-34 years': (25+34)/2,\
                               '35-54 years' : (35+54)/2, '55-74 years' : (55+74)/2, '75+ years' : 75})

# data["elapsed_years"] = data["year"] - 1987


data["gdp_for_year ($)"] = data["gdp_for_year ($)"].str.replace(",","").astype(float)

data["pop_cut"] = (data["population"] // 100000) * 100000

# print(data.shape)
#
print(data.keys())
#
# printdf(data.head())

# uncomment this to get the pictures and make something up about the correlations u see
plt.figure(figsize=(10, 6))
for k in data.keys():
    if k in ["population", "gdp_for_year ($)", "gdp_per_capita ($)"]:
        plt.plot(data[k], data["suicides/100k pop"], "o", markersize=1)
        plt.xlabel(k)
        plt.ylabel("suicides/100k pop")
        plt.title(k + " vs per 100k pop suicide count")
        plt.grid()
        plt.show()

data["Constant"] = 1
print("\nr^2 for fitting k against per capita suicide")
for k in data.keys():
    if k not in ["country", "age", "sex", "suicides_no", "suicides/100k pop", "country-year", "generation", "Constant"]:
        m = sm.OLS(data["suicides/100k pop"], data[[k, "Constant"]]).fit()
        print(k,m.rsquared)

for k in data.keys():
    if k not in ["suicides_no", "suicides/100k pop", "country-year", "Constant", "age_adj"]:
        print("\nhighest avg per cap suicide by " + k)
        hello = data.groupby(k, as_index=False)['suicides/100k pop'].mean().sort_values(["suicides/100k pop"], ascending=False)
        print(hello.head(10))