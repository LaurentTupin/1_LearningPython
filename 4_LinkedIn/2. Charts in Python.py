
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
	
	
	
	
#Labels and Annotations
	#A. Labels
	plt.bar(x,y)
	plt.xlabel('your x-axis label')
	plt.ylabel('your y-axis label')
	
	#Pie Chart
	veh_type = ['bicycle', 'moto','car','van']
	plt.pie(z, labels = veh_type)
	plt.show()
	
	#Object Oriented Method
	mpg = df_cars['mpg']
	fig = plt.figure()						#Generate blank figure	
	ax = fig.add_axes([0.1, 0.1, 1, 1])		#add axis	
	mpg.plot()
	ax.set_xticks(range(32))	
	ax.set_title('Miles per galon of cars in mtcars')
	ax.set_xticklabels(cars['car_name'], rotation=60, fontsize = 'medium')
	ax.set_xlabel('Car name')
	ax.set_ylabel('Miles per gallon')
	
	#B. Legend
	#Pie Chart
	veh_type = ['bicycle', 'moto','car','van']
	plt.pie(z)
	plt.legend(veh_type, loc = 'best')
	plt.show()
	
	#Object Oriented Method
	fig = plt.figure()
	ax = fig.add_axes([0.1, 0.1, 1, 1])
	mpg.plot()
	ax.set_xticks(range(32))	
	ax.set_title('Miles per galon of cars in mtcars')
	ax.set_xticklabels(cars['car_name'], rotation=60, fontsize = 'medium')
	ax.set_xlabel('Car name')
	ax.set_ylabel('Miles per gallon')
	ax.legend(loc = 'best')
	
	#C. Annotate
	mpg.max()			#Find the max value = 33.9
	
	fig = plt.figure()
	ax = fig.add_axes([0.1, 0.1, 1, 1])
	mpg.plot()
	ax.set_xticks(range(32))	
	ax.set_title('Miles per galon of cars in mtcars')
	ax.set_xticklabels(cars['car_name'], rotation=60, fontsize = 'medium')
	ax.set_xlabel('Car name')
	ax.set_ylabel('Miles per gallon')
	ax.legend(loc = 'best')
	
	ax.annonate('Toyota Corrolla', xy = (19,33.9), xytext = (21,35), arrowprops = dict(facecolor='black', shrink=0.05))
	
	
#Create Vizu from Time Series Data
	df = pd.read_csv(..., index_col = 'Order Date', parse_dates = True)
	df.['order Quantity'].plot()
	#Cannot see anything because of too many Date
	
	df2 = df.sample(n=100, random_state = 25, axis = 0)
	df2.['order Quantity'].plot()
	
	
#Construct Histograms, box plots and scatter plots
	from pandas.tools.plotting import scatter_matrix
	
	#Call
	mpg.plot(kind = 'hist')
	#or (same same)
	plt.hist(mpg)
	plt.plot()
		# with seaborn
	sb.displot(mpg)			# show a Trend line as well (much better charts)
	
	#scatter plots
	cars.plot(kind='scatter', x='hp', y='mpg', c=['darkgray'], s = 150)
		# with seaborn
	sb.regplot(x='hp', y='mpg', data = cars, scatter = True)	# show a Trend line (much better charts)
	
	#scatter plots matrix
	sb.pairplot(cars)
		#Illisible
	
	cars_df = pd.DataFrame((cars.ix[:,(1,3,4,6)].values), columns = ['mpg','disp','hp','wt'])
	cars_target = cars[:,9].values
	target_names = [0, 1]
	cars_df['group'] = dp.Series(cars_target, dty = "category")
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
