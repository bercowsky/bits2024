import typing as tp


def virtual(func: tp.Callable) -> tp.Callable:
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"Method '{func.__name__}' must be overridden in the derived class."
        )

    return wrapper
