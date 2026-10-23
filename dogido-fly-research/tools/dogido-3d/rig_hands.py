"""v03: independently editable flapping-hand bones on the existing continuous skin."""
from pathlib import Path
import math
import bpy
from mathutils import Vector, Quaternion

OUT = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(OUT / 'dogido-round-v02.blend'))
day = bpy.data.scenes['Day - 昼の質感']
root = bpy.data.objects['Dogido - 全体移動']
body = bpy.data.objects['Body - 丸い本体']
asset = body.users_collection[0]
rest = [tuple(v.co) for v in body.data.vertices]
face = bpy.data.objects['Face - 原画の目・眉・頬・口']
face_uv = [tuple(uv.uv) for uv in face.data.uv_layers.active.data]

armature = bpy.data.armatures.new('Dogido - 手のパタパタ骨格')
rig = bpy.data.objects.new('Rig - 左右の手を動かす', armature)
asset.objects.link(rig)
rig.parent = root
rig.show_in_front = True
armature.display_type = 'STICK'
rig['instructions'] = 'Pose Mode: Hand.L / Hand.R. 32-frame flap cycle; separate from floating root.'
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')
anchor = armature.edit_bones.new('Body')
anchor.head, anchor.tail = (0, 0, .46), (0, 0, 2.49)
for sign, label in [(-1, 'L'), (1, 'R')]:
    bone = armature.edit_bones.new('Hand.' + label)
    bone.head = (sign * .77, -.15, 1.15)
    bone.tail = (sign * 1.03, -.16, .91)
    bone.parent = anchor
bpy.ops.object.mode_set(mode='OBJECT')

groups = {name: body.vertex_groups.new(name=name) for name in ('Body', 'Hand.L', 'Hand.R')}
def smooth(value):
    t = max(0., min(1., value))
    return t*t*(3-2*t)

fixed_indices, moving_indices = [], []
for v in body.data.vertices:
    p = body.matrix_world @ v.co
    weight = smooth((abs(p.x) - .78) / .27) * smooth((1.42 - p.z) / .28)
    groups['Body'].add([v.index], 1-weight, 'REPLACE')
    if weight > 0:
        groups['Hand.L' if p.x < 0 else 'Hand.R'].add([v.index], weight, 'REPLACE')
    if abs(p.x) < .7:
        fixed_indices.append(v.index)
    if weight > .95:
        moving_indices.append(v.index)
modifier = body.modifiers.new('Hands - 付け根を支点にパタパタ', 'ARMATURE')
modifier.object = rig
modifier.use_deform_preserve_volume = True
for sign, label in [(-1, 'L'), (1, 'R')]:
    pose = rig.pose.bones['Hand.' + label]
    pose.rotation_mode = 'QUATERNION'
    local_axis = pose.bone.matrix_local.to_3x3().inverted() @ Vector((0, 1, 0))
    for frame in range(1, 98, 8):
        angle = math.radians(23) * math.sin((frame-1)/32 * 2*math.pi) * -sign
        pose.rotation_quaternion = Quaternion(local_axis, angle)
        pose.keyframe_insert(data_path='rotation_quaternion', frame=frame, group='Hand.' + label)

assert [tuple(v.co) for v in body.data.vertices] == rest
assert [tuple(uv.uv) for uv in face.data.uv_layers.active.data] == face_uv
assert face.modifiers.get(modifier.name) is None
assert len(moving_indices) > 50

def evaluated_positions(frame):
    day.frame_set(frame)
    bpy.context.view_layer.update()
    obj = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return [v.co.copy() for v in obj.data.vertices]

up, down = evaluated_positions(9), evaluated_positions(25)
center_delta = max((up[i]-down[i]).length for i in fixed_indices)
hand_delta = max((up[i]-down[i]).length for i in moving_indices)
assert center_delta < 1e-5, center_delta
assert hand_delta > .10, hand_delta
day.frame_set(1)
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'dogido-round-v03.blend'))

# Front-facing proof frames and a short local video: no game runtime changes.
camera = day.camera
camera.location = (0, -7, 1.46)
camera.rotation_euler = (Vector((0, 0, 1.46))-camera.location).to_track_quat('-Z', 'Y').to_euler()
for frame, name in ((9, 'hands-up-v03.png'), (25, 'hands-down-v03.png')):
    day.frame_set(frame)
    day.render.filepath = str(OUT / name)
    bpy.ops.render.render(write_still=True, scene=day.name)
frames = OUT / 'flap-frames-v03'
frames.mkdir(exist_ok=True)
day.render.resolution_x = day.render.resolution_y = 640
day.eevee.taa_render_samples = 48
for n, frame in enumerate(range(1, 97, 2)):
    day.frame_set(frame)
    day.render.filepath = str(frames / f'{n:03}.png')
    bpy.ops.render.render(write_still=True, scene=day.name)
print(f'VERIFIED_HAND_RIG: immutable rest geometry and face UV; center delta={center_delta:.8f}, hand delta={hand_delta:.4f}; two independent hand bones; 48 preview frames; v02 preserved. NOT IN GAME.')
