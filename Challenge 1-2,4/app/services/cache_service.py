import logging

logger = logging.getLogger(__name__)

class Node:
    """A Node in a Doubly Linked List."""
    def __init__(self, key: str, value: any):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation using a Hash Map and a Doubly Linked List.
    
    Why this data structure?
    -----------------------
    1. Hash Map (Dictionary): Provides O(1) average-time lookups to check if a key exists
       in the cache and to retrieve the corresponding node in the list.
    2. Doubly Linked List: Maintains the access order of elements. It allows for O(1)
       additions to the head (marking as Most Recently Used) and O(1) removals from the
       tail (evicting the Least Recently Used). It also allows O(1) removals from the
       middle if we have a direct reference to the node.
    
    LATENCY OPTIMIZATION:
    In production, model inference (YOLO + NLP) is the most time-consuming part of the
    request. Serving identical queries from the cache avoids expensive computations, 
    reducing latency from hundreds of milliseconds to under 1ms.
    """
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}  # Hash Map: key -> Node
        
        # Dummy head and tail nodes for the doubly linked list
        self.head = Node("head", None)
        self.tail = Node("tail", None)
        self.head.next = self.tail
        self.tail.prev = self.head
        
        logger.info(f"Initialized LRUCache with capacity {capacity}")

    def _remove(self, node: Node):
        """Removes a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node):
        """Adds a node to the front of the list (next to head)."""
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def get(self, key: str):
        """
        Retrieves an item from the cache. 
        Moves the accessed item to the head (Most Recently Used).
        Returns None if key is not present.
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return None

    def put(self, key: str, value: any):
        """
        Inserts or updates an item in the cache.
        Moves the item to the head. 
        If capacity is reached, evicts the Least Recently Used item (tail).
        """
        if key in self.cache:

            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add(node)
        else:

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
            
            if len(self.cache) > self.capacity:
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
                logger.debug(f"Evicted LRU item: {lru_node.key}")
