from collections import deque, Iterable
import greenlet


"""
Returns `True` if all elements on `iterable` are `None`, and `False`
otherwise.
"""
def all_none(iterable):
    for item in iterable:
        if item is not None:
            return False
    return True

"""
Force `value` to be a list.

Returns `value` casted a `list` it it is iterable, an empty list if it is
`None`, or a one-element list containing `value` otherwise.
"""
def listify(value):
    if isinstance(value, Iterable) and not isinstance(value, str):
        return list(value)
    elif value is None:
        return []
    else:
        return [value]


"""
Call a function with the current continuation.

callcc (which should actually be call/cc or call-with-current-continuation)
is a function which accepts a function which calls a callback and returns
the thing which that function calls the callback with. Pretty much.

Source: http://sigusr2.net/2011/Aug/09/call-cc-for-python.html
"""
class ContinuationError(Exception):
    pass

def callcc(f):
    saved = [greenlet.getcurrent()]

    def cont(val):
        if saved[0] == None:
            raise ContinuationError("one shot continuation called twice")
        else:
            return saved[0].switch(val)

    def new_cr():
        v = f(cont)
        return cont(v)

    value_cr = greenlet.greenlet(new_cr)
    value = value_cr.switch()
    saved[0] = None
    return value

"""
Build a queue of unique elements.
"""
class SetQueue(set):
    def __init__(self, *args, **kwargs):
        super(SetQueue, self).__init__(self, *args, **kwargs)
        self._queue = deque()

    def __iter__(self):
        for item in self._queue:
            yield item

    def update(*args, **kwargs):
        return NotImplemented

    def copy(self):
        return NotImplemented

    def add(self, item):
        if item not in self:
            super(SetQueue, self).add(item)
            self._queue.append(item)

    def pop(self):
        item = self._queue.popleft()
        super(SetQueue, self).remove(item)
        return item

    def remove(self, item):
        super(SetQueue, self).remove(item)
        self._queue.remove(item)

    def clear(self):
        super(SetQueue, self).clear()
        self._queue.clear()
