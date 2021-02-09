from random import randint


#initialise

def init(l, h):
    """ prends la longueur et hauteur du tableau
    et renvoie toujours un tableau à 2 dimensions rempli de 0"""
    #attention ne pas ecrire [ [0] * h] *l] car cela relie chaque colonne avec les autres
    g = [ [0] * h for i in range(l)]
    return g

# Soit g notre grille de jeu
g = init(7,6)



# Fonctions qui sont appelées en jeu

def display(g):
    """fonction d'affichage qui affiche dans le bon sens le tableau
        en plus de convertir les nombres en symboles:
        1 -> O, 2 -> X  et 0 -> " "  """
    # on crée une copie qui va être affichée
    cg = init(7,6)

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


def coup_possible(g, c):
    """détermine si l'on peut jouer dans la colonne:
        - si la colonne demandée existe dans g
        - si la colonne n'est pas totalement remplie """
    if  c < len(g) and c >= 0:
        if g[c][0] == 0:
            return True
    else:
        return False


#------------ Fonctions de vérification ------------------------

def vertical (g,j,l,c):
    """ vérifie la colonne où le coup est joué """
    point=0
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
    coord = [0,0] # 0 c, 1 ;l
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


def check(g,j,l,c):
    """ fonction qui exécute toutes les vérifications"""
    gagner = ""
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
        print ("Le joueur", int(j)+1, "a gagné par", gagner, "!")
        return True



def coup_aléatoire (g, j):
    """fonction qui joue un coup aléatoire pour le joueur entré en argument """
    c = randint (0, len(g)-1)
    while not coup_possible (g, c):
        c = randint (0, len(g))
    if jouer(g, j, c):
        return True


# fonctions principales pour faire tourner le jeu


def fin (g):
    """détermine si la grille est pleine"""
    for i in range (len(g)):
        if coup_possible(g, i):
            return False
    return True


def select():
    """permet de choisir le mode de jeu"""
    mode = 0
    while mode != "alea" and mode != "2j":
        mode = input("alea, 2j ")

    if mode == "alea":
        main_alea()
    if mode == "2j":
        main_2j()

    # En cas d'égalité
    if fin(g):
        display(g)
        print ("Le tableau est complet !")

"""
    recommencer = input("Recommencer? oui, non ")
    if recommencer == "non":
        print ("Merci d'avoir jouer")
    elif recommencer == "oui":
        g = init (7, 6)
        select()"""



# main script contre un bot
def main_alea():
    """fait tourner le jeu contre un bot aléatoire"""
    #choix arbitraire du joueur modifiable
    j = True
    # choix aléatoire du 1er joueur
    a = randint (0,1)
    if a == 0:
        j = not j

    while not fin(g):
        if j:
            if coup_aléatoire (g, j):
                print("Perdu")
                return False
            j =  not j
            if fin(g):
                return False
        display(g)

        c = int(input("colonne?"))
        if jouer(g, j, c):
            return True
        j =  not j
    return False

# main script pour 2 joueurs
def main_2j():
    """fait tourner le jeu en local à 2 joueurs"""
    #choix arbitraire du joueur modifiable
    j = True
    while not fin(g):
        display(g)
        c = int(input("colonne?"))
        j =  not j
        if jouer(g, j, c):
            return True



def jouer(g,j,c):
    """joue le coup à partir du joueur, de la grille et de la colonne"""

    if coup_possible(g,c):

        # si le coup est possible prendre la 1er case vide en partant du bas
        for i in range(len(g[c])-1,-1, -1):
            if g[c][i] == 0:
                g[c][i] = 1 if j else 2
                if check(g,j,i,c):
                    return True
                break
    else:
        # fait rejouer le joueur si celui-ci a demandé un coup impossible
        jouer(g,j, int(input("recommence")))




assert coup_possible(g, len(g)) == False , "Erreur d'index trop grand"
assert coup_possible(g, -1) == False , "Erreur d'index trop petit"
assert fin([[1,1],[1,1]]) == True , "Erreur de fin"
assert fin([[1,0],[0,1]]) == False , "Erreur de fin"

print(coup_possible(g, 0))

select()

