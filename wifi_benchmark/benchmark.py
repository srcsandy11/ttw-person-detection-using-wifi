"""RX1-only binary occupancy benchmark, with session-label controls."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
meta = json.loads((HERE / 'data/metadata.json').read_text())
features = [name for name in meta['feature_names'] if name.startswith('rx1_')]
assert len(features) == 13
splits = {}
for name in ('train', 'val', 'test'):
    with (HERE / f'data/{name}_features.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    assert all(r['split'] == name for r in rows)
    x = np.array([[float(r[k]) for k in features] for r in rows])
    y = np.array([int(r['y']) for r in rows])
    groups = np.array([r['session_id'] for r in rows])
    assert set(y) == {0, 1} and np.isfinite(x).all()
    splits[name] = (x, y, groups)
for a, b in [('train','val'), ('train','test'), ('val','test')]:
    assert not (set(splits[a][2]) & set(splits[b][2]))
    # Exact equality of selected numeric feature vectors, independent of labels.
    xa, xb = splits[a][0], splits[b][0]
    da = {row.tobytes() for row in xa}
    db = {row.tobytes() for row in xb}
    overlap = len(da & db)
    if overlap:
        raise ValueError(f'{a}/{b}: {overlap} duplicate feature vectors')

x, y, groups = splits['train']
mu, sigma = x.mean(axis=0), x.std(axis=0)
sigma[sigma < 1e-12] = 1
def design(x):
    return np.column_stack((np.ones(len(x)), (x-mu)/sigma))
X = design(x)

def fit(target):
    w = np.zeros(X.shape[1])
    for _ in range(3000):
        p = 1/(1+np.exp(-np.clip(X @ w, -40, 40)))
        gradient = X.T @ (p-target)/len(target)
        gradient[1:] += 0.01*w[1:]
        w -= 0.1*gradient
    return w

def predict(x, w):
    return 1/(1+np.exp(-np.clip(design(x)@w,-40,40)))

def metrics(y, pred):
    tn = int(((y==0)&(pred==0)).sum()); fp = int(((y==0)&(pred==1)).sum())
    fn = int(((y==1)&(pred==0)).sum()); tp = int(((y==1)&(pred==1)).sum())
    return {'tn':tn,'fp':fp,'fn':fn,'tp':tp,
            'accuracy':(tn+tp)/len(y), 'balanced_accuracy':(tn/(tn+fp)+tp/(tp+fn))/2,
            'occupied_precision':tp/(tp+fp) if tp+fp else 0,
            'occupied_recall':tp/(tp+fn), 'empty_false_positive_rate':fp/(tn+fp),
            'occupied_f1':2*tp/(2*tp+fp+fn)}

def session_metrics(y,g,p):
    gy=[]; gp=[]
    for session in sorted(set(g)):
        mask=g==session
        assert len(set(y[mask])) == 1
        gy.append(y[mask][0]); gp.append(int(p[mask].mean()>=0.5))
    return metrics(np.array(gy),np.array(gp))

w=fit(y)
out={'model':'L2 logistic regression, learning rate 0.1, 3000 iterations, L2 0.01',
     'threshold':0.5, 'duplicate_check':'zero exact feature-vector matches between every pair of splits',
     'note':'Overlapping windows are correlated; session-level results reflect one vote per recording.',
     'features':features, 'splits':{}}
for name,(x,y,g) in splits.items():
    p=predict(x,w)
    out['splits'][name]={'sessions':len(set(g)),'windows':len(y),
                          'window_metrics':metrics(y,(p>=0.5).astype(int)),
                          'session_metrics':session_metrics(y,g,p)}
model={'feature_names':features,'means':mu.tolist(),'standard_deviations':sigma.tolist(),
       'intercept':float(w[0]), 'coefficients':w[1:].tolist(),
       'threshold':0.5, 'formula':'sigmoid(intercept + sum(coefficient * (feature - mean) / standard_deviation))',
       'source_baseline':'RX1 baseline from training empty sessions only; source baseline profile required to compute features'}
(HERE/'model.json').write_text(json.dumps(model,indent=2)+'\n')

# Permute training labels at session level; never permute correlated windows independently.
train_x, train_y, train_groups=splits['train']
sessions=sorted(set(train_groups))
labels=np.array([train_y[train_groups==s][0] for s in sessions])
assert all(len(set(train_y[train_groups==s]))==1 for s in sessions)
rng=np.random.default_rng(20261122)
test_x,test_y,test_groups=splits['test']
controls=[]
for _ in range(50):
    shuffled=rng.permutation(labels)
    lookup=dict(zip(sessions,shuffled))
    perm_y=np.array([lookup[g] for g in train_groups])
    pw=fit(perm_y)
    p=predict(test_x,pw)
    controls.append({'window_balanced_accuracy':metrics(test_y,(p>=0.5).astype(int))['balanced_accuracy'],
                     'session_balanced_accuracy':session_metrics(test_y,test_groups,p)['balanced_accuracy']})
out['permutation_control']={'iterations':len(controls),'seed':20261122,'unit':'entire training session',
    'description':'Shuffle training session labels, fit same model, score against unshuffled test labels. Empty/nonempty session counts preserved.',
    'window_balanced_accuracy_mean':float(np.mean([c['window_balanced_accuracy'] for c in controls])),
    'window_balanced_accuracy_min':float(np.min([c['window_balanced_accuracy'] for c in controls])),
    'window_balanced_accuracy_max':float(np.max([c['window_balanced_accuracy'] for c in controls])),
    'window_balanced_accuracy_at_least_actual_count':sum(c['window_balanced_accuracy']>=out['splits']['test']['window_metrics']['balanced_accuracy'] for c in controls),
    'session_balanced_accuracy_mean':float(np.mean([c['session_balanced_accuracy'] for c in controls])),
    'session_balanced_accuracy_min':float(np.min([c['session_balanced_accuracy'] for c in controls])),
    'session_balanced_accuracy_max':float(np.max([c['session_balanced_accuracy'] for c in controls]))}
(HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'test':out['splits']['test'],'control':out['permutation_control']},indent=2))
