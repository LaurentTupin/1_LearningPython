
#============================================================================================
# Part of the LinkedIn course: Python for Data Science Essential Training
#============================================================================================

#2. Data Visualization Basics

# Install
pip install seaborn

# First example
	#Import
	import matplotlib.pyplot as plt
	from matplotlib import rcParams
	import seaborn

	#Other Import
	import numpy as np
	from numpy.random import randn
	import pandas as pd
	from pandas import Series, Dataframe
	
	#To keep the chart in Jupyter and not opening an external thing
	%matplotlib inline
	
	#Change the size & style of all charts
	rcParams['figure.figsize'] = 5,4
	seaborn.set_style('whitegrid')
	
	#Line Chart
	plt.plot(x,y)		#x,y being list of point
	
	#Several Line chart on the same chart
	plt.plot(x,y)
	plt.plot(x1,y1)	
	
	#---------With pd------------
	df_cars = pd.read_csv(path)
	mpg = df_cars['mpg']
	mpg.plot()
	#---------With pd 2------------
	df = [['cyl','wt','mpg']]
	df.plot()
	
	#Bar Chart
	plt.bar(x,y)		#x,y being list of point
	#---------With pd------------
	mpg.plot(kind = 'bar')
	mpg.plot(kind = 'barh')		# Horizontal Bar
	
	#Pie Chart
	plt.pie(x)		#x being list of point
	plt.show()
	
	#Saving a plot
	plt.savefig('FileName.jpeg')		#Working Directory		// To know it, type: %pwd
	plt.show()

	
# Define Plot Elements
	#Object Oriented Method
	fig = plt.figure()						#Generate blank figure	
	ax = fig.add_axes([0.1, 0.1, 1, 1])		#add axis	
	ax.plot(x,y)							#Show
	
	#With limit on axis + tick + grid
	fig = plt.figure()
	ax = fig.add_axes([0.1, 0.1, 1, 1])
	ax.set_xlim([1,9])
	ax.set_ylim([0,5])
	ax.set_xticks([1,2,4,5,6,8,9,10])
	ax.set_yticks([0,1,2,3,4,5])
	ax.grid()								#grid
	ax.plot(x,y)			
	
	#sub plot
	fig = plt.figure()
	fig, (ax1, ax2) = plt.subplots(1,2)
	ax1.plot(x)								#Function f(x) = x showed in this 1st Charts
	ax1.plot(x, y)
	
	
#Format Plot
	wide = [0.5,0.5,0.5,0.9,0.5,0.5,0.5,0.5]
	color = ['Salmon']
	plt.bar(x,y, width = wide, color = color, align = 'center')
	
	#Format df
	df = df_cars[['cyl','mpg','wt']]
	color_theme = ['darkgray','lightsalmon','powderblue']
	df.plot(color = color_theme)
	
	#Format Pie chart
	color_theme = ['#A9A9A9','#FFA07A','...','...','...']
	plt.pie(z, color = color_theme)
	plt.show()
	
	#Line style
	plt.plot(x,y, ls = 'steps', lw = 5)
	plt.plot(x1,y1, ls = '--', lw = 10)
	
	#Marker
	plt.plot(x,y,   marker = '1', mew = 20)
	plt.plot(x1,y1, marker = '+', mew = 15)
	
	
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
	seaborn.displot(mpg)			# show a Trend line as well (much better charts)
	
	#scatter plots
	cars.plot(kind='scatter', x='hp', y='mpg', c=['darkgray'], s = 150)
		# with seaborn
	seaborn.regplot(x='hp', y='mpg', data = cars, scatter = True)	# show a Trend line (much better charts)
	
	#scatter plots matrix
	seaborn.pairplot(cars)
		#Illisible
	
	cars_df = pd.DataFrame((cars.ix[:,(1,3,4,6)].values), columns = ['mpg','disp','hp','wt'])
	cars_target = cars[:,9].values
	target_names = [0, 1]
	cars_df['group'] = dp.Series(cars_target, dty = "category")
	seaborn.pairplot(cars_df, hue='group', palette='hls')
	 # Data Analysis:
		# Heavy cars are automatic, light cars are manual
		# Automatic cars have less Miles per gallon (but because they are heavier)
		
	#Box Plots
	cars.boxplot(column='mpg', by ='am')
	cars.boxplot(column='wt', by ='am')
		# with seaborn
	seaborn.boxplot(x='am', y='mpg', data = cars, palette='hls')
#--------------------------------------------------------------------
