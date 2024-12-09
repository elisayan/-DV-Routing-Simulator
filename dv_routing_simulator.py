class Node:
    def __init__(self, node_id):
        # Initialize a node with its ID and an empty routing table
        self.node_id = node_id
        self.routing_table = {node_id: (0, None)}
        self.neighbors = {}

    def add_neighbor(self, neighbor_id, cost):    
        # Add a neighbor to this node with the associated cost
        self.neighbors[neighbor_id] = cost
        self.routing_table[neighbor_id] = (cost, neighbor_id)
        
    def initialize_routing_table(self, all_node_ids):
        for node_id in all_node_ids:
            if node_id != self.node_id:
                self.routing_table[node_id] = (float('inf'), None)

    def update_routing_table(self, network):
        # Update the routing table based on neighbors' information
        updated = False
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
        print(f"Routing table for Node {self.node_id}:")
        for destination, (cost, next_hop) in sorted(self.routing_table.items()):
            next_hop_str = next_hop if next_hop else "None"
            print(f"  {self.node_id} --> {destination} (Cost: {cost}, Next Hop: {next_hop_str})")
        print()


class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id):
        self.nodes[node_id] = Node(node_id)

    def add_link(self, node_id1, node_id2, cost):
        # Create a bidirectional link between two nodes with a specified cost
        self.nodes[node_id1].add_neighbor(node_id2, cost)
        self.nodes[node_id2].add_neighbor(node_id1, cost)

    def simulate_routing(self, max_iterations=10):
        # Simulate the routing process for a set number of iterations
        for iteration in range(max_iterations):
            print(f"\n --- Iteration {iteration + 1} ---")
            updated_any = False
            
            for node in self.nodes.values():
                updated = node.update_routing_table(self)
                if updated:
                    updated_any = True
                    print(f"[{node.node_id}] updated paths:")
                    for destination, (cost, next_hop) in sorted(node.routing_table.items()):
                        if destination != node.node_id:
                            print(f"  {node.node_id} --> {destination} (Cost: {cost}, Next Hop: {next_hop})")
                    print()

            self.print_routing_tables()

            if not updated_any:
                break

    def print_routing_tables(self):
        for node in self.nodes.values():
            node.print_routing_table()


if __name__ == "__main__":
    network = Network()

    network.add_node('A')
    network.add_node('B')
    network.add_node('C')
    network.add_node('D')
    
    all_node_ids = list(network.nodes.keys())
    for node in network.nodes.values():
        node.initialize_routing_table(all_node_ids)
        
    print("Initial Routing Tables:")
    network.print_routing_tables()
        
    print("Adding links and updating routing tables:")
    
    network.add_link('A', 'B', 3)
    print("Connected A <-> B:")
    network.print_routing_tables()
    
    network.add_link('A', 'C', 1)
    print("Connected A <-> C:")
    network.print_routing_tables()
    
    network.add_link('B', 'C', 2)
    print("Connected B <-> C:")
    network.print_routing_tables()
    
    network.add_link('B', 'D', 4)
    print("Connected B <-> D:")
    network.print_routing_tables()
    
    network.add_link('C', 'D', 5)
    print("Connected C <-> D:")
    network.print_routing_tables()

    network.simulate_routing()
