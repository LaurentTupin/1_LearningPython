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

def fXy_transformDfIntoNpArr(df, str_targetName):
    y = df[str_targetName].values
    X = df.drop(str_targetName, axis=1).values
    return X, y

def dDf_TransformXinDf(X, l_feature_names):
    df = pd.DataFrame(X, columns = l_feature_names)
    return df

def IrisData():
    from sklearn import datasets
    iris = datasets.load_iris()
    #    print(iris.keys())
    l_feature_names = iris.feature_names
    l_target_names = iris.target_names
    # Build the data model
    X = iris.data
    y = iris.target
    return X, y, l_feature_names, l_target_names

def cours1_scatter_matrix():
    X, y, l_feature_names, l_target_names = IrisData()
    print(l_target_names)
    df = dDf_TransformXinDf(X, l_feature_names)
    # Some Chart / plot
    pd.plotting.scatter_matrix(df, c = y, s = 100, marker = 'D', figsize = [12,8])
cours1_scatter_matrix()

def EDA_countPlot():
    X, y, l_feature_names, l_target_names = IrisData()
    print(l_target_names)
    df = dDf_TransformXinDf(X, l_feature_names)
    df['flower'] = y    
    # Some Chart / plot
    for xx in l_feature_names:
        #   Be sure to begin your plotting statements for each figure with plt.figure() 
        #   so that a new figure will be set up. 
        #   Otherwise, your plots will be overlayed onto the same figure.
        plt.figure()
        sb.countplot(data=df, x=xx, hue='flower') #, palette='RdBu'
        plt.show()
EDA_countPlot()

def ClassificationChallenge():
    X, y, l_feature_names, l_target_names = IrisData()
    print(l_target_names)
    # K-Nearest neighbors
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors = 6)
    knn.fit(X, y)
    y_predict = knn.predict(np.array([[5.6,2.8,3.9,1.1], 
                                      [5.7, 2.6, 3.8, 1.3], 
                                      [4.7, 3.2, 1.3, 0.2]]))
    #    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
    #                         metric_params=None, n_jobs=1, n_neighbors=6, p=2,
    #                         weights='uniform')
    return y_predict

y_predict = ClassificationChallenge()
print(y_predict)









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
