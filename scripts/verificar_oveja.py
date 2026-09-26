"""Reabre la oveja editable y valida fuente/licencia, escala y rig existente."""
import hashlib
import json
from pathlib import Path
import bpy
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'assets/oveja/procedencia.json').read_text())
for entry in manifest['files']:
    assert hashlib.sha256((root/'assets/oveja'/entry['path']).read_bytes()).hexdigest()==entry['sha256']
bpy.ops.wm.open_mainfile(filepath=str(root/'scenes/07_oveja_r04.blend'),use_scripts=False)
rig=bpy.data.objects['SheepRig'];mesh=bpy.data.objects['Sheep_Quaternius']
assert len(rig.data.bones)==24 and len(mesh.data.vertices)==307
assert max(len(v.groups) for v in mesh.data.vertices)<=4
assert len(mesh.data.materials)==2 and mesh.data.shape_keys is None
assert {'Death','Idle','Jump','Run','Walk','WalkSlow'} <= set(bpy.data.actions.keys())
assert rig.animation_data.action is None and all(t.mute for t in rig.animation_data.nla_tracks)
ev=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
verts=[ev.matrix_world@v.co for v in ev.data.vertices]
height=max(v.z for v in verts)-min(v.z for v in verts)
assert abs(height-1.18)<1e-5 and abs(min(v.z for v in verts))<1e-5
assert not any(im.source=='FILE' for im in bpy.data.images)
print('SHEEP_REOPEN_OK '+json.dumps(dict(height_m=height,bones=24,vertices=307,native_actions=6,external_textures=0,physical_device=False)))
