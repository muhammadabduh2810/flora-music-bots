import os

from WinxMusic.utils.decorators import asyncify
from config import autoclean


@asyncify
def auto_clean(popped):
    def _auto_clean(popped_item):
        try:
            rem = popped_item["file"]
            autoclean.remove(rem)
            count = autoclean.count(rem)
            if count == 0:
                if "vid_" not in rem and "live_" not in rem and "index_" not in rem:
                    try:
                        os.remove(rem)
                    except Exception:
                        pass
        except Exception:
            pass

    if isinstance(popped, dict):
        _auto_clean(popped)
    elif isinstance(popped, list):
        for pop in popped:
            _auto_clean(pop)
    else:
        raise ValueError("Diharapkan muncul menjadi kamus atau daftar.")
