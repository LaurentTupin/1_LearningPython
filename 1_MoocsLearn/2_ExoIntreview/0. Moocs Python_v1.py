#----------------------------------------------------------
#Installer :
# -	Anaconda 2.3.0
# -	Jet Brains PyCharm Community Edition 4.0.3
# -	Pyodbc
#   o https://code.google.com/archive/p/pyodbc/downloads
#   o 3.0.7 32-bit Windows Installer for Python 2.7       
#----------------------------------------------------------

#----------------------------------------------------------
# Moocs : Youtube
# Moocs : https://openclassrooms.com 
#          Laurent.tu...               mv.3
#----------------------------------------------------------


#Type num�rique
	--> type(variable)
	int
	long 	#Pr�cision illimit�
	float	#Pr�cision limit�
	complex		
		c = 1 + 3 j
		c.real 	--> 1.0
		c.imag 	--> 3.0
	#Conversion
		int(4.3)  	--> 4
	#Op�ration
		5 / 3  	--> 1
		5 % 3  	--> 2 		#modulo
		5 / 3.0  	--> 1.6666666 
		5 / float(3)  --> 1.6666666 
		5 // 3.1  --> 1.0	# Division enti�re
		1 < 3  	--> True
		3**2  	--> 9		#Puissance
		sqrt(9)	--> 3		#Racine carr� (from math import *)
	#Autres op�rations
		#On peut affecter une m�me valeur � plusieurs variables :
		>>> x = y = 3
		#Permutation de variables
		>>> a,b = b,a # permutation
	# condition
		if a.isdigit():

#S�quence
	String
	Liste
	Tuple
	
#String
	#on peut couper une instruction, pour l'�crire sur deux lignes
	>>> 1 + 4 - 3 * 19 + 33 - 45 * 2 + (8 - 3) \
	... -6 + 23.5
	#le symbole � \ � permet, avant un saut de ligne,
	#d'indiquer � Python que � cette instruction se poursuit � la ligne suivante �. 
	
	#Pour �crire un v�ritable anti-slash dans une cha�ne, il faut le doubler : � \\ �
	
	#Permet d'�crire plusieurs lignes
	>>> chaine3 = """Ceci est un nouvel
	... essai sur plusieurs
	... lignes"""
	
	#� \n � symbolise un saut de ligne
	
	#Youtube
	s = 'egg, bacon'		#String de 10 caract�res
	S[0]  	--> 'e'
	s[9]  	--> 'n'
	'x' in s  	-->  False
	s + ' and spam'  --> 'egg, bacon and spam'
	len(s)  	--> 10
	min(s)  	--> ' '
	max(s)  	--> 'o'
	s.index('g')  --> 1	#Position du premier 'g' (commence � 0)
	s.count('g')  --> 2
	s * 3  		--> 'egg, baconegg, baconegg, bacon'
	'#' * 30  	--> '################################################'
	
	
	#Slicing
		egg, bacon
		0123456789
		s[0:3]  	--> 'egg'		# 0 inclus : 3 exclus
		s[:3]  		--> 'egg'
		s[5:10]  	--> 'bacon'	# 5 inclus : 10 exclus (max est 10)
		s[5:]  		--> 'bacon'		# 5 inclus : fin
		s[:]				# Copie de s (Shalow copy)
	#Pas sur un clicing
		s[0:10:2]   --> 'eg ao'	# Pas de 2
		s[::2]   	--> 'eg ao'
		s[:8:3]   	--> 'e,a'
	#Autres
		s[100] 		--> Error
		s[5:100]  	--> 'bacon'		# �a fonctionne
		s[50:100]  	--> ''			# �a fonctionne mais retourne vide
	# N�gatif
		#Ordre normal
		e	g	g	,		b	a	c	o	n
		-10 -9	-8	-7	-6	-5	-4	-3	-2	-1
		s[-10:-7] 	--> 'egg'
		s[:-3] 		-->'egg, ba'
		#Ordre inverse
		s[::-1] 	--> 'nocab , gge'
		s[2:0:-1] 	--> 'gg'
		s[2::-1] 	--> 'gge'
		
# String (compl�ments)
	# *** Est immuable, si op�ration --> nouvelle string affect� � variable ***
	
	# M�thode
	'spam'.upper() 	--> 'SPAM'
	'SPAM'.lower()
	'SPAM'.reverse() 	--> 'MAPS'
	'spam'.replace ('s', 'p') 	--> 'ppam'
	
	# Changement par liste
	s = "le poulet, c'est bon"
	l = s.split()
	l 		--> ['le', 'poulet,', "c'est", 'bon']
	l[3] 	--> 'bon'
	l[3] = 'mauvais'
	s = " ".join(l)
	s 		--> "le poulet, c'est mauvais"
	s = "-".join(l)
	s 		--> "le-poulet,-c'est-mauvais"
	
	#Boucle For : String = Liste
	chaine = "Bonjour les ZER0S"		#Lettre est une variable cr��e par le for, ce n'est pas � vous de l'instancier. 
	for lettre in chaine:
		if lettre in "AEIOUYaeiouy": 
			print(lettre + ' est une voyelle')
		
	
	
	
#Liste
	#Liste ne stocke que r�f�rence vers objet
	# donc ne prend pas de place (juste adresse)
	
	# ********* M�me op�ration car s�quence *********
	
	# Range (c'est une liste)
		range(3) 		--> [0, 1 , 2]
		range(1, 10, 2) --> [1, 3 , 5, 7, 9]
	
	l = []	# liste vide
	l = [4,' spam', True, 3.2]
	l[3] 		--> 3.2
	l[0] = l[0] + 2
	l 			-->  [6, 'spam', True, 3.2]
	l[1:2] 		-->  'spam'
	
	# Ins�rer
		l[1:2] = ['egg', 'spam']
		l 		-->  [6,'egg', 'spam', True, 3.2]
		l[3:4] = ['egg', 'beans']
		l 		-->  [6,'egg', 'spam', 'egg', 'beans', 3.2]	# ca a enlev� TRUE
	# Contracter ou effacer
		l[1:3] = []	# liste vide
		l 		-->  [6, 'egg', 'beans', 3.2]	# ca a enlev� TRUE
	
	# Econome en m�moire car pas de copie
		# append
			l.append('34')
			l 		-->  [6, 'egg', 'beans', 3.2, '34']
		# extend ()
			l.extend([3, 5, 9])
			l 		-->  [6, 'egg', 'beans', 3.2, '34', 3, 5, 9]
		#Supprimer
			del l[0] 		# On supprime le premier �l�ment de la liste
			l.remove('a') 	#Attention ne supprime que la premiere occurrence !
			l = [i for i in l if i != 'a']
			
		# pop
			#Retourne le dernier �l�ment de la liste et l'enl�ve de la liste
			l.pop 	-->  9
			l 		-->  [6, 'egg', 'beans', 3.2, '34', 3, 5]
	
	#Fonction ordre
		l.sort()
		sorted(l)
		l.reverse()
		# Exemple :  prendre le 3�me plus grand mots
			sorted(s, key=len, reverse=True)[2]
		
		

