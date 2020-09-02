'''
Liens: 
https://campus.datacamp.com/courses/intermediate-python/
Part of the LinkedIn course: Python for Data Science Essential Training
'''

# Liste Entrance
x = range(1, 10)
y = [1,2,3,4,0,4,3,2,1]
y1 = [9, 8,7, 6, 5, 4, 3, 2, 1]

year = list(range(1950, 2101))
pop = [2.53, 2.57, 2.62, 2.67, 2.71, 2.76, 2.81, 2.86, 2.92, 2.97, 3.03, 3.08, 
       3.14, 3.2, 3.26, 3.33, 3.4, 3.47, 3.54, 3.62, 3.69, 3.77, 3.84, 3.92, 
       4.0, 4.07, 4.15, 4.22, 4.3, 4.37, 4.45, 4.53, 4.61, 4.69, 4.78, 4.86, 
       4.95, 5.05, 5.14, 5.23, 5.32, 5.41, 5.49, 5.58, 5.66, 5.74, 5.82, 5.9, 
       5.98, 6.05, 6.13, 6.2, 6.28, 6.36, 6.44, 6.51, 6.59, 6.67, 6.75, 6.83, 
       6.92, 7.0, 7.08, 7.16, 7.24, 7.32, 7.4, 7.48, 7.56, 7.64, 7.72, 7.79, 
       7.87, 7.94, 8.01, 8.08, 8.15, 8.22, 8.29, 8.36, 8.42, 8.49, 8.56, 8.62, 
       8.68, 8.74, 8.8, 8.86, 8.92, 8.98, 9.04, 9.09, 9.15, 9.2, 9.26, 9.31, 
       9.36, 9.41, 9.46, 9.5, 9.55, 9.6, 9.64, 9.68, 9.73, 9.77, 9.81, 9.85, 
       9.88, 9.92, 9.96, 9.99, 10.03, 10.06, 10.09, 10.13, 10.16, 10.19, 10.22, 
       10.25, 10.28, 10.31, 10.33, 10.36, 10.38, 10.41, 10.43, 10.46, 10.48, 10.5, 
       10.52, 10.55, 10.57, 10.59, 10.61, 10.63, 10.65, 10.66, 10.68, 10.7, 10.72, 
       10.73, 10.75, 10.77, 10.78, 10.79, 10.81, 10.82, 10.83, 10.84, 10.85]
popPerCountry = [31.889923, 3.600523, 33.333216, 12.420476, 40.301927, 20.434176, 8.199783, 0.708573, 150.448339, 
                 10.392226, 8.078314, 9.119152, 4.552198, 1.639131, 190.010647, 7.322858, 14.326203, 8.390505, 
                 14.131858, 17.696293, 33.390141, 4.369038, 10.238807, 16.284741, 1318.683096, 44.22755, 0.71096, 
                 64.606759, 3.80061, 4.133884, 18.013409, 4.493312, 11.416987, 10.228744, 5.46812, 0.496374, 
                 9.319622, 13.75568, 80.264543, 6.939688, 0.551201, 4.906585, 76.511887, 5.23846, 61.083916, 
                 1.454867, 1.688359, 82.400996, 22.873338, 10.70629, 12.572928, 9.947814, 1.472041, 8.502814, 
                 7.483763, 6.980412, 9.956108, 0.301931, 1110.396331, 223.547, 69.45357, 27.499638, 4.109086, 
                 6.426679, 58.147733, 2.780132, 127.467972, 6.053193, 35.610177, 23.301725, 49.04479, 2.505559, 
                 3.921278, 2.012649, 3.193942, 6.036914, 19.167654, 13.327079, 24.821286, 12.031795, 3.270065, 
                 1.250882, 108.700891, 2.874127, 0.684736, 33.757175, 19.951656, 47.76198, 2.05508, 28.90179, 
                 16.570613, 4.115771, 5.675356, 12.894865, 135.031164, 4.627926, 3.204897, 169.270617, 3.242173, 
                 6.667147, 28.674757, 91.077287, 38.518241, 10.642836, 3.942491, 0.798094, 22.276056, 8.860588, 
                 0.199579, 27.601038, 12.267493, 10.150265, 6.144562, 4.553009, 5.447502, 2.009245, 9.118773, 
                 43.997828, 40.448191, 20.378239, 42.292929, 1.133066, 9.031088, 7.554661, 19.314747, 23.174294, 
                 38.13964, 65.068149, 5.701579, 1.056608, 10.276158, 71.158647, 29.170398, 60.776238, 301.139947, 
                 3.447496, 26.084662, 85.262356, 4.018332, 22.211743, 11.746035, 12.311143]
