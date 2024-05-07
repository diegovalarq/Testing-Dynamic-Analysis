class Node:
    def __init__(self, method_name):
        self.method_name = method_name
        self.parent = None
        self.childs = []
        self.count = 0

    def add_child(self, child):
        child.parent = self
        self.childs.append(child)

    def update_count(self):
        self.count += 1

    def is_method_child(self, method_name):
        for child in self.childs:
            if child.method_name == method_name:
                return True
        return False
    
    def get_child_of_method(self, method_name):
        for child in self.childs:
            if child.method_name == method_name:
                return child
        return None

    def __str__(self):
        return self.data