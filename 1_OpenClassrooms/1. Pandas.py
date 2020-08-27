#----------------------------------------------------------'
#Installer :
# -	Anaconda 2.3.0
# -	Jet Brains PyCharm Community Edition 4.0.3
# -	Pyodbc
#   o https://code.google.com/archive/p/pyodbc/downloads 
#   o 3.0.7 32-bit Windows Installer for Python 2.7       
#----------------------------------------------------------


#####################################
######## Fonction dans Cobra ########
##### Moocs Youtube Data School #####
#####################################

# 1. Import
import pandas as pd

# 2. Read Table
	# csv
	orders = pd.read_table('data/chip.csv')
	# url
	orders = pd.read_table('http://bit.ly/chiporders')
	# Separateur personnalisé
	orders = pd.read_table('http://bit.ly/movieusers', sep = '|')
	# with No header
	orders = pd.read_table('http://bit.ly/movieusers', sep = '|', header = None)
	# Définir le nom des colonnes
	user_cols = ['user_Id', 'age', 'gender', 'occupation', 'zip_code']
	orders = pd.read_table('http://bit.ly/movieusers', sep = '|', header = None, names = user_cols)
	# Remplacer le nom des colonnes
	orders = pd.read_table('http://bit.ly/movieusers', sep = '|', header = 0, names = user_cols)
		

# 3. read_csv
	# Use the ',' as default sep
	orders = pd.read_table('http://bit.ly/movieusers', sep = ',')
	# ou
	orders = pd.read_csv('http://bit.ly/movieusers')
	
	# COBRA
		extract = pd.read_csv(filePath, header=0)
		
	