gdp_cap = [974.5803384, 5937.029525999998, 6223.367465, 4797.231267, 12779.37964, 
           34435.367439999995, 36126.4927, 29796.04834, 1391.253792, 33692.60508, 
           1441.284873, 3822.137084, 7446.298803, 12569.85177, 9065.800825, 10680.79282, 
           1217.032994, 430.0706916, 1713.778686, 2042.09524, 36319.23501, 706.016537, 
           1704.063724, 13171.63885, 4959.114854, 7006.580419, 986.1478792, 277.5518587, 
           3632.557798, 9645.06142, 1544.750112, 14619.222719999998, 8948.102923, 22833.30851, 
           35278.41874, 2082.4815670000007, 6025.3747520000015, 6873.262326000001, 5581.180998, 
           5728.353514, 12154.08975, 641.3695236000002, 690.8055759, 33207.0844, 30470.0167, 
           13206.48452, 752.7497265, 32170.37442, 1327.60891, 27538.41188, 5186.050003, 942.6542111, 
           579.2317429999998, 1201.637154, 3548.3308460000007, 39724.97867, 18008.94444, 36180.78919, 
           2452.210407, 3540.651564, 11605.71449, 4471.061906, 40675.99635, 25523.2771, 28569.7197, 
           7320.8802620000015, 31656.06806, 4519.461171, 1463.249282, 1593.06548, 23348.139730000006, 
           47306.98978, 10461.05868, 1569.331442, 414.5073415, 12057.49928, 1044.770126, 759.3499101, 
           12451.6558, 1042.581557, 1803.151496, 10956.99112, 11977.57496, 3095.7722710000007, 
           9253.896111, 3820.17523, 823.6856205, 944.0, 4811.060429, 1091.359778, 36797.93332, 
           25185.00911, 2749.320965, 619.6768923999998, 2013.977305, 49357.19017, 22316.19287, 
           2605.94758, 9809.185636, 4172.838464, 7408.905561, 3190.481016, 15389.924680000002, 
           20509.64777, 19328.70901, 7670.122558, 10808.47561, 863.0884639000002, 1598.435089, 
           21654.83194, 1712.472136, 9786.534714, 862.5407561000002, 47143.17964, 18678.31435, 
           25768.25759, 926.1410683, 9269.657808, 28821.0637, 3970.095407, 2602.394995, 4513.480643, 
           33859.74835, 37506.41907, 4184.548089, 28718.27684, 1107.482182, 7458.396326999998,
           882.9699437999999, 18008.50924, 7092.923025, 8458.276384, 1056.380121, 33203.26128, 
           42951.65309, 10611.46299, 11415.80569, 2441.576404, 3025.349798, 2280.769906, 1271.211593, 469.70929810000007]
