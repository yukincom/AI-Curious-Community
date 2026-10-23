"""v02: right-side-based face alignment only; keep v01 intact.

Uses the author's viewer-right face half for both sides of the 3D surface.
Only face UV coordinates change; no original PNG or body geometry is edited.
"""
from pathlib import Path
import hashlib
import struct
import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(OUT / 'dogido-round-v01.blend'))
face = bpy.data.objects['Face - 原画の目・眉・頬・口']

def geometry_digest():
    digest = hashlib.sha256()
    for obj in sorted(bpy.data.objects, key=lambda item: item.name):
        if obj.type != 'MESH':
            continue
        digest.update(obj.name.encode())
        for vertex in obj.data.vertices:
            digest.update(struct.pack('fff', *vertex.co))
        for row in obj.matrix_world:
            digest.update(struct.pack('ffff', *row))
    return digest.hexdigest()

before = geometry_digest()
image = next(image for image in bpy.data.images if image.packed_file)
image_digest = hashlib.sha256(image.packed_file.data).hexdigest()
uv = face.data.uv_layers.active
for loop in face.data.loops:
    x = face.data.vertices[loop.vertex_index].co.x
    # Original face was oblique. Its center is near source x=940; center this
    # on the round body. Keep the existing viewer-right feature scale/height.
    uv.data[loop.index].uv.x = (940.0 + abs(x) / 1.48 * 910.0) / 1398.0
uv.name = 'Face_v02 - 原画の右半顔を基準に中央合わせ'
face['face_adjustment'] = 'Viewer-right source half; x=940 centered; original right-eye scale retained.'
assert geometry_digest() == before, 'Protected body/hand/face geometry changed'
assert hashlib.sha256(image.packed_file.data).hexdigest() == image_digest
by_vertex = {}
for loop in face.data.loops:
    by_vertex[loop.vertex_index] = tuple(uv.data[loop.index].uv)
for j in range(45):
    for i in range(65):
        assert by_vertex[j*65+i] == by_vertex[j*65+64-i], 'Face UV not symmetric'

bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'dogido-round-v02.blend'))
day = bpy.data.scenes['Day - 昼の質感']
night = bpy.data.scenes['Night - 暗所の淡い発光']
for scene, filename in ((day, 'day-v02.png'), (night, 'night-v02.png')):
    scene.render.filepath = str(OUT / filename)
    bpy.ops.render.render(write_still=True, scene=scene.name)
camera = day.camera
for loc, filename in (((0, -7, 1.46), 'front-v02.png'), ((7, -1, 2.4), 'side-v02.png')):
    camera.location = loc
    target = Vector((0, 0, 1.46 if filename.startswith('front') else 1.37))
    camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
    day.render.filepath = str(OUT / filename)
    bpy.ops.render.render(write_still=True, scene=day.name)
assert all((OUT / name).stat().st_size > 1000 for name in ('dogido-round-v02.blend', 'day-v02.png', 'night-v02.png', 'front-v02.png', 'side-v02.png'))
print('VERIFIED_FACE_V02: symmetric UV from viewer-right artwork; unchanged original PNG, mesh geometry and transforms; v01 preserved; NOT IN GAME.')
