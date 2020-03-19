try:
    from .production import *
except Exception:
    try:
        from .dev import *
    except Exception:
        raise ImportError("Project Needs production.py or dev.py File...! ")
