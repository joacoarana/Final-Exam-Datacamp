# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 18:56:34 2023

@author: rjara
"""


#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pp_sales=pd.read_csv("C:/Users/rjara/OneDrive/Desktop/Datacamp/FINAL EXAM/product_sales.csv")

#%% DATA VALIDATION

pp_sales['week'].value_counts()

#6 weeks of Data 1-6

pp_sales['customer_id'].value_counts()
# 15000 customers

pp_sales['years_as_customer'].value_counts()

# From 1 to 63

pp_sales['state'].value_counts()

#ALL US STATES

#%% Clean Data

#Revenue column has missing values
pp_sales.isna().any()
pp_sales.columns
pp_sales['revenue']

#REMOVE ROWS W MISSING VALUES (1074 rows)

pp_sales[pp_sales.isna()['revenue']==True]
pp_sales_nan= pp_sales.dropna()

# Sales_method has inconclusive values--- Example; 'em + call'

e= list(pp_sales_nan[pp_sales_nan['sales_method']== 'email'].index)

# REPLACE inconclusive values

pp_sales_clea=pp_sales_nan.replace('email', 'Email')
pp_sales_clean= pp_sales_clea.replace('em + call','Email + Call' )


#%% number of customers

pp_sales['sales_method'].value_counts()
pp_sales_clean['sales_method'].value_counts()

'''
Email=7466
Call= 4962
email + call= 2572
'''

#SALES FOR EACH APPROACH

count= [7466, 4962, 2572]
sales_method= ['Email', 'Call', 'Email + Call']

plt.bar(sales_method, count)
plt.xlabel('Sales Method', fontsize= 18)
plt.ylabel('Amount', fontsize=18)
plt.title("Sales for each Approach", fontsize=20)
plt.style.use("seaborn")
plt.show()

#COUNTPLOTS
sns.countplot(data=pp_sales, x='sales_method')
sns.countplot(data=pp_sales_clean, x='sales_method')

#%% spread of the revenue

pp_sales_clean.groupby('sales_method')['revenue'].sum().plot(kind='bar')
plt.xlabel('Sales Method', fontsize= 25, fontname='Times New Roman')
plt.ylabel('Total Revenue', fontsize=25, fontname='Times New Roman')
plt.title("Total Revenue for each Approach", fontsize=30, fontname='Times New Roman')
plt.style.use("seaborn")
plt.show()

sns.histplot(data= pp_sales_clean, x='revenue', bins=30, kde=True)
plt.xlabel('Revenue', fontsize=25,fontname='Times New Roman')
plt.ylabel('Count', fontsize=25,fontname='Times New Roman')
plt.title('Revenue Distribution', fontsize=30, fontname='Times New Roman')

# SPREAD MEASSUREMENTS
pp_sales_clean['revenue'].mean()
pp_sales_clean['revenue'].median()
pp_sales_clean['revenue'].std()
pp_sales_clean['revenue'].max()
pp_sales_clean['revenue'].min()
pp_sales_clean['revenue'].agg([np.var, np.std, np.mean, np.median, np.max, np.min])

# ADD a column: REVENUE RANGE

pp_sales_clean['revenue_range']= np.nan

pp_sales_clean.loc[pp_sales_clean['revenue']<= 50,'revenue_range'] = '0-50'
pp_sales_clean.loc[(pp_sales_clean['revenue']> 50) & (pp_sales_clean['revenue']<=100),'revenue_range'] = '50-100'
pp_sales_clean.loc[(pp_sales_clean['revenue']> 100) & (pp_sales_clean['revenue']<=150),'revenue_range'] = '100-150'
pp_sales_clean.loc[pp_sales_clean['revenue']> 150,'revenue_range'] = '+150'


category_order = ["0-50", "50-100", "100-150", "+150"]

sns.set_style("darkgrid")
sns.countplot(x=pp_sales_clean['revenue_range'], order=category_order )
plt.xlabel('Revenue Range in US$', fontsize=25,fontname='Times New Roman')
plt.ylabel('Count', fontsize=25,fontname='Times New Roman')
plt.title('Revenue Range', fontsize=30, fontname='Times New Roman')
plt.show()


#%% spread by method

# SPREAD MEASSUREMENTS
pp_sales_clean
pp_sales_clean.groupby('sales_method')['revenue'].agg([np.var, np.std, np.mean, np.median, np.max, np.min])
pp_sales_clean.groupby('sales_method')['nb_sold'].agg([np.var, np.std, np.mean, np.median, np.max, np.min])

#BOXPLOT PER METHOD

sns.boxplot(data=pp_sales_clean, x='sales_method', y='revenue')
plt.xlabel('Sales Method', fontsize=25,fontname='Times New Roman')
plt.ylabel('Revenue', fontsize=25,fontname='Times New Roman')
plt.show()

#SEPARATE DFs per method

email= pp_sales_clean[pp_sales_clean['sales_method']== 'Email']

call= pp_sales_clean[pp_sales_clean['sales_method']== 'Call']

email_call= pp_sales_clean[pp_sales_clean['sales_method']== 'Email + Call']

category_order = ["0-50", "50-100", "100-150", "+150"]

#distributions of each method

#EMAIL
email['revenue'].hist(bins=15)
sns.countplot(x=email['revenue_range'], order= category_order)


#CALL

call['revenue'].hist(bins=15)
sns.countplot(x=call['revenue_range'], order= category_order)

# EMAIL + CALL

email_call['revenue'].hist(bins=15)
sns.countplot(x=email_call['revenue_range'], order= category_order)

#%% BY TIME

#EMAIL

email.groupby('week').size()
email.groupby('week').size().plot(kind='line')
email.groupby('week')['revenue'].sum()
email.groupby('week')['revenue'].sum().plot(kind='bar')
email.groupby('week')['revenue_range'].value_counts()
sns.catplot(x='week', hue='revenue_range', data=email, kind='count')



# Stacked barchart of sales by revenue_range (I pivot the table to get it)

email_week_rev_range= email.loc[:, ['week', 'revenue_range']]
email_week_rev_range['count']= 1
email_w_rr_pivoted=email_week_rev_range.pivot_table(values='count' , index='week', columns='revenue_range', aggfunc='sum')

email_w_rr_pivoted.plot(kind='bar', stacked= True)
plt.show()

#CALL

call.groupby('week').size()
call.groupby('week').size().plot(kind='line')
call.groupby('week')['revenue'].sum()
call.groupby('week')['revenue'].sum().plot(kind='line')
call.groupby('week')['revenue_range'].value_counts()
sns.catplot(x='week', hue='revenue_range', data=call, kind='count')


# CALL & EMAIL

email_call.groupby('week').size()
email_call.groupby('week').size().plot(kind='line')
email_call.groupby('week')['revenue'].sum()
email_call.groupby('week')['revenue'].sum().plot(kind='line')
email_call.groupby('week')['revenue_range'].value_counts()
sns.catplot(x='week', hue='revenue_range', data=email_call, kind='count')

#"Method's Revenue by Week" --- LINE

email.groupby('week')['revenue'].sum().plot(kind='line')
call.groupby('week')['revenue'].sum().plot(kind='line')
email_call.groupby('week')['revenue'].sum().plot(kind='line')
plt.legend(['Email','Call', 'Email + Call'])
plt.xlabel('Week', fontsize=25,fontname='Times New Roman')
plt.ylabel('Revenue', fontsize=25,fontname='Times New Roman')
plt.title("Method's Revenue by Week", fontsize=30, fontname='Times New Roman')
plt.show()

# REVENUE BY WEEK --- STACKED BARCHART

barch=pp_sales_clean.loc[:, ['week', 'revenue', 'sales_method']]
barch_pivoted=barch.pivot_table(values='revenue', index='week', columns= 'sales_method', aggfunc='sum')

barch_pivoted.plot(kind='bar',stacked= True)
plt.xlabel('Week', fontsize=25,fontname='Times New Roman')
plt.ylabel('Total Revenue', fontsize=25,fontname='Times New Roman')
plt.title('Revenue by Week', fontsize=30, fontname='Times New Roman')
plt.legend()

#%% USEFUL

#Exploring
pp_sales_clean.groupby(['sales_method','week'])['nb_sold'].mean()
pp_sales_clean.groupby(['sales_method','week'])['nb_site_visits'].mean()
pp_sales_clean.groupby(['sales_method','week'])['state'].value_counts()


#Total revenue per week
pp_sales_clean.groupby('week')['revenue'].sum().plot(kind='line')
plt.xlabel('Week', fontsize=25,fontname='Times New Roman')
plt.ylabel('Amount', fontsize=25,fontname='Times New Roman')
plt.title('Total Revenue by Week', fontsize=30, fontname='Times New Roman')
plt.show()


#PERCENTAGES
pp_sales_clean.groupby(['week', 'sales_method'])['revenue'].sum() / pp_sales_clean.groupby('week')['revenue'].sum()



