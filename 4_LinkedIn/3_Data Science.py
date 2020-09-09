'''
#============================================================================================
# Part of the LinkedIn course: Python for Data Science Essential Training
## https://www.linkedin.com/learning/python-for-data-science-essential-training/introduction-to-machine-learning?u=69004890
#============================================================================================
'''

import pandas as pd
import numpy as np
from collections import Counter

# Charts
import matplotlib.colors as matpltlib_color
import matplotlib.pyplot as plt
import seaborn as sb
from IPython.display import Image
from IPython.core.display import HTML
from pylab import rcParams
from mpl_toolkits.mplot3d import Axes3D

#Statistics
from scipy.stats import spearmanr, chi2_contingency
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, cophenet

# Data Science: scikit-learn (sklearn)
from sklearn import preprocessing, datasets, metrics
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import FactorAnalysis, PCA
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering




#==============================================================================
# Data
#==============================================================================
rcParams['figure.figsize'] = 10, 6
sb.set_style('whitegrid')
##  %matplotlib inline

def IrisData():
    df_iris = datasets.load_iris()
    #    print(iris.keys())
    l_feature_names = df_iris.feature_names
    l_target_names = df_iris.target_names
    # Build the data model
    X = df_iris.data
    y = df_iris.target
    return X, y, l_feature_names, l_target_names

def fDf_readDf_col(str_path, l_column = [], d_param = {}):
    df = pd.read_csv(str_path, **d_param)
    if l_column:
        df = df[l_column]
    return df

#==============================================================================
# Function
#==============================================================================
def fXy_transformDfIntoNpArr(df, str_targetName):
    y = df[str_targetName].values
    X = df.drop(str_targetName, axis=1).values
    return X, y

def dDf_TransformXinDf(X, l_feature_names):
    df = pd.DataFrame(X, columns = l_feature_names)
    return df

def dDf_TransformX_y_inDf(X, y, l_feature_names, str_yName = 'y_'):
    df = dDf_TransformXinDf(X, l_feature_names)
    df[str_yName] = y
    return df

def BoxPlot_sb(df, str_column = '', str_colBy = '', d_param = {}):
    plt.figure()
    if not str_column == '':    d_param['y'] = str_column
    if not str_colBy == '':     d_param['x'] = str_colBy
    sb.boxplot(data = df, **d_param)
    plt.show()
    
def ScatterPlotMatrix_yIsColor(df, str_colNameYcolor = None, d_param = {}):
    sb.pairplot(df, hue = str_colNameYcolor, **d_param)  

def ScatterPlot_df(df, d_param = {}):
    df.plot(kind = 'scatter', **d_param)


#==============================================================================
# Course: Dimensionality Reduction
#==============================================================================
def Factor_Analysis():
    '''
    # Factor Analysis - Assumptions:
        # 1. Features are Metrics
        # 2. Features are Continuous or ordinal
        # 3. Correlation r > 0.3 between features in your dataset
        # 4. More than 100 observations
        # 5. Sample is homogenous'''
    print('\n', '--- Factor_Analysis ----------------', '\n')
    # Data
    X, y, l_feature_names, l_target_names = IrisData()
    # Factor    
    factor = FactorAnalysis().fit(X)    
    df_factor = pd.DataFrame(factor.components_, columns = l_feature_names)
    print(df_factor)
    return df_factor
    
def SVD_Singular_Value_Decomposition():
    '''
    # Singular Value Decomposition (SVD):
        # Linear Algebra method
        # Decomposes a matrix into 3 MATRICES
        # To reduce information redundancy and noise
    # A = u*s*v
        # u : Left Orthogonal Matrix; holds important info about OBSERVATIONS
        # s : Diagonal Matrix; Contains info on decomposition processes performed during compression
        # v : Right Orthogonal Matrix; holds important info about FEATURES
    '''    
    
def PCA_Principal_Component_Analysis():
    '''
    PCA = Most common application of SVD
    Unsupervised ML algo
        Reduces variables down to a set of UNCORRELATED synthetic representations 
        Called : principal components
    '''
    
    # 1. Singular Value Decomposition (SVD)
    print('\n', '---SVD----------------')
    print(help(SVD_Singular_Value_Decomposition))
    
    # 2. PCA
    # Data
    X, y, l_feature_names, l_target_names = IrisData()
    print('\n', '---PCA----------------', '\n')
    print('X: ','\n', X[:10])
    pca = PCA()
    
    arr_pcaIris = pca.fit_transform(X)
    print('PCA on Iris: ','\n', arr_pcaIris[:10])
    
    arr_explainedVarRatio = pca.explained_variance_ratio_
    print('explained_variance_ratio_: \n This Tells how much information is compressed into the first few components'
          ,'\n Just make sure you keep at least 70% of the datasets original info \n', arr_explainedVarRatio)
    
    flt_cumulativeExplained_Var = arr_explainedVarRatio.sum()
    print('cumulative Explained Var: ','\n', flt_cumulativeExplained_Var)
    
    # keep only the first 2 compoments (its 97.7 % of the data) - the rest is junk / outliers data
    df_comps = pd.DataFrame(pca.components_, columns = l_feature_names)
    print('df_comps: ','\n', df_comps)
    return df_comps

