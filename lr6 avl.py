class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1        # высота узла (лист = 1)

class AVLTree:
    def __init__(self):
        self.root = None

    #Вспомогательные методы
    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    #Повороты
    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        self._update_height(z)
        self._update_height(y)
        return y

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self._update_height(z)
        self._update_height(y)
        return y

    #Вставка
    def _insert(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        # Балансировка
        self._update_height(node)
        balance = self._balance_factor(node)

        # Левое поддерево перевешивает
        if balance > 1:
            if value < node.left.value:          # Левый-левый случай
                return self._right_rotate(node)
            else:                                # Левый-правый случай
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)

        # Правое поддерево перевешивает
        if balance < -1:
            if value > node.right.value:         # Правый-правый случай
                return self._left_rotate(node)
            else:                                # Правый-левый случай
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

        return node

    def insert(self, value):
        self.root = self._insert(self.root, value)

    #Удаление
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node, value):
        if not node:
            return node

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Узел найден
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)

        if not node:
            return node

        # Балансировка
        self._update_height(node)
        balance = self._balance_factor(node)

        # Левый перекос
        if balance > 1:
            if self._balance_factor(node.left) >= 0:   # Левый-левый
                return self._right_rotate(node)
            else:                                      # Левый-правый
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)

        # Правый перекос
        if balance < -1:
            if self._balance_factor(node.right) <= 0:  # Правый-правый
                return self._left_rotate(node)
            else:                                      # Правый-левый
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

        return node

    def delete(self, value):
        self.root = self._delete(self.root, value)

    #Вспомогательная печать
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)


avl = AVLTree()
for v in [10, 20, 30, 40, 50, 25]:
    avl.insert(v)
print("Inorder AVL:", avl.inorder())

avl.delete(30)
print("After delete 30:", avl.inorder())