life_exp = [43.828, 76.423, 72.301, 42.731, 75.32, 81.235, 79.829, 75.635, 64.062, 79.441, 56.728, 65.554, 74.852, 50.728, 
            72.39, 73.005, 52.295, 49.58, 59.723, 50.43, 80.653, 44.74100000000001, 50.651, 78.553, 72.961, 72.889, 65.152, 
            46.462, 55.322, 78.782, 48.328, 75.748, 78.273, 76.486, 78.332, 54.791, 72.235, 74.994, 71.33800000000002, 
            71.878, 51.57899999999999, 58.04, 52.947, 79.313, 80.657, 56.735, 59.448, 79.406, 60.022, 79.483, 70.259, 56.007, 
            46.38800000000001, 60.916, 70.19800000000001, 82.208, 73.33800000000002, 81.757, 64.69800000000001, 70.65, 70.964, 
            59.545, 78.885, 80.745, 80.546, 72.567, 82.603, 72.535, 54.11, 67.297, 78.623, 77.58800000000002, 71.993, 42.592, 
            45.678, 73.952, 59.44300000000001, 48.303, 74.241, 54.467, 64.164, 72.801, 76.195, 66.803, 74.543, 71.164, 42.082, 
            62.069, 52.90600000000001, 63.785, 79.762, 80.204, 72.899, 56.867, 46.859, 80.196, 75.64, 65.483, 
            75.53699999999998, 71.752, 71.421, 71.688, 75.563, 78.098, 78.74600000000002, 76.442, 72.476, 46.242, 65.528, 
            72.777, 63.062, 74.002, 42.56800000000001, 79.972, 74.663, 77.926, 48.159, 49.339, 80.941, 72.396, 58.556, 
            39.613, 80.884, 81.70100000000002, 74.143, 78.4, 52.517, 70.616, 58.42, 69.819, 73.923, 71.777, 51.542, 
            79.425, 78.242, 76.384, 73.747, 74.249, 73.422, 62.698, 42.38399999999999, 43.487]
CountryColor = ['red', 'green', 'blue', 'blue', 'yellow', 'black', 'green', 'red', 'red', 'green', 'blue', 'yellow', 
                'green', 'blue', 'yellow', 'green', 'blue', 'blue', 'red', 'blue', 'yellow', 'blue', 'blue', 'yellow', 
                'red', 'yellow', 'blue', 'blue', 'blue', 'yellow', 'blue', 'green', 'yellow', 'green', 'green', 'blue', 
                'yellow', 'yellow', 'blue', 'yellow', 'blue', 'blue', 'blue', 'green', 'green', 'blue', 'blue', 'green', 
                'blue', 'green', 'yellow', 'blue', 'blue', 'yellow', 'yellow', 'red', 'green', 'green', 'red', 'red', 
                'red', 'red', 'green', 'red', 'green', 'yellow', 'red', 'red', 'blue', 'red', 'red', 'red', 'red', 'blue', 
                'blue', 'blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'yellow', 'red', 'green', 'blue', 'blue', 
                'red', 'blue', 'red', 'green', 'black', 'yellow', 'blue', 'blue', 'green', 'red', 'red', 'yellow', 'yellow', 
                'yellow', 'red', 'green', 'green', 'yellow', 'blue', 'green', 'blue', 'blue', 'red', 'blue', 'green', 'blue', 
                'red', 'green', 'green', 'blue', 'blue', 'green', 'red', 'blue', 'blue', 'green', 'green', 'red', 'red', 
                'blue', 'red', 'blue', 'yellow', 'blue', 'green', 'blue', 'green', 'yellow', 'yellow', 'yellow', 'red', 
                'red', 'red', 'blue', 'blue']


#===================== Matplotlib ===============================

# Import 
import numpy as np
import pandas as pd
# Matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sb


#---------------------------------------------------------
# Notes
rcParams['figure.figsize'] = 10,4
sb.set_style('whitegrid')

# Colors
d_color1 = {'color':['darkgray','lightsalmon','powderblue']}
d_colorsPie1 = {'colors':['#A9A9A9','#FFA07A','#B0E0E6','#FFE4C4','#BDB76B']}


def Notes():
    # JUPYTER : To keep the chart in Jupyter and not opening an external thing
    ### %matplotlib inline
    
    #Change the size & style of all charts
    rcParams['figure.figsize'] = 5,4
    sb.set_style('whitegrid')
    
def SavePlotAsImage(plt, str_path):
    plt.savefig(str_path)
    plt.show()

def fDf_readDf_col(str_path, l_column = [], d_param = {}):
    df = pd.read_csv(str_path, **d_param)
    if l_column:
        df = df[l_column]
    return df



#===================== Object Oriented Method ===============================

