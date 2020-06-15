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


#Type numérique
	--> type(variable)
	int
	long 	#Précision illimité
	float	#Précision limité
	complex		
		c = 1 + 3 j
		c.real 	--> 1.0
		c.imag 	--> 3.0
	#Conversion
		int(4.3)  	--> 4
	#Opération
		5 / 3  	--> 1
		5 % 3  	--> 2 		#modulo
		5 / 3.0  	--> 1.6666666 
		5 / float(3)  --> 1.6666666 
		5 // 3.1  --> 1.0	# Division entière
		1 < 3  	--> True
		3**2  	--> 9		#Puissance
		sqrt(9)	--> 3		#Racine carré (from math import *)
	#Autres opérations
		#On peut affecter une même valeur à plusieurs variables :
		>>> x = y = 3
		#Permutation de variables
		>>> a,b = b,a # permutation
	# condition
		if a.isdigit():

#Séquence
	String
	Liste
	Tuple
	
#String
	#on peut couper une instruction, pour l'écrire sur deux lignes
	>>> 1 + 4 - 3 * 19 + 33 - 45 * 2 + (8 - 3) \
	... -6 + 23.5
	#le symbole « \ » permet, avant un saut de ligne,
	#d'indiquer à Python que « cette instruction se poursuit à la ligne suivante ». 
	
	#Pour écrire un véritable anti-slash dans une chaîne, il faut le doubler : « \\ »
	
	#Permet d'écrire plusieurs lignes
	>>> chaine3 = """Ceci est un nouvel
	... essai sur plusieurs
	... lignes"""
	
	#« \n » symbolise un saut de ligne
	
	#Youtube
	s = 'egg, bacon'		#String de 10 caractères
	S[0]  	--> 'e'
	s[9]  	--> 'n'
	'x' in s  	-->  False
	s + ' and spam'  --> 'egg, bacon and spam'
	len(s)  	--> 10
	min(s)  	--> ' '
	max(s)  	--> 'o'
	s.index('g')  --> 1	#Position du premier 'g' (commence à 0)
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
		s[5:100]  	--> 'bacon'		# ça fonctionne
		s[50:100]  	--> ''			# ça fonctionne mais retourne vide
	# Négatif
		#Ordre normal
		e	g	g	,		b	a	c	o	n
		-10 -9	-8	-7	-6	-5	-4	-3	-2	-1
		s[-10:-7] 	--> 'egg'
		s[:-3] 		-->'egg, ba'
		#Ordre inverse
		s[::-1] 	--> 'nocab , gge'
		s[2:0:-1] 	--> 'gg'
		s[2::-1] 	--> 'gge'
		
# String (compléments)
	# *** Est immuable, si opération --> nouvelle string affecté à variable ***
	
	# Méthode
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
	chaine = "Bonjour les ZER0S"		#Lettre est une variable créée par le for, ce n'est pas à vous de l'instancier. 
	for lettre in chaine:
		if lettre in "AEIOUYaeiouy": 
			print(lettre + ' est une voyelle')
		
	
	
	
#Liste
	#Liste ne stocke que référence vers objet
	# donc ne prend pas de place (juste adresse)
	
	# ********* Même opération car séquence *********
	
	# Range (c'est une liste)
		range(3) 		--> [0, 1 , 2]
		range(1, 10, 2) --> [1, 3 , 5, 7, 9]
	
	l = []	# liste vide
	l = [4,' spam', True, 3.2]
	l[3] 		--> 3.2
	l[0] = l[0] + 2
	l 			-->  [6, 'spam', True, 3.2]
	l[1:2] 		-->  'spam'
	
	# Insérer
		l[1:2] = ['egg', 'spam']
		l 		-->  [6,'egg', 'spam', True, 3.2]
		l[3:4] = ['egg', 'beans']
		l 		-->  [6,'egg', 'spam', 'egg', 'beans', 3.2]	# ca a enlevé TRUE
	# Contracter ou effacer
		l[1:3] = []	# liste vide
		l 		-->  [6, 'egg', 'beans', 3.2]	# ca a enlevé TRUE
	
	# Econome en mémoire car pas de copie
		# append
			l.append('34')
			l 		-->  [6, 'egg', 'beans', 3.2, '34']
		# extend ()
			l.extend([3, 5, 9])
			l 		-->  [6, 'egg', 'beans', 3.2, '34', 3, 5, 9]
		#Supprimer
			del l[0] 		# On supprime le premier élément de la liste
			l.remove('a') 	#Attention ne supprime que la premiere occurrence !
			l = [i for i in l if i != 'a']
			
		# pop
			#Retourne le dernier élément de la liste et l'enlève de la liste
			l.pop 	-->  9
			l 		-->  [6, 'egg', 'beans', 3.2, '34', 3, 5]
	
	#Fonction ordre
		l.sort()
		sorted(l)
		l.reverse()
		# Exemple :  prendre le 3ème plus grand mots
			sorted(s, key=len, reverse=True)[2]
		
		

#Tuple
	# ********* Même opération car séquence *********
	# Comme liste mais immuable (pas de modification après création)
	
	t = ()	# liste vide	
	type(t) 		-->  <type 'tuple'>
	
	t = (4, )			# Seulement si un seul élément
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
	while True: 	#ne s'arrête jamais
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
		# Si aucun Return, ça retourne <None>
		# Sinon : 
		Return 'fin'

	-->fct_carre(l)
	-->fct_carre(l2)
	
	#Description
	def table(nb, max=10):
		"""Fonction affichant la table de multiplication par nb 
		de 1*nb à max*nb (max >= 0)"""
		# La chaine qui permet de définir la fonction est une docString
		# Si on tape help(table), elle s'affichera

		
