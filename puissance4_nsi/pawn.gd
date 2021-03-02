extends Sprite


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var p = Vector2(0,0)

# Called when the node enters the scene tree for the first time.
func _ready():
	anim()
func anim():
	pass



# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func start(count, c, i ):
	self.position = Vector2(-500, -500)
	if count % 2 == 1:
		self.texture = load("res://pionjaune.png")
	else:
		self.texture = load("res://pionrouge.png")
	var tween = get_node("Tween")
	tween.interpolate_property(self, "position",
		get_parent().get_node("Player").position, Vector2(265 + 87.5 * c, 120 + 87.5*i), 1,
		Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)
	tween.start()

