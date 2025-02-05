
    class Node:
       def __init__(self, key):
       
        self.key = key  
        self.left = None  
        self.right = None  
        
    class BST:
    def __init__(self):
        
        self.root = None 

    def insert(self, key):
    
    self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, root, key):
    
    if root is None:  
        return Node(key)
    
    if key < root.key:  
        root.left = self._insert_recursive(root.left, key)
    else:  
        root.right = self._insert_recursive(root.right, key)
    
    return root  

    def delete(self, key):
    
    self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key):
    
    if root is None:
        return root
    if key < root.key:
        root.left = self._delete_recursive(root.left, key)
    elif key > root.key:
        root.right = self._delete_recursive(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        
        min_larger_node = self._min_value_node(root.right)
        root.key = min_larger_node.key  
        root.right = self._delete_recursive(root.right, min_larger_node.key)  
    return root  


    def _min_value_node(self, root):
   
    current = root
    while current.left is not None:
        current = current.left
    return current


    def inorder_traversal(self):
    
    self._inorder_recursive(self.root)
    print()  

    def _inorder_recursive(self, root):
   
    if root:
        self._inorder_recursive(root.left)  
        print(root.key, end=" ")  
        self._inorder_recursive(root.right)  
