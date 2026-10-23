"""Blender-only, non-destructive round-body/material study; no game deployment.

Run Blender --background --factory-startup --python tools/dogido-3d/build.py.
Original face artwork is packed unmodified and projected by a shader, not redrawn.
"""
from pathlib import Path
import math
import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent
SOURCE = OUT / 'assets/character.png'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.name = 'Day - 昼の質感'
asset = bpy.data.collections.new('Dogido - 編集用モデル')
scene.collection.children.link(asset)
stage = bpy.data.collections.new('Preview - カメラと照明')
scene.collection.children.link(stage)

def collect(obj, collection):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    collection.objects.link(obj)
    return obj

root = bpy.data.objects.new('Dogido - 全体移動', None)
asset.objects.link(root)
root['body_opacity'] = 0.86
root['soft_glow'] = 0.38
root['prototype_only'] = 'Round body + original face; not a Fabric-ready model.'
root.id_properties_ui('body_opacity').update(min=0.0, max=1.0, description='体の不透明度')
root.id_properties_ui('soft_glow').update(min=0.0, max=2.0, description='暗所で見える自己発光')

def linear(c):
    return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4

def color(hexcode):
    return tuple(linear(int(hexcode[i:i+2], 16) / 255) for i in (0, 2, 4)) + (1,)

def material(name, rgb, rough=.65):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = color(rgb)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Specular IOR Level'].default_value = .18
    m.diffuse_color = color(rgb)
    return m, p

def driver(socket, prop):
    d = socket.driver_add('default_value').driver
    d.expression = 'value'
    v = d.variables.new()
    v.name = 'value'
    v.targets[0].id = root
    v.targets[0].data_path = f'["{prop}"]'

body_mat, body_shader = material('Body - わずかに透ける淡いクリーム', 'FFF5C6', .76)
body_mat.surface_render_method = 'DITHERED'
body_shader.inputs['Emission Color'].default_value = color('FFF0B4')
# Only the front-facing shell contributes opacity; two shells must not stack
# into near-opaque plastic. No glass refraction / sparkling jelly appearance.
nodes, links = body_mat.node_tree.nodes, body_mat.node_tree.links
geometry = nodes.new('ShaderNodeNewGeometry')
fresnel = nodes.new('ShaderNodeFresnel')
fresnel.inputs['IOR'].default_value = 1.3
rim = nodes.new('ShaderNodeMath')
rim.operation = 'MULTIPLY'
rim.inputs[1].default_value = .45
links.new(fresnel.outputs[0], rim.inputs[0])
glow = nodes.new('ShaderNodeMath')
glow.operation = 'ADD'
driver(glow.inputs[0], 'soft_glow')
links.new(rim.outputs[0], glow.inputs[1])
links.new(glow.outputs[0], body_shader.inputs['Emission Strength'])
transparent = nodes.new('ShaderNodeBsdfTransparent')
mix_alpha = nodes.new('ShaderNodeMixShader')
driver(mix_alpha.inputs[0], 'body_opacity')
links.new(transparent.outputs[0], mix_alpha.inputs[1])
links.new(body_shader.outputs[0], mix_alpha.inputs[2])
mix_back = nodes.new('ShaderNodeMixShader')
links.new(geometry.outputs['Backfacing'], mix_back.inputs[0])
links.new(mix_alpha.outputs[0], mix_back.inputs[1])
links.new(transparent.outputs[0], mix_back.inputs[2])
links.new(mix_back.outputs[0], nodes.get('Material Output').inputs['Surface'])

def sphere(name, loc, scale, mat, collection=asset):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=40, location=loc)
    o = collect(bpy.context.object, collection)
    o.name, o.scale = name, scale
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    if collection == asset:
        o.parent = root
    return o

body = sphere('Body - 丸い本体', (0, 0, 1.46), (1.0, .94, 1.03), body_mat)
arms = []
for sign, label in [(-1, 'L'), (1, 'R')]:
    arm = sphere('Hand_' + label + ' - 小さな手', (sign * .91, -.16, 1.08), (.17, .26, .32), body_mat)
    arm.rotation_euler[1] = sign * -.44
    arms.append(arm)
# A continuous skin avoids translucent double surfaces at hand/body junctions.
# Keep construction hands hidden for later reshaping, without duplicate renders.
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
for arm in arms:
    union = body.modifiers.new('Hand blend', 'BOOLEAN')
    union.operation, union.object = 'UNION', arm
    bpy.ops.object.modifier_apply(modifier=union.name)
    arm.hide_render = True
    arm.hide_set(True)
