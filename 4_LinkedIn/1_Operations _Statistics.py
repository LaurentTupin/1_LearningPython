'''
#============================================================================================
# Part of the LinkedIn course: Python for Data Science Essential Training
## https://www.linkedin.com/learning/python-for-data-science-essential-training/introduction-to-machine-learning?u=69004890
#============================================================================================
'''

import pandas as pd
import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt
import seaborn as sb
from pylab import rcParams

#Statistics
from scipy.stats import spearmanr, chi2_contingency
from scipy.stats.stats import pearsonr


df_cars = pd.read_csv(r'mtcars.csv')

#--------------------------------------------------------------------------------------------
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
    def cross_Tab(df, str_varRow, str_varCol):
        cT = pd.crosstab(df[str_varRow], df[str_varCol])
        return cT
    
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
    - Your data is normally distributed
    - Continuous, numeric variables
    - Variables are linearly related
    '''
    # Visualisation settings
    ### %matplotlib inline
    rcParams['figure.figsize'] = 8, 4
    plt.style.use('seaborn-whitegrid')
    
    df_cars = df[['mpg','hp','qsec','wt']].copy()
    
    # scatter plot metrix  - refer to ScatterPlotMatrix_sb
    ###  sb.pairplot(df_cars)
    
    # Find the R and deduct Linear Correlated
    def fBl_IsLinearCorrelated(ser1, ser2):
        R, p_value = pearsonr(ser1, ser2)
        print(R, ' || ', p_value)
        if R > 0.75 or R < -0.75:   return True
        else:                       return False
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

Parametric_methods(df_cars)









