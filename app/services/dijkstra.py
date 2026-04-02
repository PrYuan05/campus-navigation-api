import heapq

# Define the graph representing the campus map
# Each key is a location, and its value is a dictionary of neighboring locations and the time.
def find_shortest_path(graph: dict, start: str, end: str):
    shortest_times = {node: float('inf') for node in graph}
    shortest_times[start] = 0
    previous_nodes = {}
    queue = [(0, start)]
    
    while queue:
        current_time, current_node = heapq.heappop(queue)
        if current_node == end:
            break
            
        # if current_node is not in graph, it means it's an isolated node with no outgoing edges, we can skip it
        if current_node not in graph:
            continue
            
        for neighbor, time_to_neighbor in graph[current_node].items():
            time = current_time + time_to_neighbor
            if time < shortest_times[neighbor]:
                shortest_times[neighbor] = time
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (time, neighbor))
                
    path = []
    current = end
    while current in previous_nodes:
        path.insert(0, current)
        current = previous_nodes[current]
    if path:
        path.insert(0, start)
        
    # if no path is found (e.g., the graph is not connected), return an empty list
    if len(path) == 1 and path[0] != start:
        return [], 0
        
    return path, shortest_times[end]