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