body.data.remesh_voxel_size = .025
bpy.ops.object.voxel_remesh()
smooth = body.modifiers.new('Soft rounded surface', 'SMOOTH')
smooth.factor, smooth.iterations = 1.1, 5
bpy.ops.object.modifier_apply(modifier=smooth.name)
for poly in body.data.polygons:
    poly.use_smooth = True

# Curved decal follows the sphere. Face-only bounds in the original full sprite;
# brown/peach/white ink is selected in the material, original PNG remains intact.
verts, uvs, faces = [], [], []
NX, NZ = 64, 44
for j in range(NZ + 1):
    v = j / NZ
    z = -.34 + v * .985
    for i in range(NX + 1):
        u = i / NX
        x = (u - .5) * 1.48
        y = -.94 * math.sqrt(max(.01, 1 - x*x - (z / 1.03)**2)) - .008
        verts.append((x, y, 1.46 + z))
        uvs.append(((430 + u * 910) / 1398, 1 - (825 - v * 605) / 1336))
for j in range(NZ):
    for i in range(NX):
        a = j*(NX+1)+i
        faces.append((a, a+1, a+NX+2, a+NX+1))
mesh = bpy.data.meshes.new('Face - 球面に沿う原画投影')
mesh.from_pydata(verts, [], faces)
mesh.update()
uv = mesh.uv_layers.new(name='Authored_face_crop')
for poly in mesh.polygons:
    poly.use_smooth = True
    for loop in poly.loop_indices:
        uv.data[loop].uv = uvs[mesh.loops[loop].vertex_index]
face = bpy.data.objects.new('Face - 原画の目・眉・頬・口', mesh)
asset.objects.link(face)
face.parent = root
face_mat, p = material('Face - 原画をそのまま使う', 'FFFFFF', .9)
face_mat.surface_render_method = 'DITHERED'
face_mat.use_backface_culling = True
nodes, links = face_mat.node_tree.nodes, face_mat.node_tree.links
image = bpy.data.images.load(str(SOURCE), check_existing=True)
image.pack()
tex = nodes.new('ShaderNodeTexImage')
tex.image = image
tex.extension = 'CLIP'
links.new(tex.outputs['Color'], p.inputs['Base Color'])
links.new(tex.outputs['Color'], p.inputs['Emission Color'])
p.inputs['Emission Strength'].default_value = .2
separate = nodes.new('ShaderNodeSeparateColor')
links.new(tex.outputs['Color'], separate.inputs['Color'])

def mathnode(operation, a, b):
    n = nodes.new('ShaderNodeMath')
    n.operation = operation
    for index, value in enumerate((a, b)):
        if isinstance(value, (float, int)):
            n.inputs[index].default_value = value
        else:
            links.new(value, n.inputs[index])
    return n.outputs[0]

warm_ink = mathnode('GREATER_THAN', separate.outputs['Red'], mathnode('MULTIPLY', separate.outputs['Green'], 1.25))
white_ink = mathnode('GREATER_THAN', separate.outputs['Blue'], .88)
mask = mathnode('MULTIPLY', mathnode('MAXIMUM', warm_ink, white_ink), tex.outputs['Alpha'])
trans = nodes.new('ShaderNodeBsdfTransparent')
mix = nodes.new('ShaderNodeMixShader')
links.new(mask, mix.inputs[0])
links.new(trans.outputs[0], mix.inputs[1])
links.new(p.outputs[0], mix.inputs[2])
links.new(mix.outputs[0], nodes.get('Material Output').inputs['Surface'])
mesh.materials.append(face_mat)

# Gentle editable float loop. No autonomous behavior / Minecraft world changes.
scene.frame_start, scene.frame_end = 1, 96
scene.render.fps = 24
for frame, z in [(1, 0), (25, .075), (49, 0), (73, -.035), (97, 0)]:
    root.location.z = z
    root.keyframe_insert(data_path='location', frame=frame)
scene.frame_set(1)

floor_mat, _ = material('Preview - 青灰色の床', '596878')
wall_mat, _ = material('Preview - 背景', '839099')
stripe_mat, _ = material('Preview - 透け具合の目安', '647681')

