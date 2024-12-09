import threading
import time

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.routing_table = {node_id: (0, None)}
        self.neighbors = {}
        self.lock = threading.Lock()

    def add_neighbor(self, neighbor_id, cost):
        with self.lock:
            self.neighbors[neighbor_id] = cost
            self.routing_table[neighbor_id] = (cost, neighbor_id)

    def update_routing_table(self, network):
        updated = False
        with self.lock:
            for neighbor_id in self.neighbors:
                neighbor = network.nodes[neighbor_id]
                for destination, (cost, next_hop) in neighbor.routing_table.items():
                    if destination == self.node_id:
                        continue
                    new_cost = self.neighbors[neighbor_id] + cost
                    if destination not in self.routing_table or new_cost < self.routing_table[destination][0]:
                        self.routing_table[destination] = (new_cost, neighbor_id)
                        updated = True
        return updated

    def print_routing_table(self):
        with self.lock:
            print(f"Node {self.node_id}:")
            for destination, (cost, next_hop) in sorted(self.routing_table.items()):
                next_hop_str = next_hop if next_hop else "None"
                print(f"  - Destination: {destination} (Cost: {cost}), Next Hop: {next_hop_str}")
            print()



class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id):
        self.nodes[node_id] = Node(node_id)

    def add_link(self, node_id1, node_id2, cost):
        self.nodes[node_id1].add_neighbor(node_id2, cost)
        self.nodes[node_id2].add_neighbor(node_id1, cost)

    def simulate_routing(self, max_iterations=10):
        def update_node(node):
            for _ in range(max_iterations):
                updated = node.update_routing_table(self)
                if not updated:
                    break
                time.sleep(0.1)

        threads = []
        for node in self.nodes.values():
            thread = threading.Thread(target=update_node, args=(node,))
            threads.append(thread)
            thread.start()

        for thread in threads: 
            thread.join()

    def print_routing_tables(self):
        for node in self.nodes.values():
            node.print_routing_table()


if __name__ == "__main__":
    network = Network()

    network.add_node('A')
    network.add_node('B')
    network.add_node('C')
    network.add_node('D')
    
    network.add_link('A', 'B', 1)
    network.add_link('A', 'C', 4)
    network.add_link('B', 'C', 2)
    network.add_link('B', 'D', 5)
    network.add_link('C', 'D', 1)

    network.simulate_routing()

    network.print_routing_tables()
