import bpy
import random
import math


class Planet:
    def __init__(self, size, speed):
        self.size = size
        self.speed = speed


possibilities = [111, 000, 2]
planet_list = [Planet(0, 0)]
circle_radius = 50


def create_emission_shader(color, strength, mat_name):
    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    node_emission = nodes.new(type="ShaderNodeEmission")
    node_emission.inputs[0].default_value = color
    node_emission.inputs[1].default_value = strength
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    links = mat.node_tree.links
    link = links.new(node_emission.outputs[0], node_output.inputs[0])
    return mat


def generate_planet_list(shots):
    temp_planet = Planet(0, 0)
    for i in range(shots):
        cur_val = random.choices(possibilities, weights=[462, 504, 34])
        if (cur_val == [111]):
            temp_planet.size += 0.4
        elif (cur_val == [000]):
            temp_planet.speed += 15
        elif (cur_val == [2]):
            if (temp_planet.speed != 0 and temp_planet.size != 0):
                planet_list.append(temp_planet)
            temp_planet = Planet(0, 0)


def generate_ring(radius, index):
    obj = bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        major_radius=radius,
        minor_radius=0.1,
        major_segments=100
    )
    bpy.ops.object.shade_smooth()
    bpy.context.object.name = "ring" + str(index)


def generate_sun():
    sun_check = bpy.context.scene.objects.get("sun")
    if sun_check is None:
        bpy.ops.curve.primitive_bezier_circle_add(
            location=(0, 0, 0), radius=0.01)
        bpy.context.object.name = "sun rotation"
        bpy.context.object.data.path_duration = 500
        obj = bpy.ops.mesh.primitive_ico_sphere_add(
            location=(0, 0, 0),
            subdivisions=5,
            radius=40)
        bpy.ops.object.shade_smooth()
        bpy.context.object.name = "sun"
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        bpy.context.object.constraints["Follow Path"].target = bpy.data.objects["sun rotation"]
        bpy.context.object.constraints["Follow Path"].use_curve_follow = True
        bpy.ops.constraint.followpath_path_animate(
            constraint="Follow Path", owner='OBJECT')


def generate_planet(cur_circle_radius, index):
    angle = 2 * math.pi * random.random()
    x = cur_circle_radius * math.cos(angle)
    y = cur_circle_radius * math.sin(angle)

    bpy.ops.curve.primitive_bezier_circle_add(location=(0, 0, 0))
    bpy.context.object.name = "path" + str(index)
    bpy.context.object.data.path_duration = planet_list[index].speed

    obj = bpy.ops.mesh.primitive_ico_sphere_add(
        location=(x, y, 0),
        subdivisions=5,
        radius=planet_list[index].size)
    bpy.context.object.name = "planet" + str(index)
    bpy.ops.object.shade_smooth()

    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    bpy.context.object.constraints["Follow Path"].target = bpy.data.objects["path" + str(
        index)]
    bpy.context.object.constraints["Follow Path"].use_curve_follow = True
    bpy.ops.constraint.followpath_path_animate(
        constraint="Follow Path",
        owner='OBJECT')

    return obj


generate_planet_list(200)
generate_sun()

sun_obj = bpy.context.scene.objects.get("sun")
sun_obj.data.materials.append(
    create_emission_shader(
        (1, 0.35, 0.13, 0.5), 10, "SunMat"
    )
)

for i in range(len(planet_list)):
    generate_planet(circle_radius + i * 10, i)
    generate_ring(circle_radius + i * 10, i)
    temp_planet = bpy.context.scene.objects.get("planet" + str(i))
    temp_line = bpy.context.scene.objects.get("ring" + str(i))

    temp_planet.data.materials.append(
        create_emission_shader(
            (random.uniform(0, 1),
             random.uniform(0, 1),
             random.uniform(0, 1), 1), 3, "PlanetMat"
        )
    )
    temp_line.data.materials.append(
        create_emission_shader(
            (0.5, 0.5, 0.5, 0.5), 0.3, "RingMat"
        )
    )
