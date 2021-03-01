extends Node2D

# ------------- Fonctions qui gèrent la grille -------------------

# initialise la grille
func init(l, h):
	""" prends la longueur et hauteur du tableau
	et renvoie toujours un tableau à 2 dimensions rempli de 0"""
	#attention ne pas ecrire [ [0] * h] *l] car cela relie chaque colonne avec les autres
	var g = []
	for i in range(l):
		g.append([0,0,0,0,0,0])
	return g
var g
var j
var c
var count = 0
onready var instancedObject = preload("res://pawn.tscn")
func _ready():
	randomize()
	g = init (7, 6)
	j = true
	count = 0
signal change_player
func _process(delta):
	if Input.is_action_just_pressed("rclic"):
		if get_global_mouse_position().y < 150:
			if get_global_mouse_position().x > 220 and get_global_mouse_position().x < 290:
				c = 0
			if get_global_mouse_position().x > 320 and get_global_mouse_position().x < 380:
				c = 1
			if get_global_mouse_position().x > 410 and get_global_mouse_position().x < 470:
				c = 2
			if get_global_mouse_position().x > 500 and get_global_mouse_position().x < 580:
				c = 3
			if get_global_mouse_position().x > 590 and get_global_mouse_position().x < 670:
				c = 4
			if get_global_mouse_position().x > 680 and get_global_mouse_position().x < 760:
				c = 5
			if get_global_mouse_position().x > 770 and get_global_mouse_position().x < 850:
				c = 6
			if c != null and coup_possible(g,c):
				count +=1
				jouer(g, j, c, "2j")
				j = not j
				print(g)
				emit_signal("change_player", j)
	c = null

func display(g):
	"""fonction d'affichage qui affiche dans le bon sens le tableau
		en plus de convertir les nombres en symboles:
		1 -> O, 2 -> X  et 0 -> " "  """
	# on crée une copie qui va être affichée
	var cg = init(len(g), len(g[0]))

	# on remplit la copie à l'aide de g
	for i in range(len(g)):
		for j in range(len(g[i])):
			cg[i][j] = "O" if g[i][j] == 1 else "X" if g[i][j] == 2  else " "

	# on affiche
	print(" _______________")
	for i in range(len(g[0])):
		for j in range(len(g)):
			print()



#------------ Fonctions de vérification de fin de jeu ------------------------

func vertical (g, j, l, c):
	""" vérifie la colonne où le coup est joué """
	var point = 0
	for i in range (6):
		if g[c][i]== 1 and j:
			point+=1
		elif g[c][i]==2 and not j:
			point+=1
		else:
			point=0
		if point==4:
			return true


func horiz (g, j, l, c):
	""" vérifie la ligne où le coup est joué """
	var point=0
	for i in range (7):
		if g[i][l]==1 and j:
			point+=1
		elif g[i][l]==2 and not j:
			point+=1
		else:
			point=0
		if point==4:
			return true

func diagd (g, j, l, c):
	""" vérifie la diagonale haut gauche vers bas droite """
	var point=0
	var t = max(l,c) - min(l,c)
	var coord = [0,0] # 0 c, 1 l
	if l > c :
		coord [1] = t
	else:
		coord [0] = t
	while true:
		if g[coord [0]][coord [1]]==1 and j:
			point+=1
		elif g[coord [0]][coord [1]]==2 and not j:
			point+=1
		else:
			point=0
		if point==4:
			return true
		coord[0] += 1
		coord[1] += 1
		if coord[0] > 6 or coord[1] > 5:
			return false

func diagm (g, j, l, c):
	""" vérifie la diagonale bas gauche vers haut droit """
	var point=0
	var coord = [c,l]
	while coord[0] >= 0 and coord[1] < 5:
		coord[0] -= 1
		coord[1] += 1
	while true:
		if g[coord [0]][coord [1]]==1 and j:
			point+=1
		elif g[coord [0]][coord [1]]==2 and not j:
			point+=1
		else:
			point=0

		if point==4:
			return true
		coord[0] += 1
		coord[1] -= 1
		if coord[0] > 6 or coord[1]<0:
			return false

var vic
func check (g, j, l, c, mode):
	""" fonction qui exécute toutes les vérifications"""
	var gagner = "" # Variable qui permet d'afficher quelle vérification est vérifiée

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
		return true


