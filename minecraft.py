from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.fps_counter.enabled = False
window.exit_button.visible = False

punch = Audio('assets/punching', autoplay=False)

blocks = [
    load_texture('assets/blocks/Erde.png'),
    load_texture('assets/blocks/Erde.png'),
    load_texture('assets/blocks/Blatt.png'),
    load_texture('assets/blocks/Eisenerz.png'),
    load_texture('assets/blocks/Golderz.png'),
    load_texture('assets/blocks/Steinkohle.png'),
]

block_id = 1


def input(key):
    global block_id, hand

    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks)-1
        hand.texture = blocks[block_id]


sky = Entity(
    parent=scene,
    model='sphere',
    texture=load_texture('assets/sky'),
    scale=500,
    double_sided=True
)

hand = Entity(
    parent=camera.ui,
    model='cube',
    texture=blocks[block_id],
    scale=0.4,
    position=Vec2(0.6, -0.6),
    rotation=Vec3(-10, -10, 10),
)


def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='assets/blocks/Blatt.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.1)),
            scale=1.0
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                Voxel(position=self.position + mouse.normal,
                      texture=blocks[block_id])
            elif key == 'right mouse down':
                destroy(self)


map_size = 20
for z in range(map_size):
    for x in range(map_size):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()

app.run()