# Dictionnaire
	# ----- Voire Table de hash ----- 
	# Definition: Collection non ordonnée de couple Clé-Valeur
	
	#Création
		d = dict()
		d = dict{}
		# A la main
		d = {'marc' : 39, 'alice' : 30, 'eric' : 38}
		# par liste de Tuple
		l = [('marc',39),('alice',30),('eric',38)]
		d = dict(l)
	
	#Opération
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
	# Definition : Ensemble non ordonné d'objet unique (objet immuable)
	
	#Création
		# A la main
		s = {1,2,3,'spam'}
		# par liste 
		l = [1,2,3,3,'spam']
		s = set(l)
		s		--> set([1,2,3,'spam'])  #Objet doit être unique
	#Opération
		s.add('egg')
		s		--> set([1,2,3,'egg','spam'])
		s.remove(2)
		s		--> set([1,3,'egg','spam'])
		s.update([5,6])
		s		--> set([1,3,5,6,'egg','spam'])
	#Différence
		s2 = {1,5,'ham'}
		s - s2 	--> set([3,6,'egg','spam'])				# Différence
		s | s2 	--> set([1,3,5,6,'egg','spam','ham'])	# Union
		s & s2 	--> set([1,5])							# Intersection

	#FrozenSet (Set immuable)
		fs = frozenset(s)
		fs.add(3)  --> Error 
		
		
# Référence partagée
	# -- au moins 2 variables référence un même objet --
	a = [1,2]
	b = a
	a[0] = 'spam'
	b[0] 	--> 'spam' # et non pas 1
	
	#Shalow Copy
	# -- Faire que b reste le même --
	b = a[:]
	a[0] = 'spam'
	b[0] 	--> 1
		#Exception
		a = [1,[2]]
		b = a[:]
		a [1][0] = 'Spam'
		b [1][0]	--> 'spam' # et non pas 1
		#Comment éviter cela
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
	# Est considéré comme faux :
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
	# Un itérateur ne peut parcourir un objet qu'une seule fois
	# Objet a 2 méthodes 
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
	#w : write (va créer le fichier ou le vider
	for i in range(100):
		line = '{} {}\n'.format(i, i**2)
		#\n : retour chariot
		f.write(line)
	f.close()		#Save et close
	
	#Lire 
	#parcourir les lignes car un fichier a un itérateur par ligne
	f = open (r'C:\tmp\spam.txt', 'r')
	f2 = open (r'C:\tmp\spam2.txt', 'w')
	for l in f:
		f2.write(l.replace(' ',', '))
	f.close()
	f2.close()
	
# Fonction LAMBDA
	f = lambda x: x**2 - 3
	f(1) 	--> -2  	#Aucun interêt
	
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
	
# Compréhension de liste
# Puissance des itérateurs avec syntaxe simple
	# Comme MAP
	[x**2 for x in range(10)]
		--> [0,1,4,9,16,25,36,49,64,81]
	
	# Comme FILTER
	[x**2 for x in range(10) if x % 7 ==0]
		--> [0,49]
	
	#Compréhension de SET (idem)
	{i**3 for i range(10)}
		--> set([0,1,8,64,512,343,216,729,27,125])
	
	#Compréhension de Dictionnaire (idem)
	{i: i **2 for i in range(10)}
		--> {0:0, 1:1, 2:4, 3:9, 4:16, 5:25, 6:36, 7:49, 8:64, 9:81}
	# Changer des dico
	d = {123 : 'marc', 145 : 'eric', 655 : 'jean'}
	d[123]		--> 'marc'
	# Le dico n'est pas fait pour accéder au clé par valeur
	# Sans faire de manière itérative
	# --> renverser dictionnaire à l'envers
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



			#Les parenthèses délimitent les tuples, les crochets [] délimitent les listes 
			# et les accolades {} délimitent les dictionnaires.
			
#Voyons comment ajouter des clés et valeurs dans notre dictionnaire vide :
>>> mon_dictionnaire = {}
>>> mon_dictionnaire["pseudo"] = "Prolixe"
>>> mon_dictionnaire["mot de passe"] = "*"
>>> mon_dictionnaire
{'mot de passe': '*', 'pseudo': 'Prolixe'}
>>>
			
#Nous indiquons entre crochets la clé à laquelle nous souhaitons accéder. 
#Si la clé n'existe pas, elle est ajoutée au dictionnaire avec la valeur spécifiée après le signe =. 
#Sinon, l'ancienne valeur à l'emplacement indiqué est remplacée par la nouvelle :
>>> mon_dictionnaire = {}
>>> mon_dictionnaire["pseudo"] = "Prolixe"
>>> mon_dictionnaire["mot de passe"] = "*"
>>> mon_dictionnaire["pseudo"] = "6pri1"
>>> mon_dictionnaire
{'mot de passe': '*', 'pseudo': '6pri1'}
>>>

