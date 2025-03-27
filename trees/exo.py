array = [10,20,30,40,50,60,70]

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

root10 = TreeNode(array[0])
node20 = TreeNode(array[1])
node30 = TreeNode(array[2])
node40 = TreeNode(array[3])
node50 = TreeNode(array[4])
node60 = TreeNode(array[5])
node70 = TreeNode(array[6])

root10.left = node20
root10.right = node30

node20.left = node40
node20.right = node50

node30.left = node60
node30.right = node70

def getLeft(index):
    return 2*index+1

def getRight(index):
    return 2*index+2

def getParent(index):
    return (index-1)//2

def getData(index):
    if 0 <= index < len(array):
        return array[index]
    return None

left = getLeft(5)
data = getData(left)
print(data)