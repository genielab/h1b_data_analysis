import numpy as np
import pandas as pd
import re

def validate_city(x):
    x = re.sub("\n"," ", x)
    x = re.sub("\s","",x)
    return x.isalpha()

def derive_city_variable(x):
    result = ''
    if(pd.notnull(x['work_city']) and validate_city(x['work_city'])==True):
        return x['work_city'].upper()
    elif(pd.notnull(x['emp_city']) and validate_city(x['emp_city'])==True):
        return x['emp_city'].upper()
    else:
        return None
    
def calc_emp_avg_annual_wage(x):
    result = None
    if(x['wage_from']>0 and x['wage_to']>0):
        result = round((x['wage_from'] + x['wage_to'])/2,2)
    else:
        result = x['wage_from']
    
    if(x['wage_unit']=="M"):
        result=round(result*12,2)
    elif(x['wage_unit']=="BW"):
        result=round(result*26,2)
    elif(x['wage_unit']=="W"):
        result = round(result*52,2)
    elif(x['wage_unit']=="H"):
        result = round(result*40*52,2)
    return(result)

def convert_amount_to_human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


# federal tax 
# https://www.nerdwallet.com/blog/taxes/federal-income-tax-brackets/
def federal_income_tax_2018(x):
    result = np.nan
    avg_annual_wage = x['avg_annual_wage']
    if(avg_annual_wage<=9525.00):
        result = round(10*avg_annual_wage/100, 2)
    elif((avg_annual_wage>=9526.00) & (avg_annual_wage<=38700.00)):
        temp = avg_annual_wage-9525.00
        result = 952.50 + round(12*temp/100,2)
    elif((avg_annual_wage>=38701.00) & (avg_annual_wage<=82500.00)):
        temp = avg_annual_wage-38700.00
        result = 4453.50 + round(22*temp/100,2)
    elif((avg_annual_wage>=82501.00) & (avg_annual_wage<=157500.00)):
        temp = avg_annual_wage-82500.00
        result = 14089.50 + round(24*temp/100,2)
    elif((avg_annual_wage>=157501.00) & (avg_annual_wage<=200000.00)):
        temp = avg_annual_wage-157500.00
        result = 32089.50 + round(32*temp/100,2)
    elif((avg_annual_wage>=200001) & (avg_annual_wage<=500000.00)):
        temp = avg_annual_wage-200000.00
        result = 45689.50 + round(35*temp/100,2)
    elif(avg_annual_wage>=500001):
        temp = avg_annual_wage-500000.00
        result = 150689.50 + round(37*temp/100,2)  
    return(result)

def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq:
    # http://www.statsdirect.com/help/generatedimages/equations/equation154.svg
    # from:
    # http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    # All values are treated equally, arrays must be 1d:
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array += 0.0000001
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

def calc_monthly_mortgage_payment_for_30yrfixed(x):
    # assume 10% down payment
    # assume interest rate 4%
    if(np.isfinite(x['zhvi_allhomes_2018'])):
        home_value = x['zhvi_allhomes_2018']
        home_value = home_value - (0.10*home_value)
        result = round(home_value * 0.0033 * (((1+0.0033) ** 340)/(((1+0.0033) ** 340)-1)),2)
        return result
    else:
        return(np.nan)