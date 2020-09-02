
#============================================================================================
# Part of the LinkedIn course: Python for Data Science Essential Training
#============================================================================================


# First example
	#Import
	import matplotlib.pyplot as plt
	from matplotlib import rcParams
	import seaborn as sb

	#Other Import
	import numpy as np
	import pandas as pd
	from pandas import Series, Dataframe
	
	
	
#Construct Histograms, box plots and scatter plots
	
	#Call
	mpg.plot(kind = 'hist')
	#or (same same)
	plt.hist(mpg)
	plt.plot()
		# with seaborn
	sb.displot(mpg)			# show a Trend line as well (much better charts)
	
	#scatter plots
	cars.plot(kind='scatter', x='hp', y='mpg', c=['darkgray'], s=150)
		# with seaborn
	sb.regplot(x='hp', y='mpg', data = cars, scatter = True)	# show a Trend line (much better charts)
	
	#scatter plots matrix
	sb.pairplot(cars)
		#Illisible
    # Make differently
    cars_df = pd.DataFrame((df_cars.ix[:,(1,3,4,6)].values), columns = ['mpg','disp','hp','wt'])
    cars_target = df_cars[:,9].values
    target_names = [0, 1]
    cars_df['group'] = dp.Series(cars_target, dtype = "category")
    sb.pairplot(cars_df, hue='group', palette='hls')
         # Data Analysis:
        # Heavy cars are automatic, light cars are manual
        # Automatic cars have less Miles per gallon (but because they are heavier)


    
    
    
    
    
    
	#Box Plots
	cars.boxplot(column='mpg', by ='am')
	cars.boxplot(column='wt', by ='am')
		# with seaborn
	sb.boxplot(x='am', y='mpg', data = cars, palette='hls')
#--------------------------------------------------------------------