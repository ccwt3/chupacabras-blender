"""Reopen the source and FBX, checking animated geometry, support and final loop."""
import json,os,sys
from pathlib import Path
import bpy
from mathutils.kdtree import KDTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from oveja import positions
ROOT=Path(__file__).resolve().parents[1]
NAME='ataque_ar_'+os.environ.get('CHUPA_ATTACK_REV','r01')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')),use_scripts=False)
report=json.loads((ROOT/"exports"/(NAME+".json")).read_text())
frames=tuple(sorted(set([1,49,61,73,85,109,157,193,229,265,301,report["loop_start_frame"],report["loop_end_frame"]])))
expected={}
root=bpy.data.objects['ChupacabrasAssetRoot'];scene=bpy.context.scene
yaws=[]
for frame in range(1,report['loop_end_frame']+1):
 scene.frame_set(frame);yaws.append(root.rotation_euler.z)
assert max(abs(a-b) for a,b in zip(yaws,yaws[1:]))<.2,'Abrupt turn'
scene.frame_set(1);home=root.location.copy()
scene.frame_set(report['loop_start_frame']);assert root.location.xy.length<.001,'Finish over the marker'
assert report.get('max_foot_reach_excess',0)<.001

for frame in frames:
 bpy.context.scene.frame_set(frame)
 expected[frame]={name:positions(bpy.data.objects[name]) for name in ('Chupacabras_Nocturno','Sheep_Quaternius')}
for obj in (bpy.data.objects[n] for n in expected[1]):
 assert max(len([g for g in v.groups if g.weight>1e-6]) for v in obj.data.vertices)<=4
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(ROOT/'exports'/(NAME+'.fbx')),use_anim=True,anim_offset=0)
bpy.context.scene.render.fps=24
errors=[]
for frame in frames:
 bpy.context.scene.frame_set(frame)
 for name,points in expected[frame].items():
  actual=positions(bpy.data.objects[name]);assert len(points)==len(actual)
  tree=KDTree(len(actual))
  for i,v in enumerate(actual):tree.insert(v,i)
  tree.balance()
  error=max(tree.find(v)[2] for v in points);errors.append(error)
  assert error<.001,(name,frame,error)
result=dict(passed=True,samples=len(frames),max_fbx_error=max(errors),physical_device=False)
(ROOT/'previews'/NAME).mkdir(exist_ok=True)
(ROOT/'previews'/NAME/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('ATTACK_FBX_CHECKS_OK',json.dumps(result))
