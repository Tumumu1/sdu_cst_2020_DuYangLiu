import random
from hashlib import sha256

#定义节点
class Node:
    def __init__(self, left_node, hash, right_node):
        self.left = left_node
        self.hash = hash
        self.right = right_node

#定义merkle tree
class MerkleTree:
    # 选用SHA256
    def hash(input):
        return sha256(str(input).encode('utf-8')).hexdigest()

    #生成整个树
    def generate_tree(datablocks):
        child_nodes = []
        for datablock in datablocks:
            child_nodes.append(Node(None, MerkleTree.hash(datablock), None))
        return MerkleTree.build_tree(child_nodes)

    def build_tree(child_nodes):
        parents = []
        while len(child_nodes) != 1:
            index = 0
            length = len(child_nodes)
            while index < length:
                left_child = child_nodes[index]
                if (index + 1) < length:
                    right_child = child_nodes[index + 1]
                else:
                    right_child = Node(None, left_child.hash, None)
                parent_hash = MerkleTree.hash(left_child.hash + right_child.hash)
                parents.append(Node(left_child, parent_hash, right_child))
                index += 2
            child_nodes = parents
            parents = []
        return child_nodes[0]

    #打印树
    def print_tree(root):
        if not root:
            return
        if not root.left and not root.right:
            print(root.hash)
            return
        temp = [root, None]
        while len(temp) > 0:
            node = None
            try:
                node = temp.pop(0)
            except:
                pass
            if node:
                print(node.hash)
            else:
                print('')
                if len(temp) > 0:
                    temp.append(None)
            if node and node.left:
                temp.append(node.left)
            if node and node.right:
                temp.append(node.right)

#生成一个包含n个叶子节点的merkle tree, 返回根节点
def create_random_tree(n):
    lis=[]
    for i in range(n):
        x=random.randint(0,100)
        lis.append(x)
    for a in enumerate(lis):
        root = MerkleTree.generate_tree(a)
        MerkleTree.print_tree(root1)
    return root



if __name__ == '__main__':
    root1 = create_random_tree(100000)