def part4_DimensionalityReduction():
    df_factor = Factor_Analysis()
    df_comps = PCA_Principal_Component_Analysis()
    #    sb.heatmap(df_factor)
    #    sb.heatmap(df_comps)
#part4_DimensionalityReduction()




#--------------------------------------------------------------------------------------------
# 5. Outlier Analysis
#--------------------------------------------------------------------------------------------
def outlier_tukeyBoxplots(df):
    '''
    # Tukey Boxplots
        # IQR (spread) = Diff betweem the 1st Quartile(25%) and 3rd Quartile(75%)
        # a = Q1 - 1.5 IQR
        # b = Q3 + 1.5 IQR
        # Below a and above b, the variable is suspect for outliers
    '''
    BoxPlot_sb(df)
    #    df.boxplot(return_type = 'dict')
    #    plt.plot()
    
    # ANALYSIS
    #   On Sepal Width, you have point under 2.1 and above 4 which are outliers
    df_outliers = df[(df['sepal width (cm)'] > 4) | (df['sepal width (cm)'] < 2.05)]
    return df_outliers
    
def f_FindOutliers_fromQuantile(quantile25, quantile75):
    IQR = quantile75 - quantile25
    outlier_low = quantile25 - 1.5*IQR
    outlier_up = quantile75 + 1.5*IQR
    return outlier_low, outlier_up
#print(f_FindOutliers_fromQuantile(3.6,4.8))

def f_FindOutliersInSerie(ser):
    quantile25 = ser.quantile(0.25)
    quantile75 = ser.quantile(0.75)
    return f_FindOutliers_fromQuantile(quantile25, quantile75)

def fDf_findOutliers_Stat(df, l_col = []):
    df_outlierss = None
    if not l_col:
        l_col = df.columns
    for col in l_col:
        outlier_low, outlier_up = f_FindOutliersInSerie(df[col])
        df_outliers_col = df[(df[col] > outlier_up) | (df[col] < outlier_low)].copy()
        df_outliers_col['col'] = col
        if df_outlierss is None: df_outlierss = df_outliers_col.copy()
        else:                    df_outlierss = pd.concat([df_outlierss, df_outliers_col], sort = False)
    return df_outlierss

def outlier_DEBSCAN(df, flt_eps = 0.1):
    '''
    # DEBSCAN (Collective Outliers): unsupervised ML method that clusters core sample and denotes non-cores
    #   MAKE SURE less than 5% of the data is removed 
    #   ADJUST your model to make it so: 
    #   - eps           max distance btw 2 samples for them to be clustered (start at eps = 0.1)
    #           eps bas: on ne cluster pas et donc pas de outlier a definir
    #           eps haut: on cluster bcp et on peut donc mettre plein de groupe a exclure
    #   - min_samples   min number of samples to be qualified as a core point (start low)
    '''
    int_len = len(df)
    samp = int_len/2
    proportion_5p = 5/100
    proportion = 1.0
    # while to find the right sample
    while proportion > proportion_5p:
        samp -= max(int(samp/5), 1)
        model = DBSCAN(eps = flt_eps, min_samples = samp).fit(df)
        d_repartitionValue = Counter(model.labels_)
        proportion = d_repartitionValue[-1] / int_len 
    if proportion == 0:
        print('Increase the eps as nothing has been outlier. EPS = {}'.format(flt_eps))
        return None
    print('EPS', flt_eps, '| samp', samp, '| Lenght Outliers', d_repartitionValue[-1])
    return model


