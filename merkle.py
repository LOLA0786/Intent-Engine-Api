import hashlib

def hash_leaf(data: bytes) -> bytes:
    return hashlib.sha256(b'\x00' + data).digest()

def hash_node(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b'\x01' + left + right).digest()

def merkle_root(leaves: list[bytes]) -> bytes:
    nodes = [hash_leaf(l) for l in leaves]
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        nodes = [hash_node(nodes[i], nodes[i+1]) for i in range(0, len(nodes), 2)]
    return nodes[0]