#Tuple
	# ********* M�me op�ration car s�quence *********
	# Comme liste mais immuable (pas de modification apr�s cr�ation)
	
	t = ()	# liste vide	
	type(t) 		-->  <type 'tuple'>
	
	t = (4, )			# Seulement si un seul �l�ment
	t = (4, 'spam')
	
	#On peut omettre les ()
	t = 4, 'spam'
	
	# Convertir en liste pour le modifier
	l = list(t)
	l.append('x')
	t = tuple(l)
	t 		-->  (4, 'spam', 'x')
	
# IF
	if 'x' in l:
		print 'Bravo'
	elif 'n' in l:
		print 'pas mal'
	else:
		'shit'

# Boucle
	# FOR
	for x in range(1,11):
		print x , x**2
	
	# WHILE
	L = range(10)
	while L:
		L.pop(0)
		print L
		--> 0
		--> [1,2,3,4,5,6,7,8,9]
		--> 1
		--> [2,3,4,5,6,7,8,9]
	#On sort au bout de 10
	while True: 	#ne s'arr�te jamais
		s=raw_input('Question ?')
		if 'non' in s:
			break
			#Sort de la boucle while si l'utilisateur met 'non'
	

# Fonction
	l = [1, 3, 8]
	l2 = [2, 5, 10]
	
	def fct_carre(l):
		for x in l:
			print x, x**2
		# Si aucun Return, �a retourne <None>
		# Sinon : 
		Return 'fin'

	-->fct_carre(l)
	-->fct_carre(l2)
	
	#Description
	def table(nb, max=10):
		"""Fonction affichant la table de multiplication par nb 
		de 1*nb � max*nb (max >= 0)"""
		# La chaine qui permet de d�finir la fonction est une docString
		# Si on tape help(table), elle s'affichera

		
# Dictionnaire
	# ----- Voire Table de hash ----- 
	# Definition: Collection non ordonn�e de couple Cl�-Valeur
	
	#Cr�ation
		d = dict()
		d = dict{}
		# A la main
		d = {'marc' : 39, 'alice' : 30, 'eric' : 38}
		# par liste de Tuple
		l = [('marc',39),('alice',30),('eric',38)]
		d = dict(l)
	
	#Op�ration
		len(d) 		--> 3 
		'marc' in d 	--> True
		'louis' in d 	--> False
		'louis' not in d 	--> True
		d['marc']	--> 39
		del['marc']
		d 			-->  {'alice' : 30, 'eric' : 38}
		
	#Liste
		d.keys()	--> ['alice','eric']
		d.values()	--> [30, 38]
		d.items()	--> [('alice',30),('eric',38)]

		
# Set (ensemble)
	# Definition : Ensemble non ordonn� d'objet unique (objet immuable)
	
	#Cr�ation
		# A la main
		s = {1,2,3,'spam'}
		# par liste 
		l = [1,2,3,3,'spam']
		s = set(l)
		s		--> set([1,2,3,'spam'])  #Objet doit �tre unique
	#Op�ration
		s.add('egg')
		s		--> set([1,2,3,'egg','spam'])
		s.remove(2)
		s		--> set([1,3,'egg','spam'])
		s.update([5,6])
		s		--> set([1,3,5,6,'egg','spam'])
	#Diff�rence
		s2 = {1,5,'ham'}
		s - s2 	--> set([3,6,'egg','spam'])				# Diff�rence
		s | s2 	--> set([1,3,5,6,'egg','spam','ham'])	# Union
		s & s2 	--> set([1,5])							# Intersection

	#FrozenSet (Set immuable)
		fs = frozenset(s)
		fs.add(3)  --> Error 
		
		
# R�f�rence partag�e
	# -- au moins 2 variables r�f�rence un m�me objet --
	a = [1,2]
	b = a
	a[0] = 'spam'
	b[0] 	--> 'spam' # et non pas 1
	
	#Shalow Copy
	# -- Faire que b reste le m�me --
	b = a[:]
	a[0] = 'spam'
	b[0] 	--> 1
		#Exception
		a = [1,[2]]
		b = a[:]
		a [1][0] = 'Spam'
		b [1][0]	--> 'spam' # et non pas 1
		#Comment �viter cela
		import Copy
		a = [1,[2]]
		b = copy.deepcopy(a)
		a [1][0] = 'Spam'
		b [1][0]	--> 2
		
#Module (Fichier .py)
	import math
	dir(math)  	--> toutes les fonctions du module math
	help(math)	--> toute l'aide
	help(math.tan)	--> Retrun the tan of x...
	math.log(10)	--> 2.302...
	
# Revenir sur if
	# Est consid�r� comme faux :
	False 0 [] {} () '' None
	# Tester si c'est un chiffre
	s = '123'
	if s.isdigit():
		p = int(s) + 10		# Ca fonctionne
	
# ITERATEUR
	# tout les built-in has an iterator (you can make a boucle FOR on it)
	s = {1, 2, 3, 'a'}
	for i in s: ...
	
	#Iter
	it = s.__iter__()
	it.next		--> 'a'
	it.next		--> 1
	it.next		--> 2
	it.next		--> 3
	it.next		--> ERREUR StopIteration
	# Un it�rateur ne peut parcourir un objet qu'une seule fois
	# Objet a 2 m�thodes 
		__iter__()
		next()
	# Donc
	L = [1,2,3]
	it = L.__iter__()
	it2 = L.__iter__()
		it is it2  	--> False
	
	
#Liste de lecture 4		

# FICHIER
	#Ecrire
	f = open (r'C:\tmp\spam.txt', 'w')
	# r = raw string
	#w : write (va cr�er le fichier ou le vider
	for i in range(100):
		line = '{} {}\n'.format(i, i**2)
		#\n : retour chariot
		f.write(line)
	f.close()		#Save et close
	
	#Lire 
	#parcourir les lignes car un fichier a un it�rateur par ligne
	f = open (r'C:\tmp\spam.txt', 'r')
	f2 = open (r'C:\tmp\spam2.txt', 'w')
	for l in f:
		f2.write(l.replace(' ',', '))
	f.close()
	f2.close()
	
# Fonction LAMBDA
	f = lambda x: x**2 - 3
	f(1) 	--> -2  	#Aucun inter�t
	
	#On peut mettre dans une liste
	L = [lambda x : x**2 - 3, lambda x : x**3 - 5]
	# Puis faire :
	def f(x): 
		print x, x(3)		# x est donc une fonction
	f(L[0])		--> 	<fonction <lambda> at 0x02b684> 1
		# x : Adresse de la fonction, x(3) = 1
	
	# On aurait pu faire direct
	f(lambda x : x**2 - 3)
	
#MAP
	L = range(10)
	map(lambda x : x**2, L)
		--> [0,1,4,9,16,25,36,49,64,81]

#FILTER
	filter(lambda x : x % 2 ==0, L]
		--> [0,2,4,6,8]
	
