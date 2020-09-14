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
from sklearn import preprocessing, datasets, metrics, neighbors, naive_bayes
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.decomposition import FactorAnalysis, PCA
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split



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
# Charts
#==============================================================================
def BoxPlot_sb(df, str_column = '', str_colBy = '', d_param = {}):
    plt.figure()
    if not str_column == '':    d_param['y'] = str_column
    if not str_colBy == '':     d_param['x'] = str_colBy
    sb.boxplot(data = df, **d_param)
    plt.show()
def ScatterPlotMatrix_yIsColor(df, str_colNameYcolor = None, d_param = {}):
    sb.pairplot(df, hue = str_colNameYcolor, **d_param)  
def ch_pairplot(df):
    ScatterPlotMatrix_yIsColor(df)
def ScatterPlot_df(df, d_param = {}):
    df.plot(kind = 'scatter', **d_param)
def ch_regplot(df, str_col1, str_col2, bl_scatter = True):
    sb.regplot(x = str_col1, y = str_col2, data = df, scatter = bl_scatter)
def ch_countplot(df, str_col1, str_palette = 'hls'):
    sb.countplot(x = str_col1, data = df, palette = str_palette)



#==============================================================================
# Function
#==============================================================================
def fXy_dfInto_TrainTestSplit(df, str_targetColName = 'y', flt_testSize = 0.3, int_rdn = 0):
    X, y = fXy_transformDfIntoNpArr(df, str_targetColName)
    X_train, X_test, y_train, y_expect = train_test_split(X, y, test_size = flt_testSize, random_state = int_rdn)
    return X_train, X_test, y_train, y_expect
        
def fXy_dfInto_Scale_TrainTestSplit(df, str_targetColName = 'y', flt_testSize = 0.3, int_rdn = 0):
    X, y = fXy_dfInto_Scale(df, str_targetColName)
    X_train, X_test, y_train, y_expect = train_test_split(X, y, test_size = flt_testSize, random_state = int_rdn)
    return X_train, X_test, y_train, y_expect

def f_compScore_R_onModel(model,X,y):
    score_RegLin = model.score(X,y)
    print('Linear Regression R is : ', score_RegLin)
    return score_RegLin

def CompareScore_PredictionVsReality(y_expect, y_pred):
    comp = metrics.classification_report(y_expect, y_pred)
    print('classification report is : ', round(comp, 4))
    return comp

def f_compScore_accuracy(y_expect, y_pred):
    comp = accuracy_score(y_expect, y_pred)
    print('accuracy_score is : ', round(comp, 4))
    return comp


#-----------------------------------
# df <==> X, y
#-----------------------------------
def fXy_dfInto_Scale(df, str_targetColName = 'y'):
    X_noScale, y = fXy_transformDfIntoNpArr(df, str_targetColName)
    #X = preprocessing.scale(X_noScale)    # (CANNOT TAKE too long df)
    # Create the Scaler object
    scaler = preprocessing.StandardScaler()
    # Fit your data on the scaler object
    X = scaler.fit_transform(X_noScale)
    return X, y

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
    return m_corel
def fFlt_spearmanrCorrel(seri_1, seri_2):
    spearmanr_coef, p_value = spearmanr(seri_1, seri_2)
    print ('Spearman Rank Correlation Coefficient %0.3f' % (spearmanr_coef))
    return spearmanr_coef
def fBl_Independant_spearmanr(seri_1, seri_2):
    spearmanr_coef = fFlt_spearmanrCorrel(seri_1, seri_2)
    bl_indep = (spearmanr_coef < 0.8) and (spearmanr_coef > -0.8)
    print(' Series are indep: {}'.format(bl_indep))
    return bl_indep





#==============================================================================
# Course 4: Dimensionality Reduction
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
    sb.heatmap(df_factor)
    sb.heatmap(df_comps)
part4_DimensionalityReduction()




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
    X_scale = preprocessing.scale(X)
    
    # Clustering
    model_KMeans = KMeans(n_clusters = int_clusters, random_state = 5)
    model_KMeans.fit(X_scale)
    y_predictRelabel = np.choose(model_KMeans.labels_, [1, 0, 2]).astype(np.int64)
    
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
    CompareScore_PredictionVsReality(df['y_Species'], y_predictRelabel)
    return model_KMeans


