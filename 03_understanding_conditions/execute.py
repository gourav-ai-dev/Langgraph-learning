
def execute_branching(graph):
    graph_obj = graph.get_graph()
    with open("graph.dot", "w") as f:
         f.write("digraph G {\n")
         
         # Add nodes
         for node_id in graph_obj.nodes:
             f.write(f'  "{node_id}";\n')
         
         # Add edges
         for edge in graph_obj.edges:
             label = f' [label="{edge.data}"]' if edge.data else ""
             f.write(f'  "{edge.source}" -> "{edge.target}"{label};\n')

         f.write("}")
         