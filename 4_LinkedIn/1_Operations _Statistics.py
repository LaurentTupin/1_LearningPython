'''
#============================================================================================
# Part of the LinkedIn course: Python for Data Science Essential Training
## https://www.linkedin.com/learning/python-for-data-science-essential-training/introduction-to-machine-learning?u=69004890
#============================================================================================
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from pylab import rcParams
#Statistics
from scipy.stats import chi2_contingency
from scipy.stats.stats import pearsonr
# Data Science: sklearn
from sklearn import preprocessing

df_cars = pd.read_csv(r'mtcars.csv')


#==============================================================================
# Function
#==============================================================================
def cross_Tab(df, str_varRow, str_varCol):
    cT = pd.crosstab(df[str_varRow], df[str_varCol])
    return cT

# Find the R and deduct Linear Correlated
def fBl_IsLinearCorrelated(ser1, ser2):
    R, p_value = pearsonr(ser1, ser2)
    print(R, ' || ', p_value)
    if R > 0.75 or R < -0.75:   return True
    else:                       return False
    
# Find the p and deduct Correlation
def fBl_nonParametricCorrelation(df, str_varRow, str_varCol):
    # Put data into Cross Table
    cT = cross_Tab(df, str_varRow, str_varCol)
    # Apply the function chi2_contingency on the Table
    chi2, p, dof, expected = chi2_contingency(cT.values)
    print('p: %0.3f || chi2: %0.1f  || dof: %0.0f '%(p, chi2, dof))
    ### print(expected)
    if p < 0.05:        return True     #IF p < 0.05 THEN variables are correlated
    elif p >= 0.05:     return False    #IF p > 0.05 THEN variables are independent
    else:               return 'ERROR in fBl_nonParametricCorrelation'

def fArr_normalization(ser, t_rangeLimit = (0,1)):
    arr_matrix = ser.values.reshape(-1,1)
    o_scaled = preprocessing.MinMaxScaler(feature_range = t_rangeLimit)
    arr_scaled_matrix = o_scaled.fit_transform(arr_matrix)
    return arr_scaled_matrix




#==============================================================================
# Course
#==============================================================================
# 3. Basic Math and Statistics
def Operation_OnNumpy():
    #Round = 2 for the printing
    np.set_printoptions(precision = 2)
    
    # Create Array
    # 1 row
    a = np.array(range(1,7))
    print('a \n', a)
        # OR    d = np.arange(1, 35)
    # 2 rows
    b = np.array([[10, 20, 30], 
                  [40, 50, 60]])
    print('b \n', b)
    # random Array
    np.random.seed(25)
    c = np.random.randn(6)
    print('c \n', c)
    
    # Arithmetic on Array
    arr_multi = a * 10
    print('arr_multi \n', arr_multi)
    arr_add = a + c
    print('arr_add \n', arr_add)
    
    # Linear Algebra: Matrix multiplication
    aa = np.array([[2., 4., 6.], 
                   [1., 3., 5.], 
                   [10., 20., 30.]])
    bb = np.array([[0., 1., 2.], 
                   [3., 5., 5.], 
                   [6., 20., 7.]])
    # ==> Matrix de 3*3 multiplication simple
    cc = aa * bb
    print('cc \n',cc)
        # cc = np.array([0, 4, 12], [3, 15, 25], [60, 400, 210])
    
    # Dot prodict (multiplication scalaire / scalar)
    cc = np.dot(aa, bb)
    print('cc \n',cc)
        #==> Matrix de 3*3 multiplication matricielle
        # cc = np.array([[48, xx, xx], [xx, xx, xx], [xx, xx, xx])
        #                   48 = 2*0 + 4*3 + 6*6

#Operation_OnNumpy()


def Statistics(df_cars):
    #df
    
    #Basics Stat
    print(' HEAD: \n',      df_cars.head(), 
          '\n--------------------')
    print(' SUM: \n',       df_cars.sum(), 
          '\n--------------------')
    #SUM by rows of all float columns
    print(' SUM row: \n',   df_cars.sum(axis = 1) , 
          '\n--------------------') 
    print(' median: \n',    df_cars.median(), 
          '\n--------------------')
    print(' mean: \n',      df_cars.mean(), 
          '\n--------------------')
    print(' max: \n',       df_cars.max(), 
          '\n--------------------')
    print(' idxmax on mpg: \n', df_cars['mpg'].idxmax(), 
          '\n--------------------')
    #Vol
    print(' std: \n',       df_cars.std(), 
          '\n--------------------')
    #vol ** 2 
    print(' var: \n',       df_cars.var(), 
          '\n--------------------')
    #Get them all
    print(' describe: \n',  df_cars.describe(), 
          '\n--------------------')
    # Unique values of a Series
    print(' value_counts: \n', df_cars['gear'].value_counts(), 
          '\n--------------------')        
        # => List of Unique values (index) in a Series with their recurence (Value)
#Statistics(df_cars)


def Categorical_Data(df_cars):
    ValCount_carb = df_cars['carb'].value_counts()
    print(ValCount_carb, 
          '\n--------------------')
    
    df_cars_cat = df_cars[['cyl','vs','am','gear','carb']]
    print(df_cars_cat.head(), 
          '\n--------------------')
    gears_group = df_cars_cat.groupby('gear')
    print(gears_group.describe(), 
          '\n--------------------')
    # adding a new column
    df_cars['group'] = pd.Series(df_cars.gear, dtype = 'category')
    print(type(df_cars['group']))
    print(df_cars['group'].value_counts(), 
          '\n--------------------')
    #CrossTab
    cT = cross_Tab(df_cars, 'am', 'gear')
    print(cT)
#Categorical_Data(df_cars)



    

def Parametric_methods(df):
    # R is the Pearson Correlation Coefficient
    '''
    - Continuous, numeric variables
    - Your data is normally distributed
    - Variables are linearly related
    '''
    # Visualisation settings
    ### %matplotlib inline
    rcParams['figure.figsize'] = 8, 4
    plt.style.use('seaborn-whitegrid')
    
    df_cars = df[['mpg','hp','qsec','wt']].copy()
    
    # scatter plot metrix  - refer to ScatterPlotMatrix_sb
    ###  sb.pairplot(df_cars)
    
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['mpg'], df_cars['hp'])
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['mpg'], df_cars['qsec'])
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['mpg'], df_cars['wt'])
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['hp'], df_cars['qsec'])
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['hp'], df_cars['wt'])
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['qsec'], df_cars['wt'])
    print(bl_linearCor)
    
    # Using Pandas to get Pearson Correlation Coefficient
    corr = df_cars.corr()
    print(corr)
    
    # With Seaborn for Charts
    sb.heatmap(corr, xticklabels = corr.columns.values, yticklabels = corr.columns.values)
#Parametric_methods(df_cars)



def NonParametric_methods(df):
    '''   Assumptions Spearman Rank Correlation
    - Your data is NON-normally distributed
    - Variables are ordinal (numeric but able to be ranked like categorical variable)
        * bin the variable, if x in [0, 100], put it in 10 groups for the Var to be Discrete (in Categroy): 0-10-20-...-100
    - Variables are NON-linearly related
    '''
    # Visualisation settings
    ### %matplotlib inline
    rcParams['figure.figsize'] = 6, 2
    plt.style.use('seaborn-whitegrid')
    
    df_cars = df[['cyl','vs','am','gear']].copy()
    # scatter plot metrix  - refer to ScatterPlotMatrix_sb
    ###      sb.pairplot(df_cars)
    
    # Find the R and deduct Linear Correlated
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['cyl'], df_cars['vs'])
    #--> -0.814
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['cyl'], df_cars['am'])
    #--> -0.522
    bl_linearCor = fBl_IsLinearCorrelated(df_cars['cyl'], df_cars['gear'])
    #--> -0.564
    print(bl_linearCor)
    
    # Chi-Square Test of independance
    bl_Correlation = fBl_nonParametricCorrelation(df_cars, 'cyl', 'vs')
    bl_Correlation = fBl_nonParametricCorrelation(df_cars, 'cyl', 'am')
    bl_Correlation = fBl_nonParametricCorrelation(df_cars, 'cyl', 'gear')
    print(bl_Correlation)
    #    cT = cross_Tab(df_cars, 'cyl', 'am')
    #    print(cT)
    #    chi2, p, dof, expected = chi2_contingency(cT.values)
    #    #IF p < 0.05 THEN variables are correlated
    #    #IF p > 0.05 THEN variables are independent
#NonParametric_methods(df_cars)




def fArr_standardization(ser, d_param = {}):
    arr_standard = preprocessing.scale(ser, **d_param)
    # print(arr_standard)
    return arr_standard




def ReShapedatasets(df):
    '''
    # You need to scale your variables, examples: Inflation when comparing 1990 and 2016 prices /revenues
        # 1. Normalization: putting each observation on a relative scale between 0 & 1
            # (Value of observation) / (Sum of all observation in variable)
        # 2. Standardization - rescaling data so it has a zero mean and a unit variance
    '''
    # Visualisation settings
    ### %matplotlib inline
    rcParams['figure.figsize'] = 10, 4
    plt.style.use('seaborn-whitegrid')
    
    # plot
    df_cars = df[['mpg']].copy()
    ###         plt.plot(df_cars['mpg'])
    ###         print(df_cars.describe())
    
    # 1. Normalization: putting each observation on a relative scale between 0 & 1
    arr_Norm = fArr_normalization(df_cars['mpg'])
    plt.plot(arr_Norm)
    
    # 2. Standardization: rescaling data so it has a zero mean and a unit variance
    arr_std_1 = fArr_standardization(df_cars['mpg'], d_param = dict(with_mean = False, with_std = False)) 
        # Just like the original ## df_cars ##
    arr_std_2 = fArr_standardization(df_cars['mpg'], d_param = dict(with_std = False))          # Minus the mean
    arr_std_3 = fArr_standardization(df_cars['mpg'], d_param = dict(with_mean = False))         # Divided by the Std Deviation
    arr_std_4 = fArr_standardization(df_cars['mpg'])                                            # Standardized
    
    # Chart
    df_cars['Minus_Mean'] = pd.Series(arr_std_2)   #, dtype = 'category'
    df_cars['DivBy_Std'] = pd.Series(arr_std_3)   #, dtype = 'category'
    df_cars['Standardized'] = pd.Series(arr_std_4)   #, dtype = 'category'
    df_cars.plot(alpha = 0.5, lw = 3, ls= '--')
      
ReShapedatasets(df_cars)







