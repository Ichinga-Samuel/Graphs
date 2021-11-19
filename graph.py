from collections import defaultdict, deque


class Graph:
    def __init__(self, graph=None, grid=None, edges=None, style='directed'):
        """
        Initialize graph with suitable arguments for you use case
        :param graph: An Adjacency List
        :param grid:  A 2-d grid for grid problems
        :param edges: An array of edges that make up the graph
        :param style: Either directed or undirected
        """
        self.graph = defaultdict(list) if graph is None else graph
        self.nodes = [] if graph is None else list(graph.keys())
        self.visited = set()   # a set to keep track of visited nodes
        self.queue = deque()   # queue for breadth first search
        self.stack = []        # stack for depth first search
        self.components = []    # an array to keep track of separate components
        if grid is not None:
            self.grid = grid
            self.rows, self.cols = len(grid), len(grid[0])
        if edges is not None:
            if style == 'directed':
                self.build_directed(edges)
            if style == 'undirected':
                self.build_undirected(edges)

    def build_directed(self, edges):
        """
        Create an adjacency list given an array of edges
        :param edges:
        :return:
        """
        for edge in edges:
            a, b = edge
            self.graph[a].append(b)
            self.graph[b]  # Important! without this a node that is not leading to any other node will not be included in the adjacency diagram
        self.nodes = list(self.graph.keys())

    def build_undirected(self, edges):
        """
        Create an adjacency list for an undirected graph given array of edges
        :param edges: an array of edges
        :return:
        """
        for edge in edges:
            a, b = edge
            self.graph[a].append(b)
            self.graph[b].append(a)
        self.nodes = list(self.graph.keys())    # the graph keys are the nodes of the graph

    def depth_first_iterative(self, start):
        """
        An iterative implementation of depth first search
        :param start:
        :return:
        """
        self.stack.append(start)
        while self.stack:
            node = self.stack.pop()
            if node not in self.visited:
                print(node)
                self.visited.add(node)
                self.stack.extend(self.graph[node])
        self.components += 1

    def depth_first_recursive(self, start):
        """
        Recursive implementation of depth first traversal
        :param start:
        :return:
        """
        if start in self.visited:
            return
        print(start)
        self.visited.add(start)
        nodes = self.graph[start]
        for node in nodes:
            self.depth_first_recursive(node)

    def breadth_first(self, start):
        self.queue.append(start)
        while self.queue:
            node = self.queue.popleft()
            if node not in self.visited:
                print(node)
                self.visited.add(node)
                self.queue.extend(self.graph[node])

    def has_path_depth_first(self, src, dst):
        if src == dst:
            return True
        if src in self.visited:
            return False
        self.visited.add(src)
        nodes = self.graph[src]
        for node in nodes:
            if self.has_path_depth_first(node, dst):
                return True
        return False

    def has_path_breadth_first(self, src, dst):
        self.queue.append(src)
        while self.queue:
            node = self.queue.popleft()
            if node == dst:
                return True
            if node not in self.visited:
                self.visited.add(node)
                self.queue.extend(self.graph[node])
        return False

    def explore(self, start):
        """
         explore a grid and find connected group of nodes
        :param start:
        :return:
        """
        c = set()
        if start in self.visited:
            return c
        self.visited.add(start)
        c.add(start)
        nodes = self.graph[start]
        for node in nodes:
            b = self.explore(node)
            c = c.union(b)
        return c

    def connected_components_count(self):
        self.get_components()
        return len(self.components)

    def get_components(self):
        for node in self.nodes:
            component = self.explore(node)
            if component:
                self.components.append(component)

    def largest_component(self):
        self.get_components()
        return max(self.components, key=lambda i: len(i))

    def shortest_path(self, start, end):
        self.queue.append([start, 0])
        self.visited.add(start)
        while self.queue:
            node, distance = self.queue.popleft()
            print(node, distance)
            if node == end:
                return distance
            nodes = self.graph[node]
            print(nodes)
            [(self.visited.add(n), self.queue.append([n, distance + 1])) for n in nodes if n not in self.visited]
        return -1

    def get_islands(self, check='w'):
        """
        Get component islands in a grid
        :param check: condition to check. eg 'w' in the typical island problem
        :return:
        """
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == check: continue
                island = self.traverse_grid(i, j, check=check)
                if island:
                    self.components.append(island)

    def number_of_islands(self):
        self.get_islands()
        return len(self.components)

    def minimum_island(self):
        self.get_islands()
        return min(self.components, key=lambda i: len(i))

    def traverse_grid(self, i, j, check="w"):
        if not ((0 <= i < self.rows) and (0 <= j < self.cols)):
            return set()
        if self.grid[i][j] == check: return set()
        node = f"{i},{j}"
        island = set()
        if node in self.visited:
            return set()
        self.visited.add(node)
        island.add(node)
        left = self.traverse_grid(i - 1, j)
        right = self.traverse_grid(i + 1, j)
        down = self.traverse_grid(i, j - 1)
        up = self.traverse_grid(i, j + 1)
        island = {*island, *left, *right, *down, *up}
        return island


edges = [
    ['a', 'b'],
    ['a', 'c'],
    ['b', 'd'],
    ['c', 'e'],
    ['d', 'f']
]
edges1 = [
    ['f', 'i'],
    ['f', 'g'],
    ['g', 'h'],
    ['i', 'g'],
    ['i', 'k'],
    ['j', 'i']
]

edges3 = [
    ['i', 'j'],
    ['k', 'i'],
    ['m', 'k'],
    ['k', 'l'],
    ['o', 'n']
]

graph = {
    0: [8, 1, 5],
    1: [0],
    5: [0, 8],
    8: [0, 5],
    2: [3, 4],
    3: [2, 4],
    4: [3, 2]
}

edges5 = [
    ['w', 'x'],
    ['x', 'y'],
    ['z', 'y'],
    ['z', 'v'],
    ['w', 'v']
]

grid = [
    ['w', 'l', 'w', 'w', 'w'],
    ['w', 'l', 'w', 'w', 'w'],
    ['w', 'w', 'w', 'l', 'w'],
    ['w', 'w', 'l', 'l', 'w'],
    ['l', 'w', 'w', 'l', 'l'],
    ['l', 'l', 'w', 'w', 'w']
]
g = Graph(grid=grid)
b = g.minimum_island()
print(b)
