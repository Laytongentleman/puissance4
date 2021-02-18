from random import randint

# ------------- Fonctions qui gèrent la grille -------------------

# initialise la grille
def init(l, h):
    """ prends la longueur et hauteur du tableau
    et renvoie toujours un tableau à 2 dimensions rempli de 0"""
    #attention ne pas ecrire [ [0] * h] *l] car cela relie chaque colonne avec les autres
    g = [ [0] * h for i in range(l)]
    return g


def display(g):
    """fonction d'affichage qui affiche dans le bon sens le tableau
        en plus de convertir les nombres en symboles:
        1 -> O, 2 -> X  et 0 -> " "  """
    # on crée une copie qui va être affichée
    cg = init(len(g), len(g[0]))

    # on remplit la copie à l'aide de g
    for i in range(len(g)):
        for j in range(len(g[i])):
            cg[i][j] = "O" if g[i][j] == 1 else "X" if g[i][j] == 2  else " "

    # on affiche
    print(" _______________")
    for i in range(len(g[0])):
        print("", end=" |")
        for j in range(len(g)):
            print(cg[j][i], end="|")
        print()



#------------ Fonctions de vérification de fin de jeu ------------------------

def vertical (g, j, l, c):
    """ vérifie la colonne où le coup est joué """
    point = 0
    for i in range (6):
        if g[c][i]== 1 and j:
            point+=1
        elif g[c][i]==2 and not j:
            point+=1
        else:
            point=0
        if point==4:
            return True

def horiz (g, j, l, c):
    """ vérifie la ligne où le coup est joué """
    point=0
    for i in range (7):
        if g[i][l]==1 and j:
            point+=1
        elif g[i][l]==2 and not j:
            point+=1
        else:
            point=0
        if point==4:
            return True

def diagd (g, j, l, c):
    """ vérifie la diagonale haut gauche vers bas droite """
    point=0
    t = max(l,c) - min(l,c)
    coord = [0,0] # 0 c, 1 l
    if l > c :
        coord [1] = t
    else:
        coord [0] = t
    while True:
        if g[coord [0]][coord [1]]==1 and j:
            point+=1
        elif g[coord [0]][coord [1]]==2 and not j:
            point+=1
        else:
            point=0
        if point==4:
            return True
        coord[0] += 1
        coord[1] += 1
        if coord[0] > 6 or coord[1] > 5:
            return False

def diagm (g, j, l, c):
    """ vérifie la diagonale bas gauche vers haut droit """
    point=0
    coord = [c,l]
    while coord[0] >= 0 and coord[1] < 5:
        coord[0] -= 1
        coord[1] += 1
    while True:
        if g[coord [0]][coord [1]]==1 and j:
            point+=1
        elif g[coord [0]][coord [1]]==2 and not j:
            point+=1
        else:
            point=0

        if point==4:
            return True
        coord[0] += 1
        coord[1] -= 1
        if coord[0] > 6 or coord[1]<0:
            return False

def check (g, j, l, c, mode):
    """ fonction qui exécute toutes les vérifications"""
    gagner = "" # Variable qui permet d'afficher quelle vérification est vérifiée

    if vertical(g,j,l,c):
        gagner = "vertical"

    if horiz(g,j,l,c):
        gagner = "horizontal"

    if diagd(g,j,l,c):
        gagner = "diagonale Descendante"

    if diagm(g,j,l,c):
        gagner = "diagonale Montante"

    if gagner != "":
        display(g)
        if mode == "2j":
            print ("Le joueur", int(j)+1, "a gagné par", gagner, "!")
        if mode == "alea":
            if j:
                vic = "gagné"
            else:
                vic = "perdu"
            print ("Le bot a", vic, "par", gagner, "!")
        print ()
        return True


def fin (g):
    """détermine si la grille est pleine"""
    for i in range (len(g)):
        if coup_possible(g, i):
            return False
    display(g)
    print ("La grille est complète !")
    return True



# -------------- Fonctions qui gèrent le coup du joueur ou du bot -----------------

def coup_possible (g, c):
    """détermine si l'on peut jouer dans la colonne:
        - si la colonne demandée existe dans g
        - si la colonne n'est pas totalement remplie """
    if  c < len(g) and c >= 0:
        if g[c][0] == 0:
            return True
    return False


def choix_colonne (g):
    """demande au joueur la colone dans la quelle il veut jouer quand qu'il n'a pas donnée un nombre possible"""
    # variable qui permet de ne pas avoir une erreur si le joueur ne donnent pas un chiffre
    rep = None
    c = None

    while c == None and str(c) != rep:
        rep = input("colonne? ")

        for i in range (len(g)):
            if rep == str(i):
                c = i

    while not coup_possible (g, c):
        # fait rejouer le joueur si celui-ci a demandé une colonne pleine
        print ("La colonne est pleine. ")
        c = choix_colonne(g)
    return c


def coup_aléatoire (g, j):
    """fonction qui joue un coup aléatoire pour le joueur entré en argument """

    # donne une colonne au hasard
    c = randint (0, len(g)-1)
    while not coup_possible (g, c):
        c = randint (0, len(g)-1)

    # joue le coup du bot
    return jouer(g, j, c, "alea")


