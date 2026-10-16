from pathlib import Path
import subprocess,time,json
adb='/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Data/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb';pkg='com.chupacabras.ar.figure'
out=Path('/home/cacawatin/code/blender/chupacabras/docs/evidencias/ataque_escala_r09_20261011/lifecycle');out.mkdir(exist_ok=False)
def call(*args,binary=False):
 data=subprocess.check_output([adb,'-s','ZY32FL5RJQ',*args]);return data if binary else data.decode().strip()
pid=call('shell','pidof',pkg);before=call('logcat','-d','--pid='+pid,'-v','brief')
call('shell','input','keyevent','KEYCODE_HOME');time.sleep(2)
launch=call('shell','am','start','-W','-n',pkg+'/com.unity3d.player.UnityPlayerGameActivity');time.sleep(5)
after=call('logcat','-d','--pid='+pid,'-v','brief');same=call('shell','pidof',pkg)==pid
reopened=after.count('CHUPACABRAS_CAMERA')>before.count('CHUPACABRAS_CAMERA')
assert same and reopened,(same,reopened)
(out/'launch.txt').write_text(launch);(out/'logcat.txt').write_text(after)
(out/'resumed.png').write_bytes(call('exec-out','screencap','-p',binary=True))
report={'same_process':same,'camera_reopened':reopened,'passed':True};(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
