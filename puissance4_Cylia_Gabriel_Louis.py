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



# Intermediate Functions

def display(g):
    """fonction d'affichage qui affiche dans le bon sens le tableau en plus de convertir les nb en symboles"""
    cg = init(7,6)
    for i in range(len(g)):
        for j in range(len(g[i])):
            cg[i][j] = "O" if g[i][j] == 1 else "X" if g[i][j] == 2  else 0
    for i in range(len(g[0])):
        for j in range(len(g)):
            print(cg[j][i], end=" | ")
        print()


def coup_possible(g, c):
    """détermine si la grille g a de la place sur la colonne c"""
    if len(g)-1 < c or g[c][0] != 0:
        return False
    return True



#verif
def vertical (g,j,l,c):
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
    point=0
    for i in range (7):
        if g[i][l]==1 and j:
            point+=1
        elif g[i][l]==2 and not j:
            point+=1
        else:
            point=0
        print(point, l,i)
        if point==4:
            return True

def diag (g, j, l, c):
    point=0
    for i in range (6):
        pass


def check(g,j,l,c):
    if vertical(g,j,l,c):
        print("Le joueur", int(j)+1, "a gagné par vertical !")
    if horiz(g,j,l,c):
        print("Le joueur", int(j)+1, "a gagné par horizontal !")
    if diag (g,j,l,c):
        print ("Le joueur", int(j)+1, "a gagné par diagonal !")


def coup_aléatoire (g, j):
    c = randint (0, len(g)-1)
    while not coup_possible (g, c):
        c = randint (0, len(g))
    jouer (g, j, c)



#Vérifie si complet
def fin (g):
    for i in range (len(g)):
        if coup_possible(g, i):
            return True
    return False


# main script
def main():
    """fait tourner le jeu"""
    a = randint (0,1)
    j = True
    if a == 0:
        j = not j
    while fin(g):
        if j:
            coup_aléatoire (g, j)
            j =  not j
            if not fin(g):
                break
        print("_____________________________")
        display(g)
        c = int(input("colonne?"))
        jouer(g, j, c)
        j =  not j
    print("_____________________________")
    display(g)
    print ("Le tableau est complet !")




def jouer(g,j,c):
    """joue le coup à partir du joueur, de la grille et de la colonne"""

    if coup_possible(g,c):
        for i in range(len(g[c])-1,-1, -1):
            if g[c][i] == 0:
                g[c][i] = 1 if j else 2
                check(g,j,i,c)
                break
    else:
        print("c'est complet")
        jouer(g,j, int(input("recommence")))


print(coup_possible(g, 0))

main()

