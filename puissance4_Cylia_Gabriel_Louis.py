

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

#Vérifie si colonne libre
def coup_possible(g, c):
    """détermine si la grille g a de la place sur la colonne c"""
    if g[c][0] == 0:
        return True
    else:
        return False

#Vérifie si complet
def fin (g):
    for i in range (len(g)):
        if coup_possible(g, i):
            return True
    return False

# main script
def main():
    """fait tourner le jeu"""
    j = True
    while fin(g):
        display(g)
        c = int(input("colonne?"))
        j =  not j
        jouer(g, j, c)
    display(g)
    print ("Le tableau est complet !")

#coup du joueur
def jouer(g,j,c):
    """joue le coup à partir du joueur, de la grille et de la colonne"""
    if coup_possible(g,c):
        for i in range(len(g[c])-1,-1, -1):
            if g[c][i] == 0:
                g[c][i] = 1 if j else 2
                break
    else:
        print("c'est complet")
        jouer(g,j, int(input("recommence")))


print(coup_possible(g, 0))

main()


