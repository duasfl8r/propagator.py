from collections import deque, Iterable

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
