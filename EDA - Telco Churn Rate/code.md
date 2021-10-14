# Telco Customer Churn EDA

## Task Description ##

In this analysis I will focus on exploring the telco customer churn dataset. 
The target variable is 'churn' which indicates if a customer has cancelled their contract. 

## Analysis Goal ## 

Identify patterns and correlations that can explain the target variable churn.
The typical scenario is working in the Analytics Team at Telco and receiving a request from a product owner asking to identify patterns within the data to support prospective action items to increase retention.


The goal of this analysis is to identify patterns and correlations with the target variable and finally list some potential action items for a potential management audience. 

## Documentation ## 

This dataset was downloaded from [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn/version/1?select=WA_Fn-UseC_-Telco-Customer-Churn.csv)

The data dictionary can be found the [IBM Communit URL](https://community.ibm.com/community/user/businessanalytics/blogs/steven-macko/2019/07/11/telco-customer-churn-1113)


## Import Relevant Libraries ## 

```python
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
```

## Read the data ## 

```python
df = pd.read_csv(r'D:\Documents\dataSets\telco_customer_churn.csv')
```

## Data Understanding ## 

In this section, we will focus on inspecting the data surface properties: 
 
- data format 
- number of records and features
- missing values

How many observations we have and how many features describe each observation? 
```python
df.shape
df.columns
```
The data set describes personas and membership details. 

We can try to identify trends and patterns related to the churn label based on two aspects. 

Taking a look at the data

```python
df.head()
```

Inspect null values and data types. 
Moreover, I want to get an idea of I should expect within each column for better understanding of telco stored data. 
I am going to iterate through all columns and return a list of the unique values stored in which one of them.


```python
df.info()
df.dtypes.value_counts()
for c in df.columns: 
    print(f"Column:{c}",df[c].unique() )
```
Observations:
- No NULL values to handle
- The target variable 'Churn' is stored as an object, we will eventually convert into Boolean 1/0 for statistical analysis
- Boolean values are mainly stored in Yes/No Format. 
- No cleansing needed within columns.
- Total Charges is Obj Type. Why? 

```python
df['TotalCharges'].sample(10)
```
There are no characters attached to the total charges column. I will try to convert the column into float.

```python
pd.to_numeric(df['TotalCharges'], errors = 'coerce')
df['TotalCharges'].isna().sum()
```
No null values, but converting into numeric throws and error: 

```doctest
ValueError: Unable to parse string " " at position 488
```

We find out that the data contains empty strings ' ' which affects 11 observations. 

**Logic**:

- I could assume that those values should be 0 as it could have originally been stored as NULL and finally replaced with empty string
- To support this idea I could have a look at the 'Tenure'. If the tenure is 0 then we can assume that these are new customers and the monthly charges value should be 0

```python
df['tenure'][df.TotalCharges== ' ']
```
The hypothesis is confirmed. All observations where 'TotalCharges' equals ' ' have 0 tenure.
I'm going to investigate also 'MonthlyCharges' just to be sure to have clean data. However, I believe that the value of monthly charges is coming from order data which is stored when the customer signs in the contract. 
Hence, we shouldn't miss it. 

```python
df['MonthlyCharges'][df.TotalCharges== ' ']
```
No empty strings. We can proceed replacing ' ' with 0 in 'Total Charges'

```python
df['TotalCharges'] = df.TotalCharges.str.strip()
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
df['TotalCharges'] = df['TotalCharges'].fillna(0)
df['TotalCharges'].dtype
# Quickly verifying the impact on the distribution 
df.TotalCharges.describe()
```

I want to store all Obj Data in lower cases.

```python
for c in df.columns: 
    if df[c].dtype == 'O':
        df[c] = df[c].str.lower()

# Verify 
for c in df.columns: 
    print(f"Column:{c}",df[c].unique() )
```

We are now confident to have a clean base to work on. The data understanding part is over and we will switch now to data exploration. 


## Plotting Categorical Data ##

First of all let's have a look at the telco churn rate. 

```python
churn_share = round(df.Churn.value_counts()/len(df),2)
churn_share
```

27% of the customers have stopped their membership with the phone provider.

Let's have a look at the categorical data to identify which groups have a higher share of cancellations.

```python
# Define Plot Style https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
plt.style.use('fivethirtyeight')
for c, n in enumerate([c for c in df.columns if df[c].dtype == 'O' and c != 'customerID']): 
    plt.figure(c)
    _ = sns.countplot(data = df, x = n, hue = 'Churn')
    plt.xticks(rotation =75)

```
```python
def percentage_of_totals(col1,data = df,target = 'Churn'): 
    ct = pd.crosstab(data[target], 
                     data[col1], 
                     normalize = 'index')
    sns.heatmap(ct, annot = True)
    
    plt.show()
#Example
percentage_of_totals('Partner')
```
To have a better understanding of the share of each categorical variable compared to the churn outcome, 
I defined a function 'percentage_of_totals' to generate the percentage of total churn compared to a user-defined variable
It will return a correlation heatmap showing the different percentages within groups.

Observations: 
- Churn by gender seems to be equally spread
- Not having a partner lead 53% of the times to churn
- Not having dependents lead 83% of the times to churn. This can be expected as it goes in relation with not having a partner
- Most of the customers have phone service. In this case the share of cancellations is at 90% for both outcomes
- Multiple lines also doesn't show a pattern (share is equally spread)
- Internet service shows 69% churns when fiber optic was part of the membership
- Online security is an additional internet service. Not owning it leads to 70% churn. I currently don't understand the role of this feature and I'll think about it later on.
- We don't know if this online addons are related to fiber which has a high churn rate or to dsl which on the contrary has a low churn rate. I will need to compare the 3 variables to make a story out of it.
    - there are 3 scenarios: 
      1. No internet --> Low churn rate --> no online addons --> low churn
      2. Internet DSL --> Lower churn among internet service --> having addons -- > lower churn rate
      3. Internet Fiber --> Highest churn rate among internet services --> not owning addons --> high churn
- Investigation needed 

... To be continued