def dendrogram_show(X):
    ward_linkage = linkage(X, 'ward')
    #    print(ward_linkage)
    plt.figure()
    dendrogram(ward_linkage, truncate_mode='lastp', p = 12, leaf_font_size = 15., show_contracted = True) # leaf_rotation = 45., 
    # plot details
    plt.title('Truncated Hierarchial Clustering Dendogram')
    plt.xlabel('Cluster Size')
    plt.ylabel('Distance')
    plt.axhline(y = 500)
    plt.axhline(y = 150)
    plt.show()

def Hierarchical_Clustering(df):
    '''
    UnSupervised ML algo to predict subgroups by their distance btw neighbors
     - Always Scale you variables
     - Look at scatterplot to estimate number of cluster centers, to set the parameter k
    '''
    X, y = fXy_transformDfIntoNpArr(df, 'am')
    dendrogram_show(X)
    #   ==> Datasets y is am (= 0 or 1), so lets subgroups by !!! 2 !!!
    #   ==> From the dendogram, we see that we have to set the MAX distance > 400 (otherwise we have more than 2 cluster)
    k_nbCLusters = 2
    #int_maxDist = 500
    d_result = {}
    l_affinity = ['euclidean', 'manhattan']
    l_linkage = ['ward','complete', 'average']
    for aff in l_affinity:
        for lnkg in l_linkage:
            try:
                Hclustering = AgglomerativeClustering(n_clusters = k_nbCLusters, affinity = aff, linkage = lnkg)
                Hclustering.fit(X)
            except Exception as err:    print(' ERROR in Hierarchical_Clustering: ({}, {}) || {} \n'.format(aff, lnkg, err))
            else:
                int_score = metrics.accuracy_score(y, Hclustering.labels_)
                if int_score in d_result:   
                    int_len = len(d_result[int_score])
                    d_result[int_score] = {**d_result[int_score], int_len: (aff, lnkg)}
                else:   d_result[int_score] = {0: (aff, lnkg)}
    flt_best = max(list(d_result.keys()))
    print('Best accuracy_score: ', flt_best)
    print('With the parameters: ', d_result[flt_best], '\n\n')
    
    
def K_NearestNeighbor(df):
    '''
    SUPERVISED ML algo to predict classification fo new unlabeled observations
     - Always Scale you variables
     - Too long on large datasets == SHITTY
    '''
    # Prepare your data
    X_train, X_test, y_train, y_expect = fXy_dfInto_Scale_TrainTestSplit(df, str_targetColName = 'am', flt_testSize = 0.33, int_rdn = 17)

    # Building and training your model with training data
    model_KNear = neighbors.KNeighborsClassifier()
    model_KNear.fit(X_train, y_train)
    # print(model_KNear)
    
    # Evaluating your model's predictions against the test dataset
    y_pred = model_KNear.predict(X_test)
    CompareScore_PredictionVsReality(y_expect, y_pred)
    return model_KNear
    
    
def part6_ClusterAnalysis():
    # pas trop de chiffre ap. virgule
    np.set_printoptions(precision = 4, suppress = True)
    # Data
    X, y, l_feature_names, l_target_names = IrisData()
    df_iris = dDf_TransformX_y_inDf(X, y, l_feature_names, 'y_Species')
    df_cars = fDf_readDf_col(r'mtcars.csv', ['mpg', 'disp', 'hp', 'wt', 'am'])
    
    # K-Means Clustering
    print(l_target_names)
    K_Means(df_iris)
    
    # Hierarchical methods (Hierarchical Clustering Dendrogram)
    Hierarchical_Clustering(df_cars)
    
    # K-Nearest Neighbor
    K_NearestNeighbor(df_cars)
    # RECALL means missing, Precision means right / wonrg
#part6_ClusterAnalysis()




#--------------------------------------------------------------------------------------------
# 7. Network Analysis with NetworkX
    ## NOTHING NOTED

#--------------------------------------------------------------------------------------------
# 8. Basic Algo Learning 
def Linear__Regression():
    '''
    Simple ML method you use to quantify and make predictions based on relations btw NUMERICAL Values
    '''
    df_enroll = pd.read_csv(r'enrollment_forecast.csv')
    df_enroll = df_enroll[['year','roll','unem','hgrad','inc']]
    # Graph to see correlation btw columns
    ch_pairplot(df_enroll)
    #   roll is linear with all. Unem is not great but acceptable
    #   All variables are numeric
    
    # Matrix of correlation - Check there is no correlation between variables
    fBl_matrixCorrel(df_enroll)
    #   hgrad and unem are not correlated, we will keep those 2
    
    # Choose coluns input / col result
    X, y = fXy_dfInto_Scale(df_enroll[['unem','hgrad','roll']], str_targetColName = 'roll')

    # Linear Reg
    model_LinReg = LinearRegression(normalize = True)
    model_LinReg.fit(X,y)
    
    # Score
    score_RegLin = f_compScore_R_onModel(model_LinReg, X, y)
    return score_RegLin