#Pour accéder à la valeur d'une clé précise, c'est très simple :
>>> mon_dictionnaire["mot de passe"]
'*'
>>>
			#Si la clé n'existe pas dans le dictionnaire, une exception de type KeyError sera levée.

			#Exemple : Echéquier
			echiquier = {}
			echiquier['a', 1] = "tour blanche" # En bas à gauche de l'échiquier
			echiquier['b', 1] = "cavalier blanc" # À droite de la tour
			echiquier['c', 1] = "fou blanc" # À droite du cavalier
			echiquier['d', 1] = "reine blanche" # À droite du fou
			# ... Première ligne des blancs
			echiquier['a', 2] = "pion blanc" # Devant la tour
			echiquier['b', 2] = "pion blanc" # Devant le cavalier, à droite du pion
			# ... Seconde ligne des blancs
			
#On peut aussi créer des dictionnaires déjà remplis :
placard = {"chemise":3, "pantalon":6, "tee-shirt":7}
			
#Supprimer des clés d'un dictionnaire
placard = {"chemise":3, "pantalon":6, "tee shirt":7}
del placard["chemise"]

#La méthode pop supprime également la clé précisée mais elle renvoie la valeur supprimée :
>>> placard = {"chemise":3, "pantalon":6, "tee shirt":7}
>>> placard.pop("chemise")
3
>>>


# On se sert parfois des dictionnaires pour stocker des fonctions.
>>> print_2 = print # L'objet print_2 pointera sur la fonction print
>>> print_2("Affichons un message")
Affichons un message
>>>

			#En pratique, on affecte rarement des fonctions de cette manière. C'est peu utile. 
			#Par contre, on met parfois des fonctions dans des dictionnaires :
			
>>> def fete():
...     print("C'est la fête.")
... 
>>> def oiseau():
...     print("Fais comme l'oiseau...")
...
>>> fonctions = {}
>>> fonctions["fete"] = fete # on ne met pas les parenthèses
>>> fonctions["oiseau"] = oiseau
>>> fonctions["oiseau"]
<function oiseau at 0x00BA5198>
>>> fonctions["oiseau"]() # on essaye de l'appeler
Fais comme l'oiseau...
>>>

			#On commence par définir deux fonctions, fete et oiseau (pardonnez l'exemple).
			#On crée un dictionnaire nommé fonctions
			#On met dans ce dictionnaire les fonctions fete et oiseau. 
						#La clé pointant vers la fonction est le nom de la fonction, tout bêtement, 
						#mais on aurait pu lui donner un nom plus original.
			#On essaye d'accéder à la fonction oiseau en tapant fonctions[« oiseau »]. 
						#Python nous renvoie un truc assez moche, <function oiseau at 0x00BA5198>, 
						#mais vous comprenez l'idée : c'est bel et bien notre fonction oiseau. 
						#Toutefois, pour l'appeler, il faut des parenthèses, comme pour toute fonction qui se respecte.
			#En tapant fonctions["oiseau"](), on accède à la fonction oiseau et on l'appelle dans la foulée.


#LES METHODES DE PARCOURS

#Parcours des clés
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
			
			#La méthode keys (« clés » en anglais) renvoie la liste des clés contenues dans le dictionnaire. 
			# En vérité, ce n'est pas tout à fait une liste (essayez de taper fruits.keys() dans votre interpréteur) 
			# mais c'est une séquence qui se parcourt comme une liste.

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
...     print("Un des fruits se trouve dans la quantité 21.")
... 
Un des fruits se trouve dans la quantité 21.
>>>


#Parcours des clés et valeurs simultanément       
			#Pour avoir en même temps les indices et les objets d'une liste, on utilise la fonction enumerate 
			#Pour faire de même avec les dictionnaires, on utilise la méthode items
			#Elle renvoie une liste, contenant les couples clé : valeur, sous la forme d'un tuple. 
			
>>> fruits = {"pommes":21, "melons":3, "poires":31}
>>> for cle, valeur in fruits.items():
...     print("La clé {} contient la valeur {}.".format(cle, valeur))
... 
La clé melons contient la valeur 3.
La clé poires contient la valeur 31.
La clé pommes contient la valeur 21.
>>>



#LES DICTIONNAIRES ET PARAMÈTRES DE FONCTION

			#on avait réussi à intercepter tous les paramètres de la fonction… sauf les paramètres nommés.
			
#Récupérer les paramètres nommés dans un dictionnaire
>>> def fonction_inconnue(**parametres_nommes):
...     """Fonction permettant de voir comment récupérer les paramètres nommés
...     dans un dictionnaire"""
...     
...     
...     print("J'ai reçu en paramètres nommés : {}.".format(parametres_nommes))
... 
>>> fonction_inconnue() # Aucun paramètre
J'ai reçu en paramètres nommés : {}
>>> fonction_inconnue(p=4, j=8)
J'ai reçu en paramètres nommés : {'p': 4, 'j': 8}
>>>
			
			#Pour capturer tous les paramètres nommés non précisés dans un dictionnaire, il faut mettre deux étoiles ** avant le nom du paramètre.
			#Si vous passez des paramètres non nommés à cette fonction, Python lèvera une exception.

#Ainsi, pour avoir une fonction qui accepte n'importe quel type de paramètres, 
#nommés ou non, dans n'importe quel ordre, dans n'importe quelle quantité, il faut la déclarer de cette manière :
def fonction_inconnue(*en_liste, **en_dictionnaire):     


#Transformer un dictionnaire en paramètres nommés d'une fonction
>>> parametres = {"sep":" >> ", "end":" -\n"}
>>> print("Voici", "un", "exemple", "d'appel", **parametres)
Voici >> un >> exemple >> d'appel -
>>>
			#Les paramètres nommés sont transmis à la fonction par un dictionnaire. 
			#Pour indiquer à Python que le dictionnaire doit être transmis comme des paramètres nommés, 
			# on place deux étoiles avant son nom ** dans l'appel de la fonction.