# Compr�hension de liste
# Puissance des it�rateurs avec syntaxe simple
	# Comme MAP
	[x**2 for x in range(10)]
		--> [0,1,4,9,16,25,36,49,64,81]
	
	# Comme FILTER
	[x**2 for x in range(10) if x % 7 ==0]
		--> [0,49]
	
	#Compr�hension de SET (idem)
	{i**3 for i range(10)}
		--> set([0,1,8,64,512,343,216,729,27,125])
	
	#Compr�hension de Dictionnaire (idem)
	{i: i **2 for i in range(10)}
		--> {0:0, 1:1, 2:4, 3:9, 4:16, 5:25, 6:36, 7:49, 8:64, 9:81}
	# Changer des dico
	d = {123 : 'marc', 145 : 'eric', 655 : 'jean'}
	d[123]		--> 'marc'
	# Le dico n'est pas fait pour acc�der au cl� par valeur
	# Sans faire de mani�re it�rative
	# --> renverser dictionnaire � l'envers
	d2 = {d(k) : k for k in d}
	d2['eric']		--> 145
	
#4.5







	
	
	


#----------------------------------------------------------
# Moocs : https://openclassrooms.com 
#          Laurent.tu...               mv2.
#----------------------------------------------------------


#----------------------------------------------------------
# 2.5. Les Fichiers
#----------------------------------------------------------







#----------------------------------------------------------


#----------------------------------------------------------
# 2.4. Les Dictionnaires
#----------------------------------------------------------



			#Les parenth�ses d�limitent les tuples, les crochets [] d�limitent les listes 
			# et les accolades {} d�limitent les dictionnaires.
			
#Voyons comment ajouter des cl�s et valeurs dans notre dictionnaire vide :
>>> mon_dictionnaire = {}
>>> mon_dictionnaire["pseudo"] = "Prolixe"
>>> mon_dictionnaire["mot de passe"] = "*"
>>> mon_dictionnaire
{'mot de passe': '*', 'pseudo': 'Prolixe'}
>>>
			
#Nous indiquons entre crochets la cl� � laquelle nous souhaitons acc�der. 
#Si la cl� n'existe pas, elle est ajout�e au dictionnaire avec la valeur sp�cifi�e apr�s le signe =. 
#Sinon, l'ancienne valeur � l'emplacement indiqu� est remplac�e par la nouvelle :
>>> mon_dictionnaire = {}
>>> mon_dictionnaire["pseudo"] = "Prolixe"
>>> mon_dictionnaire["mot de passe"] = "*"
>>> mon_dictionnaire["pseudo"] = "6pri1"
>>> mon_dictionnaire
{'mot de passe': '*', 'pseudo': '6pri1'}
>>>

#Pour acc�der � la valeur d'une cl� pr�cise, c'est tr�s simple :
>>> mon_dictionnaire["mot de passe"]
'*'
>>>
			#Si la cl� n'existe pas dans le dictionnaire, une exception de type KeyError sera lev�e.

			#Exemple : Ech�quier
			echiquier = {}
			echiquier['a', 1] = "tour blanche" # En bas � gauche de l'�chiquier
			echiquier['b', 1] = "cavalier blanc" # � droite de la tour
			echiquier['c', 1] = "fou blanc" # � droite du cavalier
			echiquier['d', 1] = "reine blanche" # � droite du fou
			# ... Premi�re ligne des blancs
			echiquier['a', 2] = "pion blanc" # Devant la tour
			echiquier['b', 2] = "pion blanc" # Devant le cavalier, � droite du pion
			# ... Seconde ligne des blancs
			
#On peut aussi cr�er des dictionnaires d�j� remplis :
placard = {"chemise":3, "pantalon":6, "tee-shirt":7}
			
#Supprimer des cl�s d'un dictionnaire
placard = {"chemise":3, "pantalon":6, "tee shirt":7}
del placard["chemise"]

#La m�thode pop supprime �galement la cl� pr�cis�e mais elle renvoie la valeur supprim�e :
>>> placard = {"chemise":3, "pantalon":6, "tee shirt":7}
>>> placard.pop("chemise")
3
>>>


# On se sert parfois des dictionnaires pour stocker des fonctions.
>>> print_2 = print # L'objet print_2 pointera sur la fonction print
>>> print_2("Affichons un message")
Affichons un message
>>>

			#En pratique, on affecte rarement des fonctions de cette mani�re. C'est peu utile. 
			#Par contre, on met parfois des fonctions dans des dictionnaires :
			
>>> def fete():
...     print("C'est la f�te.")
... 
>>> def oiseau():
...     print("Fais comme l'oiseau...")
...
>>> fonctions = {}
>>> fonctions["fete"] = fete # on ne met pas les parenth�ses
>>> fonctions["oiseau"] = oiseau
>>> fonctions["oiseau"]
<function oiseau at 0x00BA5198>
>>> fonctions["oiseau"]() # on essaye de l'appeler
Fais comme l'oiseau...
>>>

			#On commence par d�finir deux fonctions, fete et oiseau (pardonnez l'exemple).
			#On cr�e un dictionnaire nomm� fonctions
			#On met dans ce dictionnaire les fonctions fete et oiseau. 
						#La cl� pointant vers la fonction est le nom de la fonction, tout b�tement, 
						#mais on aurait pu lui donner un nom plus original.
			#On essaye d'acc�der � la fonction oiseau en tapant fonctions[� oiseau �]. 
						#Python nous renvoie un truc assez moche, <function oiseau at 0x00BA5198>, 
						#mais vous comprenez l'id�e : c'est bel et bien notre fonction oiseau. 
						#Toutefois, pour l'appeler, il faut des parenth�ses, comme pour toute fonction qui se respecte.
			#En tapant fonctions["oiseau"](), on acc�de � la fonction oiseau et on l'appelle dans la foul�e.


#LES METHODES DE PARCOURS

#Parcours des cl�s
>>> fruits = {"pommes":21, "melons":3, "poires":31}                                
>>> for cle in fruits:
			#ou 
			#for cle in fruits.keys():
...     print(cle)
... 
melons
poires
pommes
>>>
			
			#La m�thode keys (� cl�s � en anglais) renvoie la liste des cl�s contenues dans le dictionnaire. 
			# En v�rit�, ce n'est pas tout � fait une liste (essayez de taper fruits.keys() dans votre interpr�teur) 
			# mais c'est une s�quence qui se parcourt comme une liste.

#Parcours des valeurs
>>> fruits = {"pommes":21, "melons":3, "poires":31}
>>> for valeur in fruits.values():
...     print(valeur)
... 
3
31
21
>>>

#Condition
>>> if 21 in fruits.values():
...     print("Un des fruits se trouve dans la quantit� 21.")
... 
Un des fruits se trouve dans la quantit� 21.
>>>


#Parcours des cl�s et valeurs simultan�ment       
			#Pour avoir en m�me temps les indices et les objets d'une liste, on utilise la fonction enumerate 
			#Pour faire de m�me avec les dictionnaires, on utilise la m�thode items
			#Elle renvoie une liste, contenant les couples cl� : valeur, sous la forme d'un tuple. 
			
