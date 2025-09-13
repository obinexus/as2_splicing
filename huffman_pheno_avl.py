import heapq
from collections import defaultdict, namedtuple

# Your genetic framework components
GeneticNode = namedtuple('GeneticNode', ['genotype', 'phenotype', 'balance_factor'])
MF_Pair = namedtuple('MF_Pair', ['mother_genotype', 'father_genotype', 'child_phenotype'])

class LosslessGeneticAVL:
    def __init__(self):
        self.genotype_tree = {}  # AVL for genetic structure
        self.phenotype_map = {}   # Huffman-like encoding for traits
        self.mf_pairs = []        # Mother-Father relationships
        
    class HuffmanNode:
        def __init__(self, trait, frequency):
            self.trait = trait
            self.frequency = frequency
            self.left = None
            self.right = None
            self.code = ''
            
        def __lt__(self, other):
            return self.frequency < other.frequency

    def build_phenotype_encoder(self, trait_frequencies):
        # Build Huffman tree for phenotype encoding
        heap = [self.HuffmanNode(trait, freq) for trait, freq in trait_frequencies.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = self.HuffmanNode(None, left.frequency + right.frequency)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
            
        # Generate codes
        root = heap[0]
        codes = {}
        
        def generate_codes(node, current_code):
            if node is None:
                return
            if node.trait is not None:
                codes[node.trait] = current_code
                node.code = current_code
            generate_codes(node.left, current_code + '0')
            generate_codes(node.right, current_code + '1')
            
        generate_codes(root, '')
        return codes, root

    def add_mf_pair(self, mother_genotype, father_genotype, child_phenotype):
        # Store the MF pair relationship
        pair = MF_Pair(mother_genotype, father_genotype, child_phenotype)
        self.mf_pairs.append(pair)
        
        # Update genotype tree (simplified AVL structure)
        genetic_distance = self.calculate_genetic_distance(mother_genotype, father_genotype)
        node_id = f"MF_{len(self.mf_pairs)}"
        
        self.genotype_tree[node_id] = GeneticNode(
            genotype={'mother': mother_genotype, 'father': father_genotype},
            phenotype=child_phenotype,
            balance_factor=genetic_distance  # Using genetic distance as balance factor
        )
        
        return node_id

    def calculate_genetic_distance(self, genotype1, genotype2):
        # Simple Hamming distance for genetic comparison
        return sum(1 for a, b in zip(genotype1, genotype2) if a != b)

    def find_diamond_dependencies(self):
        # Detect diamond patterns in genetic relationships
        diamonds = []
        for i, pair1 in enumerate(self.mf_pairs):
            for j, pair2 in enumerate(self.mf_pairs[i+1:], i+1):
                # Check if pairs share genetic material that could create diamond
                if self.share_genetic_material(pair1, pair2):
                    diamonds.append((f"MF_{i+1}", f"MF_{j+1}"))
        return diamonds

    def share_genetic_material(self, pair1, pair2):
        # Check if two MF pairs share genetic similarities that could cause diamond dependency
        shared_genes = (set(pair1.mother_genotype) & set(pair2.mother_genotype) or
                       set(pair1.father_genotype) & set(pair2.father_genotype))
        return len(shared_genes) > 0

    def encode_phenotype(self, phenotype_traits, trait_frequencies):
        # Encode phenotype using Huffman-like encoding
        codes, tree = self.build_phenotype_encoder(trait_frequencies)
        encoded = ''.join(codes[trait] for trait in phenotype_traits)
        return encoded, codes

    def decode_phenotype(self, encoded_str, huffman_tree):
        # Decode phenotype without information loss
        decoded = []
        current_node = huffman_tree
        
        for bit in encoded_str:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
                
            if current_node.trait is not None:
                decoded.append(current_node.trait)
                current_node = huffman_tree
                
        return decoded

# Example usage with your genetic framework
genetic_avl = LosslessGeneticAVL()

# Add MF pairs (using simplified genetic representations)
genetic_avl.add_mf_pair("ATCG", "GCTA", ["neurodivergent_trait1", "baseline_cognition"])
genetic_avl.add_mf_pair("GCTA", "TAGC", ["enhanced_pattern_recognition", "baseline_cognition"])
genetic_avl.add_mf_pair("ATCG", "TAGC", ["neurodivergent_trait2", "creative_cognition"])

# Find diamond dependencies (your genetic conflict detection)
diamonds = genetic_avl.find_diamond_dependencies()
print("Diamond dependencies found:", diamonds)

# Encode/Decode phenotype information without loss
trait_frequencies = {
    "neurodivergent_trait1": 0.2,
    "neurodivergent_trait2": 0.3,
    "baseline_cognition": 0.4,
    "enhanced_pattern_recognition": 0.05,
    "creative_cognition": 0.05
}

phenotype = ["neurodivergent_trait1", "baseline_cognition", "creative_cognition"]
encoded, codes = genetic_avl.encode_phenotype(phenotype, trait_frequencies)
decoded = genetic_avl.decode_phenotype(encoded, genetic_avl.build_phenotype_encoder(trait_frequencies)[1])

print("Original phenotype:", phenotype)
print("Encoded:", encoded)
print("Decoded:", decoded)
print("Lossless:", phenotype == decoded)