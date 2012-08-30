from collections import deque

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