>>> fruits = {"pommes":21, "melons":3, "poires":31}
>>> for cle, valeur in fruits.items():
...     print("La cl� {} contient la valeur {}.".format(cle, valeur))
... 
La cl� melons contient la valeur 3.
La cl� poires contient la valeur 31.
La cl� pommes contient la valeur 21.
>>>



#LES DICTIONNAIRES ET PARAM�TRES DE FONCTION

			#on avait r�ussi � intercepter tous les param�tres de la fonction� sauf les param�tres nomm�s.
			
#R�cup�rer les param�tres nomm�s dans un dictionnaire
>>> def fonction_inconnue(**parametres_nommes):
...     """Fonction permettant de voir comment r�cup�rer les param�tres nomm�s
...     dans un dictionnaire"""
...     
...     
...     print("J'ai re�u en param�tres nomm�s : {}.".format(parametres_nommes))
... 
>>> fonction_inconnue() # Aucun param�tre
J'ai re�u en param�tres nomm�s : {}
>>> fonction_inconnue(p=4, j=8)
J'ai re�u en param�tres nomm�s : {'p': 4, 'j': 8}
>>>
			
			#Pour capturer tous les param�tres nomm�s non pr�cis�s dans un dictionnaire, il faut mettre deux �toiles ** avant le nom du param�tre.
			#Si vous passez des param�tres non nomm�s � cette fonction, Python l�vera une exception.

#Ainsi, pour avoir une fonction qui accepte n'importe quel type de param�tres, 
#nomm�s ou non, dans n'importe quel ordre, dans n'importe quelle quantit�, il faut la d�clarer de cette mani�re :
def fonction_inconnue(*en_liste, **en_dictionnaire):     


#Transformer un dictionnaire en param�tres nomm�s d'une fonction
>>> parametres = {"sep":" >> ", "end":" -\n"}
>>> print("Voici", "un", "exemple", "d'appel", **parametres)
Voici >> un >> exemple >> d'appel -
>>>
			#Les param�tres nomm�s sont transmis � la fonction par un dictionnaire. 
			#Pour indiquer � Python que le dictionnaire doit �tre transmis comme des param�tres nomm�s, 
			# on place deux �toiles avant son nom ** dans l'appel de la fonction.

#Comme vous pouvez le voir, c'est comme si nous avions �crit :
>>> print("Voici", "un", "exemple", "d'appel", sep=" >> ", end=" -\n")
Voici >> un >> exemple >> d'appel -
>>>

#----------------------------------------------------------





#----------------------------------------------------------
# 2.3. LES LISTES ET TUPLES (2/2)
#----------------------------------------------------------

#Pour � convertir � une cha�ne en liste, on va utiliser une m�thode de cha�ne nomm�e split 
>>> ma_chaine = "Bonjour � tous"
>>> ma_chaine.split(" ")
['Bonjour', '�', 'tous']
>>>

#Pour � convertir � une liste en cha�ne
>>> ma_liste = ['Bonjour', '�', 'tous']
>>> " ".join(ma_liste)
'Bonjour � tous'
>>>

#Une application pratique
#si on a un nombre flottant tel que � 3.999999999999998 �, on souhaite obtenir comme r�sultat � 3.999 �
>>> afficher_flottant(3.99999999999998)
'3,999'

def afficher_flottant(flottant):
			#"""Fonction prenant en param�tre un flottant et renvoyant une cha�ne de caract�res repr�sentant la troncature de ce nombre. 
			#La partie flottante doit avoir une longueur maximum de 3 caract�res.
			#De plus, on va remplacer le point d�cimal par la virgule"""
			
			if type(flottant) is not float:
						raise TypeError("Le param�tre attendu doit �tre un flottant")
			flottant = str(flottant)
			partie_entiere, partie_flottante = flottant.split(".")
			# La partie enti�re n'est pas � modifier
			# Seule la partie flottante doit �tre tronqu�e
			return ",".join([partie_entiere, partie_flottante[:3]])


#Les fonctions dont on ne conna�t pas � l'avance le nombre de param�tres
>>> def fonction_inconnue(*parametres):
...     """Test d'une fonction pouvant �tre appel�e avec un nombre variable de param�tres"""
...     
...     print("J'ai re�u : {}.".format(parametres))
... 
>>> fonction_inconnue() # On appelle la fonction sans param�tre
J'ai re�u : ().
>>> fonction_inconnue(33)
J'ai re�u : (33,).
>>> fonction_inconnue('a', 'e', 'f')
J'ai re�u : ('a', 'e', 'f').
>>> var = 3.5
>>> fonction_inconnue(var, [4], "...")
J'ai re�u : (3.5, [4], '...').
>>>#Python va placer tous les param�tres de la fonction dans un tuple, 
#que l'on peut ensuite traiter comme on le souhaite.

def fonction_inconnue(nom, prenom, *commentaires):
>>>#vous devez imp�rativement pr�ciser un nom et un pr�nom, et ensuite vous mettez ce que vous voulez

 
def afficher(*parametres, sep=' ', fin='\n'):
			"""Fonction charg�e de reproduire le comportement de print.
			
			Elle doit finir par faire appel � print pour afficher le r�sultat.
			Mais les param�tres devront d�j� avoir �t� format�s. 
			On doit passer � print une unique cha�ne, en lui sp�cifiant de ne rien mettre � la fin :

			print(chaine, end='')"""
			
			# Les param�tres sont sous la forme d'un tuple
			# Or on a besoin de les convertir
			# Mais on ne peut pas modifier un tuple
			# On a plusieurs possibilit�s, ici je choisis de convertir le tuple en liste
			parametres = list(parametres)
			# On va commencer par convertir toutes les valeurs en cha�ne
			# Sinon on va avoir quelques probl�mes lors du join
			for i, parametre in enumerate(parametres):
						parametres[i] = str(parametre)
			# La liste des param�tres ne contient plus que des cha�nes de caract�res
			# � pr�sent on va constituer la cha�ne finale
			chaine = sep.join(parametres)
			# On ajoute le param�tre fin � la fin de la cha�ne
			chaine += fin
			# On affiche l'ensemble
			print(chaine, end='')
  
  
#On utilise une �toile * dans les deux cas. 
#Si c'est dans une d�finition de fonction, cela signifie que les param�tres fournis non attendus 
#lors de l'appel seront captur�s dans la variable, sous la forme d'un tuple. 
#Si c'est dans un appel de fonction, au contraire, cela signifie que la variable 
#sera d�compos�e en plusieurs param�tres envoy�s � la fonction.
>>> liste_des_parametres = [1, 4, 9, 16, 25, 36]
>>> print(*liste_des_parametres)
1 4 9 16 25 36
>>>



#Les compr�hensions de liste
			"Les compr�hensions de liste (� list comprehensions � en anglais) sont un moyen de filtrer ou modifier une liste tr�s simplement."
			"Les compr�hensions de liste permettent de parcourir une liste en en renvoyant une seconde, modifi�e ou filtr�e."
			#S'�crit : nouvelle_squence = [element for element in ancienne_squence if condition]
			