#Comme vous pouvez le voir, c'est comme si nous avions écrit :
>>> print("Voici", "un", "exemple", "d'appel", sep=" >> ", end=" -\n")
Voici >> un >> exemple >> d'appel -
>>>

#----------------------------------------------------------





#----------------------------------------------------------
# 2.3. LES LISTES ET TUPLES (2/2)
#----------------------------------------------------------

#Pour « convertir » une chaîne en liste, on va utiliser une méthode de chaîne nommée split 
>>> ma_chaine = "Bonjour à tous"
>>> ma_chaine.split(" ")
['Bonjour', 'à', 'tous']
>>>

#Pour « convertir » une liste en chaîne
>>> ma_liste = ['Bonjour', 'à', 'tous']
>>> " ".join(ma_liste)
'Bonjour à tous'
>>>

#Une application pratique
#si on a un nombre flottant tel que « 3.999999999999998 », on souhaite obtenir comme résultat « 3.999 »
>>> afficher_flottant(3.99999999999998)
'3,999'

def afficher_flottant(flottant):
			#"""Fonction prenant en paramètre un flottant et renvoyant une chaîne de caractères représentant la troncature de ce nombre. 
			#La partie flottante doit avoir une longueur maximum de 3 caractères.
			#De plus, on va remplacer le point décimal par la virgule"""
			
			if type(flottant) is not float:
						raise TypeError("Le paramètre attendu doit être un flottant")
			flottant = str(flottant)
			partie_entiere, partie_flottante = flottant.split(".")
			# La partie entière n'est pas à modifier
			# Seule la partie flottante doit être tronquée
			return ",".join([partie_entiere, partie_flottante[:3]])


#Les fonctions dont on ne connaît pas à l'avance le nombre de paramètres
>>> def fonction_inconnue(*parametres):
...     """Test d'une fonction pouvant être appelée avec un nombre variable de paramètres"""
...     
...     print("J'ai reçu : {}.".format(parametres))
... 
>>> fonction_inconnue() # On appelle la fonction sans paramètre
J'ai reçu : ().
>>> fonction_inconnue(33)
J'ai reçu : (33,).
>>> fonction_inconnue('a', 'e', 'f')
J'ai reçu : ('a', 'e', 'f').
>>> var = 3.5
>>> fonction_inconnue(var, [4], "...")
J'ai reçu : (3.5, [4], '...').
>>>#Python va placer tous les paramètres de la fonction dans un tuple, 
#que l'on peut ensuite traiter comme on le souhaite.

def fonction_inconnue(nom, prenom, *commentaires):
>>>#vous devez impérativement préciser un nom et un prénom, et ensuite vous mettez ce que vous voulez

 
def afficher(*parametres, sep=' ', fin='\n'):
			"""Fonction chargée de reproduire le comportement de print.
			
			Elle doit finir par faire appel à print pour afficher le résultat.
			Mais les paramètres devront déjà avoir été formatés. 
			On doit passer à print une unique chaîne, en lui spécifiant de ne rien mettre à la fin :

			print(chaine, end='')"""
			
			# Les paramètres sont sous la forme d'un tuple
			# Or on a besoin de les convertir
			# Mais on ne peut pas modifier un tuple
			# On a plusieurs possibilités, ici je choisis de convertir le tuple en liste
			parametres = list(parametres)
			# On va commencer par convertir toutes les valeurs en chaîne
			# Sinon on va avoir quelques problèmes lors du join
			for i, parametre in enumerate(parametres):
						parametres[i] = str(parametre)
			# La liste des paramètres ne contient plus que des chaînes de caractères
			# À présent on va constituer la chaîne finale
			chaine = sep.join(parametres)
			# On ajoute le paramètre fin à la fin de la chaîne
			chaine += fin
			# On affiche l'ensemble
			print(chaine, end='')
  
  
#On utilise une étoile * dans les deux cas. 
#Si c'est dans une définition de fonction, cela signifie que les paramètres fournis non attendus 
#lors de l'appel seront capturés dans la variable, sous la forme d'un tuple. 
#Si c'est dans un appel de fonction, au contraire, cela signifie que la variable 
#sera décomposée en plusieurs paramètres envoyés à la fonction.
>>> liste_des_parametres = [1, 4, 9, 16, 25, 36]
>>> print(*liste_des_parametres)
1 4 9 16 25 36
>>>



#Les compréhensions de liste
			"Les compréhensions de liste (« list comprehensions » en anglais) sont un moyen de filtrer ou modifier une liste très simplement."
			"Les compréhensions de liste permettent de parcourir une liste en en renvoyant une seconde, modifiée ou filtrée."
			#S'écrit : nouvelle_squence = [element for element in ancienne_squence if condition]
			
#Metttre au carré
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
			#La liste contient des tuples, contenant chacun un couple : le nom du fruit et sa quantité en magasin.
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
			# On change le sens de l'inventaire, la quantité avant le nom
			inventaire_inverse = [(qtt, nom_fruit) for nom_fruit,qtt in inventaire]
			# On n'a plus qu'à trier dans l'ordre décroissant l'inventaire inversé
			# On reconstitue l'inventaire trié
			inventaire = [(nom_fruit, qtt) for qtt,nom_fruit in sorted(inventaire_inverse, \
						reverse=True)]
						
