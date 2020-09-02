'''
Skill Track : https://learn.datacamp.com/skill-tracks/machine-learning-fundamentals-with-python
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

####################################################
#### METTRE les charts dans le chart
####################################################


#==============================================================================
# Course 1: Supervised Learning with scikit-learn
#==============================================================================

# NOTES
    # Classification:   Target Variable consists of Categories (Bollean or plus...)
    # Regression :      Target Variable is continuous (like a Price)

#-----------------------------------------------------
# 1.1 Classification
#-----------------------------------------------------

plt.style.use('ggplot')

def IrisData():
    from sklearn import datasets
    iris = datasets.load_iris()
    #    print(iris.keys())
    print(iris.target_names)
    # Build the data model
    X = iris.data
    y = iris.target
    #    print(type(X), type(y))
    df = pd.DataFrame(X, columns = iris.feature_names)
    return df, y

def cours1_scatter_matrix():
    df, y = IrisData()
    # Some Chart / plot
    pd.plotting.scatter_matrix(df, c = y, s = 100, marker = 'D', figsize = [12,8])
#cours1()

def EDA_countPlot():
    df, y = IrisData()
    df['flower'] = y
    # Some Chart / plot
    for xx in ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)','petal width (cm)']:
        #   Be sure to begin your plotting statements for each figure with plt.figure() 
        #   so that a new figure will be set up. 
        #   Otherwise, your plots will be overlayed onto the same figure.
        plt.figure()
        sb.countplot(x=xx, hue='flower', data=df) #, palette='RdBu'
        plt.xticks([0,1], ['No', 'Yes'])
        plt.show()
EDA_countPlot()








#==============================================================================
# Course 2: Unsupervised Learning in Python
#==============================================================================


#==============================================================================
# Course 3: Linear Classifiers in Python
#==============================================================================


#==============================================================================
# Course 4: Case Study: School Budgeting with Machine Learning in Python
#==============================================================================


#==============================================================================
# Course 5: Introduction to Deep Learning in Python
#==============================================================================
