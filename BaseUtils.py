import time
import crayons
import functools


def time_func(_func=None, *, runs=3):
    """https://realpython.com/primer-on-python-decorators/"""

    if runs < 1:
        raise ValueError('runs should be higher than 0 not {}'.format(runs))

    def decorator(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):

            value = None
            start = time.perf_counter()

            for _ in range(runs):
                value = func(*args, **kwargs)

            end = time.perf_counter()
            run_time = (end - start) / (_ + 1)
            print(crayons.red('{} took {:.4f} secs on an average of {} runs'.format(func.__name__, run_time, runs), bold=True))
            return value

        return inner

    if _func is None:
        return decorator
    return decorator(_func)


@time_func(runs=10)
def test():
    for i in range(100000):
        print(i)


if __name__ == '__main__':
    test()

