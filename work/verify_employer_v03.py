"""Replay saved v0.3 artefacts and verify hashes without overwriting them."""
import hashlib
import json
from pathlib import Path, PureWindowsPath

from employer_measurement_v03 import assess, evaluate

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'outputs/employer-v03/run-001'


def main():
    read=lambda name:json.loads((RUN/name).read_text(encoding='utf-8'))
    manifest=read('manifest.json')
    for path,digest in {**manifest['source_hashes'],**manifest['preserved_output_hashes']}.items():
        assert hashlib.sha256(ROOT.joinpath(*PureWindowsPath(path).parts).read_bytes()).hexdigest()==digest,path
    packets={(p['id'],p['profile']):p['records'] for p in read('observations.json')}
    truth={t['id']:t for t in read('truth.json')}
    runs=read('assessments.json')
    for r in runs:
        records=packets[r['id'],r['profile']]
        assert r['assessments']==[assess(records,q,r['threshold'],r['flow_rule']) for q in range(13)]
        r['actual']=truth[r['id']]['actual']
        r['no_ai']=truth[r['id']]['no_ai']
    settings=read('evaluation.json')['settings']
    for s in settings:
        selected=[r for r in runs if r['profile']==s['profile'] and r['threshold']==s['threshold']
                  and r['flow_rule']==s['flow_rule'] and truth[r['id']]['family']==s['family']]
        assert s['metrics']==evaluate(selected)
    # Stale cumulative data cannot be mistaken for a complete current window.
    stale=next(s for s in settings if s['profile']=='staggered' and s['threshold']==.1
               and s['flow_rule']=='cumulative' and s['family']=='structural')
    assert stale['metrics']['hiring']['true_alerts']==0
    assert stale['metrics']['hiring']['positive_abstentions']==stale['metrics']['hiring']['positives']
    # Late automation of new work is outside the fixed early event window.
    later=next(r for r in runs if r['id']==8 and r['profile']=='immediate' and r['threshold']==.1
               and r['flow_rule']=='fixed_event')
    assert sum(x['layoffs'] for x in later['actual'][7:])>0
    assert not later['assessments'][-1]['outcomes']['layoffs']['alert']
    print(f"PASS: {len(runs)} saved variants, {len(runs)*13} assessments, {len(settings)} evaluation settings; source and baseline hashes unchanged; stale-window and late-event checks.")


if __name__=='__main__':
    main()
