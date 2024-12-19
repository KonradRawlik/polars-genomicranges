import polars as pl
from .into import into_irange

def start(r):
    if isinstance(r, pl.Expr):
        return r.struct.field('start')
    else:
        return into_irange(r).start

def end(r):
    if isinstance(r, pl.Expr):
        return r.struct.field('end')
    else:
        return into_irange(r).end

def width(r):
    return end(r) - start(r)

def is_empty(r):
    return width(r) <= 0

def normalize_empty(r):
    return pl.when(width(r) < 0).then(r.struct.with_fields(end=start(r))).otherwise(r)