# 4. dataFrame
	# Difference btw Data & Series
	'''DataFrame is actually stored in memory as a collection of Series	'''
	
	# Les objets issues de read_csv ou read_table sont des dataframe
	type (orders)				--> pandas.core.frame.dataFrame
	
	# Read dataFrame
	orders ['City'] 
	orders.City					# Same (dont work if there is a space)
	
	# Type = Series
	type(orders ['City'])		--> pandas.core.Series.Series
	
	# Creation de colonnes / Series
	orders ['Location'] = orders ['City'] + ', ' + orders ['State'] 
	
	# Decrire un dataFrame
	oders.shape		--> (960, 6)	#rows, columns
	orders.describe
		--> Count
			mean
			std
			min
			25%
			...
			max
	orders.dtypes		--> type des colonnes
	
	# column name
		orders.columns
			--> Index ([u'City', u'Colors Reported'...], dtype = 'object')
		
		orders.rename(columns = {'Colors Reported':'Colors_Reported'}, inplace = True)
			#Dico with key = old name and value = new name
			#Inplace = affect the dataFrame
		# or
		orders.columns = ['col1', 'col2', 'col3'...]
	# plus rapide
	orders.columns = orders.columns.str.replace(' ','_')
	
	
	# Drop
	ufo.drop('Colors reported', inplace=True, axis = 1)
	# Drop rows (the 2 first)
	ufo.drop([0, 1], inplace=True, axis = 0)
		# axis = 0 --> row
			#axis = 'index'
		# axis = 1 --> column
			# axis = 'columns'
		# Inplace = affect the dataFrame (update l'existante)
		
		# COBRA
		mat.drop(['IDX CLOSE', 'col 2', 'col 3'], inplace=True, axis=1)
	
	# focus : axis
		drinks.mean()
			# donne la moyenne de chaque colonnes (numérique bien sûr)
			# méthode automatiquement set sur les lignes, equivalent à :
		drinks.mean(axis = 'index')
		
		# Mais on peut aussi demander
		drinks.mean(axis = 'columns')
			# Fait la moyenne de chaque lignes en faisant la moyenne des colonnes
			# Aucun sens ici, juste pour info
			
	
	# Sort
	movies['title'].sort_values(ascending = False)
		--> Series, ne change pas le dataFrame sous-jacent
	movies.sort_values('title', ascending = True)
		--> Sort le dataFrame sous-jacent
	movies.sort_values(['title', 'duration'], ascending = True)
		--> sort sur plusieurs critères
		
		# COBRA (old version)
		mat = mat.sort(['DATE'], ascending=[1])
		# sort is not used anymore in PY 3
	
	# Filter
	movies[movies.duration >= 200]
			# Later: Filtre sur les lignes qui contiennent Chicken dans item_name
				orders[orders.['item_name'].str.contains('Chicken')]
	
	# loc
	movies.loc[movies.duration >= 200, 'genre']
		# Filtrer sur les lignes en duration et sélectionner uniquement la colonne Genre	
	
		# Détail : Liste en Série
			# Créer une liste de Bool à partir d'une Series
			booleans = []
			for lenght in movies.duration: 	#Series
				if lenght >= 200:
					booleans.append(True)
				else:
					booleans.append(False)
			# ou plus court	
			booleans = []
			booleans = movies.duration >= 200
			
			# Convertir une liste en Series
			series_bl_duration = pd.Series(booleans)
			# Filtrer (montre toutes les colonnes mais juste les lignes qui sont plus longues que 200 min)
			movies[series_bl_duration]
	
	# Multiple-Filter
		'''Drame de plus de 200 min'''
		movies[(movies.duration >= 200) & (movies.genre == 'Drama')]
		# & est comme un AND
		
		movies[(movies.duration >= 200) | (movies.genre == 'Drama')]
		# | est comme un OR
		
		movies[(movies.duration >= 200) & (movies.genre == 'Drama') | (movies.genre == 'Crime')]
		# ou
		movies[(movies.duration >= 200) & (movies.genre.isin(['Crime', 'Drama']))]
	
	
	# Filtrer sur les colonnes numériques
		import numpy as np
		drinks = pd.read_csv ('http...')
		drinks.select_dtypes(include = [np.number]).dtypes
	
	# Boucler
		for index, row in ufo.iterrows():
			print (index, row.city, row.State)
			
		# COBRA
		for i, d_param in all_etf.iterrows():
		
		# Udemy - Python Finance
		for stock_df, allo in zip([aapl,cisco,ibm,amzn],[0.3, 0.2, 0.4, 0.1]): 
			stock_df['Allocation'] = stock_df['Normed Return'] * allo
	
	
	# String method
		orders.['item_name'].str.upper()
			# Series de colonnes que l'on a remis en majuscules
		orders.['item_name'].str.contains('Chicken')
			# Series de Boolean True ou False si la valeur contient 'Chicken' ou pas
		
		# Filtre sur les lignes qui contiennent Chicken dans item_name
		orders[orders.['item_name'].str.contains('Chicken')]
		
		# Chainer les méthodes
		orders.['item_name'].str.replace('[','').str.replace(']','')
		
		# Remplacer les 2 à la fois
		orders.['item_name'].str.replace('[\[\]]','')
			# \[ 	-->		enlève '['
			# [] qui entoure indique que l'on utilise les méthodes REGEX
			
	# Changer le type d'une colonne
		drinks.dtypes
			--> contry 						object	(--> string)
				beer_servings				int64
				total_litre_pure_alcohol	float64
				continent					object
		
		# En replace : utiliser methode de Series
		drinks['beer_servings'] = drinks.beer_servings.astype(float)
		drinks.dtypes
			--> contry 						object
				beer_servings				float64
				total_litre_pure_alcohol	float64
				continent					object
		
		# Enlever le $ et convertir en float
		orders.item_price.str.replace('$','').astype(float).mean
			# on a la moyenne du prix car c'est converti en float
	
	# Group By
		import pandas as pd
		drinks = pd.read_csv('http:// bit.ly/drinksbycountry')*
		# moyenne de la conso bière
		drinks.beer_servings.mean()
			--> 106.16
		
		# Comment faire par Continent
		drinks.groupby('continent').beer_servings.mean()
			--> Africa			61
				Asia			37
				Europe			193
				North America	145
				
		# Pour avoir seulement l'afrique pour checker
		drinks[drinks.continent == 'Africa'].beer_servings.mean()
			--> 61
		
		# En ayant plusieurs aggrégats
		drinks.groupby('continent').beer_servings.agg(['count', 'min', 'max', 'mean'])
		
		# En faisant un graph direct de barre
		drinks.groupby('continent').beer_servings.mean().plot(kind = 'bar')
		
		
	# Travailler sur les Series
		movies.genre.value_counts()
			--> Drama	278
				Comedy	156
				Action	136...
		# Graph
		movies.genre.value_counts().plot(kind='bar')
		
		movies.genre.value_counts(normalize = True)
			--> Drama	28%
				Comedy	15%
				Action	13%...
		
		# Valeur unique
		movies.genre.unique()
			--> 16
		
		# Tableau croisé dynamique
		pd.crosstab(movies.genre, movies.content_rating)
			--> colonnes :
			Genre	Nb de film		A (notes)	B	C
			Action	10				2			5	3
			...
		
	# Handle missing values
		
	
	
	
	
	# COBRA
	--cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    --cursor = cnxn.cursor()
    --cursor.execute("SELECT TOP 1 str_IsinLongName "
    --               "FROM V_Ref_FundIsinPListing "
    --               "WHERE str_Isin = '" + isin + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['NAME'])
    name = str(extract.head(1)['NAME'].iloc[0])
	
	
	# COBRA	-- WHERE 
		mat['INDEX CLOSE'] = mat['INDEX CLOSE'].where(mat['INDEX CLOSE'].notnull(), mat['IDX CLOSE'])
	
	# COBRA
		mat_synth = pd.DataFrame()
		mat_synth.loc[0, 'NAME'] = mat.head(1)['NAME'].iloc[0]
		mat_synth.loc[0, 'ISIN'] = mat.head(1)['ISIN'].iloc[0]
	
	
	# shift
	pricesEtf['ETF RETURN'] = pricesEtf['ETF ADJ'] / pricesEtf['ETF ADJ'].shift(1) - 1
	pricesEtf['ETF RETURN'] = pricesEtf['ETF ADJ'].pct_change(1)
	
	# merge
	mat = pd.merge(mat, pricesIdx, how='left', on=['DATE', 'INDEX'])
	
	
	
	# ExcelWriter
	writer = pd.ExcelWriter(str.replace(fileFolder + '\\' + fileName, '\\\\', '\\'), datetime_format='yyyy-mm-dd')
    wb = writer.book
	wb.formats[0].font_size = 9
    mat_details.to_excel(writer, sheet_name='Details', index=False, startrow=2, startcol=0)
    mat_synth.to_excel(writer, sheet_name='Synthesis', index=False, startrow=2, startcol=0)
    ws_details = writer.sheets['Details']
    ws_synth = writer.sheets['Synthesis']
	
	


	

	
	
# NUMPY
	import numpy as np
	# isnan
		np.isnan
		# Je l'utilise pour savoir si une valeur dans un dataFrame is null
		(", NULL" if np.isnan(d_param['ETF PERF']) else ", " + str(d_param['ETF PERF']) + " ") +
	

	
	
	
#----------------------------------------------------------
# Exo & Fonction classique
#----------------------------------------------------------

# Volatilite
def Vol (Price):
	tab = pd.dataFrame()
	tab = price
	tab['return'] = tab['price'] / tab['price'].shift(1) -1
	return tab['return'].std(ddof = 1) * math.sqrt(252)
	
	
	