def jouer (g,j,c, mode):
    """joue le coup à partir du joueur, de la grille et de la colonne"""

    for i in range(len(g[c])-1,-1, -1):
        if g[c][i] == 0:
            g[c][i] = 1 if j else 2

            # retourne si le joueur a gagné ou non
            return check (g, j, i, c, mode)


# ---------------- fonctions principales pour faire tourner le jeu ---------------------

# Pour démarer une partie ou quitter le jeu
def jeu ():
    """ Gère le début et la fin du jeu"""
    # Permet le comtage des points
    point = [0, 0,0, 0,0, 0]

    recommencer = input("Voulez-vous jouer à puissance 4 ? oui, non : ")
    # permet de rejouer ou de ne pas jouer du tout
    while recommencer != "non":

        if recommencer == "oui":
            # initialise une grille pour le jeu
            g = init (7, 6)
            select (g, point)
        recommencer = input("Recommencer ? oui, non : ")

    # Affiche le nombre de victoire à condition qu'il y ait eu au moins une partie
    if point[-1] != 0:
        victoire (point)

        # Politesse de fin
        print ("Merci d'avoir jouer. ")
    print ("A une prochaine fois. ")


def victoire (point):
    """Affiche le nombre de victoire par joueur selon le mode de jeu, ainsi que le nombre de partie"""

    if point[1] != 0 or point[2] != 0:
        print ()
        print ("Le joueur 1 (X) a gagné", point[1], "fois. ")
        print ("Le joueur 2 (O) a gagné", point[2], "fois. ")

    if point[3] != 0 or point[4] != 0:
        print ()
        print ("Le bot a perdu", point[3], "fois. ")
        print ("Le bot a gagné", point[4], "fois. ")

    print ()
    print ("Le nombre de partie nule est de :", point[0])
    print ("Le nombre totale de partie est de :", point[-1])
    print ()


# Permet d'avoir plusieurs modes de jeu
def select (g, point):
    """ choix du mode de jeu """

    print ()
    mode = 0
    while mode != "alea" and mode != "2j":
        mode = input("Mode ? alea, 2j : ")
    print ()

    # permet de choisir qui commence la partie
    j = choix_debut (point, mode)

    if mode == "alea":
        point[main_alea(g, j)] += 1
    if mode == "2j":
        point[main_2j(g, j)] += 1

    # compte le nombre de partie
    point[-1] += 1


def choix_debut (point, mode):
    """ renvoie le joueur qui commence la partie """
    # booléen désignant les joueurs
    j = True

    choix = ""
    while choix != "oui" and choix != "non":
        choix = input ("Voulez-vous choisir le premier joueur ? oui, non : ")

    if choix == "non":
        # choix aléatoire
        a = randint (0,1)
        if a == 0:
            j = not j

        if mode == "2j":
            if j:
                print ("C'est le joueur 1 (X) qui commence. ")
            else :
                print ("C'est le joueur 2 (O) qui commence. ")

        else:
            if j:
                print ("Le bot joue en premier. ")
            else :
                print ("Le bot joue en deuxième. ")

    # choix du joueur qui commence en fonction du mode
    elif choix == "oui":
        print ()
        commencer = ""

        if mode == "2j":
            print ("Le joueur 1 (X) a gagné", point[1], "fois. ")
            print ("Le joueur 2 (O) a gagné", point[2], "fois. ")
            print ()

            while commencer != "1" and commencer != "2":
                commencer = input ("Qui commence? 1, 2 : ")

            if commencer == "2":
                j = not j

        elif mode == "alea":
            print ("Le bot a perdu", point[3], "fois. ")
            print ("Le bot a gagné", point[4], "fois. ")
            print ()

            while commencer != "oui" and commencer != "non":
                commencer = input (" Voulez-vous commencer ? oui, non : ")

            if commencer == "oui":
                j = not j

    return j


# main script contre un bot
def main_alea (g, j):
    """fait tourner le jeu contre un bot aléatoire"""

    while not fin(g):

        # permet de choisir si le bot commence ou non
        if j:
            if coup_aléatoire (g, j):
                print("Perdu")
                return 4

            if fin(g):
                return 0
            j = not j
        display(g)

        c = choix_colonne(g)
        if jouer(g, j, c, "alea"):
            return 3

        j =  not j
    return 0


# main script pour 2 joueurs
def main_2j (g, j):
    """fait tourner le jeu en local à 2 joueurs"""

    while not fin(g):
        display(g)
        c = choix_colonne(g)
        j =  not j

        if jouer(g, j, c, "2j"):
            return int(j)+1

    return 0



jeu()



"""
g = init(7,6)
assert coup_possible(g, len(g)) == False , "Erreur d'index trop grand"
assert coup_possible(g, -1) == False , "Erreur d'index trop petit"
assert fin([[1,1],[1,1]]) == True , "Erreur de fin"
assert fin([[1,0],[0,1]]) == False , "Erreur de fin"
"""



