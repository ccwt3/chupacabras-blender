"""Read-only G20 sampling; run only after the user positions the visible figure."""
import argparse
import datetime
import json
from pathlib import Path
import shlex
import subprocess
import time

ADB = '/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Data/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb'
PACKAGE = 'com.chupacabras.ar.figure'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--seconds', type=int, default=310)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error('Duration must be positive')
    devices = subprocess.check_output([ADB, 'devices'], text=True).splitlines()[1:]
    serials = [row.split()[0] for row in devices if len(row.split()) >= 2 and row.split()[1] == 'device']
    if len(serials) != 1:
        parser.error('Exactly one authorized device is required')
    adb = [ADB, '-s', serials[0]]

    def shell(command):
        result = subprocess.run(adb + ['shell', command], capture_output=True, text=True, timeout=20)
        return {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}

    model = shell('getprop ro.product.model')['stdout'].strip()
    if model != 'moto g(20)':
        parser.error('Unexpected device: ' + model)
    pid = shell('pidof ' + PACKAGE)['stdout'].strip()
    if not pid.isdigit():
        parser.error('Figure app must be running')
    surfaces = shell('dumpsys SurfaceFlinger --list')['stdout'].splitlines()
    layers = [line for line in surfaces if line.startswith('SurfaceView - ' + PACKAGE + '/')]
    if len(layers) != 1:
        parser.error('Expected one figure SurfaceView: ' + repr(layers))
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'metadata.json').write_text(json.dumps({
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'model': model, 'pid': pid, 'surface': layers[0], 'duration_requested_s': args.seconds,
        'limits': 'SurfaceFlinger presentation timestamps, not GPU execution times. USB charging and ADB sampling remain active.'
    }, indent=2) + '\n')
    started = time.monotonic()
    index = 0
    with (args.output / 'samples.jsonl').open('w') as stream:
        while True:
            elapsed = time.monotonic() - started
            sample = {'elapsed_s': elapsed, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
            sample['latency'] = shell('dumpsys SurfaceFlinger --latency ' + shlex.quote(layers[0]))
            if index % 10 == 0 or elapsed >= args.seconds:
                sample['memory'] = shell('dumpsys meminfo ' + PACKAGE)
                sample['thermal'] = shell('dumpsys thermalservice')
                sample['battery'] = shell('dumpsys battery')
                sample['cpu'] = shell('dumpsys cpuinfo | grep ' + shlex.quote(PACKAGE))
                sample['foreground'] = shell('dumpsys activity activities | grep mResumedActivity')
                sample['tracking_tail'] = shell('tail -n 1 /sdcard/Android/data/' + PACKAGE + '/files/probe_*/tracking.csv')
                print(f'{elapsed:.0f}s collected', flush=True)
            stream.write(json.dumps(sample) + '\n')
            stream.flush()
            if elapsed >= args.seconds:
                break
            index += 1
            time.sleep(max(0, min(started + index * 3, started + args.seconds) - time.monotonic()))
    subprocess.run(adb + ['pull', '/sdcard/Android/data/' + PACKAGE + '/files', str(args.output / 'files')], check=True)
    log = subprocess.run(adb + ['logcat', '-d', '--pid=' + pid, '-v', 'threadtime'], capture_output=True, text=True, check=True)
    (args.output / 'logcat.txt').write_text(log.stdout)


if __name__ == '__main__':
    main()