def Define_figure(d_format):
    #Generate blank figure
    fig = plt.figure()
    #add axis
    fig = fig.add_axes(d_format['l_axes'])
    #With limit on axis + tick + grid
    if 'set_xlim' in d_format:        fig.set_xlim(d_format['set_xlim'])
    if 'set_ylim' in d_format:        fig.set_ylim(d_format['set_ylim'])
    if 'set_xticks' in d_format:      fig.set_xticks(d_format['set_xticks'])
    if 'set_xticklabels' in d_format: fig.set_xticklabels(d_format['set_xticklabels'], rotation=60, fontsize = 'medium')
    if 'set_yticks' in d_format:      fig.set_yticks(d_format['set_yticks'])
    if 'set_title' in d_format:       fig.set_title(d_format['set_title'])
    if 'set_xlabel' in d_format:      fig.set_xlabel(d_format['set_xlabel'])
    if 'set_ylabel' in d_format:      fig.set_ylabel(d_format['set_ylabel'])
    if 'bl_grid' in d_format:       fig.grid()
    if 'legend' in d_format:        fig.legend(**d_format['legend'])
    if 'annotate' in d_format:      fig.annotate(**d_format['annotate']) 
    return fig
#fig = Define_figure(d_format = dict(l_axes=[0.1, 0.1, 1, 1], set_xlim= [1,9], set_ylim= [0,5], bl_grid= True,
#                                    set_xticks= range(1,10), set_yticks= range(6),
#                                    set_xticklabels=['a','2','b','4','c','6','d','8','e'],
#                                    set_title= 'Miles per galon of cars in mtcars',
#                                    set_xlabel= 'Miles per galon of cars in mtcars',
#                                    set_ylabel= 'Miles per gallon',
#                                    legend= {'loc':'upper right'}, #best...
#                                    annotate= dict(s= 'Toyota Corrolla', xy= (4,4), xytext= (5,4.2), 
#                                                   arrowprops= dict(facecolor='red', shrink= 0.05))
#                                    ))
    

    
#--- LINE CHART ------------------------------------------------------
def LinePlot(x, y, o_fig = None):
    if o_fig:
        o_fig.plot(x, y)
    else:   
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
## With simple List
#LinePlot(x, y)
#LinePlot(x, y, o_fig = fig) 

def LinePlot_listOfLines(l_Line):
    for line in l_Line:
        x = line[0]
        y = line[1]
        d_format = line[2]
        plt.plot(x, y, **d_format)
        #        plt.plot(x,y, ls = 'steps', lw = 5)
        #         plt.plot(x1,y1, ls = '--', lw = 10)
        #        plt.plot(x,y,   marker = '1', mew = 20)
        #        plt.plot(x1,y1, marker = '+', mew = 15)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
## With several lines
#LinePlot_listOfLines([(x,y, {'ls' : 'steps', 'lw': 5, 'marker':1}), (x,y1, {'ls' : '--', 'lw' : 10})])
#LinePlot_listOfLines([(x,y, {'ls' : '--', 'marker':'1', 'mew':20}), (x,y1, {'ls' : '--', 'marker':'+', 'mew':5})])

def LinePlot_df(df, d_param = {}):
    df.plot(**d_param)
## With DataFrame
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['cyl','mpg', 'wt'])
#LinePlot_df(df_cars, d_param = d_color1)


#--- Pie Chart ------------------------------------------------------
def Pie_chart(x, d_param = {}, o_fig = None):
    if o_fig:
        o_fig.pie(x, **d_param)
    else:   
        plt.pie(x, **d_param)
        #plt.legend(['bicycle', 'moto','car','van'], loc = 'best')
        plt.show()
## With simple List
#Pie_chart(x)
## With Format
#Pie_chart(x, d_param = {**d_colorsPie1, 'labels' : ['bicycle', 'moto','car','van','bicycle', 'moto','car','car','van']})


#--- Bar Chart ------------------------------------------------------
def Bar_chart(x, y, d_param = {}, o_fig = None):
    if o_fig:
        o_fig.bar(x,y, **d_param)
    else:   
        plt.bar(x,y, **d_param)
        # Label sur Abscisse et ordonne
        plt.xlabel('x')
        plt.ylabel('y')
## With simple List
#Bar_chart(x = year, y = pop, o_fig = fig)
## Plus format
#Bar_chart(x, y, d_param = {'width' : [0.5,0.5,0.5,0.9,0.5,0.5,0.5,0.5,0.5], 'color' : ['Salmon'], 'align' : 'center'})