def Logictic__Regression():
    '''
    Simple ML method you use to predict numeric / categorical variable
    Diff with Linear Reg is that you predict Categroies for ordinal Var
     - Free of missing values
     - Predictant variable is binary / ordinal
    '''
    df_cars = pd.read_csv(r'mtcars.csv')
    df_cars.columns = ['car_names','mpg','cyl','disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']
    
    # Checking for missing values
    print('Nb of missing values in df: ', fSer_MissingValue(df_cars).sum())
    print('enough values in df: ', check_enoughValues(df_cars, 2))
    
    # Graph to see correlation btw columns
    ch_regplot(df_cars, 'drat', 'carb')
    # Spearman Rank Correlation Coefficient (Need to be low: no correlation btw different inputs)
    fBl_Independant_spearmanr(df_cars['drat'], df_cars['carb'])
    
    # Checking that your target is binary or ordinal
    #    ch_countplot(df_cars, 'am')
    
    # Choose coluns input / col result
    X, y = fXy_dfInto_Scale(df_cars[['drat','carb','am']], str_targetColName = 'am')

    model_LogReg = LogisticRegression(solver = 'lbfgs')
    model_LogReg.fit(X,y)
    
    # Score
    f_compScore_R_onModel(model_LogReg, X, y) # close to 1 means the model fit the data
    
    # Predict
    y_pred = model_LogReg.predict(X)
    CompareScore_PredictionVsReality(y, y_pred)
    
    
    
def NaiveBayes_Multinomial(X_train, X_test, y_train, y_expect):
    model_ = naive_bayes.MultinomialNB()
    model_.fit(X_train, y_train)
    # Evaluating your model's predictions against the test dataset
    y_pred = model_.predict(X_test)
    f_compScore_accuracy(y_expect, y_pred)
     
def NaiveBayes_Bernoulli(X_train, X_test, y_train, y_expect, o_binarize = True):
    model_ = naive_bayes.BernoulliNB(binarize = o_binarize)
    model_.fit(X_train, y_train)
    # Evaluating your model's predictions against the test dataset
    y_pred = model_.predict(X_test)
    f_compScore_accuracy(y_expect, y_pred)
    
def NaiveBayes_Gaussian(X_train, X_test, y_train, y_expect):
    model_ = naive_bayes.GaussianNB()
    model_.fit(X_train, y_train)
    # Evaluating your model's predictions against the test dataset
    y_pred = model_.predict(X_test)
    f_compScore_accuracy(y_expect, y_pred)
    
def NaiveBayes_Classifier():
    '''
    Likelyhood of an event to occur (Conditional Probability)
    DO NOT SCALE DATA
     - Multinomial  - Good when your feature describe discrete frequency counts (ex: words counting)
     - Bernoulli    - Good for make predictions from binary features
     - Gaussian     - When distribution is normal
    '''
    # Prepare your data
    df_spam = pd.read_csv(r'spambase.data.csv', header = None)
    X_train, X_test, y_train, y_expect = fXy_dfInto_TrainTestSplit(df_spam, str_targetColName = 57, flt_testSize = 0.33, int_rdn = 17)
    X_train = X_train[:, :48]
    X_test = X_test[:, :48]
    
    # NaiveBayes_Multinomial
    NaiveBayes_Multinomial(X_train, X_test, y_train, y_expect)
    # Bernoulli
    NaiveBayes_Bernoulli(X_train, X_test, y_train, y_expect)
    NaiveBayes_Bernoulli(X_train, X_test, y_train, y_expect, o_binarize = 0.1)
    # Gaussian
    NaiveBayes_Gaussian(X_train, X_test, y_train, y_expect)

def part8_algo():
    Linear__Regression()
    Logictic__Regression()
    NaiveBayes_Classifier()
#part8_algo()



#--------------------------------------------------------------------------------------------
# 9. Web Based Data Visualization
    ## NOTHING NOTED