#Metttre au carr�
>>> liste_origine = [0, 1, 2, 3, 4, 5]
>>> [nb * nb for nb in liste_origine]
[0, 1, 4, 9, 16, 25]
>>>
			# nb * nb <--> nb**2

#Filter sur les chiffres pairs
>>> liste_origine = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> [nb for nb in liste_origine if nb % 2 == 0]
[2, 4, 6, 8, 10]
>>>

#Diminuer de 1 et Filter sur les chiffres < 1
>>> qtt_a_retirer = 7 # On retire chaque semaine 7 fruits de chaque sorte
>>> fruits_stockes = [15, 3, 18, 21] # Par exemple 15 pommes, 3 melons...
>>> [nb_fruits - qtt_a_retirer for nb_fruits in fruits_stockes if nb_fruits > qtt_a_retirer]
[8, 11, 14]
>>>

#_____________________________________________________
#Exo
			#La liste contient des tuples, contenant chacun un couple : le nom du fruit et sa quantit� en magasin.
			>>> inventaire = [
			...     ("pommes", 22),
			...     ("melons", 4),
			...     ("poires", 18),
			...     ("fraises", 76),
			...     ("prunes", 51),
			... ]
			>>>
			#Trier la liste pour avoir
			[
						("fraises", 76),
						("prunes", 51),
						("pommes", 22),
						("poires", 18),
						("melons", 4),
			]

#Solution 1
			# On change le sens de l'inventaire, la quantit� avant le nom
			inventaire_inverse = [(qtt, nom_fruit) for nom_fruit,qtt in inventaire]
			# On n'a plus qu'� trier dans l'ordre d�croissant l'inventaire invers�
			# On reconstitue l'inventaire tri�
			inventaire = [(nom_fruit, qtt) for qtt,nom_fruit in sorted(inventaire_inverse, \
						reverse=True)]
						
#Solution 2
			# On change le sens de l'inventaire, la quantit� avant le nom
			inventaire_inverse = [(qtt, nom_fruit) for nom_fruit,qtt in inventaire]
			# On trie l'inventaire invers� dans l'ordre d�croissant
			inventaire_inverse.sort(reverse=True)
			# Et on reconstitue l'inventaire
			inventaire = [(nom_fruit, qtt) for qtt,nom_fruit in inventaire_inverse]
#_____________________________________________________

#--------------------------------------------------------------------------------




#----------------------------------------------------------
# 2.2. LES LISTES ET TUPLES (1/2)
#----------------------------------------------------------

#Cr�ation de listes
>>> ma_liste = list() # On cr�e une liste vide
>>> type(ma_liste)
<class 'list'>
>>> ma_liste
[]
>>>
#Autres m�thode
>>> ma_liste = [] # On cr�e une liste vide
>>>
#Liste non vide
>>> ma_liste = [1, 2, 3, 4, 5] # Une liste avec cinq objets
>>> print(ma_liste)
[1, 2, 3, 4, 5]
>>>

#Liste de liste
>>> ma_liste = [1, 3.5, "une chaine", []]
>>>

#Acc�der aux �l�ments d'une liste
>>> ma_liste = ['c', 'f', 'm']
>>> ma_liste[0] # On acc�de au premier �l�ment de la liste
'c'
>>> ma_liste[2] # Troisi�me �l�ment
'm'
>>> ma_liste[1] = 'Z' # On remplace 'f' par 'Z'
>>> ma_liste
['c', 'Z', 'm']
>>>

#Ajouter un �l�ment � la fin de la liste
>>> ma_liste = [1, 2, 3]
>>> ma_liste.append(56) # On ajoute 56 � la fin de la liste
>>> ma_liste
[1, 2, 3, 56]
>>>

#La m�thode append, comme beaucoup de m�thodes de listes, travaille directement sur l'objet et ne renvoie donc rien !
>>> chaine1 = "une petite phrase"
>>> chaine2 = chaine1.upper() # On met en majuscules chaine1
>>> chaine1                   # On affiche la cha�ne d'origine
'une petite phrase'
>>> # Elle n'a pas �t� modifi�e par la m�thode upper
... chaine2                   # On affiche chaine2
'UNE PETITE PHRASE'
>>> # C'est chaine2 qui contient la cha�ne en majuscules
... # Voyons pour les listes � pr�sent
... liste1 = [1, 5.5, 18]
>>> liste2 = liste1.append(-15) # On ajoute -15 � liste1
>>> liste1                      # On affiche liste1
[1, 5.5, 18, -15]
>>> # Cette fois, l'appel de la m�thode a modifi� l'objet d'origine (liste1)
... # Voyons ce que contient liste2
... liste2
>>> # Rien ? V�rifions avec print
... print(liste2)
None
>>>

#ins�rer un �l�ment dans une liste au milieu
>>> ma_liste = ['a', 'b', 'd', 'e']
>>> ma_liste.insert(2, 'c') # On ins�re 'c' � l'indice 2
>>> print(ma_liste)
['a', 'b', 'c', 'd', 'e']
>>> #La m�thode va d�caler les objets d'indice sup�rieur ou �gal � 2. c va donc s'intercaler entre b et d.

#Concat�nation de listes
>>> ma_liste1 = [3, 4, 5]
>>> ma_liste2 = [8, 9, 10]
>>> ma_liste1.extend(ma_liste2) # On ins�re ma_liste2 � la fin de ma_liste1
>>> print(ma_liste1)
[3, 4, 5, 8, 9, 10]
>>> ma_liste1 = [3, 4, 5]
>>> ma_liste1 + ma_liste2
[3, 4, 5, 8, 9, 10]
>>> ma_liste1 += ma_liste2 # Identique � extend
>>> print(ma_liste1)
[3, 4, 5, 8, 9, 10]
>>>

# DELETE
>>> ma_liste = [-5, -2, 1, 4, 7, 10]
>>> del ma_liste[0] # On supprime le premier �l�ment de la liste
>>> ma_liste
[-2, 1, 4, 7, 10]
>>> del ma_liste[2] # On supprime le troisi�me �l�ment de la liste
>>> ma_liste
[-2, 1, 7, 10]
>>>

# REMOVE
#On peut aussi supprimer des �l�ments de la liste gr�ce � la m�thode remove 
#qui prend en param�tre non pas l'indice de l'�l�ment � supprimer, mais l'�l�ment lui-m�me.
>>> ma_liste = [31, 32, 33, 34, 35]
>>> ma_liste.remove(32)
>>> ma_liste
[31, 33, 34, 35]
>>> #La m�thode remove ne retire que la premi�re occurrence de la valeur trouv�e dans la liste !


#PARCOURIR une liste
>>> ma_liste = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
>>> i = 0 # Notre indice pour la boucle while
>>> while i < len(ma_liste):
...     print(ma_liste[i])
...     i += 1 # On incr�mente i, ne pas oublier !

