"""Cooperative per-GPU lease plus current free-VRAM check before model loading."""
from contextlib import contextmanager
import csv
import fcntl
import io
import os
from pathlib import Path
import time

from pilot.common import checked,write_json


def gpu_inventory():
    raw=checked(['nvidia-smi','--query-gpu=index,uuid,memory.free,memory.total',
                 '--format=csv,noheader,nounits'],timeout=20)
    return [dict(index=row[0].strip(),uuid=row[1].strip(),free_mib=float(row[2]),total_mib=float(row[3]))
            for row in csv.reader(io.StringIO(raw)) if row]


@contextmanager
def gpu_lease(root,slots,stage,minimum_free_gib=12.5,lock_directory=None):
    """No process killing or quota modification. Nonparticipating jobs may still start."""
    root=Path(root);locks=[];admitted=False
    record=dict(status='checking',stage=stage,minimum_free_gib=minimum_free_gib,pid=os.getpid())
    path=root/(stage+'-gpu-preflight.json')
    directory=Path(lock_directory) if lock_directory else Path('/tmp')/('test4py-gpu-leases-'+str(os.getuid()))
    directory.mkdir(parents=True,exist_ok=True)
    try:
        inventory=gpu_inventory();selected=[]
        for slot in slots:
            match=[g for g in inventory if str(slot) in (g['index'],g['uuid'])]
            if len(match)!=1:raise RuntimeError('Cannot resolve selected physical GPU: '+str(slot))
            selected.append(match[0])
        if len({g['uuid'] for g in selected})!=len(selected):raise RuntimeError('Duplicate GPU selection')
        for gpu in sorted(selected,key=lambda g:g['uuid']):
            lock=(directory/(gpu['uuid']+'.lock')).open('a')
            try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:
                lock.close();raise RuntimeError('GPU is reserved by another Test4Py run: '+gpu['index'])
            locks.append(lock)
        current={g['uuid']:g for g in gpu_inventory()}
        record['gpus']=[current[g['uuid']] for g in selected]
        busy=[g for g in record['gpus'] if g['free_mib']<minimum_free_gib*1024]
        if busy:raise RuntimeError('GPU busy: insufficient current free VRAM; no model launched. '+
                                  ', '.join(g['index']+': '+str(round(g['free_mib']/1024,2))+' GiB free' for g in busy))
        record['status']='passed';write_json(path,record)
        admitted=True
        yield
    except Exception as exc:
        record.update(status='passed' if admitted else 'blocked',error=repr(exc));write_json(path,record)
        raise
    finally:
        for lock in reversed(locks):fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
        record['released_epoch']=time.time();write_json(path,record)
