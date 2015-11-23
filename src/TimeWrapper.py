from functools import wraps
from time import time

def timed(f):
  @wraps(f)
  def wrapper(*args, **kwds):
    start = time()
    result = f(*args, **kwds)
    elapsed = ((time() - start)) * 1000
    elapsed = float("{0:.2f}".format(elapsed))
    print(f.__name__ + " took " + str(elapsed) + " ms to finish")
    return result
  return wrapper
