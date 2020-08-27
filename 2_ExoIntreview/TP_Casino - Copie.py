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
            mise = int(mise)
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

