class RBNode:
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color        # 'red' или 'black'
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

class RedBlackTree:
    def __init__(self):
        self.root = None

    #Поиск
    def search(self, value):
        curr = self.root
        while curr:
            if value == curr.value:
                return curr
            elif value < curr.value:
                curr = curr.left
            else:
                curr = curr.right
        return None

    #Повороты (с обновлением родителей)
    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    #Вставка
    def insert(self, value):
        new_node = RBNode(value)          # новый узел всегда красный
        if self.root is None:
            self.root = new_node
            self.root.color = 'black'
            return

        # 1. Обычная вставка в BST
        curr = self.root
        while True:
            if value < curr.value:
                if curr.left is None:
                    curr.left = new_node
                    new_node.parent = curr
                    break
                else:
                    curr = curr.left
            else:
                if curr.right is None:
                    curr.right = new_node
                    new_node.parent = curr
                    break
                else:
                    curr = curr.right

        # 2. Восстановление свойств красно-чёрного дерева
        self._insert_fix(new_node)

    def _insert_fix(self, node):
        while node.parent and node.parent.color == 'red':
            if node.parent == node.grandparent().left:
                uncle = node.uncle()
                if uncle and uncle.color == 'red':
                    # Случай 1: дядя красный → перекрашивание
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.grandparent().color = 'red'
                    node = node.grandparent()
                else:
                    if node == node.parent.right:
                        # Случай 2: узел — правый ребёнок → малый левый поворот
                        node = node.parent
                        self._rotate_left(node)
                    # Случай 3: узел — левый ребёнок → большой правый поворот
                    node.parent.color = 'black'
                    node.grandparent().color = 'red'
                    self._rotate_right(node.grandparent())
            else:
                uncle = node.uncle()
                if uncle and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.grandparent().color = 'red'
                    node = node.grandparent()
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = 'black'
                    node.grandparent().color = 'red'
                    self._rotate_left(node.grandparent())
        self.root.color = 'black'

    #Вспомогательные методы для удаления
    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node:
            new_node.parent = old_node.parent

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def _delete_fix(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self._rotate_left(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and \
                   (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.right is None or sibling.right.color == 'black':
                        if sibling.left:
                            sibling.left.color = 'black'
                        sibling.color = 'red'
                        self._rotate_right(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.right:
                        sibling.right.color = 'black'
                    self._rotate_left(x.parent)
                    x = self.root
            else:   # зеркально (x — правый ребёнок)
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self._rotate_right(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and \
                   (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.left is None or sibling.left.color == 'black':
                        if sibling.right:
                            sibling.right.color = 'black'
                        sibling.color = 'red'
                        self._rotate_left(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.left:
                        sibling.left.color = 'black'
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = 'black'

    #Удаление
    def delete(self, value):
        node_to_remove = self.search(value)
        if node_to_remove is None:
            return

        if node_to_remove.left is None or node_to_remove.right is None:
            # У узла не более одного ребёнка
            child = node_to_remove.left or node_to_remove.right
            self._replace_node(node_to_remove, child)
            if node_to_remove.color == 'black' and child:
                self._delete_fix(child)
        else:
            # Узел имеет двух детей → ищем преемника
            successor = self._find_min(node_to_remove.right)
            node_to_remove.value = successor.value
            self.delete(successor.value)   # удаляем преемника рекурсивно

    #Обход для проверки
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

rbt = RedBlackTree()
for v in [10, 20, 30, 40, 50, 25]:
    rbt.insert(v)
print("Inorder RBT:", rbt.inorder())

rbt.delete(30)
print("After delete 30:", rbt.inorder())
