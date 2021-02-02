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
            cg[i][j] = "O" if g[i][j] == 1 else "X" if g[i][j] == 2  else " "
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
        if point==4:
            return True

def diagd (g, j, l, c):
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
    if vertical(g,j,l,c):
        print("Le joueur", int(j)+1, "a gagné par vertical !")
    if horiz(g,j,l,c):
        print("Le joueur", int(j)+1, "a gagné par horizontal !")
    if diagd(g,j,l,c):
        print ("Le joueur", int(j)+1, "a gagné par diagonal Descendante!")
    if diagm(g,j,l,c):
        print ("Le joueur", int(j)+1, "a gagné par diagonal Montante!")
    if diagm(g,j,l,c) or  diagd(g,j,l,c) or vertical(g,j,l,c) or horiz(g,j,l,c):
        return True



def coup_aléatoire (g, j):
    c = randint (0, len(g)-1)
    while not coup_possible (g, c):
        c = randint (0, len(g))
    if jouer(g, j, c):
        return True



#Vérifie si complet
def fin (g):
    for i in range (len(g)):
        if coup_possible(g, i):
            return True
    return False


def select():
    mode = input("alea, 2j")
    return mode

# main script
def main():
    j = True
    if select() == "alea":
        """fait tourner le jeu contre un bot aléatoire"""
        a = randint (0,1)
        if a == 0:
            j = not j
        while fin(g):
            if j:
                if coup_aléatoire (g, j):
                    print("Perdu")
                    return True
                j =  not j
                if not fin(g):
                    break
            print("_____________________________")
            display(g)
            c = int(input("colonne?"))
            if jouer(g, j, c):
                return True
            j =  not j
    if select() == "2j":
        """fait tourner le jeu en local à 2 joueurs"""
        while fin(g):
            print("_____________________________")
            display(g)
            c = int(input("colonne?"))
            j =  not j
            if jouer(g, j, c):
                return True
    print("_____________________________")
    display(g)
    print ("Le tableau est complet !")



def jouer(g,j,c):
    """joue le coup à partir du joueur, de la grille et de la colonne"""

    if coup_possible(g,c):
        for i in range(len(g[c])-1,-1, -1):
            if g[c][i] == 0:
                g[c][i] = 1 if j else 2
                if check(g,j,i,c):
                    return True
                break
    else:
        jouer(g,j, int(input("recommence")))


print(coup_possible(g, 0))

main()