#Solution 2
			# On change le sens de l'inventaire, la quantité avant le nom
			inventaire_inverse = [(qtt, nom_fruit) for nom_fruit,qtt in inventaire]
			# On trie l'inventaire inversé dans l'ordre décroissant
			inventaire_inverse.sort(reverse=True)
			# Et on reconstitue l'inventaire
			inventaire = [(nom_fruit, qtt) for qtt,nom_fruit in inventaire_inverse]
#_____________________________________________________

#--------------------------------------------------------------------------------




#----------------------------------------------------------
# 2.2. LES LISTES ET TUPLES (1/2)
#----------------------------------------------------------

#Création de listes
>>> ma_liste = list() # On crée une liste vide
>>> type(ma_liste)
<class 'list'>
>>> ma_liste
[]
>>>
#Autres méthode
>>> ma_liste = [] # On crée une liste vide
>>>
#Liste non vide
>>> ma_liste = [1, 2, 3, 4, 5] # Une liste avec cinq objets
>>> print(ma_liste)
[1, 2, 3, 4, 5]
>>>

#Liste de liste
>>> ma_liste = [1, 3.5, "une chaine", []]
>>>

#Accéder aux éléments d'une liste
>>> ma_liste = ['c', 'f', 'm']
>>> ma_liste[0] # On accède au premier élément de la liste
'c'
>>> ma_liste[2] # Troisième élément
'm'
>>> ma_liste[1] = 'Z' # On remplace 'f' par 'Z'
>>> ma_liste
['c', 'Z', 'm']
>>>

#Ajouter un élément à la fin de la liste
>>> ma_liste = [1, 2, 3]
>>> ma_liste.append(56) # On ajoute 56 à la fin de la liste
>>> ma_liste
[1, 2, 3, 56]
>>>

#La méthode append, comme beaucoup de méthodes de listes, travaille directement sur l'objet et ne renvoie donc rien !
>>> chaine1 = "une petite phrase"
>>> chaine2 = chaine1.upper() # On met en majuscules chaine1
>>> chaine1                   # On affiche la chaîne d'origine
'une petite phrase'
>>> # Elle n'a pas été modifiée par la méthode upper
... chaine2                   # On affiche chaine2
'UNE PETITE PHRASE'
>>> # C'est chaine2 qui contient la chaîne en majuscules
... # Voyons pour les listes à présent
... liste1 = [1, 5.5, 18]
>>> liste2 = liste1.append(-15) # On ajoute -15 à liste1
>>> liste1                      # On affiche liste1
[1, 5.5, 18, -15]
>>> # Cette fois, l'appel de la méthode a modifié l'objet d'origine (liste1)
... # Voyons ce que contient liste2
... liste2
>>> # Rien ? Vérifions avec print
... print(liste2)
None
>>>

#insérer un élément dans une liste au milieu
>>> ma_liste = ['a', 'b', 'd', 'e']
>>> ma_liste.insert(2, 'c') # On insère 'c' à l'indice 2
>>> print(ma_liste)
['a', 'b', 'c', 'd', 'e']
>>> #La méthode va décaler les objets d'indice supérieur ou égal à 2. c va donc s'intercaler entre b et d.

#Concaténation de listes
>>> ma_liste1 = [3, 4, 5]
>>> ma_liste2 = [8, 9, 10]
>>> ma_liste1.extend(ma_liste2) # On insère ma_liste2 à la fin de ma_liste1
>>> print(ma_liste1)
[3, 4, 5, 8, 9, 10]
>>> ma_liste1 = [3, 4, 5]
>>> ma_liste1 + ma_liste2
[3, 4, 5, 8, 9, 10]
>>> ma_liste1 += ma_liste2 # Identique à extend
>>> print(ma_liste1)
[3, 4, 5, 8, 9, 10]
>>>

# DELETE
>>> ma_liste = [-5, -2, 1, 4, 7, 10]
>>> del ma_liste[0] # On supprime le premier élément de la liste
>>> ma_liste
[-2, 1, 4, 7, 10]
>>> del ma_liste[2] # On supprime le troisième élément de la liste
>>> ma_liste
[-2, 1, 7, 10]
>>>

# REMOVE
#On peut aussi supprimer des éléments de la liste grâce à la méthode remove 
#qui prend en paramètre non pas l'indice de l'élément à supprimer, mais l'élément lui-même.
>>> ma_liste = [31, 32, 33, 34, 35]
>>> ma_liste.remove(32)
>>> ma_liste
[31, 33, 34, 35]
>>> #La méthode remove ne retire que la première occurrence de la valeur trouvée dans la liste !


#PARCOURIR une liste
>>> ma_liste = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
>>> i = 0 # Notre indice pour la boucle while
>>> while i < len(ma_liste):
...     print(ma_liste[i])
...     i += 1 # On incrémente i, ne pas oublier !

>>> # Cette méthode est cependant préférable
... for elt in ma_liste: # elt va prendre les valeurs successives des éléments de ma_liste
...     print(elt)


#La fonction ENUMERATE et les TUPLES
>>> ma_liste = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
>>> for i, elt in enumerate(ma_liste):
...     print("À l'indice {} se trouve {}.".format(i, elt))
... 
À l'indice 0 se trouve a.
À l'indice 1 se trouve b.
À l'indice 2 se trouve c.
À l'indice 3 se trouve d.
À l'indice 4 se trouve e.
À l'indice 5 se trouve f.
À l'indice 6 se trouve g.
À l'indice 7 se trouve h.
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
>>>#Quand on parcourt chaque élément de l'objet renvoyé par enumerate, 
#on voit des tuples qui contiennent deux éléments : d'abord l'indice, 
#puis l'objet se trouvant à cet indice dans la liste passée en argument à la fonction enumerate.

