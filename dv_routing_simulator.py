graph = {
    'A': {'B': 1, 'C': 5},
    'B': {'A': 1, 'C': 2, 'D': 4},
    'C': {'A': 5, 'B': 2, 'D': 1},
    'D': {'B': 4, 'C': 1}
}

routing_table = {
    'A': {
        'A': (0, None),
        'B': (1, 'B'),
        'C': (5, 'C'),
        'D': (float('inf'), None)},
    'B': {
        'A': (1, 'A'),
        'B': (0, None),
        'C': (2, 'C'),
        'D': (4, 'D')},
    'C': {
        'A': (5, 'A'),
        'B': (2, 'B'),
        'C': (0, None),
        'D': (1, 'D')},
    'D': {
        'A': (float('inf'), None),
        'B': (4, 'B'),
        'C': (1, 'C'),
        'D': (0, None)}
}

def update_routing_table(node, neighbors, routing_table):
    updated = False
    for neighbor, cost in neighbors.items():
        for dest, (neighbor_cost, next_hop) in routing_table[neighbor].items():
            new_cost = cost + neighbor_cost
            if dest not in routing_table[node] or new_cost < routing_table[node][dest][0]:
                routing_table[node][dest] = (new_cost, neighbor)
                updated = True
    return updated

def simulate_routing(graph):
    routing_table = {node: {n: (cost, n) for n, cost in neighbors.items()} for node, neighbors in graph.items()}
    for node in graph:
        for dest in graph:
            if dest not in routing_table[node]:
                routing_table[node][dest] = (float('inf'), None)

    converged = False
    while not converged:
        converged = True
        for node, neighbors in graph.items():
            if update_routing_table(node, neighbors, routing_table):
                converged = False

    return routing_table

def print_routing_tables(routing_table):
    for node, table in routing_table.items():
        print(f"Routing table from {node}:")
        for dest, (cost, next_hop) in table.items():
            print(f"  To {dest}: Cost = {cost}, Next = {next_hop}")


if __name__ == "__main__":
    print_routing_tables(routing_table)
