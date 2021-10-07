import heapq
import itertools

class BPQLRU:
    """Bounded priority queue implementation."""

    def __init__(self, capacity):
        self._pq = []
        self._entry_finder = {}
        self._REMOVED = "<removed-item>"
        self._counter = itertools.count()
        self._capacity = capacity
        self._cached = 0
    
    def put(self, key, value):
        if key in self._entry_finder:
            self._cached -= len(self._entry_finder[key])
            self.remove(key)
        
        if (self._cached + len(value)) > self._capacity:
            evicted_value = self.pop()
            self._cached -= len(evicted_value)

        count = next(self._counter)
        entry = [count, (key, value)]
        self._entry_finder[key] = entry
        heapq.heappush(self._pq, entry)
        self._cached += len(value)

    def pop(self):
        while self._pq:
            _, item = heapq.heappop(self._pq)
            if item is not self._REMOVED:
                del self._entry_finder[item[0]]
                return item[1]

    def remove(self, key):
        entry = self._entry_finder.pop(key)
        entry[-1] = self._REMOVED
    
    def get(self, key):
        if key in self._entry_finder:
            self.put(key, self._entry_finder[key][1][1]) # update item on the heap with new priority
            return self._entry_finder[key][1]
        return (None, None)