>>> autre_liste = [
...     [1, 'a'],
...     [4, 'd'],
...     [7, 'g'],
...     [26, 'z'],
...         ] # J'ai étalé la liste sur plusieurs lignes
>>> for nb, lettre in autre_liste:
...     print("La lettre {} est la {}e de l'alphabet.".format(lettre, nb))
La lettre a est la 1e de l'alphabet.
La lettre d est la 4e de l'alphabet.
La lettre g est la 7e de l'alphabet.
La lettre z est la 26e de l'alphabet.
>>>


#Nous avons brièvement vu les tuples un peu plus haut, grâce à la fonction enumerate. 
#Les tuples sont des listes immuables, qu'on ne peut modifier. #
#En fait, vous allez vous rendre compte que nous utilisons depuis longtemps des tuples sans nous en rendre compte.
#Un tuple se définit comme une liste, sauf qu'on utilise comme délimiteur des parenthèses au lieu des crochets.
tuple_vide = ()
tuple_non_vide = (1,) # est équivalent à ci dessous
tuple_non_vide = 1,
tuple_avec_plusieurs_valeurs = (1, 2, 5)
# À la différence des listes, les tuples, une fois créés, ne peuvent être modifiés : 
#  on ne peut plus y ajouter d'objet ou en retirer.


#Une fonction renvoyant plusieurs valeurs
def decomposer(entier, divise_par):
			"""Cette fonction retourne la partie entière et le reste de
			entier / divise_par"""

			p_e = entier // divise_par
			reste = entier % divise_par
			return p_e, reste
>>> #Et on peut ensuite capturer la partie entière et le reste dans deux variables, au retour de la fonction :
>>> partie_entiere, reste = decomposer(20, 3)
>>> partie_entiere
6
>>> reste
2
>>>#Si vous essayez de faire retour = decomposer(20, 3), vous allez capturer un tuple contenant deux éléments : 
#la partie entière et le reste de 20 divisé par 3.





#----------------------------------------------------------
# 2.1. Notre premier objet : les chaînes de caractères
#----------------------------------------------------------

# Mettre la chaîne en minuscule
>>> chaine = "NE CRIE PAS SI FORT !"
>>> chaine.lower()               
'ne crie pas si fort !'

# Si vous tapez type(chaine) dans l'interpréteur, vous obtenez <class 'str'>
# Un objet est issu d'une classe. 
# Les fonctions définies dans une classe sont appelées des méthodes.

# objet.methode()
# Une classe est un modèle qui servira à construire un objet ; 
#c'est dans la classe qu'on va définir les méthodes propres à l'objet.

# l'utilisateur peut taper « q » en majuscule ou en minuscule, la boucle s'arrêtera
chaine = str() # Crée une chaîne vide
# On aurait obtenu le même résultat en tapant chaine = ""
while chaine.lower() != "q":
			print("Tapez 'Q' pour quitter...")
			chaine = input()
print("Merci !")

#str() crée un objet chaîne de caractères

>>> minuscules = "une chaine en minuscules"
>>> minuscules.upper() # Mettre en majuscules
'UNE CHAINE EN MINUSCULES'
>>> minuscules.capitalize() # La première lettre en majuscule
'Une chaine en minuscules'
>>> espaces = "   une  chaine avec  des espaces   "
>>> espaces.strip() # On retire les espaces au début et à la fin de la chaîne
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
#J'ai coupé notre instruction, plutôt longue, à l'aide du signe « \ » placé avant un saut de ligne, 
#pour indiquer à Python que l'instruction se prolongeait au-dessous.


#Seconde syntaxe de la méthode format
# formatage d'une adresse
>>> adresse = "{no_rue}, {nom_rue}, {code_postal}, {nom_ville}".format(no_rue=5, nom_rue="rue des Postes", code_postal=75003, nom_ville="Paris")
>>> print(adresse)
5, rue des Postes 75003 Paris (France)

#La concaténation de chaînes
>>> prenom = "Paul"
>>> message = "Bonjour"
>>> chaine_complete = message + prenom # On utilise le symbole '+' pour concaténer deux chaînes
... print(chaine_complete) # Résultat :
BonjourPaul
>>> # Pas encore parfait, il manque un espace
... chaine_complete = message + " " + prenom
>>> print(chaine_complete) # Résultat :
Bonjour Paul

#La Conversion de données : Str
>>> age = 21
>>> message = "J'ai " + str(age) + " ans."
>>> print(message)
J'ai 21 ans.
>>>

#Parcours et sélection de chaînes par indices
#sélectionner la première lettre d'une chaîne
>>> chaine = "Salut les ZER0S !"
>>> chaine[0] # Première lettre de la chaîne
'S'
>>> chaine[2] # Troisième lettre de la chaîne
'l'
>>> chaine[-1] # Dernière lettre de la chaîne
'!'
#Rappelez-vous, on commence à compter à partir de 0. La première lettre est donc à l'indice 0

#La longueur de la chaîne 
>>> chaine = "Salut"
>>> len(chaine)
5


