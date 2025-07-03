# this is a hack to disable tqdm, to avoid its calling to sys.executable
# since after packaging the app, it will lead to more than one process running

import tqdm


def dummy_tqdm(iterable=None, *args, **kwargs):
    if iterable is None:
        return []
    return iterable


tqdm.tqdm = dummy_tqdm

if hasattr(tqdm, "auto"):
    tqdm.auto.tqdm = dummy_tqdm  # type: ignore
if hasattr(tqdm, "notebook"):
    tqdm.notebook.tqdm = dummy_tqdm