def cube(name, loc, scale, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = collect(bpy.context.object, stage)
    o.name, o.scale = name, scale
    o.data.materials.append(mat)
    return o

cube('Preview floor', (0, 0, -.12), (200, 200, .2), floor_mat)
cube('Preview backdrop', (0, 2.4, 2.7), (16, .1, 5.6), wall_mat)
for z in [.65, 1.15, 1.65, 2.15, 2.65]:
    cube('Backdrop band - 透過確認', (0, 2.33, z), (16, .025, .025), stripe_mat)

def light(name, loc, energy, size, tint):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy, data.shape, data.size = energy, 'DISK', size
    data.color = tint
    obj = bpy.data.objects.new(name, data)
    stage.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (Vector((0, 0, 1.4)) - obj.location).to_track_quat('-Z', 'Y').to_euler()
    return obj

key = light('Key - 昼', (-3, -4, 6), 450, 5, (1, .92, .8))
fill = light('Fill - 昼', (4, -1, 3), 140, 4, (.76, .85, 1))
bpy.ops.object.camera_add(location=(3.1, -7.2, 3.1))
camera = collect(bpy.context.object, stage)
camera.name = 'Camera - 少し横から'
camera.rotation_euler = (Vector((0, 0, 1.37)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.type, camera.data.ortho_scale = 'ORTHO', 3.85
scene.camera = camera
scene.world = bpy.data.worlds.new('World - 昼')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.25, .3, .4, 1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = .45
scene.render.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 128
scene.render.resolution_x, scene.render.resolution_y = 1000, 1000
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'AgX'
scene.render.film_transparent = False

# Linked geometry for two lighting conditions; neither modifies the original PNG.
night = scene.copy()
night.name = 'Night - 暗所の淡い発光'
night.world = scene.world.copy()
night.world.name = 'World - 夜'
night.world.node_tree.nodes['Background'].inputs[0].default_value = (.025, .04, .08, 1)
night.world.node_tree.nodes['Background'].inputs[1].default_value = .12
# Separate preview collections/lights so edits in one scene do not affect the other.
night.collection.children.unlink(stage)
night_stage = bpy.data.collections.new('Preview - 夜の照明')
night.collection.children.link(night_stage)
for obj in stage.objects:
    copy = obj.copy()
    if obj.type == 'LIGHT':
        copy.data = obj.data.copy()
        copy.data.energy *= .045
        copy.data.color = (.5, .65, 1)
    night_stage.objects.link(copy)
    if obj == camera:
        night.camera = copy

# Very restrained halo for the dark-condition preview; the body remains legible.
compositor = bpy.data.node_groups.new('Night - 淡いにじみ', 'CompositorNodeTree')
compositor.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
rl = compositor.nodes.new('CompositorNodeRLayers')
rl.scene = night
halo = compositor.nodes.new('CompositorNodeGlare')
halo.inputs['Type'].default_value = 'Fog Glow'
halo.inputs['Threshold'].default_value = .35
halo.inputs['Strength'].default_value = .2
halo.inputs['Size'].default_value = .15
output = compositor.nodes.new('NodeGroupOutput')
compositor.links.new(rl.outputs['Image'], halo.inputs['Image'])
compositor.links.new(halo.outputs['Image'], output.inputs['Image'])
night.compositing_node_group = compositor

for sc in (scene, night):
    sc.unit_settings.system = 'METRIC'
    sc['NOTE'] = 'Appearance study only. Transparency/emission shaders must be implemented separately in Fabric.'

# Select just the editable body on opening; render-stage assets remain separate.
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_distance = 5
            area.spaces.active.region_3d.view_location = (0, 0, 1.45)
            area.spaces.active.shading.type = 'MATERIAL'

assert len(asset.objects) == 5
assert image.size[:] == (1398, 1336)
assert .8 < root['body_opacity'] < 1
assert 0 < root['soft_glow'] < .5
assert body.dimensions.y > 1.8
blend = OUT / 'dogido-round-v01.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
for sc, filename in ((scene, 'day.png'), (night, 'night.png')):
    sc.render.filepath = str(OUT / filename)
    bpy.ops.render.render(write_still=True, scene=sc.name)
# Side view is important evidence that this is a round 3D body, not a billboard.
saved_loc, saved_rotation = camera.location.copy(), camera.rotation_euler.copy()
camera.location = (7, -1, 2.4)
camera.rotation_euler = (Vector((0, 0, 1.37)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
scene.render.filepath = str(OUT / 'side.png')
bpy.ops.render.render(write_still=True, scene=scene.name)
camera.location, camera.rotation_euler = saved_loc, saved_rotation
assert all((OUT / name).stat().st_size > 1000 for name in ('dogido-round-v01.blend', 'day.png', 'night.png', 'side.png'))
print('VERIFIED_OUTPUTS: editable round body, packed original face, opacity 0.86, base emission 0.38 + soft rim, day/night/side previews. NOT IN GAME.')
