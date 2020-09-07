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
from scipy.stats import spearmanr, chi2_contingency
from scipy.stats.stats import pearsonr

# Data Science: sklearn
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import classification_report







#--------------------------------------------------------------------------------------------
# 4. Dimensionality Reduction
def part4_DimensionalityReduction():
    # Factor Analysis
        # Assumptions:
        # 1. Features are Metrics
        # 2. Features are Continuous or ordinal
        # 3. Correlation r >0.3 between features in your dataset
        # 4. More than 100 observations
        # 5. Sample is homogenous

    #Import
    import numpy as np
    import pandas as pd
    import sklearn
    from sklearn.decomposition import FactorAnalysis
    from sklearn import datatsets

    iris = datasets.load_iris()
    x = iris.data
    varable_names = iris.feature_names
        # x[0:10,]
        # ==> Array (10 / 4)

    factor = FactorAnalysis().fit(x)
    pd.DataFrame(factor.components_, columns=varable_names)


    # Principal component Analysis (PCA)
        # Singular Value Decomposition (SVD)
    import matplotlib.pyplot as plt
    import seaborn as sb
    from IPython.display import Image
    from IPython.core.display import HTML
    from pylab import rcParams
    from sklearn.decomposition import PCA

    ##  %matplotlib inline
    rcParams['figure.figsize'] = 5, 4
    sb.set_style('whitegrid')

    iris = datasets.load_iris()
    x = iris.data
    varable_names = iris.feature_names

    pcs = PCA()
    iris_pca = pca.fit_transform(x)
        # pca.explained_variance_ratio_
        # ==> Array (1 / 4)

        # pca.explained_variance_ratio_.sum()
        # ==> 1.0

    # Only keep the 2 first columns as they explain more than 95% of the data
    comps = pd.DataFrame(pca.components_, columns = varable_names)
        # comps
        # ==> Array  4x4
        # sp.heatmap(comps)
        # ==> Heatmap


#--------------------------------------------------------------------------------------------
# 5. Outlier Analysis
def part5_OutlierAnalysis():
    '''
    1. Point Outliers
    2. Contextual Ouliers
    3. Collective Outliers
    '''

    # Tukey Boxplots
    # IQR (spread) = Diff betweem the 1st Quartile(25%) and 3rd Quartile(75%)
    # a = Q1 - 1.5 IQR
    # b = Q3 + 1.5 IQR
    # Below a and above b, the variable is suspect for outliers

    # Multivariate Analysis for outlier detection
    sb.boxplot(x='Species', y='Sepal Length', data=df, palette='hls')
    sb.pairplot(df, hue='Species', palette='hls')            # Scatterplot

    # Linear Projection method for multivariate data
    from sklearn.cluster import DBSCAN
    from collections import Counter

    df = pd.read_csv(...)
    data = df.ix[:, 0:4].values
    target = df.ix[:, 4].values

    model = DBSCAN(eps=0.8, min_samples=19).fit(data)
    outliers_df = pd.DataFrame(data)
    print(Counter(model.labels_))
    print(outliers_df[model.labels_ == -1])

    fig = plt.figure()
    ax = fig.add_axes([.1, .1, 1, 1])
    colors = model.labels_
    ax.scatter(data[:,2], data[:,1], c=colors, s=120)
    ax.set_xlabel('Petal Length')
    ax.set_ylabel('Sepal Width')
    plt.title('DBScan for ouliers detection')


#--------------------------------------------------------------------------------------------
# 6. Cluster Analysis
def part6_ClusterAnalysis():
    # K-means clustering
    from sklearn.cluster import KMeans
    from mpl_toolkits.mplot3d import Axes3D
    from sklearn.preprocessing import scale
    from sklearn import datasets
    from sklearn.metrics import confusion_matrix, classification_report
    import sklearn.metrics as sm

    iris = datasets.load_iris()
    X = preprocessing.scale(iris.data)
    Y = pd.DataFrame(iris.target)
    variables_names = iris.feature_names

    clustering = KMeans(n_clusters = 3, random_state = 5)
    clustering.fit(X)

    iris_df = pd.DataFrame(iris.data)

    plt.subplot(1,2,1)
    plt.scatter(x = iris_df.Petal_Length, y = iris_df.Petal_Width, c = color_theme[iris.target], s = 50)
    plt.title('Ground Truth Classification')

    plt.subplot(1,2,2)
    plt.scatter(x = iris_df.Petal_Length, y = iris_df.Petal_Width, c = color_theme[clustering.labels_], s = 50)
    plt.title('K-Means')

    # Hierarchial methods (Hierarchial Clustering Dendrogram)
    import scipy
    from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, cophenet
    from scipy.spatial.distance import pdist
    import sklearn
    from sklearn.cluster import AgglomerativeClustering
    import sklearn.metrics as sm

    np.set_printoptions(precision = 4, suppress = True)        # pas trop de chiffre ap. virgule

    X = cars.ix[:,(1,3,4,6)].values
    Y = cars.ix[:,(9)].values
    Z = linkage(X, 'ward')
    dendrogram(Z, truncate_mode='lastp', p=12, leaf_rotation = 45., leaf_font_size = 15., show_contracted = True)

    plt.xlabel('Cluster Size')
    plt.ylabel('Distance')
    plt.axhline(y = 500)
    plt.axhline(y = 150)
    plt.show()

    k=2
    Hclustering = AgglomerativeClustering(n_clusters = k, affinity = 'euclidian', linkage = 'ward')                #BEST
    Hclustering.fit(X)
    sm.accuracy_score(y, Hclustering.labels_)
    # -->0.78125

    Hclustering = AgglomerativeClustering(n_clusters = k, affinity = 'euclidian', linkage = 'complete')
    Hclustering.fit(X)
    sm.accuracy_score(y, Hclustering.labels_)
    # -->0.4375

    Hclustering = AgglomerativeClustering(n_clusters = k, affinity = 'euclidian', linkage = 'average')            #BEST
    Hclustering.fit(X)
    sm.accuracy_score(y, Hclustering.labels_)
    # -->0.78125

    Hclustering = AgglomerativeClustering(n_clusters = k, affinity = 'manhattan', linkage = 'average')
    Hclustering.fit(X)
    sm.accuracy_score(y, Hclustering.labels_)
    # --> 0.71875

    # Instance-based learning with k-Nearest Neighbor
    import sklearn
    from sklearn import neighbors
    from sklearn import preprocessing
    from sklearn import metrics
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.cross_validation import train_test_split

    X_prime = cars.ix[:,(1,3,4,6)].values
    y = cars.ix[:,9].values

    X = preprocessing.preprocessing.scale(X_prime)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .33, random_state = 17)

    # Building and training your model with training data
    clf = neighbors.KNeighborsClassifier()
    clf.fit(X_train, y_train)
    print(clf)

    # Evaluating your model's predictions against the test dataset
    y_exepect = y_test
    y_pred = clf.predict(X_test)
    print(metrics.classification_report(y_exepect, y_pred))