func fin (g):
	"""détermine si la grille est pleine"""
	for i in range (len(g)):
		if coup_possible(g, i):
			return false
	display(g)
	print ("La grille est complète !")
	return true



# -------------- Fonctions qui gèrent le coup du joueur ou du bot -----------------

func coup_possible (g, c):
	"""détermine si l'on peut jouer dans la colonne:
		- si la colonne demandée existe dans g
		- si la colonne n'est pas totalement remplie """
	if  c < len(g) and c >= 0:
		if g[c][0] == 0:
			return true
	return false





func coup_aleatoire (g, j):
	"""fonction qui joue un coup aléatoire pour le joueur entré en argument """

	# donne une colonne au hasard
	var c = randi()%(len(g)-1)+1
	while not coup_possible (g, c):
		randomize() 
		c = randi()%(len(g)-1)+1

	# joue le coup du bot
	return jouer(g, j, c, "alea")


func vertical_ia (g, j, l, c, n):
	""" vérifie la colonne où le coup est joué """
	var point = 0
	for i in range (6):
		if g[c][i]== 1 and j:
			point+=1
		elif g[c][i]==2 and not j:
			point+=1
		else:
			point=0
		if point==n:
			return [true,i]
	return [false]
func horiz_ia (g, j, l, c, n):
	""" vérifie la ligne où le coup est joué """
	var point = 0
	for i in range (7):
		if g[i][l]==1 and j:
			point+=1
		elif g[i][l]==2 and not j:
			point+=1
		else:
			point=0
		if point==n:
			return [true,i]
	return [false]

func diagd_ia (g, j, l, c, n):
	""" vérifie la diagonale haut gauche vers bas droite """
	var point=0
	var t = max(l,c) - min(l,c)
	var coord = [0,0] # 0 c, 1 l
	if l > c :
		coord [1] = t
	else:
		coord [0] = t
	while true:
		if g[coord [0]][coord [1]]==1 and j:
			point+=1
		elif g[coord [0]][coord [1]]==2 and not j:
			point+=1
		else:
			point=0
		if point==n:
			print(coord)
			return [true,coord]
		coord[0] += 1
		coord[1] += 1
		if coord[0] > 6 or coord[1] > 5:
			return [false]

func diagm_ia (g, j, l, c, n):
	""" vérifie la diagonale bas gauche vers haut droit """
	var point=0
	var coord = [c,l]
	while coord[0] >= 0 and coord[1] < 5:
		coord[0] -= 1
		coord[1] += 1
	while true:
		if g[coord [0]][coord [1]]==1 and j:
			point+=1
		elif g[coord [0]][coord [1]]==2 and not j:
			point+=1
		else:
			point=0

		if point==n:
			return [true,coord]
		coord[0] += 1
		coord[1] -= 1
		if coord[0] > 6 or coord[1]<0:
			return [false]

func anticipation(g, c, y, liste):
	if coup_possible(g,c):
		for i in range(len(g[c])-1, -1, -1):
			if i == y and g[c][y] == 0:
				print(i, c, g[c][y])
				return true
			if i == y and g[c][y] != 0:
				return false
			if g[c][i] == 0:
				liste[c] = 0
				return false
				
	return false