>>> # Cette m�thode est cependant pr�f�rable
... for elt in ma_liste: # elt va prendre les valeurs successives des �l�ments de ma_liste
...     print(elt)


#La fonction ENUMERATE et les TUPLES
>>> ma_liste = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
>>> for i, elt in enumerate(ma_liste):
...     print("� l'indice {} se trouve {}.".format(i, elt))
... 
� l'indice 0 se trouve a.
� l'indice 1 se trouve b.
� l'indice 2 se trouve c.
� l'indice 3 se trouve d.
� l'indice 4 se trouve e.
� l'indice 5 se trouve f.
� l'indice 6 se trouve g.
� l'indice 7 se trouve h.
>>>
>>> for elt in enumerate(ma_liste):
...     print(elt)
... 
(0, 'a')
(1, 'b')
(2, 'c')
(3, 'd')
(4, 'e')
(5, 'f')
(6, 'g')
(7, 'h')
>>>#Quand on parcourt chaque �l�ment de l'objet renvoy� par enumerate, 
#on voit des tuples qui contiennent deux �l�ments : d'abord l'indice, 
#puis l'objet se trouvant � cet indice dans la liste pass�e en argument � la fonction enumerate.

>>> autre_liste = [
...     [1, 'a'],
...     [4, 'd'],
...     [7, 'g'],
...     [26, 'z'],
...         ] # J'ai �tal� la liste sur plusieurs lignes
>>> for nb, lettre in autre_liste:
...     print("La lettre {} est la {}e de l'alphabet.".format(lettre, nb))
La lettre a est la 1e de l'alphabet.
La lettre d est la 4e de l'alphabet.
La lettre g est la 7e de l'alphabet.
La lettre z est la 26e de l'alphabet.
>>>


#Nous avons bri�vement vu les tuples un peu plus haut, gr�ce � la fonction enumerate. 
#Les tuples sont des listes immuables, qu'on ne peut modifier. #
#En fait, vous allez vous rendre compte que nous utilisons depuis longtemps des tuples sans nous en rendre compte.
#Un tuple se d�finit comme une liste, sauf qu'on utilise comme d�limiteur des parenth�ses au lieu des crochets.
tuple_vide = ()
tuple_non_vide = (1,) # est �quivalent � ci dessous
tuple_non_vide = 1,
tuple_avec_plusieurs_valeurs = (1, 2, 5)
# � la diff�rence des listes, les tuples, une fois cr��s, ne peuvent �tre modifi�s : 
#  on ne peut plus y ajouter d'objet ou en retirer.


#Une fonction renvoyant plusieurs valeurs
def decomposer(entier, divise_par):
			"""Cette fonction retourne la partie enti�re et le reste de
			entier / divise_par"""

			p_e = entier // divise_par
			reste = entier % divise_par
			return p_e, reste
>>> #Et on peut ensuite capturer la partie enti�re et le reste dans deux variables, au retour de la fonction :
>>> partie_entiere, reste = decomposer(20, 3)
>>> partie_entiere
6
>>> reste
2
>>>#Si vous essayez de faire retour = decomposer(20, 3), vous allez capturer un tuple contenant deux �l�ments : 
#la partie enti�re et le reste de 20 divis� par 3.





#----------------------------------------------------------
# 2.1. Notre premier objet : les cha�nes de caract�res
#----------------------------------------------------------

# Mettre la cha�ne en minuscule
>>> chaine = "NE CRIE PAS SI FORT !"
>>> chaine.lower()               
'ne crie pas si fort !'

# Si vous tapez type(chaine) dans l'interpr�teur, vous obtenez <class 'str'>
# Un objet est issu d'une classe. 
# Les fonctions d�finies dans une classe sont appel�es des m�thodes.

# objet.methode()
# Une classe est un mod�le qui servira � construire un objet ; 
#c'est dans la classe qu'on va d�finir les m�thodes propres � l'objet.

# l'utilisateur peut taper � q � en majuscule ou en minuscule, la boucle s'arr�tera
chaine = str() # Cr�e une cha�ne vide
# On aurait obtenu le m�me r�sultat en tapant chaine = ""
while chaine.lower() != "q":
			print("Tapez 'Q' pour quitter...")
			chaine = input()
print("Merci !")

#str() cr�e un objet cha�ne de caract�res

>>> minuscules = "une chaine en minuscules"
>>> minuscules.upper() # Mettre en majuscules
'UNE CHAINE EN MINUSCULES'
>>> minuscules.capitalize() # La premi�re lettre en majuscule
'Une chaine en minuscules'
>>> espaces = "   une  chaine avec  des espaces   "
>>> espaces.strip() # On retire les espaces au d�but et � la fin de la cha�ne
'une  chaine avec  des espaces'
>>> titre = "introduction"
>>> titre.upper().center(20)
'    INTRODUCTION    '
>>> prenom = "Paul"
>>> nom = "Dupont"
>>> age = 21
>>> print("Je m'appelle {0} {1} et j'ai {2} ans.".format(prenom, nom, age))
Je m'appelle Paul Dupont et j'ai 21 ans.

#Ou bien la stocker : 
>>> nouvelle_chaine = "Je m'appelle {0} {1} et j'ai {2} ans.".format(prenom, nom, age)