def Bar_df_path(df, d_param = {}, bl_vertical = True):    
    if bl_vertical:     df.plot(kind = 'bar', **d_param)
    else:               df.plot(kind = 'barh', **d_param)
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['mpg'])
#Bar_df_path(df_cars)


#--- Histogram ------------------------------------------------------
def Histogram(d_param):
    plt.hist(life_exp, **d_param)
    plt.show()
    # plt.clf() cleans it up again so you can start afresh ?????
    plt.clf()
#Histogram(d_param = dict(bins = 50))

def Histogram_df(df, d_param = {}):
    df.plot(kind = 'hist', **d_param)      
    ##     or   plt.hist(df, **d_param)
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['mpg'])
#Histogram_df(df_cars, d_param = dict(bins = 50))

def Hist_df_Trendline(df, d_param = {}):
    sb.distplot(df, **d_param)
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['mpg'])
#Hist_df_Trendline(df_cars, d_param = dict(bins = 15))


#--- Scatter plot ------------------------------------------------------
def ScatterPlot(bl_logX = False):
    # Size = pop
    np_popPerCountry = np.array(popPerCountry) * 2
    # color :       c
    # opacity :     alpha
    plt.scatter(gdp_cap, life_exp, s = np_popPerCountry, c = CountryColor, alpha = 0.8)
    if bl_logX:
        # Put the x-axis on a logarithmic scale
        plt.xscale('log')
    # Add axis labels
    plt.xlabel('GDP per Capita [in USD]')
    plt.ylabel('Life Expectancy [in years]')
    # Add title
    plt.title('World Development in 2007')
    # Ticks
    tick_val = [1000, 10000, 100000]
    tick_lab = ['1k', '10k', '100k']
    plt.xticks(tick_val, tick_lab)
    # Additional customizations
    plt.text(1550, 71, 'India')
    plt.text(5700, 80, 'China')    
    # Add grid() call
    plt.grid(True)
    
    # SHOW
    plt.show()
#ScatterPlot(True)

def ScatterPlot_df(df, d_param = {}):
    df.plot(kind = 'scatter', **d_param)
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['hp','mpg'])
#ScatterPlot_df(df_cars, d_param = dict(x='hp', y='mpg', c=['darkgray'], s=150))

def ScatterPlot_df_Trendline(df, d_param = {}):
    '''show a Trend line (much better charts)'''
    sb.regplot(data = df, scatter = True, **d_param)
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['hp','mpg'])
#ScatterPlot_df_Trendline(df_cars, d_param = dict(x='hp', y='mpg'))



#--- Scatter plot Matrix ------------------------------------------------------
def ScatterPlotMatrix(df, d_param = {}):
    sb.pairplot(df, **d_param)
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['hp','mpg'])
#ScatterPlotMatrix(df_cars)

def ScatterPlotMatrix_yIsColor(df, str_colNameYcolor, d_param = {}):
    sb.pairplot(df, hue = str_colNameYcolor, **d_param)
#df_cars = fDf_readDf_col(r'4_LinkedIn\mtcars.csv', ['mpg','disp','hp','wt', 'am'])
#ScatterPlotMatrix_yIsColor(df_cars, str_colNameYcolor = 'am', d_param = dict(palette='hls'))
    '''
    # Data Analysis:
    #   0 is automatic - 1 is manual transmission 
    #   wt: Heavy cars are automatic, light cars are manual
    #   mpg: Automatic cars have less Miles per gallon (but because they are heavier)
    '''







#===================== Create Vizu from Time Series Data =====================
def cours2_5():
    df_Superstore = fDf_readDf_col(r'4_LinkedIn\Superstore-Sales.csv', d_param = dict(index_col = 'Order Date', parse_dates = True))
    print(df_Superstore.head())
    # too heavy to see anything
    df_Superstore['Order Quantity'].plot()
    # need to take sample instead
    df2 = df_Superstore.sample(n = 100, random_state = 10, axis = 0)
    df2['Order Quantity'].plot()
    plt.ylabel('Order Quantity')
#cours2_5()





