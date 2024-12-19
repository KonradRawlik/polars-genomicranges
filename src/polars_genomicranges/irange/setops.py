import polars as pl

from .core import start, end, width, normalize_empty

def union(a, b, gap='fill'):
    s = pl.min_horizontal(start(a),start(b))
    e = pl.max_horizontal(end(a),end(b))
    union = pl.struct(start=s,end=e)
    if gap == 'fill':
        return union
    elif gap is None:
        return pl.when(width(intersection(a,b,normal_empty=False)) < 0).then(None).otherwise(union)
    else:
        raise ValueError

def intersection(a, b, normal_empty=True):
    s = pl.max_horizontal(start(a),start(b))
    e = pl.min_horizontal(end(a),end(b))
    intersection = pl.struct(start = s, end = e).alias('intersection')
    if normal_empty:
        intersection = normalize_empty(intersection)
    return intersection

def setdiff(a, b):
    contained = (start(a) < start(b)) & (end(b) < start(b))
    s = pl.max_horizontal(start(a), start(b))
    e = pl.min_horizontal(end(a), end(b))
    proper = s < e
    right = e == end(a)
    ans_end = pl.when(proper & right).then(s).otherwise(end(a))
    ans_start = pl.when(proper & ~right).then(e).otherwise(start(a))
    return pl.when(contained).then(None).otherwise(pl.struct(start = ans_start, end = ans_end))
    
def gap(a, b):
    s = pl.min_horizontal(end(a), end(b))
    e = pl.max_horizontal(start(a),start(b))
    return pl.struct(start = s, end = e)

