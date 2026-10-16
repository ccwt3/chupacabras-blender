from pathlib import Path
import subprocess,json,time,statistics,sys,shlex
ADB='/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Data/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb'
SERIAL='ZY32FL5RJQ';PACKAGE='com.chupacabras.ar.figure'
out=Path('/home/cacawatin/code/blender/chupacabras/docs/evidencias/ataque_escala_r09_20261011')/sys.argv[1]
out.mkdir(exist_ok=False)
def adb(*args,binary=False):
 r=subprocess.run([ADB,'-s',SERIAL,*args],capture_output=True,check=True)
 return r.stdout if binary else r.stdout.decode().strip()
assert 'moto g' in adb('shell','getprop','ro.product.model').lower()
pid=adb('shell','pidof',PACKAGE);assert pid.isdigit()
(out/'device.json').write_text(json.dumps({name:adb('shell','getprop',name) for name in ['ro.product.model','ro.build.version.release','ro.build.version.sdk','ro.product.cpu.abilist']},indent=2))
(out/'page_size.txt').write_text(adb('shell','getconf','PAGE_SIZE'))
(out/'memory_start.txt').write_text(adb('shell','dumpsys','meminfo',PACKAGE))
(out/'battery_start.txt').write_text(adb('shell','dumpsys','battery'))
layers=adb('shell','dumpsys','SurfaceFlinger','--list').splitlines()
matching=[s for s in layers if PACKAGE in s and s.startswith('SurfaceView - ')]
(out/'layers.txt').write_text('\n'.join(matching))
assert len(matching)==1,matching
layer=matching[0]
duration=int(sys.argv[2]);start=time.monotonic();timestamps=set();samples=[];cutoff=None
while time.monotonic()-start<duration:
 elapsed=time.monotonic()-start
 raw=adb('shell','dumpsys','SurfaceFlinger','--latency',shlex.quote(layer))
 with (out/'surface_latency.txt').open('a') as f:f.write(f'\nSAMPLE {elapsed:.3f}\n'+raw+'\n')
 current=[]
 for row in raw.splitlines()[1:]:
  cols=row.split()
  if len(cols)==3 and all(c.isdigit() for c in cols):
   actual=int(cols[1])
   if 0<actual<9223372036854775807:current.append(actual)
 if cutoff is None and current:cutoff=max(current)
 timestamps.update(v for v in current if cutoff is not None and v>=cutoff)
 if not samples or elapsed-samples[-1]>=30:
  samples.append(elapsed)
  (out/f'memory_{int(elapsed):03d}.txt').write_text(adb('shell','dumpsys','meminfo',PACKAGE))
  foreground=adb('shell','dumpsys','activity','activities')
  if any(PACKAGE in line for line in foreground.splitlines() if 'mResumedActivity:' in line):
   (out/f'screen_{int(elapsed):03d}.png').write_bytes(adb('exec-out','screencap','-p',binary=True))
  print('MOBILE_SAMPLE',round(elapsed),len(timestamps),flush=True)
 time.sleep(1)
(out/'memory_end.txt').write_text(adb('shell','dumpsys','meminfo',PACKAGE))
(out/'battery_end.txt').write_text(adb('shell','dumpsys','battery'))
(out/'logcat.txt').write_text(adb('logcat','-d','--pid='+pid,'-v','threadtime'))
ordered=sorted(timestamps);intervals=[(b-a)/1e6 for a,b in zip(ordered,ordered[1:])]
report=dict(duration_s=time.monotonic()-start,unique_presented_frames=len(ordered),same_process=pid==adb('shell','pidof',PACKAGE),method='SurfaceFlinger actualPresentTime; includes only this app SurfaceView; visibility requires separate observation')
if intervals:
 ordered_intervals=sorted(intervals)
 report.update(fps=(len(ordered)-1)*1e9/(ordered[-1]-ordered[0]),median_ms=statistics.median(intervals),p95_ms=ordered_intervals[int(.95*(len(intervals)-1))],max_ms=max(intervals))
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
