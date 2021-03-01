extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	self.scale = Vector2(0.35,0.35)

func _process(delta):
	self.position = get_global_mouse_position()
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass

func _on_Node2D_change_player(j):
	if j:
		self.texture = load("res://pionjaune.png")
	else:
		self.texture = load("res://pionrouge.png")


