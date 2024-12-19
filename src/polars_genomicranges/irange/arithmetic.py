from typing import Optional

import polars as pl
from .core import start, end, width
from .into import into_irange

def shift(range_expr, *args, **kwargs):
    assert len(args) <= 1 
    if len(args) == 1:
        kwargs['delta'] = args[0]
    assert len(kwargs) == 1
    match kwargs:
        case {'delta' : amount} | {'right' : amount}:
            delta = amount
        case {'left' : amount}:
            delta = -amount
    return range_expr.struct.with_fields(start = start(range_expr) + delta, end = end(range_expr) + delta)

def resize(range_expr, to_width, anchor='start'):
    match anchor:
        case 'start':
            return range_expr.struct.with_fields(end = start(range_expr) + to_width)
        case 'end':
            return range_expr.struct.with_fields(start = end(range_expr) - to_width)
        case 'center':
            half_width = to_width / 2
            center = start(range_expr) + width(range_expr)/2
            return range_expr.struct.with_fields(start = center - half_width, end = center + half_width)
        case _:
            raise ValueError

def restrict(range_expr, to:Optional = None, **kwargs):
    if to is not None:
        assert len(kwargs) == 0
        to = into_irange(to)
    else:
        to = into_irange(**kwargs) 
    return range_expr.struct.with_fields(start = start(range_expr).clip(start(to),end(to)), end = end(range_expr).clip(start(to), end(to)))

def flank(range_expr, width, anchor='start', direction='out'):
    match anchor:
        case 'start':
            match direction:
                case 'out':
                    return range_expr.struct.with_fields(start = start(range_expr) - width, end = start(range_expr))
                case 'in':
                    return range_expr.struct.with_fields(end = start(range_expr) + width)
                case 'both':
                    return range_expr.struct.with_fields(start = start(range_expr) - width, end = start(range_expr) + width) 
        case 'end':
            match direction:
                case 'out':
                    return range_expr.struct.with_fields(start = end(range_expr), end = end(range_expr) + width)
                case 'in':
                    return range_expr.struct.with_fields(start = end(range_expr) - width)
                case 'both':
                    return range_expr.struct.with_fields(start = end(range_expr) - width, end = end(range_expr) + width) 
                
def span(range_expr):
    return pl.struct(start = start(range_expr).min(), end = end(range_expr).max()).alias('span')

def cluster(range_expr):
    #cur_end = 0
    #cur_cluster = 0 
    #for i,r in enumerate(ranges):
    #   if r.start > cur_end:
    #       cur_cluster += 1
    #       cur_end = r.end
    #   elif r.end > cur_end:
    #       cur_end = r.end
    #   cluster[i] = cur_cluster 
    right_most_end = end(range_expr).cum_max().shift(1, fill_value=0)
    no_overlaps_with_preceding = start(range_expr) > right_most_end
    cluster = no_overlaps_with_preceding.cum_sum() 
    return cluster.alias('cluster')