#Méthode de parcours par while
chaine = "Salut"
i = 0 # On appelle l'indice 'i' par convention
while i < len(chaine):
			print(chaine[i]) # On affiche le caractère à chaque tour de boucle
			i += 1

#Enfin, une dernière petite chose : vous ne pouvez changer les lettres de la chaîne en utilisant les indices.
>>> mot = "lac"
>>> mot[0] = "b" # On veut remplacer 'l' par 'b'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
#Python n'est pas content. Il ne veut pas que vous utilisiez les indices pour modifier des caractères de la chaîne. 
#Pour ce faire, il va falloir utiliser la sélection.

#Sélection de chaînes
>>> presentation = "salut"
>>> presentation[0:2] # On sélectionne les deux premières lettres
'sa'
>>> presentation[2:len(presentation)] # On sélectionne la chaîne sauf les deux premières lettres
'lut'
>>> presentation[:2] # Du début jusqu'à la troisième lettre non comprise
'sa'
>>> presentation[2:] # De la troisième lettre (comprise) à la fin
'lut'

#Remplacer les caractères d'une String
>>> mot = "lac"
>>> mot = "b" + mot[1:]
>>> print(mot)
bac
# Plutot : nous avons à notre disposition les méthodes count, find et replace




#----------------------------------------------------------
# 1.9. TP
#----------------------------------------------------------

# -*-coding:Latin-1 -*
import os
import random
# Programme modélisant une roue de casino

argent = 1000

print("Vous vous installez à la table de roulette avec", argent, "$.")

nb_choisi = -1
while nb_choisi<0 or nb_choisi>49:
						nb_choisi = input("Choisissez un nombre entre 0 et 49 : ")

						#On convertit le nbe misé
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
									print("La mise saisie est négative ou nulle.")
						if mise > argent:
									print("Vous ne pouvez miser autant, vous n'avez que", argent, "$")

#Générer un nombre aléatoire
numero_gagnant = int(random.randrange(0,50)) # Tire un nbe entre 0 et 49
print("La roulette tourne... ... et s'arrête sur le numéro", numero_gagnant)

#Tester si le nombre est égale ou non
if nb_choisi == numero_gagnant:
						print("Félicitations ! Bon numero, vous gagnez : ", 3 * mise) 
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

# Quand Python rencontre une erreur ds le code, il lève une exception.
>>> # Exemple classique : test d'une division par zéro
>>> variable = 1/0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: int division or modulo by zero

# Forme minimal du bloc TRY
			#Mettre les instructions à tester dans un premier bloc et les instructions à exécuter en cas d'erreur ds un autre bloc
			annee = input()
			try: # On essaye de convertir l'année en entier
						annee = int(annee)
			except:
						print("Erreur lors de la conversion de l'année.")
						annee = 2000                        
						#Valeur par défaut pour que la suite ne plante pas

			# Cette méthode est assez grossière. Elle essaye une instruction et intercepte n'importe quelle exception 
			# C'est une mauvaise habitude à prendre ! 
			# + Python peut lever des exceptions qui ne signifient pas nécessairement qu'il y a eu une erreur.
# Voici une manière plus élégante et moins dangereuse :

# Forme plus complète
try:
			resultat = numerateur / denominateur
except:
			print("Une erreur est survenue... laquelle ?")        
			
			# 1 : NameError : l'une des variables numerateur ou denominateur n'a pas été définie (elle n'existe pas).
			# 2 : TypeError : l'une des variables numerateur ou denominateur ne peut diviser ou être divisée (string) 
			# 3 : ZeroDivisionError : encore elle ! Si denominateur vaut 0
			
try:
			resultat = numerateur / denominateur
except NameError:
			print("La variable numerateur ou denominateur n'a pas été définie.")
except TypeError:
			print("La variable num ou denum possède un type incompatible avec la division.")
except ZeroDivisionError:
			print("La variable denominateur est égale à 0.")   

			# Plus simple, on peut capturer  l'exception et afficher son message 
try:
			# Bloc de test
except type_de_l_exception as exception_retournee:
			print("Voici l'erreur :", exception_retournee)

# Else va permettre d'exécuter une action si aucune erreur ne survient :
try:
			resultat = numerateur / denominateur
except NameError:
			print("La variable numerateur ou denominateur n'a pas été définie.")
except TypeError:
			print("Le numerateur ou denominateur possède un type incompatible")
except ZeroDivisionError:
			print("La variable denominateur est égale à 0.")
else:
			print("Le résultat obtenu est", resultat)

# Finally permet d'exécuter du code après un bloc try
try:
			resultat = numerateur / denominateur
except TypeDInstruction:
			print("...")
finally:
			# Instruction(s) exécutée(s) qu'il y ait eu des erreurs ou non

# Pass :  tester un bloc d'instructions… mais ne rien faire si erreur
try:
			resultat = numerateur / denominateur
except: 
			pass


# Les Assertions
			# Les assertions sont un moyen simple de s'assurer, avant de continuer, qu'une condition est respectée. 
			#En général, on les utilise dans des blocs try … except.
assert test
			
			# Si le test renvoie True, l'exécution se poursuit normalement. Sinon, une exception AssertionError est levée.
			>>> var = 5
			>>> assert var == 5
			>>> assert var == 8
			Traceback (most recent call last):
			  File "<stdin>", line 1, in <module>
			AssertionError
			>>>

			#À quoi cela sert-il, concrètement ? Exemple :
			annee = input("Saisissez une année supérieure à 0 :")
			try:
						annee = int(annee) # Conversion de l'année
						assert annee > 0
			except ValueError:
						print("Vous n'avez pas saisi un nombre.")
			except AssertionError:
						print("L'année saisie est inférieure ou égale à 0.")