var liste =  [0,1,2,3,2,1,0]
func ia(g, j):
	
	"""fonction qui joue un coup aléatoire pour le joueur entré en argument """
	for n in [3,2]:
		for p in [true, false]:
			# vérifie si y a une verti gagnante
			for c in range(0, len(g)):
				var rep = vertical_ia(g, p, 0, c,  n)
				if rep[0]:
					print(rep, p)
					var ant = anticipation(g, c, rep[1]-3, liste)
					if ant:
						return jouer(g, j, c, "alea")
			
			# Vérifie si y a une horizontale gagnante:
			for l in range(0, len(g[0])):
				var rep = horiz_ia(g,p,l,0, n)
				if rep[0]:
					if coup_possible(g,rep[1]+1):
						var c = rep[1]+1
						var ant = anticipation(g, c, l, liste)
						if ant:
							return jouer(g, j, c, "alea")

							
					if coup_possible(g,rep[1]-3) :
						var c = rep[1]-3
						if anticipation(g, c, l, liste):
							return jouer(g, j, c, "alea")
			# diago descendante
			for c in range(0,len(g)):
				var rep = diagd_ia (g, p, 0, c, n)
				if rep[0]:
					print("diagd")
					if coup_possible(g, rep[1][0]+1):
						c = rep[1][0]+1
						var ant = anticipation(g, c, rep[1][1]+1, liste)
						if ant:
							return jouer(g, j, c, "alea")
					if coup_possible(g, rep[1][0]-3):
						c = rep[1][0]-3
						var ant = anticipation(g, c, rep[1][1]-3, liste)
						if ant:
							return jouer(g, j, c, "alea")
			for l in range(0,len(g[0])):
				var rep = diagd_ia (g, p, l, 0, n)
				if rep[0]:
					print("diagd")
					if coup_possible(g, rep[1][0]+1):
						var c = rep[1][0]+1
						var ant = anticipation(g, c, rep[1][1]+1, liste)
						if ant:
							return jouer(g, j, c, "alea")
					if coup_possible(g, rep[1][0]-3):
						var c = rep[1][0]-3
						var ant = anticipation(g, c, rep[1][1]-3, liste)
						if ant:
							return jouer(g, j, c, "alea")



			#Vérifie si y a une diagm
			for c in range(0,len(g)):
				var rep = diagm_ia (g, p, len(g[c])-1, c, n)
				if rep[0]:
					print("diagd")
					if coup_possible(g, rep[1][0]+1):
						c = rep[1][0]+1
						var ant = anticipation(g, c, rep[1][1]-1, liste)
						if ant:

							return jouer(g, j, c, "alea")
					if coup_possible(g, rep[1][0]-3):
						c = rep[1][0]-3
						var ant = anticipation(g, c, rep[1][1]+3, liste)
						if ant:
							return jouer(g, j, c, "alea")

			for l in range(0,len(g[0])):
				var rep = diagm_ia (g, p, l, 0, n)
				if rep[0]:
					print("diagd")
					if coup_possible(g, rep[1][0]+1):
						var c = rep[1][0]+1
						var ant = anticipation(g, c, rep[1][1]-1, liste)
						if ant:
							return jouer(g, j, c, "alea")
					if coup_possible(g, rep[1][0]-3):
						var c = rep[1][0]-3
						var ant = anticipation(g, c, rep[1][1]-3, liste)
						if ant:
							return jouer(g, j, c, "alea")



	var c = randi()%(len(g)-1)+1
	while not coup_possible (g, c):
		randomize() 
		c = randi()%(len(g)-1)+1
	# joue le coup du bot
	return jouer(g, j, c, "alea")


func jouer (g,j,c, mode):
	"""joue le coup à partir du joueur, de la grille et de la colonne"""

	for i in range(len(g[c])-1,-1, -1):
		if g[c][i] == 0:
			g[c][i] = 1 if j else 2
			var pawn = instancedObject.instance()
			add_child(pawn)
			pawn.start(count, c, i)
			# retourne si le joueur a gagné ou non
			return check (g, j, i, c, mode)


# ---------------- fonctions principales pour faire tourner le jeu ---------------------

# Pour démarer une partie ou quitter le jeu



func victoire (point):
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








# main script pour 2 joueurs
func main_2j (g, j):
	"""fait tourner le jeu en local à 2 joueurs"""

	while not fin(g):
		display(g)
		j =  not j

		if jouer(g, j, c, "2j"):
			return int(j)+1

	return 0




func main_ia (g, j):
	"""fait tourner le jeu contre un bot intelligent"""

	while not fin(g):

		# permet de choisir si le bot commence ou non
		if j:
			if ia(g, j):
				print("Perdu")
				return 4

			if fin(g):
				return 0
			j = not j
		display(g)

		if jouer(g, j, c, "ia"):
			return 3

		j =  not j
	return 0





"""
g = init(7,6)
assert coup_possible(g, len(g)) == false , "Erreur d'index trop grand"
assert coup_possible(g, -1) == false , "Erreur d'index trop petit"
assert fin([[1,1],[1,1]]) == true , "Erreur de fin"
assert fin([[1,0],[0,1]]) == false , "Erreur de fin"
"""



