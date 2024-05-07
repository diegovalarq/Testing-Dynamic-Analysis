from node import Node

class CallContextTree:

    def __init__(self):
        self.root = None

    def update_tree(self, stack):
        current_node = self.root
        for method_name in stack:
            if current_node is None:
                new_node = Node(method_name)
                self.root = new_node
                current_node = new_node
                continue
            if method_name == current_node.method_name:
                current_node.update_count()
                continue
            if current_node.is_method_child(method_name):
                current_node = current_node.get_child_of_method(method_name)
                current_node.update_count()
                continue
            new_node = Node(method_name)
            new_node.update_count()
            current_node.add_child(new_node)
            current_node = new_node

    def print_tree_DFS(self): #fuente: claude.ai
        def dfs(node, indent=0):
            if node is None:
                return

            print("  " * indent + f"{node.method_name} ({node.count} seconds)")

            for child in node.childs:
                dfs(child, indent + 1)

        dfs(self.root, 0)