#----------------------------------------------------------
# 1.7. Pas à pas vers la modularité (2/2)
#----------------------------------------------------------

# Mettre notre code dans un fichier que nous pourrons lancer  à volonté, comme un véritable programme !

#Emprisonnons notre programme dans un fichier
			# Programme testant si une année est bissextile: 
						#Insérez le code dans ce fichier et enregistrez-le avec l'extension .py (exemple bissextile.py)
						
						# -*-coding:Latin-1 -*
						import os 
						# Programme testant si une année, est bissextile ou non
						annee = input("Saisissez une année : ") 
						annee = int(annee) 
						if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
									print("L'année saisie est bissextile.")
						else:
									print("L'année saisie n'est pas bissextile.")
						os.system("pause")
						
			#Explication du code :
						# -*-coding:Latin-1 -*
									#il est nécessaire de préciser à Python l'encodage de ces accents
						import os 
									# On importe le module os qui dispose de variables et de fonctions utiles pour dialoguer 
									# avec votre système d'exploitation
						os.system("pause")
									# On met le programme en pause pour éviter qu'il ne se referme (Windows)

			# On peut aussi appeler un module depuis un autre, contenu dans le même répertoire en précisant le nom du fichier (sans l'extension .py)
			
			# multipli.py
			"""module multipli contenant la fonction table"""
			def table(nb, max=10):
						"""Fonction affichant la table de multiplication par nb de
						1 * nb jusqu'à max * nb"""
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
			
			# Si l'on met tout le code dans le même module Comment séparer les fonctions à importer dans d'éventuels autres modules
			# et les commande qui ne doivent être actionné que si l'on clic sur ce module
			
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
			
			# Voilà. À présent, si vous faites un double-clic directement sur le fichier multipli.py, vous allez voir
			# la table de multiplication par 4. En revanche, si vous l'importez, le code de test ne s'exécutera pas. 
			
			# Si la variable __name__ est égale à __main__           Cela veut dire que le fichier appelé est le fichier exécuté


# Les packages
# Un package sert à regrouper plusieurs modules
			
			# Importer des packages
			import nom_bibliotheque
			# Pointe vers le sous-package evenements
			nom_bibliotheque.evenements 
			# Pointe vers le module clavier
			nom_bibliotheque.evenements.clavier 
			
			# Importer un seul module
			from nom_bibliotheque.objets import bouton

			# Créer ses propres packages
			# En Python, vous trouverez souvent le fichier d'initialisation de package __init__.py dans un répertoire destiné à devenir un package.
			
			

#----------------------------------------------------------
# 1.6. Pas à pas vers la modularité (1/2)
#----------------------------------------------------------


#Les fonctions Lambda
			#fonctions extrêmement courtes car limitées à une seule instruction
			f = lambda x, y: x + y


# Modules
# Un module est grossièrement un bout de code que l'on a enfermé dans un fichier. 
# On emprisonne ainsi des fonctions et des variables ayant ttes un rapport entre elles. 
			# La méthode Import
			>>> import math
			# Toutes les fonctions mathématiques contenues dans ce module sont mtnt accessibles. 
			# Pour appeler une fonction du module, taper le nom du module suivi d'un point « . » puis du nom de la fonction. 
			>>> math.sqrt(16)
			4
			>>>
			
			#Mais comment suis-je censé savoir quelles fonctions existent et ce que fait math.sqrt dans ce cas précis ?
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

			#Tapez Q pour revenir à la fenêtre d'interpréteur, 
			#Espace pour avancer d'une page, Entrée pour avancer d'une ligne. 
			#Vous pouvez également passer un nom de fonction en paramètre de la fonction help.
			>>> help("math.sqrt")
			Help on built-in function sqrt in module math:
			sqrt(...)
						sqrt(x)
						Return the square root of x.


			#vous pourrez vouloir changer le nom de l'espace de noms 
			#dans lequel sera stocké le module importé
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
i = 0    # C'est notre var compteur que nous allons incrémenter dans la boucle
while i < 10:    # Tant que i est strictement inférieure à 10
			print(i + 1, "*", nb, "=", (i + 1) * nb)
			i += 1               # On incrémente i de 1 à chaque tour de boucle



#BREAK & CONTINUE
# 1 est toujours vrai -> boucle infinie
while 1: 
			lettre = input("Tapez 'Q' pour quitter : ")
			if lettre == "Q":
						print("Fin de la boucle")
						break
#Parfois, break est véritablement utile et fait gagner du temps. 
#Mais ne l'utilisez pas à outrance, préférez une boucle avec 
#une condition claire plutôt qu'un bloc d'instructions avec un break


#Le mot-clé continue permet de… continuer une boucle, en repartant directement 
#à la ligne du while ou for
i = 1
while i < 20: # Tant que i est inférieure à 20
			if i % 3 == 0:
						i += 4 # On ajoute 4 à i
						print("On incrémente i de 4. i est maintenant égale à", i)
						continue # On retourne au while sans exécuter les autres lignes
			print("La variable i =", i)
			i += 1 # Dans le cas classique on ajoute juste 1 à i

#Résultat
La variable i = 1
La variable i = 2
On incrémente i de 4. i est maintenant égale à 7
La variable i = 7...















 
