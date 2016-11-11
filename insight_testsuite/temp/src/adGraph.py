from __future__ import division
from collections import deque

# Each payer is represented as a vertex
class Vertex:

    # The payer is initialed with:
    #   id - given id
    #   distance - distance to the node as infinity
    #   visited - states as follows
    #       0 - unvisited
    #       1 - visited from source direction
    #       2 - visited from target direction
    #   adjacent - an empty adjacency set of vertex identifiers
    #   out_pay - number of outgoing payments
    #   in_pay - number of incoming payments

    def __init__(self, identifier):
        self.id = identifier
        self.distance = float('inf')
        self.visited = 0
        self.adjacent = set()
        self.out_pay = 0
        self.in_pay = 0

    # returns ratio of outgoing to incoming payments
    def get_in_out(self):
        if self.out_pay:
            return self.in_pay / self.out_pay
        else:
            return 0

    # increment count of incoming payments
    def inc_in(self):
        self.in_pay += 1

    # increment count of outgoing payments
    def inc_out(self):
        self.out_pay +=1

    # return distance from source/target
    def get_distance(self):
        return self.distance

    # set calculated distance from source/target
    def set_distance(self, newDist):
        self.distance = newDist

    # return visited state
    def get_visited(self):
        return self.visited

    # set visited state
    def set_visited(self, visited_type):
        self.visited = visited_type

    # provide a printable version of the vertex
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x for x in self.adjacent])

    # add neighbor vertex to adjacent set
    def add_neighbor(self, neighbor_id):
        self.adjacent.add(neighbor_id)

    # remove neighbor vertex from adjacent set
    def del_neighbor(self, neighbor_id):
        self.adjacent.remove(neighbor_id)

    # return adjacency set
    def get_adjacent(self):
        return self.adjacent

    # return vertex id
    def get_id(self):
        return self.id

