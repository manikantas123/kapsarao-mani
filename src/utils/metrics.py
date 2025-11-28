def pct_change(old, new):
    if old == 0:
        return float('inf') if new != 0 else 0.0
    try:
        return (old - new) / old
    except Exception:
        return 0.0