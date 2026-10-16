from pathlib import Path
import subprocess,json,hashlib,sys
ADB='/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Data/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb'
SERIAL='ZY32FL5RJQ';PACKAGE='com.chupacabras.ar.figure'
root=Path('/home/cacawatin/code/blender/chupacabras/docs/evidencias/ataque_escala_r09_20261011')
root.mkdir(exist_ok=True)
mode=sys.argv[1]
out=root/mode;out.mkdir(exist_ok=False)
def adb(*args,binary=False):
 r=subprocess.run([ADB,'-s',SERIAL,*args],capture_output=True,check=True)
 return r.stdout if binary else r.stdout.decode().strip()
assert 'moto g' in adb('shell','getprop','ro.product.model').lower()
if mode in ('install_test','install_final'):
 apk=Path(sys.argv[2]);assert apk.exists()
 old=adb('shell','dumpsys','package',PACKAGE)
 (out/'package_before.txt').write_text('\n'.join(l for l in old.splitlines() if any(s in l for s in ['Package [','versionCode=','versionName=','codePath=','primaryCpuAbi='])))
 if 'Package ['+PACKAGE+']' in old:
  cleared=adb('shell','pm','clear',PACKAGE);assert cleared=='Success',cleared
  (out/'clear_data.txt').write_text(cleared+'\n')
  result=adb('uninstall',PACKAGE);assert result=='Success',result
  (out/'uninstall.txt').write_text(result+'\n')
 remaining=adb('shell','pm','list','packages',PACKAGE)
 assert 'package:'+PACKAGE not in remaining,remaining
 scoped=['/sdcard/Android/data/'+PACKAGE,'/sdcard/Android/obb/'+PACKAGE,'/sdcard/Android/media/'+PACKAGE]
 cleanup=[]
 for path in scoped:
  present=adb('shell','test -e '+path+' && echo PRESENT || echo ABSENT')
  if present=='PRESENT': adb('shell','rm','-rf',path)
  assert adb('shell','test -e '+path+' && echo PRESENT || echo ABSENT')=='ABSENT'
  cleanup.append({'path':path,'previously_present':present=='PRESENT','absent_after_cleanup':True})
 (out/'project_cleanup.json').write_text(json.dumps(cleanup,indent=2)+'\n')
 result=adb('install',str(apk));assert 'Success' in result,result
 (out/'install.txt').write_text(result+'\n')
 installed=adb('shell','pm','path',PACKAGE).removeprefix('package:')
 adb('pull',installed,str(out/'installed.apk'))
 expected=hashlib.sha256(apk.read_bytes()).hexdigest();actual=hashlib.sha256((out/'installed.apk').read_bytes()).hexdigest();assert expected==actual
 (out/'identity.json').write_text(json.dumps(dict(package=PACKAGE,source=str(apk),sha256=actual,installed_bytes_verified=True),indent=2)+'\n')
 (out/'launch.txt').write_text(adb('shell','am','start','-W','-n',PACKAGE+'/com.unity3d.player.UnityPlayerGameActivity'))
 print('Installed verified',mode,actual)
else:raise ValueError(mode)
