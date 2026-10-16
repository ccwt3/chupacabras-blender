"""Summarize a completed perfil_figura_g20 run; retain stalls and tracking losses."""
import csv
import json
import math
from pathlib import Path
import re
import statistics
import sys


def distribution(values):
    values = sorted(values)
    return dict(n=len(values), min=values[0], median=statistics.median(values),
                p95=values[math.ceil(.95 * len(values)) - 1],
                p99=values[math.ceil(.99 * len(values)) - 1], max=values[-1])


def main():
    folder = Path(sys.argv[1])
    samples = [json.loads(line) for line in (folder / 'samples.jsonl').read_text().splitlines()]

    def timestamps(sample):
        return [int(line.split()[1]) for line in sample['latency']['stdout'].splitlines()[1:]
                if len(line.split()) == 3 and 0 < int(line.split()[1]) < 2**63 - 1]

    start = max(timestamps(samples[0]))
    times = sorted({t for sample in samples for t in timestamps(sample) if t >= start})
    intervals = [(b - a) / 1e6 for a, b in zip(times, times[1:])]
    result = dict(elapsed_s=(times[-1] - start) / 1e9,
                  fps=1000 / statistics.mean(intervals), frame_ms=distribution(intervals),
                  over_50ms=sum(v > 50 for v in intervals),
                  over_100ms=sum(v > 100 for v in intervals), system=[])
    for sample in samples:
        if 'memory' not in sample:
            continue
        def value(pattern, field):
            match = re.search(pattern, sample[field]['stdout'])
            return float(match[1]) if match else None
        result['system'].append(dict(seconds=sample['elapsed_s'],
            pss_kib=value(r'TOTAL PSS:\s+(\d+)', 'memory'),
            native_alloc_kib=value(r'Native Heap\s+(?:\d+\s+){6}(\d+)', 'memory'),
            battery_tenths_c=value(r'temperature: (\d+)', 'battery'),
            thermal_status=value(r'Thermal Status: (\d+)', 'thermal')))
    first = float(samples[0]['tracking_tail']['stdout'].splitlines()[-1].split(',')[0]) + 1
    last = float(samples[-1]['tracking_tail']['stdout'].splitlines()[-1].split(',')[0]) - 1
    source = sorted((folder / 'files').glob('probe_*/tracking.csv'))[-1]
    with source.open() as stream:
        rows = [r for r in csv.DictReader(stream) if first <= float(r['seconds']) <= last]
    elapsed = float(rows[-1]['seconds']) - float(rows[0]['seconds'])
    result['tracking'] = dict(csv=str(source), seconds=elapsed, samples=len(rows),
        visible=sum(r['visible'] == 'True' for r in rows),
        lost_seconds=[float(r['seconds']) for r in rows if r['visible'] != 'True'],
        detector_hz=(int(rows[-1]['processed_frames']) - int(rows[0]['processed_frames'])) / elapsed,
        image_ms=distribution([float(r['image_ms']) for r in rows]),
        detector_ms=distribution([float(r['detect_ms']) for r in rows]))
    result['limits'] = 'All gaps retained. Surface presentation is not GPU execution time. CSV frame time is an EMA. USB charging and ADB sampling active.'
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