>>> prenom = "Paul"
>>> nom = "Dupont"
>>> age = 21
>>> print( \
...   "Je m'appelle {0} {1} ({3} {0} pour l'administration) et j'ai {2} " \
...   "ans.".format(prenom, nom, age, nom.upper()))
Je m appelle Paul Dupont (DUPONT Paul pour l'administration) et j'ai 21 ans.
#J'ai coup� notre instruction, plut�t longue, � l'aide du signe � \ � plac� avant un saut de ligne, 
#pour indiquer � Python que l'instruction se prolongeait au-dessous.


#Seconde syntaxe de la m�thode format
# formatage d'une adresse
>>> adresse = "{no_rue}, {nom_rue}, {code_postal}, {nom_ville}".format(no_rue=5, nom_rue="rue des Postes", code_postal=75003, nom_ville="Paris")
>>> print(adresse)
5, rue des Postes 75003 Paris (France)

#La concat�nation de cha�nes
>>> prenom = "Paul"
>>> message = "Bonjour"
>>> chaine_complete = message + prenom # On utilise le symbole '+' pour concat�ner deux cha�nes
... print(chaine_complete) # R�sultat :
BonjourPaul
>>> # Pas encore parfait, il manque un espace
... chaine_complete = message + " " + prenom
>>> print(chaine_complete) # R�sultat :
Bonjour Paul

#La Conversion de donn�es : Str
>>> age = 21
>>> message = "J'ai " + str(age) + " ans."
>>> print(message)
J'ai 21 ans.
>>>

#Parcours et s�lection de cha�nes par indices
#s�lectionner la premi�re lettre d'une cha�ne
>>> chaine = "Salut les ZER0S !"
>>> chaine[0] # Premi�re lettre de la cha�ne
'S'
>>> chaine[2] # Troisi�me lettre de la cha�ne
'l'
>>> chaine[-1] # Derni�re lettre de la cha�ne
'!'
#Rappelez-vous, on commence � compter � partir de 0. La premi�re lettre est donc � l'indice 0

#La longueur de la cha�ne 
>>> chaine = "Salut"
>>> len(chaine)
5


#M�thode de parcours par while
chaine = "Salut"
i = 0 # On appelle l'indice 'i' par convention
while i < len(chaine):
			print(chaine[i]) # On affiche le caract�re � chaque tour de boucle
			i += 1

#Enfin, une derni�re petite chose : vous ne pouvez changer les lettres de la cha�ne en utilisant les indices.
>>> mot = "lac"
>>> mot[0] = "b" # On veut remplacer 'l' par 'b'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
#Python n'est pas content. Il ne veut pas que vous utilisiez les indices pour modifier des caract�res de la cha�ne. 
#Pour ce faire, il va falloir utiliser la s�lection.

#S�lection de cha�nes
>>> presentation = "salut"
>>> presentation[0:2] # On s�lectionne les deux premi�res lettres
'sa'
>>> presentation[2:len(presentation)] # On s�lectionne la cha�ne sauf les deux premi�res lettres
'lut'
>>> presentation[:2] # Du d�but jusqu'� la troisi�me lettre non comprise
'sa'
>>> presentation[2:] # De la troisi�me lettre (comprise) � la fin
'lut'

#Remplacer les caract�res d'une String
>>> mot = "lac"
>>> mot = "b" + mot[1:]
>>> print(mot)
bac
# Plutot : nous avons � notre disposition les m�thodes count, find et replace




#----------------------------------------------------------
# 1.9. TP
#----------------------------------------------------------

# -*-coding:Latin-1 -*
import os
import random
# Programme mod�lisant une roue de casino

argent = 1000

print("Vous vous installez � la table de roulette avec", argent, "$.")

nb_choisi = -1
while nb_choisi<0 or nb_choisi>49:
						nb_choisi = input("Choisissez un nombre entre 0 et 49 : ")

						#On convertit le nbe mis�
						try: 
												nb_choisi = int(nb_choisi)
						except ValueError:
												print("Le nb n'est pas un entier")
												nb_choisi = -1
												continue
						#On teste si il est entre les bonnes bornes
						if nb_choisi < 0 or nb_choisi > 49:
												print("Le nb n'est pas entre 0 et 50")

mise = 0
while mise <= 0 or mise > argent:
						mise = input("Tapez le montant de votre mise : ")
						# On convertit la mise
						try:
									mise 
									= int(mise)
						except ValueError:
									print("Vous n'avez pas saisi de nombre")
									mise = -1
									continue
						if mise <= 0:
									print("La mise saisie est n�gative ou nulle.")
						if mise > argent:
									print("Vous ne pouvez miser autant, vous n'avez que", argent, "$")

#G�n�rer un nombre al�atoire
numero_gagnant = int(random.randrange(0,50)) # Tire un nbe entre 0 et 49
print("La roulette tourne... ... et s'arr�te sur le num�ro", numero_gagnant)

#Tester si le nombre est �gale ou non
if nb_choisi == numero_gagnant:
						print("F�licitations ! Bon numero, vous gagnez : ", 3 * mise) 
						argent += 3 * mise
elif (nb_choisi - numero_gagnant) % 2 == 0:
						print("Bonne couleur, vous gagnez : ", 0.5 * mise) 
						argent += 0.5 * mise
else:
						print("Bad Luck : ", - mise) 
						argent -=  mise


print("Votre total est de : ", argent)

os.system("pause")




#----------------------------------------------------------
# 1.8. Les exceptions
#----------------------------------------------------------

# Quand Python rencontre une erreur ds le code, il l�ve une exception.
>>> # Exemple classique : test d'une division par z�ro
>>> variable = 1/0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: int division or modulo by zero

# Forme minimal du bloc TRY
			#Mettre les instructions � tester dans un premier bloc et les instructions � ex�cuter en cas d'erreur ds un autre bloc
			annee = input()
			try: # On essaye de convertir l'ann�e en entier
						annee = int(annee)
			except:
						print("Erreur lors de la conversion de l'ann�e.")
						annee = 2000                        
						#Valeur par d�faut pour que la suite ne plante pas

			# Cette m�thode est assez grossi�re. Elle essaye une instruction et intercepte n'importe quelle exception 
			# C'est une mauvaise habitude � prendre ! 
			# + Python peut lever des exceptions qui ne signifient pas n�cessairement qu'il y a eu une erreur.
# Voici une mani�re plus �l�gante et moins dangereuse :

# Forme plus compl�te
try:
			resultat = numerateur / denominateur
except:
			print("Une erreur est survenue... laquelle ?")        
			
			# 1 : NameError : l'une des variables numerateur ou denominateur n'a pas �t� d�finie (elle n'existe pas).
			# 2 : TypeError : l'une des variables numerateur ou denominateur ne peut diviser ou �tre divis�e (string) 
			# 3 : ZeroDivisionError : encore elle ! Si denominateur vaut 0
			
try:
			resultat = numerateur / denominateur
except NameError:
			print("La variable numerateur ou denominateur n'a pas �t� d�finie.")
except TypeError:
			print("La variable num ou denum poss�de un type incompatible avec la division.")
except ZeroDivisionError:
			print("La variable denominateur est �gale � 0.")   

			# Plus simple, on peut capturer  l'exception et afficher son message 
try:
			# Bloc de test
except type_de_l_exception as exception_retournee:
			print("Voici l'erreur :", exception_retournee)

# Else va permettre d'ex�cuter une action si aucune erreur ne survient :
try:
			resultat = numerateur / denominateur
except NameError:
			print("La variable numerateur ou denominateur n'a pas �t� d�finie.")
except TypeError:
			print("Le numerateur ou denominateur poss�de un type incompatible")
except ZeroDivisionError:
			print("La variable denominateur est �gale � 0.")
else:
			print("Le r�sultat obtenu est", resultat)

# Finally permet d'ex�cuter du code apr�s un bloc try
try:
			resultat = numerateur / denominateur
except TypeDInstruction:
			print("...")
finally:
			# Instruction(s) ex�cut�e(s) qu'il y ait eu des erreurs ou non

# Pass :  tester un bloc d'instructions� mais ne rien faire si erreur
try:
			resultat = numerateur / denominateur
except: 
			pass


# Les Assertions
			# Les assertions sont un moyen simple de s'assurer, avant de continuer, qu'une condition est respect�e. 
			#En g�n�ral, on les utilise dans des blocs try � except.
assert test
			
			# Si le test renvoie True, l'ex�cution se poursuit normalement. Sinon, une exception AssertionError est lev�e.
			>>> var = 5
			>>> assert var == 5
			>>> assert var == 8
			Traceback (most recent call last):
			  File "<stdin>", line 1, in <module>
			AssertionError
			>>>

			#� quoi cela sert-il, concr�tement ? Exemple :
			annee = input("Saisissez une ann�e sup�rieure � 0 :")
			try:
						annee = int(annee) # Conversion de l'ann�e
						assert annee > 0
			except ValueError:
						print("Vous n'avez pas saisi un nombre.")
			except AssertionError:
						print("L'ann�e saisie est inf�rieure ou �gale � 0.")



#----------------------------------------------------------
# 1.7. Pas � pas vers la modularit� (2/2)
#----------------------------------------------------------

# Mettre notre code dans un fichier que nous pourrons lancer  � volont�, comme un v�ritable programme !

#Emprisonnons notre programme dans un fichier
			# Programme testant si une ann�e est bissextile: 
						#Ins�rez le code dans ce fichier et enregistrez-le avec l'extension .py (exemple bissextile.py)
						
						# -*-coding:Latin-1 -*
						import os 
						# Programme testant si une ann�e, est bissextile ou non
						annee = input("Saisissez une ann�e : ") 
						annee = int(annee) 
						if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
									print("L'ann�e saisie est bissextile.")
						else:
									print("L'ann�e saisie n'est pas bissextile.")
						os.system("pause")
						
			#Explication du code :
						# -*-coding:Latin-1 -*
									#il est n�cessaire de pr�ciser � Python l'encodage de ces accents
						import os 
									# On importe le module os qui dispose de variables et de fonctions utiles pour dialoguer 
									# avec votre syst�me d'exploitation
						os.system("pause")
									# On met le programme en pause pour �viter qu'il ne se referme (Windows)

			# On peut aussi appeler un module depuis un autre, contenu dans le m�me r�pertoire en pr�cisant le nom du fichier (sans l'extension .py)
			
			# multipli.py
			"""module multipli contenant la fonction table"""
			def table(nb, max=10):
						"""Fonction affichant la table de multiplication par nb de
						1 * nb jusqu'� max * nb"""
						i = 0
						while i < max:
									print(i + 1, "*", nb, "=", (i + 1) * nb)
									i += 1
			
			# 2. Test.py
			import os
						from multipli import *
						# test de la fonction table
						table(3, 20)
			os.system("pause")
			
			# Si l'on met tout le code dans le m�me module Comment s�parer les fonctions � importer dans d'�ventuels autres modules
			# et les commande qui ne doivent �tre actionn� que si l'on clic sur ce module
			
			"""module multipli contenant la fonction table"""
			import os
			def table(nb, max=10):
						i = 0
						while i < max:
									print(i + 1, "*", nb, "=", (i + 1) * nb)
									i += 1
			# test de la fonction table
			if __name__ == "__main__":
						table(4)
						os.system("pause")
			
			# Voil�. � pr�sent, si vous faites un double-clic directement sur le fichier multipli.py, vous allez voir
			# la table de multiplication par 4. En revanche, si vous l'importez, le code de test ne s'ex�cutera pas. 
			
			# Si la variable __name__ est �gale � __main__           Cela veut dire que le fichier appel� est le fichier ex�cut�


# Les packages
# Un package sert � regrouper plusieurs modules
			
			# Importer des packages
			import nom_bibliotheque
			# Pointe vers le sous-package evenements
			nom_bibliotheque.evenements 
			# Pointe vers le module clavier
			nom_bibliotheque.evenements.clavier 
			
			# Importer un seul module
			from nom_bibliotheque.objets import bouton

			# Cr�er ses propres packages
			# En Python, vous trouverez souvent le fichier d'initialisation de package __init__.py dans un r�pertoire destin� � devenir un package.
			
			

#----------------------------------------------------------
# 1.6. Pas � pas vers la modularit� (1/2)
#----------------------------------------------------------


#Les fonctions Lambda
			#fonctions extr�mement courtes car limit�es � une seule instruction
			f = lambda x, y: x + y


# Modules
# Un module est grossi�rement un bout de code que l'on a enferm� dans un fichier. 
# On emprisonne ainsi des fonctions et des variables ayant ttes un rapport entre elles. 
			# La m�thode Import
			>>> import math
			# Toutes les fonctions math�matiques contenues dans ce module sont mtnt accessibles. 
			# Pour appeler une fonction du module, taper le nom du module suivi d'un point � . � puis du nom de la fonction. 
			>>> math.sqrt(16)
			4
			>>>
			
			#Mais comment suis-je cens� savoir quelles fonctions existent et ce que fait math.sqrt dans ce cas pr�cis ?
			>>> help("math")
			Help on built-in module math:

			NAME
						math

			FILE
						(built-in)

			DESCRIPTION
						This module is always available. It provides access to the
						mathematical functions defined by the C standard.

			FUNCTIONS
						acos(...)
									acos(x)

									Return the arc cosine (measured in radians) of x.

			#Tapez Q pour revenir � la fen�tre d'interpr�teur, 
			#Espace pour avancer d'une page, Entr�e pour avancer d'une ligne. 
			#Vous pouvez �galement passer un nom de fonction en param�tre de la fonction help.
			>>> help("math.sqrt")
			Help on built-in function sqrt in module math:
			sqrt(...)
						sqrt(x)
						Return the square root of x.


			#vous pourrez vouloir changer le nom de l'espace de noms 
			#dans lequel sera stock� le module import�
			import math as mathematiques
			>>> mathematiques.sqrt(25)
			5
			
			#Admettons que nous ayons uniquement besoin, dans notre programme, 
			#de la fonction renvoyant la valeur absolue d'une variable
			from math import fabs
			>>> fabs(-5)                                                  #Valeur Absolue
			5                      


#----------------------------------------------------------
# 1.5. Les boucles
#----------------------------------------------------------

#Pour interrompre la boucle, vous devrez taper CTRL + C 

#WHILE
nb = 7             # On garde la var contenant le nb dont on veut la table de multiplication
i = 0    # C'est notre var compteur que nous allons incr�menter dans la boucle
while i < 10:    # Tant que i est strictement inf�rieure � 10
			print(i + 1, "*", nb, "=", (i + 1) * nb)
			i += 1               # On incr�mente i de 1 � chaque tour de boucle



#BREAK & CONTINUE
# 1 est toujours vrai -> boucle infinie
while 1: 
			lettre = input("Tapez 'Q' pour quitter : ")
			if lettre == "Q":
						print("Fin de la boucle")
						break
#Parfois, break est v�ritablement utile et fait gagner du temps. 
#Mais ne l'utilisez pas � outrance, pr�f�rez une boucle avec 
#une condition claire plut�t qu'un bloc d'instructions avec un break


#Le mot-cl� continue permet de� continuer une boucle, en repartant directement 
#� la ligne du while ou for
i = 1
while i < 20: # Tant que i est inf�rieure � 20
			if i % 3 == 0:
						i += 4 # On ajoute 4 � i
						print("On incr�mente i de 4. i est maintenant �gale �", i)
						continue # On retourne au while sans ex�cuter les autres lignes
			print("La variable i =", i)
			i += 1 # Dans le cas classique on ajoute juste 1 � i

#R�sultat
La variable i = 1
La variable i = 2
On incr�mente i de 4. i est maintenant �gale � 7
La variable i = 7...















 