# The graph is represented by a dictionary of vertices
class Graph:

    # the graph is initialized with:
    #   vert_dict - a vertex dictionary
    #   edge_queue - a queue to keep track of oldest edges (for deletion)
    def __init__(self):
        self.vert_dict = {}
        self.edge_queue = deque()

    def __iter__(self):
        return iter(self.vert_dict.values())

    # provide a printable version of the graph, printing each vertex on a separate line
    def __str__(self):
        full=''
        for v in self:
            full+=" \n"+str(v)
        return full

    # add a vertex if it is not contained in the vertex dictionary
    def add_vertex(self, identifier):
        if identifier not in self.vert_dict:
            new_vertex = Vertex(identifier)
            self.vert_dict[identifier] = new_vertex

    # delete a vertex from vertex dictionary
    def del_vertex(self, identifier):
        if identifier in self.vert_dict:
            del self.vert_dict[identifier]

    # get vertex if cotained in dictionary
    def get_vertex(self, identifier):
        if identifier in self.vert_dict:
            return self.vert_dict[identifier]
        else:
            return None

    def add_edge(self, frm, to):
        # add edge by adding vertices (will not add if already contained)
        self.add_vertex(frm)
        self.add_vertex(to)
        # the vertices need to also be added to the adjacency sets of each vertex

        # add to edge queue and adjacency lists if not already contained
        if (frm not in self.get_vertex(to).get_adjacent()) and (to not in self.get_vertex(frm).get_adjacent()):
            self.edge_queue.append((frm, to))
            self.get_vertex(to).add_neighbor(frm)
            self.get_vertex(frm).add_neighbor(to)
        # increment transaction direction counters
        self.vert_dict[to].inc_in()
        self.vert_dict[frm].inc_out()

    def del_edge(self):
        # retrieve the identifiers for the oldest edge (FIFO queue)
        frm, to = self.edge_queue.popleft()
        # delete the vertices from respective adjacency sets
        self.get_vertex(frm).del_neighbor(to)
        self.get_vertex(to).del_neighbor(frm)
        # if there are no members remaining in adjacency sets delete vertices
        if len(self.vert_dict[frm].get_adjacent()) == 0:
            self.del_vertex(frm)
        if len(self.vert_dict[to].get_adjacent()) == 0:
            self.del_vertex(to)

    # return vertices as a list of identifiers
    def get_vertices(self):
        return self.vert_dict.keys()

    # implements a traditional breadth first search as a check on the bidirectional version
    def breadth_first_search(self, frm, to):
        vertices = self.get_vertices()
        for key in vertices:
            node = self.get_vertex(key)
            node.set_distance(float('inf'))
        q = deque()

        source = self.get_vertex(frm)
        target = self.get_vertex(to)

        # source and target must exist in graph
        if source and target:
            source.set_distance(0)

            q.append(source)
            while q:
                current = q.popleft()
                connections = current.get_adjacent()
                if connections:
                    for neighbor_identifier in connections:
                        vertex = self.get_vertex(neighbor_identifier)
                        node_distance = vertex.get_distance()
                        if node_distance == float('inf'):
                            vertex.set_distance(current.get_distance() + 1)
                            q.append(vertex)
            return self.get_vertex(to).get_distance()
        else:
            return float('inf')

    # algorithm for bidirectional breadth first search described in documentation
    def bidirectional_breadth_first_search(self, frm, to):
        vertices = self.get_vertices()
        for key in vertices:
            node = self.get_vertex(key)
            node.set_distance(float('inf'))
            node.set_visited(0)

        qF = deque()
        qB = deque()

        source = self.get_vertex(frm)
        target = self.get_vertex(to)

        # source and target must exist in graph
        if source and target:

            source.set_distance(0)
            target.set_distance(0)
            source.set_visited(1)
            target.set_visited(2)

            qF.append(source)
            qB.append(target)

            depth_f = 0
            depth_b = 0
            min_dist = float('inf')

            while qF and qB:
                if len(qF) < len(qB):
                    currentF = qF.popleft()
                    connectionsF = currentF.get_adjacent()
                    new_branch_dist = currentF.get_distance()+1
                    if new_branch_dist > depth_f:
                        if min_dist < float('inf'):
                            return min_dist
                        else:
                            depth_f = new_branch_dist
                    if connectionsF:
                        for neighbor_identifier in connectionsF:
                            vertex = self.get_vertex(neighbor_identifier)
                            node_visited = vertex.get_visited()
                            if node_visited == 0:
                                vertex.set_distance(new_branch_dist)
                                vertex.set_visited(1)
                                qF.append(vertex)
                            else:
                                if node_visited == 2:
                                    new_dist = new_branch_dist+vertex.get_distance()
                                    if new_dist < min_dist:
                                        min_dist = new_dist
                else:
                    currentB = qB.popleft()
                    connectionsB = currentB.get_adjacent()
                    new_branch_dist = currentB.get_distance()+1
                    if new_branch_dist > depth_b:
                        if min_dist < float('inf'):
                            return min_dist
                        else:
                            depth_b = new_branch_dist
                    if connectionsB:
                        for neighbor_identifier in connectionsB:
                            vertex = self.get_vertex(neighbor_identifier)
                            node_visited = vertex.get_visited()
                            if node_visited == 0:
                                vertex.set_distance(new_branch_dist)
                                vertex.set_visited(2)
                                qB.append(vertex)
                            else:
                                if node_visited == 1:
                                    new_dist = new_branch_dist+vertex.get_distance()
                                    if new_dist < min_dist:
                                        min_dist = new_dist
            return min_dist
        else:
            return float('inf')

if __name__ == '__main__':

    # Check that basic four-way graph can be created

    # a - b
    # | x |
    # c - d

    g = Graph()
    g.add_edge('a', 'b')
    g.add_edge('a', 'c')
    g.add_edge('a', 'd')
    g.add_edge('b', 'c')
    g.add_edge('b', 'd')
    g.add_edge('c', 'd')
    print(g)

    for key in sorted(g.get_vertices()):
        print(key, ': ', g.get_vertex(key).get_in_out())
    # a:  0.0
    # b:  0.5
    # c:  2.0
    # d:  0

    # Check that proper shortest path distances are correct for tough case

    #   b - c - d
    #  /         \
    # a           f
    #  \         /
    #   --- e ---
    f = Graph()
    f.add_edge('a', 'b')
    f.add_edge('a', 'e')
    f.add_edge('b', 'c')
    f.add_edge('c', 'd')
    f.add_edge('d', 'f')
    f.add_edge('e', 'f')
    print(f)
    print('Expecting distance of 2 (basic BFS): ', f.breadth_first_search('a', 'f'))
    print('Expecting distance of 2 (bidirectional): ', f.bidirectional_breadth_first_search('a','f'))
    # delete first edge added
    f.del_edge()
    print(f)
    print('Expecting distance of 5 (basic BFS): ', f.breadth_first_search('a', 'b'))
    print('Expecting distance of 5 (bidirectional): ', f.bidirectional_breadth_first_search('a', 'b'))


