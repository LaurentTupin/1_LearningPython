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
# Moocs : https://openclassrooms.com (2.5)
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
		x = y = 3
		#Permutation de variables
		a,b = b,a # permutation
	# condition
		if a.isdigit():

#S�quence
	String
	Liste
	Tuple
	
#String
	#on peut couper une instruction, pour l'�crire sur deux lignes
	1 + 4 - 3 * 19 + 33 - 45 * 2 + (8 - 3) \
	... -6 + 23.5
	#le symbole � \ � permet, avant un saut de ligne,
	#d'indiquer � Python que � cette instruction se poursuit � la ligne suivante �. 
	
	#Pour �crire un v�ritable anti-slash dans une cha�ne, il faut le doubler : � \\ �
	
	#Permet d'�crire plusieurs lignes
	chaine3 = """Ceci est un nouvel
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
	'spam'.upper() 					--> 'SPAM'
	'SPAM'.lower()
	'spam et fromage'.capitalize()	--> 'Spam et fromage'		# La premi�re lettre en majuscule
	'SPAM'.reverse() 				--> 'MAPS'
	'spam'.replace ('s', 'p') 		--> 'ppam'
	'   une  chaine avec  des espaces   '.strip()			--> 'une  chaine avec  des espaces'  
	'introduction'.center(20)		--> '    introduction    '
	
	#Format
	'Je m'appelle {0} {1} et j'ai {2} ans.'.format("Paul", "Dupont", 21)	--> 'Je m'appelle Paul Dupont et j'ai 21 ans.'
	adresse = "{no_rue}, {nom_rue}, {code_postal}, {nom_ville}".format(no_rue=5, nom_rue="rue des Postes", code_postal=75003, nom_ville="Paris")
	
	
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
	
	L = list()	# liste vide
	l = []		# liste vide
	l = [4,' spam', True, 3.2]
	l[3] 		--> 3.2
	l[0] = l[0] + 2
	l 			-->  [6, 'spam', True, 3.2]
	l[1:2] 		-->  'spam'
	
	# Ins�rer
		L = ['a', 'b', 'd', 'e']
		L.insert(2, 'c') 	# On ins�re 'c' � l'indice 2
		L		--> ['a', 'b', 'c', 'd', 'e']
		l[1:2] = ['egg', 'spam']
		l 		-->  [6,'egg', 'spam', True, 3.2]
		l[3:4] = ['egg', 'beans']
		l 		-->  [6,'egg', 'spam', 'egg', 'beans', 3.2]	# ca a enlev� TRUE
	# Contracter ou effacer
		l[1:3] = []	# liste vide
		l 		-->  [6, 'egg', 'beans', 3.2]	# ca a enlev� TRUE
	
	# append			# Econome en m�moire car pas de copie
		l.append('34')
		l 		-->  [6, 'egg', 'beans', 3.2, '34']
	# extend ()
		l.extend([3, 5, 9])			# Or  L += [3, 5, 9]
		l 		-->  [6, 'egg', 'beans', 3.2, '34', 3, 5, 9]			
	# Supprimer
		del l[0] 		# On supprime le premier �l�ment de la liste
		l.remove('a') 	# Attention ne supprime que la premiere occurrence !
		l = [i for i in l if i != 'a']
	# Pop			#Retourne le dernier �l�ment de la liste et l'enl�ve de la liste
		l.pop 	-->  9
		l 		-->  [6, 'egg', 'beans', 3.2, '34', 3, 5]
	# ENUMERATE
		L = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
		for i, elt in enumerate(L):
			print("{}  {}".format(i, elt))
			--> "0  a" ...
		for elt in enumerate(ma_liste):
			print(elt)
			--> (0, 'a') ...
	#Autre mani�re
		autre_liste = [[1, 'a'], [4, 'd'], [7, 'g'], [26, 'z']]	
		for nb, lettre in autre_liste:
			print("{} {}".format(nb, lettre))
			--> "1 a" ...
	
	#Fonction ordre
		l.sort()
		sorted(l)
		l.reverse()
		# Exemple :  prendre le 3�me plus grand mots
			sorted(s, key=len, reverse=True)[2]
		
	
	#Liste de liste
		L = [1, 3.5, "une chaine", []]

	
	
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
	#Pour interrompre la boucle, vous pouvez taper CTRL + C 
	L = range(10)
	while L:
		L.pop(0)
		print L
		--> 0
		--> [1,2,3,4,5,6,7,8,9]
		--> 1
		--> [2,3,4,5,6,7,8,9]
	#On sort au bout de 10
	
	# BREAK
	while True: 	#ne s'arr�te jamais
		s = raw_input('Question ?')
		# s = input('Question ?')
		if 'non' in s:
			break
			#Sort de la boucle while si l'utilisateur met 'non'
	
	# CONTINUE
	#Le mot-cl� continue permet de� continuer une boucle, en repartant directement � la ligne du while ou for
	i = 1
	while i < 20:
		if i % 3 == 0:
			i += 4 
			print i
			continue # On retourne au while sans ex�cuter les autres lignes
		print i
		i += 1 
				-- > 1	2	7	8	13...


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
	
	# Peut retourner plusieurs valeur
	def f(x, y, z):
		return x+y, z
	a, b = f(100, 5, 3)		-->  a = 105, b = 3
		
			
	# Argument par d�faut
		def f (nom, prenom, tel = '')			
	
	# Nbe d'argument variable
		def fonction_inconnue(*parametres):
			# parametres sera un tuple
		def fonction_inconnue(nom, prenom, *commentaires):
			# parametres seront 2 var et un tuple
	
	# Nbe d'arguments variable et nomm�e
		def f (**d):
			print d
			# renvoie un dictionnaire
		f(nom = 'durant', prenom = 'marc', tel = '0365738')
			--> {nom : 'durant', prenom : 'marc', tel : '0365738'}
		
	# Unpacking * 
		def f (a, b):
			print a, b
		
		L = [1, 2]
		f(*L)
			--> 1 2
		
	# Unpacking **
		def f (a, b):
			print a, b
		
		d = ['a' : 1, 'b' : 2]
		f(**d)
			--> 1 2
		
			
# Dictionnaire
	# ----- Voire Table de hash ----- 
	# Definition: Collection non ordonn�e de couple Cl�-Valeur
	
	# Cr�ation
		d = dict()
		d = {}
		# A la main
		d = {'marc' : 39, 'alice' : 30, 'eric' : 38}
		# par liste de Tuple
		l = [('marc',39),('alice',30),('eric',38)]
		d = dict(l)
	
	# Op�ration
		len(d) 		--> 3 
		'marc' in d 	--> True
		'louis' in d 	--> False
		'louis' not in d 	--> True
		d['marc']	--> 39
		del['marc']
		d 			-->  {'alice' : 30, 'eric' : 38}
	# La m�thode pop supprime la cl� mais elle renvoie la valeur supprim�e
		d.pop('alice')		--> 'alice'
		d 			-->  {'eric' : 38}

	# Liste
		d.keys()	--> ['alice','eric']
		d.values()	--> [30, 38]
		d.items()	--> [('alice',30),('eric',38)]
	
	# Parcours
		for cle in d:	#or
		for cle in d.keys():
		for valeur in d.values():
		for cle, valeur in d.items():

	# On se sert parfois des dictionnaires pour stocker des fonctions.
		def fete():		...
		def oiseau():	...
		fonctions = {}
		fonctions["fete"] = fete
		fonctions["oiseau"] = oiseau
		fonctions["oiseau"]				--> <function oiseau at 0x00BA5198>
		# on essaye de l'appeler
		fonctions["oiseau"](10) 
		
	# Vider le dico
		d.clear()
	
# Set (ensemble)
	# Definition : Ensemble non ordonn� d'objet unique (objet immuable)
	
	# Cr�ation
		# A la main
		s = {1,2,3,'spam'}
		# Par liste 
		l = [1,2,3,3,'spam']
		s = set(l)
		s		--> set([1,2,3,'spam'])  #Objet doit �tre unique
	# Op�ration
		s.add('egg')
		s		--> set([1,2,3,'egg','spam'])
		s.remove(2)
		s		--> set([1,3,'egg','spam'])
		s.update([5,6])
		s		--> set([1,3,5,6,'egg','spam'])
	# Diff�rence
		s2 = {1,5,'ham'}
		s - s2 	--> set([3,6,'egg','spam'])				# Diff�rence
		s | s2 	--> set([1,3,5,6,'egg','spam','ham'])	# Union
		s & s2 	--> set([1,5])							# Intersection
	
	# FrozenSet (Set immuable)
		fs = frozenset(s)
		fs.add(3)  --> Error 
		
		
# R�f�rence partag�e
	# -- au moins 2 variables r�f�rence un m�me objet --
	a = [1,2]
	b = a
	a[0] = 'spam'
	b[0] 				--> 'spam' # et non pas 1
	
	# Shalow Copy
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
		
# Module (Fichier .py)
	import math
	dir(math)  	--> toutes les fonctions du module math
	help(math)	--> toute l'aide
	help(math.tan)	--> Retrun the tan of x...
	math.log(10)	--> 2.302...
	
	#moocs papier (1.7)
	# On peut appeler un module depuis un autre, contenu dans le m�me r�pertoire en pr�cisant le nom du fichier (sans l'extension .py)
	import os
	from multipli import *

	# Si l'on met tout le code dans le m�me module Comment s�parer les fonctions � importer dans d'�ventuels autres modules
	# et les commande qui ne doivent �tre actionn� que si l'on clic sur ce module
	if __name__ == "__main__":
		table(4)					#(table est dans multipli)
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
	
	
# Liste de lecture 4
# FICHIER
	#Ecrire 'w'
	f = open (r'C:\tmp\spam.txt', 'w')
	# r = raw string
	# w : write (va cr�er le fichier ou le vider
	for i in range(100):
		line = '{} {}\n'.format(i, i**2)
		#\n : retour chariot
		f.write(line)
	f.close()		#Save et close
	
	#Lire 'r'
	#parcourir les lignes car un fichier a un it�rateur par ligne
		f = open (r'C:\tmp\spam.txt', 'r')
		f2 = open (r'C:\tmp\spam2.txt', 'w')
		for l in f:
			f2.write(l.replace(' ',', '))
		f.close()
		f2.close()
	#Read
		f = open (r'C:\tmp\spam.txt', 'r')
		contenu = f.read()
		f.close()
	
	#Append 'a' : �criture mais sans �craser l'ancien fichier et mettre � la fin
	f = open (r'C:\tmp\spam.txt', 'a')	
	
	#Changer le r�pertoir courant
	import os
	os.chdir("C:/tests python")	# Assigner le CWD ( = � Current Working Directory � )
	os.getcwd() 				# Retrouver le CWD
		#Chemin relatif
		# si on se trouve dans C:, notre chemin relatif sera "test\fic.txt"
		# "..\rep1\fic1.txt" sera le chemin si on est dans "rep2"
		f = open (r'/spam.txt', 'r')
	
	#Fermer automatiquement le fichier au cas ou on oublie Close()
	with open('C:\tmp\spam.txt', 'r') as f:
		# Op�rations sur le fichier
		contenu = f.read()
		# Si une exception se produit, le fichier sera tout de m�me ferm� � la fin du bloc.
		# Il est inutile, par cons�quent, de fermer le fichier � la fin du bloc with
	
	#'b' binary		#va servir pour sauver des objets
	with open('C:\tmp\spam.txt', 'wb') as fichier:
	
	# Pickle : Enregistrer Objets dans Fichiers (Pickler)
		import pickle as p
		with open('donnees', 'wb') as fichier:
			mon_pickler = p.Pickler(fichier)
			# enregistrement
			mon_pickler.dump(objet1)
			mon_pickler.dump(objet2)
	# Unpickler : r�cup�rer les objets dans les fichiers
		with open('donnees', 'rb') as fichier:
			mon_depickler = p.Unpickler(fichier)
			# Lecture des objets contenus dans le fichier... r�cup�re dans l'ordre
			objet1 = mon_depickler.load()
			objet2 = mon_depickler.load()

	

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
	
	
	
	
# 5.2/3 Importantion des modules
	#Trouve le module dans le m�me dossier 
	#sinon dans le dossier PYTHONPATH
	#sinon Librairie standard SYS.PATH
	#Execute le fichier (fonction cr�er seulement � l'appel des fonctions)
	#SYS
		import sys
		sys.path
	#OS
		import os
	#Uniquement une valeur ou fonction
		from os import x
		# Avantage
		from math import cos()
		cos(10)		# Fonctionne direct dans faire math.cos(10)

	# Quand le module est dans un autre dossier
		import sys
		sys.path.append("F:\LYXOR-ETF-BIU\ETF_DW\Python\Cobra\Fonction\\")
		import fct_Date 
		
		
		
# 5.4 Class, Instance & M�thodes
	class c:
		x=1
	#Instance
		I = c()
	#Espace de nommage
		c.__dict__
			--> {'x':1, '__module__':'__main__', '__doc__': None}
		I.__dict__
			--> {}
	c.x 	--> 1
	I.x 	--> 1	#Car va aller chercher dans class
		
	c.y = 10	# cr�ation
	c.x = 5		# update
	I.x 	--> 5
	I.y		--> 10	#m�me si instance d�fini avant cr�ation de Y
	
	I.x = 'a'
	I.x 	--> 'a'
	c.x 	--> 5
	
	#Fonction = methode dans une classe
	class c:
		x=1
		def f(self, a):
			print self.x
			self.x = a
	I = c()
	I.f(5)		--> 1		#Raccourci de : C.f(I, 5)
	I.f(10)		--> 5
	
# 5.5 Heritage
	class C1: pass
	class C2: pass
	class C(C1, C2):
		def f(self,a):
			self.x = 10
	#C1 et C1 sont des super class pour C et si qque chose est absent dans C, �a va aller chercher dans C1 ou C2
	I1 = C ()
	I2 = C ()
	#Arbre d'h�ritage : I1 et I2 vont aller chercher dans C puis dans C1 et C2 si besoin
	
	#Exemple
	class C:
		def set_x(self, x):	
			self.x = x
		def get_x(self):
			print self.x
	#Sous classe de C
	class sousC(C):
		def get_x(self):
			print 'x est : ', self.x
	sousC.__bases__	--> Retourne les Super classe : C ici
	#Instance
	c = C()
	sc = sousC()
	c.set_x(10)		# Va aller dans C
	sc.set_x(20)	# Va aller dans sousC puis dans C
	c.get_x			--> 10
	sc.get_x		--> x est : 20
	
	
# 5.6 Surcharge	
	#Red�finir une m�thode d'une super classe ou d'une m�thode globale (__init__)
		
	###################
	class C:
		#Constructeur
		def __init__ (self, a):
			print "dans C"
			self.x = a
		def set_x (self, x):
			self.x = x
		def get_x (self):
			print self.x
	###################
	
	I =  C(10)
		--> dans C
	I.__dict__
		{'x' : 10}
	
	# Avec h�ritage
	
	
	###################
	class D(C):
		def __init__ (self):
			print "dans D"
	###################
	
	I = D()
		--> dans D
	I.get_x()
		--> ERREUR
	# le init de D ne d�finit pas x	
	# Il faut l'appeler explicitement
	class D(C):
		def __init__ (self):
			print "dans D"
			C.__init__(self, 100)
	
	# __str__
	# Pour faire un print direct
	
	###################
	class C:
		#Constructeur
		def __init__ (self, a):
			print "dans C"
			self.x = a
		def set_x (self, x):
			self.x = x
		def get_x (self):
			print self.x
		def __str__(self):
			return str(self.x)
	###################
	
	I = C(20)
		--> dans C
	print I
		--> 20
	# le print va chercher la m�thode __str__
	# l'instance va donc avoir un comportement comme un built-in normal
	

###################################
### MOOCS �crit sur les classes ###
###################################

	# 3.1 Class
		# Constructeur : m�thode de notre objet se chargeant de cr�er nos attributs
		class Personne:
			'''Classe d�finissant une personne caract�ris�e par : son nom, son pr�nom, son �ge son lieu de r�sidence'''
			
			def __init__(self): # Notre m�thode constructeur
				self.nom = "Dupont"
		
		# Quand on appelle la classe 
		bernard = Personne()
		bernard			--> 	<__main__.Personne object at 0x00B42570>
		bernard.nom		-->		'Dupont'
		bernard.nom	 = 'Tupin'
		bernard.nom		-->		'Tupin'
		
		# Avec param�tres d'entr�es
		class Personne:
			'''Classe d�finissant une personne caract�ris�e par : son nom, son pr�nom, son �ge son lieu de r�sidence'''

			def __init__(self, nom, prenom):
				self.nom = nom
				self.prenom = prenom
				self.age = 33
				self.lieu_residence = "Paris"
		
		
		# Attributs de classe : Attributs identique pour toutes instances
		class Personne:
			'''Classe d�finissant une personne caract�ris�e par : son nom, son pr�nom, son �ge son lieu de r�sidence'''
			
			objets_crees = 0 # Le compteur vaut 0 au d�part
			def __init__(self):
				'''� chaque fois qu'on cr�e un objet, on incr�mente le compteur'''
				Compteur.objets_crees += 1		
				# On ne peut pas acc�der � l'attribut depuis m�thode d'une classe � Classe 
				# Accessibilit� des variables LG pour les classes (Local, Global)
				# On doit pr�ciser '''compteur.attribut'''
		
		
		# M�thode
		class TableauNoir:
	   
		def __init__(self):
			self.surface = ""
		def ecrire(self, message_a_ecrire):
			if self.surface != "":
				self.surface += "\n"
			self.surface += message_a_ecrire
			
			
		# M�thodes de classe : ne prend pas en premier param�tre SELF (l'instance de l'objet) mais CLS (la classe de l'objet)
		class Compteur:
			'''Cette classe poss�de un attribut de classe qui s'incr�mente � chaque fois que l'on cr�e un objet de ce type'''
			objets_crees = 0 # Le compteur vaut 0 au d�part
			def __init__(self):
				'''� chaque fois qu'on cr�e un objet, on incr�mente le compteur'''
				Compteur.objets_crees += 1
			def combien(cls):
				'''M�thode de classe affichant combien d'objets ont �t� cr��s'''
				print("Jusqu'� pr�sent, {} objets ont �t� cr��s.".format(cls.objets_crees))
			combien = classmethod(combien)
		
		
		# M�thodes statiques : elles ne prennent aucun premier param�tre, ni SELF ni CLS
		#   - ind�pendant de toute donn�e, aussi bien contenue dans l'instance de l'objet que dans la classe
		class Test:
			'''Une classe de test tout simplement'''
			def afficher():
				'''Fonction charg�e d'afficher quelque chose'''
				print("On affiche la m�me chose.")
				print("peu importe les donn�es de l'objet ou de la classe.")
			afficher = staticmethod(afficher)
			
		# DIR : Voir les attributs et les m�thodes d'une classe
		class Test:
			def __init__(self):
				self.mon_attribut = "ok"
			def afficher_attribut(self):
				print("Mon attribut est {0}.".format(self.mon_attribut))
		
		un_test = Test()
		dir(un_test)
			--> ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__ge__'
				, '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__','__module__'
				, '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__'
				, '__sizeof__', '__str__', '__subclasshook__', '__weakref__'
				, 'afficher_attribut', 'mon_attribut']
			# M�thodes sp�ciales de Python
				__dict__	# Attribut qui est un dictionnaire, contient cl�s = noms des attributs, valeurs = valeurs des attributs
				un_test.__dict__	--> {'mon_attribut': 'ok'}


	# 3.2 Encapsulation
		# Propri�t� : Accesseurs et Mutateurs
		mon_objet.mon_attribut 		#va devenir
			mon_objet.get_mon_attribut()
			mon_objet.set_mon_attribut(valeur)
			
		class Personne:
			def __init__(self, nom, prenom):
				'''Constructeur de notre classe'''
				self._lieu_residence = "Paris" # Notez le soulign� _ devant le nom // interdit l'acc�s depuis l'ext�rieur
			def _get_lieu_residence(self):
				'''M�thode qui sera appel�e quand on souhaitera acc�der en lecture � l'attribut "lieu_residence"'''
				return self._lieu_residence
			def _set_lieu_residence(self, nouvelle_residence):
				'''M�thode appel�e quand on souhaite modifier le lieu de r�sidence'''
				self._lieu_residence = nouvelle_residence
			# On va dire � Python que notre attribut lieu_residence pointe vers une propri�t�
			lieu_residence = property(_get_lieu_residence, _set_lieu_residence)	
			
		# Quand on veut acc�der � objet.lieu_residence
		# Python tombe sur une propri�t� redirigeant vers la m�thode _get_lieu_residence 
		# Quand on beut modificer objet.lieu_residence --> Redirection vers _set_lieu_residence
		
		jean = Personne("Micado", "Jean")
		jean.age		-->	33
		jean.lieu_residence		-->	'Paris'
			#On acc�de � l'attribut lieu_residence !		_get_lieu_residence
		jean.lieu_residence = "Berlin"					# 	_set_lieu_residence
		jean.lieu_residence		--> 'Berlin'
			#On acc�de � l'attribut lieu_residence !		_get_lieu_residence
		
		
	# 3.3 M�thode sp�ciale
		__init__
		__del__
		
		def __del__(self):
			'''M�thode appel�e quand l'objet est supprim�'''
			print("C'est la fin ! On me supprime !")

			#La destruction ? Quand un objet se d�truit-il ?
			del (del mon_objet) 	#ou fin de fonction ou programme
			#Cela ne sert � rien la plupart du temps sauf si on veut r�cup�rer une info avant destruction
			
		__repr__
			def __repr__(self):
				'''Quand on entre notre objet dans l'interpr�teur'''
				return "Personne: nom({}), pr�nom({}), �ge({})".format(self.nom, self.prenom, self.age)
			
			#Change
			p1 = Personne("Micado", "Jean")
			p1 		--> <__main__.XXX object at 0x00B46A70>
			# en
			p1 		--> Personne: nom(Micado), pr�nom(Jean), �ge(33)

		__getattr__
			# Permet de renvoyer un message si un attribut n'existe pas
			class Protege:
				def __init__(self):
					self.alibaba = 1
				def __getattr__(self, nom):
					print("Alerte ! Il n'y a pas d'attribut {} ici !".format(nom))
			
			pro = Protege()
			pro.alibaba		-->	1
			pro.element		-->	Alerte ! Il ny a pas dattribut element ici !

		__setattr__
		__delattr__
		
		# M�thodes math�matiques
		class Duree:
			'''Classe contenant des dur�es sous la forme d'un nombre de minutes	et de secondes'''
			def __init__(self, min=0, sec=0):
				self.min = min 		# Nombre de minutes
				self.sec = sec 		# Nombre de secondes
			def __str__(self):
				return "{0:02}:{1:02}".format(self.min, self.sec)
		
		d1 = Duree(3, 5)
		print(d1)		--> 03:05
		
		# Comment additionner des dur�e
		def __add__(self, objet_a_ajouter):
			'''L'objet � ajouter est un entier, le nombre de secondes'''
			nouvelle_duree = Duree()
			# On va copier self dans l'objet cr�� pour avoir la m�me dur�e
			nouvelle_duree.min = self.min
			nouvelle_duree.sec = self.sec
			# On ajoute la dur�e
			nouvelle_duree.sec += objet_a_ajouter
			# Si le nombre de secondes >= 60
			if nouvelle_duree.sec >= 60:
				nouvelle_duree.min += nouvelle_duree.sec // 60
				nouvelle_duree.sec = nouvelle_duree.sec % 60
			# On renvoie la nouvelle dur�e
			return nouvelle_duree
########################################################
		
	
	
	
# 5.7 fonctions, module, class
	fonction:
		Pas d'�tat apr�s execution
	Module:
		Garde de l'�tat
		c une boite � outil
		une seule instance par programme car couteux en m�moire
	Class:
		Garde de l'�tat
		c une boite � outil
		instance multiples
		H�ritage
	
# 5.8 Assignation et r�f�rencement
	X est un attribut quand :	objet.X
	variable : 					X
	
	VARIABLE:
	Assignation (binding) explicite:
		X=1
	D�claration d'argument (implicite)
		def f(a):
		for i in obj:
		[i**2 for i in range(10)]
	Les imports
		import sys
		from os import times
	
	R�f�rencement
		module : 	r�gle G
		fonction : 	r�gle LEG
		Class : 	r�gle LG
			X d�f dans classe n'est pas accessible dans les m�thodes de la classe sauf si on dit Classe.X
			

# 6.1 Fonctions g�n�ratrices
	def f:
		yield 10
	
	print f()
		--> objet generator qui est un it�rateur
	
	it = f()
	iter(it) is it 
		--> True
		# le g�r�nateur est son propre it�rateur
	
	it.next()
		--> 10
	it.next()
		--> ERREUR
	
	# Meilleur exemple
	###################
	def f (x):
		for i in range(x):
			yield i**3 + 2
	###################
	
	print f(100)
		--> objet generator qui est un it�rateur
	
	for i in f (10)
		print i,
		--> 2 	0	20	54...
		
	[i for i in f(100) if i%17 ==0]
		--> liste...
	
# 6.2 Conception d'it�rateurs
	# 2 m�thodes
	.__iter__()
	.next()
	
	###################
	class Mots():
		def __init__(self, phrase):
			self.list_mots = phrase.split()
			self.count = 0
			
		def __iter__(self):
			return self
			
		def next(self):
			if self.count == len(self.list_mots):
				raise StopIteration
			self.count += 1
			return self.list_mots[self.count - 1]
	###################
	
	m = Mots('spam spam spam eggs spam beans')
	
	[x for x in m]
		--> ['spam','spam','spam','eggs','spam','beans']
	[x for x in m]
		--> []
		# Une fois � StopIteration, on ne peut pas re-parcourir l'objet
		# Il faut re-cr�er une autre instance
	
	# Comment it�rer plusieurs fois : re-cr�er un it�rateur � chaque appel de __iter__
	# ON cr�� un objet qui a un it�rateur mais qui n'est pas un it�rateur
	
	###################
	class Mots():
		def __init__(self, phrase):
			self.list_mots = phrase.split()
			
		def __iter__(self):
			return IterMots(self.list_mots)
			
	class IterMots:
		def __init__(self, phrase):
			self.list_mots = phrase
			self.count = 0
		
		def __iter__():
			return self
		
		def next(self):
			if self.count == len(self.list_mots):
				raise StopIteration
			self.count += 1
			return self.list_mots[self.count - 1]
	###################
	
	m = Mots('spam spam spam eggs spam beans')
	
	[x for x in m]
		--> ['spam','spam','spam','eggs','spam','beans']
	[x for x in m]
		--> ['spam','spam','spam','eggs','spam','beans']
	
	
	# BEAUCOUP PLUS SIMPLE avec les fonctions GENERATRICES
	###################
	class Mots():
		def __init__(self, phrase):
			self.list_mots = phrase.split()
			
		def __iter__(self):
			for i in self.list_mots:
				yield i
	###################
	
	
# 6.3 Exceptions
	def f (a, b):
		try:
			x = a/b
		except ZeroDivisionError:
			print 'division par 0'
		else:		# S'execute que s'il n'y a pas d'erreur
			print x
		finally:	# S'execute tout le temps
			# par exemple pour fermer les fichiers m�me s'il y a une erreur
		print 'Continuons'
		
	f(1,0)
		# Sans le try
		--> ERREUR
	f(1,0)
		-->'division par 0'		'Continuons'
	
	
	# R�cup�rer l'instance de l'exception
	def f (a, b):
		try:
			x = a/b
		except ZeroDivisionError as i:
			print 'division par 0', i.args
	
	f(1,0)
		-->'division par 0' ('integer division or modulo by zero,')
	
	
# MOOCS �crit sur les exceptions
	# 1.8. Les exceptions
	annee = input()
	try: # On essaye de convertir l'ann�e en entier
		annee = int(annee)
	except:
		print("Erreur lors de la conversion de l'ann�e.")
		annee = 2000  
		# Cette m�thode est assez grossi�re. Elle essaye une instruction et intercepte n'importe quelle exception 
		# C'est une mauvaise habitude � prendre ! 
		# Python peut lever des exceptions qui ne signifient pas n�cessairement qu'il y a eu une erreur.

	# Voici une mani�re plus �l�gante et moins dangereuse :
	try:
		resultat = numerateur / denominateur
	except NameError:
		print("La variable numerateur ou denominateur n'a pas �t� d�finie.")
	except TypeError:
		print("La variable num ou denum poss�de un type incompatible avec la division.")
	except ZeroDivisionError:
		print("La variable denominateur est �gale � 0.")   

	# Finally permet d'ex�cuter du code apr�s un bloc try
	try:
		resultat = numerateur / denominateur
	except ...
	finally:
		# Instruction(s) ex�cut�e(s) qu'il y ait eu des erreurs ou non


	# Pass:  tester un bloc d'instructions� mais ne rien faire si erreur
	try:
		resultat = numerateur / denominateur
	except: 
		pass			

	# Les Assertions
		# Les assertions sont un moyen simple de s'assurer, avant de continuer, qu'une condition est respect�e. 
		# En g�n�ral, on les utilise dans des blocs try � except.
	assert var == 5		# Si le test renvoie True, l'ex�cution se poursuit normalement. Sinon, une exception AssertionError est lev�e.
	assert var == 8
		Traceback (most recent call last):
		  File "<stdin>", line 1, in <module>
		AssertionError

	#� quoi cela sert-il, concr�tement ? Exemple :
	annee = input("Saisissez une ann�e sup�rieure � 0 :")
	try:
		annee = int(annee) # Conversion de l'ann�e
		assert annee > 0
	except ValueError:
		print("Vous n'avez pas saisi un nombre.")
	except AssertionError:
		print("L'ann�e saisie est inf�rieure ou �gale � 0.")

		
		
# 6.4 Exceptions personnalis�es
	# Les exceptions sont des classes
	class SplitError (Exception):
		# Elle h�rite de la classe Exception
		pass
	
	x = 1
	y  = 'a'
	
	raise SplitError('message de test', x, y)
		--> ERREUR...	SplitError: ('message de test', x, y)
	
	
	# Mettons un constructeur dans notre class exception
	class SplitError (Exception):
		def __init__(self, val, res):
			self.val = val
			self.res = res
	
	try:
		raise SplitError(res = 8, val = 'x')
	except SplitError as e:
		print e.res
		print e.val
			

# 6.5 Context manager
	# Finally: op�ration pour fermer proprement apr�s exception
	# Comment fermer proprement un serveur, sans avoir � updater tout le temps
	
	# Context Manager : 2 m�thodes
	.__enter__()
	.__exit__()
	
	with open(r'C:\...', 'w') as f:
		for i in range(10):
			f.write(str(i) + '\n')
		# Ferme le fichier m�me en cas d'expcetion
	
	# Comment impl�menter soi-m�me un context manager pour son objet
	class C:
		def __enter__(self):
			print 'dans enter'
			return self
			
		def __exit__(self, *args):
			print 'dans exit'
			print args
			return False
			# False : l'exception est retourn�
			# True : l'exception est captur� donc non retourn�
			
		def div(self, a, b):
			print a/b
		
	# appeler classe avec un context manager
	with C() as c:
		c.div(1,0)
		
	
# 7.1 M�thode static et de classe
	#Class sans prendre self (instance) en premier argument
	class C:
		nb_i = 0
		def __init__(self):
			C.nb_i += 1
	
	C()
	C()
	print C.nb_i
		--> 2
	
	#M�thode statique
	class C:
		nb_i = 0
		def __init__(self):
			C.nb_i += 1
		def num():
			return C.nb_i
		num = staticmethod(num)
	
	C.num()
		--> 2
	

# 7.1 (b) M�thode de classe	
	#Prend en premier argument la classe et non l'instance
	class C:
		nb_i = 0
		def __init__(self):
			self.count()
		def num (cls):
			return cls.nb_i
		def count (cls):
			cls.nb_i = cls.nb_i + 1
		num = classmethod(num)
		count = classmethod(count)
			
	
# 7.2 Les d�corateurs
	# plus besoin de mettre classmethod ou staticmethod � la fin
	class C:
		@classmethod
		def f(cls):
			pass
		@staticmethod
		def g():
			pass
		def h(self):
			pass
		
	# C'est un callable qui prend la fonction en argument et qui retourne un collable
	# o()
	# soit une fonction soit une classe
	
	
# 7.3 Les classes New-style
	# Fait pour r�soudre certains probl�me de consistance
	# Toujours utiliser les classes New-style
	# Classe New-style permet d'h�riter des types built-in
	
	type ('a')
		--> <type 'str'>
	# Equivalent �
	'a'.__class__
	# Le type est la classe (str) qui a instanci� notre objet 'a'
	
	class C:
		pass
	c = C()
	type(c)
		--> <type 'instance'>
	
	# Une classe qui h�rite d'une classe New-style, d'un built-in ou d'Object est une classe New-style
	class C(object):
		pass
	c = C()
	type(c)
		--> <class '__main__.C'>
		# Le type est C et non instance
		
	class C(int):
		pass
	c = C()
	type(c)
		--> <type 'int'>
		
	
# 7.4 Les m�taclasses
	3 grandes cet�gories d'objet
		- m�taclasses
		- classes
		- Instances
	
	Super-classe de toutes les classes:
		- Object
		
	Diff�rence entre instance et classe:
		- Le type d'une classe est l'objet type	
		###############
		class C(object):
			pass
		c = C()
		type(c)
			--> <class '__main__.C'>
		type(C)
			--> <type 'type'>		
		###############
	
	Type est la m�taclasse
	Type instancie toutes les classes
	Les classes instancient les instances
	Toutes les classes h�ritent de Object
	
	type(type)
		--> <type 'type'>	
	type(object)
		--> <type 'type'>	
	type.__bases__
		(<type 'object'>,)
	
	
# 7.5 Performances	
	# Taille des types built_in
	import sys
	sys.getsizeof(1)
		--> 12 (bites)
	sys.getsizeof('a')
		--> 22 (bites)
	sys.getsizeof('ab')
		--> 23 (bites)
	sys.getsizeof(None)
		--> 8 (bites)
	# Liste
	sys.getsizeof([])
		--> 36 (bites)
	sys.getsizeof([1, 2])
		--> 44 (bites)
	sys.getsizeof([1, 2465738919464672])
		--> 44 (bites)	# Liste n'est qu'une adresse vers l'integer
	
	# Performances
	import timeit
	timeit.timeit(setup = 'x = range(40)', stmt = '"a" in x', number = 6000000)
		--> 9,67 (secondes)
		# Test appartenance dans une liste prend 9 secondes - ex�cut� 6 000 000 fois
	timeit.timeit(setup = 'x = set(range(40))', stmt = '"a" in x', number = 6000000)
		--> 0,22 (secondes)
		# Set (ensemble) est bcp plus rapide qu'une liste
		# Car utilise la table de Hasch
			
	
	
	
#----------------------------------------------------------
# Exo & Fonction classique
#----------------------------------------------------------

# Ann�e bissextile
	annee = input("Saisissez une ann�e : ") 
	annee = int(annee) 
	if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
				print("L'ann�e saisie est bissextile.")
	else:
				print("L'ann�e saisie n'est pas bissextile.")
	os.system("pause")
	# On met le programme en pause pour �viter qu'il ne se referme (Windows)

	
# Arrondir un float et changer point par virgule
	afficher_flottant(3.99999999999998)		--> 	'3,999'

	def afficher_flottant(flottant):		
		if type(flottant) is not float:
					raise TypeError("Le param�tre attendu doit �tre un flottant")
		flottant = str(flottant)
		partie_entiere, partie_flottante = flottant.split(".")
		return ",".join([partie_entiere, partie_flottante[:3]])

		

#D�terminer si un  nombre est premier
	def PrimeTime(num): 
		L = [x for x in range(2,num) if num % x == 0]
		if len(L) == 0:
			return 'true'
		else:
			return 'false'
	# keep this function call here  
	print PrimeTime(raw_input())
	
	