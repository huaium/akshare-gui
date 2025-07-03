import atexit
import os
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, Literal, TypeVar, Union, overload

# safe to use global here

T = TypeVar("T")

_cpu_count_tmp = os.cpu_count()
cpu_count = _cpu_count_tmp if _cpu_count_tmp is not None else 1  # exposed

max_workers = cpu_count  # exposed
_shutdown = False
_executor = ThreadPoolExecutor(max_workers=max_workers)
_executor_lock = threading.Lock()


@overload
def thread_it(func: Callable[..., T], join: Literal[True]) -> T: ...


@overload
def thread_it(func: Callable[..., T], join: Literal[False]) -> Future[T]: ...


@overload
def thread_it(func: Callable[..., T]) -> Future[T]: ...


def thread_it(func: Callable[..., T], join: bool = False) -> Union[T, Future[T]]:
    with _executor_lock:
        if _shutdown:
            _reinit()

        future = _executor.submit(func)

    return future.result() if join else future


def shutdown():
    global _shutdown
    with _executor_lock:
        if not _shutdown:
            _executor.shutdown(wait=False)
            _shutdown = True


def _reinit():
    global _shutdown, _executor
    with _executor_lock:
        if _shutdown:
            _executor.shutdown(wait=False)  # to make sure
            _executor = ThreadPoolExecutor(max_workers=max_workers)
            _shutdown = False


atexit.register(shutdown)