def part5_OutlierAnalysis():
    '''
    1. Point Outliers
    2. Contextual Ouliers (32 degre a Moscou en Janvier)
    3. Collective Outliers
    '''
    # Data
    X, y, l_feature_names, l_target_names = IrisData()
    df = dDf_TransformX_y_inDf(X, y, l_feature_names, 'y_Species')
    print(l_target_names)
    
    # 1. find Outliers with boxplot
    df_outliers = outlier_tukeyBoxplots(df)
    print(df_outliers)
    # find Outliers with Stats
    df_outliers = fDf_findOutliers_Stat(df)
    print(df_outliers)
    
    # 2. Multivariate Analysis for outlier detection
    #   Lets isolate this variable to have it on y and Species as x
    BoxPlot_sb(df, str_column = 'sepal width (cm)', str_colBy = 'y_Species', d_param = dict(palette = 'hls'))
    # Scatterplot
    ScatterPlotMatrix_yIsColor(df, str_colNameYcolor = 'y_Species', d_param = dict(palette = 'hls'))
    
    # 3. Collective Outliers : DEBSCAN
    print('Lenght de df', len(df), ' | 5% = ', len(df) * 0.05)
    for eps in range(1, 15):
        outlier_DEBSCAN(df, flt_eps = eps/10)
    # Decision
    model = DBSCAN(eps = 0.7, min_samples = 8).fit(df)
    # Get the outliers df
    df_outliers = df[model.labels_ == -1]
    print(df_outliers)
    ScatterPlot_df(df, d_param = dict(x = 'petal length (cm)', y = 'sepal width (cm)', s = 120, legend= {'loc':'upper right'},
                                      c = model.labels_, cmap = matpltlib_color.ListedColormap(['red','green','blue','black'])))
    ScatterPlot_df(df, d_param = dict(x = 'petal length (cm)', y = 'petal width (cm)', s = 120, legend= {'loc':'upper right'},
                                      c = model.labels_, cmap = matpltlib_color.ListedColormap(['red','green','blue','black'])))
    ScatterPlot_df(df, d_param = dict(x = 'sepal width (cm)', y = 'petal width (cm)', s = 120, legend= {'loc':'upper right'},
                                      c = model.labels_, cmap = matpltlib_color.ListedColormap(['red','green','blue','black'])))
    ### ........
#part5_OutlierAnalysis()




#--------------------------------------------------------------------------------------------
# 6. Cluster Analysis
#--------------------------------------------------------------------------------------------
def K_Means(df):
    '''
    Simple UnSupervised ML algo for quickly predict groupings from unlabeled dataset
     - Always Scale you variables
     - Look at scatterplot to estimate number of cluster centers, to set the parameter k
    '''
    int_clusters = len(df['y_Species'].unique())
    X = df[['sepal length (cm)','sepal width (cm)','petal length (cm)','petal width (cm)']]
    
    # Clustering
    clustering = KMeans(n_clusters = int_clusters, random_state = 5)
    clustering.fit(X)
    y_predictRelabel = np.choose(clustering.labels_, [1, 0, 2]).astype(np.int64)
    
    # plot
    c_theme = np.array(['darkgray', 'lightsalmon', 'powderblue'])
    plt.subplot(1,2,1)
    plt.scatter(x = df['petal length (cm)'], y = df['petal width (cm)'], 
                       c = c_theme[df['y_Species']], s = 50, alpha = 0.8)
    plt.title('Ground Truth Classification')
    plt.subplot(1,2,2)
    plt.scatter(x = df['petal length (cm)'], y = df['petal width (cm)'], 
                       c = c_theme[y_predictRelabel], s = 50, alpha = 0.8)
    plt.title('K-Means')
    
    # precision
    arr_precision = classification_report(df['y_Species'], y_predictRelabel)
    print(arr_precision)
    
    return clustering


def part6_ClusterAnalysis():
    # Data
    X, y, l_feature_names, l_target_names = IrisData()
    df = dDf_TransformX_y_inDf(X, y, l_feature_names, 'y_Species')
    print(l_target_names)
    df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['cyl','mpg', 'wt'])
    
    # K-Means Clustering
    K_Means(df)
    
    # Hierarchical methods (Hierarchical Clustering Dendrogram)
    np.set_printoptions(precision = 4, suppress = True)        # pas trop de chiffre ap. virgule
    

part6_ClusterAnalysis()







def part6_ClterAnalysis():
    
    

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
    metrics.accuracy_score(y, Hclustering.labels_)
    # -->0.78125

    Hclustering = AgglomerativeClustering(n_clusters = k, affinity = 'euclidian', linkage = 'complete')
    Hclustering.fit(X)
    sm.accuracy_score(y, Hclustering.labels_)
    # -->0.4375

    Hclustering = AgglomerativeClustering(n_clusters = k, affinity = 'euclidian', linkage = 'average')            #BEST
    Hclustering.fit(X)
    metrics.accuracy_score(y, Hclustering.labels_)
    # -->0.78125

    Hclustering = AgglomerativeClustering(n_clusters = k, affinity = 'manhattan', linkage = 'average')
    Hclustering.fit(X)
    metrics.accuracy_score(y, Hclustering.labels_)
    # --> 0.71875

    # Instance-based learning with k-Nearest Neighbor
    from sklearn import neighbors
    from sklearn import preprocessing
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
# 8. Basic Algo Learning
def part8_algo():
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
    
#part8_algo()












#=========================================================================================



