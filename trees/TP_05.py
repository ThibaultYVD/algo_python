import heapq
from collections import Counter, namedtuple

class Node:
    def __init__(self, character, frequency, left=None, right=None):
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [Node(c, f) for c, f in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(None, left.frequency + right.frequency, left, right)
        heapq.heappush(heap, parent)
    
    return heap[0]

def generate_huffman_codes(tree, prefix="", huffman_codes={}):
    if tree is not None:
        if tree.character is not None:
            huffman_codes[tree.character] = prefix
        generate_huffman_codes(tree.left, prefix + "0", huffman_codes)
        generate_huffman_codes(tree.right, prefix + "1", huffman_codes)
    return huffman_codes

def compress(text):
    tree = build_huffman_tree(text)
    huffman_codes = generate_huffman_codes(tree)
    binary_code = "".join(huffman_codes[character] for character in text)
    return binary_code, huffman_codes, tree

def decompress(binary_code, tree):
    decompressed_text = ""
    current_node = tree
    for bit in binary_code:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.character is not None:
            decompressed_text += current_node.character
            current_node = tree
    return decompressed_text

if __name__ == "__main__":
    text = "huffman coding is fun"
    binary_code, dictionary, tree = compress(text)
    original_text = decompress(binary_code, tree)
    assert original_text == text
    print("Compression and decompression successful!")