#--------------------------------------------------------------------------------------------
# 7. Network Analysis with NetworkX
    #






#--------------------------------------------------------------------------------------------
# 7. Basic Algo Learning
def part7_algo():
    #-----------------------------------
    # Checking for missing values
    #-----------------------------------
    def fDf_HasMissingValue(X):
        missing_values = X==np.NAN
        x_missValue = X[missing_values == True]
        return x_missValue
    def fSer_MissingValue(df):
        ser_null = df.isnull().sum()
        return ser_null
    def check_enoughValues(df, int_nbColInput):
        int_len = len(df)
        int_len = int_len / int_nbColInput
        if int_len > 50:
            return True
        else: return False
    #-----------------------------------
    #Checking for independence between features
    #-----------------------------------
    def fBl_matrixCorrel(df):
        # Matrix of correlation
        m_corel = df.corr()
        print(m_corel)
    def fBl_spearmanrCorrel(seri_1, seri_2):
        spearmanr_coefficient, p_value = spearmanr(seri_1, seri_2)
        print ('Spearman Rank Correlation Coefficient %0.3f' % (spearmanr_coefficient))
        #print(p_value)
    #-----------------------------------
    # Charts
    #-----------------------------------
    def ch_pairplot(df):
        sb.pairplot(df)
    def ch_regplot(df, str_col1, str_col2, bl_scatter = True):
        sb.regplot(x = str_col1, y = str_col2, data = df, scatter = bl_scatter)
    def ch_countplot(df, str_col1, str_palette = 'hls'):
        sb.countplot(x = str_col1, data = df, palette = str_palette)
    
    #____CHAPTERS______________________________________________________________
    def A_LinearRegression(bl_showChart = False):
        df_enroll = pd.read_csv(r'enrollment_forecast.csv')
        # Graph to see correlation btw columns
        if bl_showChart:
            ch_pairplot(df_enroll)
        # Matrix of correlation
        fBl_matrixCorrel(df_enroll)
        
        # Choose coluns input / col result
        X = preprocessing.scale(df_enroll.iloc[:,2:4].values)
        y = df_enroll.iloc[:,1]
        
        LinReg = LinearRegression(normalize = True)
        LinReg.fit(X,y)
        return LinReg.score(X,y)
#    r = A_LinearRegression()
#    print(r)
     
    def B_LogicticRegression(bl_showChart = False):
        df_cars = pd.read_csv(r'mtcars.csv')
        df_cars.columns = ['car_names','mpg','cyl','disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']
        
        # Checking for missing values
        fSer_MissingValue(df_cars)
        print('enough values in df: ', check_enoughValues(df_cars, 2))
        
        # Graph to see correlation btw columns
        if bl_showChart:
            ch_regplot(df_cars, 'drat', 'carb')
        # Spearman Rank Correlation Coefficient (Need to be low:: no correlation btw different inputs)
        fBl_spearmanrCorrel(df_cars['drat'], df_cars['carb'])
        
        # Checking that your target is binary or ordinal
        if bl_showChart:
            ch_countplot(df_cars, 'am')
        
        # Choose coluns input / col result
        cars_data = df_cars.iloc[:,[5,11]].values
        X = preprocessing.scale(cars_data)
        y = df_cars.iloc[:,9].values
        
        LogReg = LogisticRegression()
        LogReg.fit(X,y)
        
        # Predict
        y_pred = LogReg.predict(X)
        matrix_report = classification_report(y, y_pred)
        print(matrix_report)
        
        flt_score = LogReg.score(X,y)
        return flt_score
#    r = B_LogicticRegression(True)
#    print(r)
    
part7_algo()












#=========================================================================================



