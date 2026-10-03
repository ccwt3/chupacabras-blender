import bpy,json
from pathlib import Path
r=Path('/home/cacawatin/code/blender/chupacabras');e=r/'docs/evidencias/2026-10-02_rigs_demacrado'
bpy.ops.wm.open_mainfile(filepath=str(r/'scenes/11_rigs_contacto_r03.blend'),use_scripts=False)
s=bpy.data.objects['Sheep_Quaternius']
old_faces=[tuple(p.vertices) for p in s.data.polygons]
old_coords=[tuple(v.co) for v in s.data.vertices]
old_shapes=[[tuple(v.co) for v in k.data] for k in s.data.shape_keys.key_blocks]
bpy.ops.wm.open_mainfile(filepath=str(r/'scenes/09_chupacabras_demacrado_r02.blend'),use_scripts=False)
source={o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in bpy.data.objects['ChupacabrasAssetRoot'].children if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(r/'scenes/11_rigs_contacto_demacrado_r01.blend'),use_scripts=False)
s=bpy.data.objects['Sheep_Quaternius']
assert old_faces==[tuple(p.vertices) for p in s.data.polygons]
assert old_coords==[tuple(v.co) for v in s.data.vertices]
assert old_shapes==[[tuple(v.co) for v in k.data] for k in s.data.shape_keys.key_blocks]
from mathutils import Vector
error=max((v.co-Vector(p)).length for name,points in source.items() for v,p in zip(bpy.data.objects[name].data.vertices,points))
assert error<1e-6,error
assert all(len(points)==len(bpy.data.objects[name].data.vertices) for name,points in source.items())
report=dict(passed=True,creature_meshes=len(source),rest_mesh_error=error,sheep_r03_triangles_unchanged=True,sheep_shape_keys_unchanged=True,physical_device=False)
(e/'fuentes.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
