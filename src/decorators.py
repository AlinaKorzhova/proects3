from functools import wraps


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                res = f'{func.__name__} ok'
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(res + "\n")
                else:
                    print(res)
            except Exception as e:
                error_message = f'{func.__name__} error: {e}, Inputs: args={args}, kwargs={kwargs}'
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + '\n')
                else:
                    print(error_message)
            return result
        return wrapper
    return decorator


@log()
def my_function(x, y):
    return x / y

print(my_function(9,7))

