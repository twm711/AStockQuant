from collections import Counter

def build_ladder(rows):
    """rows: records with symbol, board_height, is_broken, promoted."""
    valid=[r for r in rows if not r.get('is_broken',False)]
    counts=Counter(int(r.get('board_height',1)) for r in valid)
    max_height=max(counts,default=0)
    total=sum(1 for r in rows if int(r.get('board_height',1))==1)
    promoted=sum(1 for r in rows if r.get('promoted',False))
    return {'counts':dict(sorted(counts.items())),'max_height':max_height,'promotion_rate':round(promoted/total,4) if total else None}
