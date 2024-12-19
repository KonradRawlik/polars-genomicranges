from polars.api import register_expr_namespace

from . import irange

@register_expr_namespace('irange')
class IRangeExpr:
    def __init__(self, expr):
        self._expr = expr
    
    def start(self):
        return irange.start(self._expr)
    
    def end(self):
        return irange.end(self._expr)
    
    def width(self):
        return irange.width(self._expr)

    def is_empty(self):
        return irange.is_empty(self._expr)

    def shift(self,*args, **kwargs):
        return irange.shift(self._expr, *args, **kwargs)

    def resize(self, to_width, anchor='start'):
        return irange.resize(self._expr, to_width, anchor)
    
    def restrict(self, to = None, **kwargs):
        return irange.restrict(self._expr, to, **kwargs)

    def flank(self, width, anchor='start', direction='out'):
        return irange.flank(self._expr, width, anchor, direction)
    
    def span(self):
        return irange.span(self._expr)

    def cluster(self):
        return irange.cluster(self._expr)

    def union(self, other, gap=None):
        return irange.union(self._expr, other, gap)
    
    def intersection(self, other, normal_empty=True):
        return irange.intersection(self._expr, other, normal_empty)

    def setdiff(self, other):
        return irange.setdiff(self._expr, other)
    
    def gap(self, other):
        return irange.gap(self._expr, other)