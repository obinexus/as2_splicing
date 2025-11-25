import time
import random
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional

# --- 1. THE RIFT PROTOCOL (Constants & Types) ---
# "Mic, Umbrella, Kilo, Oscar" - Naming conventions based on your transcript.
# This represents the "Sparse" nature of the model.

class BioThreatLevel(Enum):
    SAFE = "SAFE"
    MONITORED = "MONITORED"
    CRITICAL = "CRITICAL (MRSA-LIKE)"
    PANDEMIC = "PANDEMIC"

@dataclass
class GeneNode:
    """
    Represents a single node in the Sparse Graph.
    This could be a nucleotide sequence, a protein structure, or a trait.
    """
    id: str
    name: str
    resistance_factor: float  # 0.0 to 1.0
    dependencies: List[str] = field(default_factory=list) # IDs of genes required before this one can activate
    
    def __hash__(self):
        return hash(self.id)

# --- 2. THE SPARSE DAG (Directed Acyclic Graph) ---
# "Dependency Resolution" - The core logic.
# The virus cannot evolve a trait unless it has 'resolved' the dependencies.

class GenomicDependencyGraph:
    def __init__(self):
        self.nodes: Dict[str, GeneNode] = {}
        self.active_strains: Dict[str, Set[str]] = {} # Strain ID -> Set of Acquired Gene IDs

    def add_gene(self, gene: GeneNode):
        """Adds a 'package' (gene) to the repository."""
        self.nodes[gene.id] = gene

    def resolve_dependencies(self, strain_genome: Set[str], target_gene_id: str) -> bool:
        """
        The 'Resolver'. Checks if a strain has the prerequisites to evolve 'target_gene_id'.
        This mimics 'pip install' but for viral evolution.
        """
        if target_gene_id not in self.nodes:
            return False
        
        target = self.nodes[target_gene_id]
        
        # Check if all dependencies are currently present in the strain's genome
        for dep_id in target.dependencies:
            if dep_id not in strain_genome:
                return False # Dependency missing, cannot evolve this trait yet
        
        return True

# --- 3. ACTIVE GOVERNANCE (The Observer) ---
# "Who governs the governor?" - This class acts as the immutable observer.
# It watches the graph for "illegal" or "dangerous" state changes.

class ActiveGovernor:
    def __init__(self, threshold: float):
        self.alert_threshold = threshold
        self.logs: List[str] = []

    def observe(self, strain_id: str, resistance_score: float, mutations: List[str]):
        """
        The Active Observer loop.
        It does not interfere, it calculates state and flags entropy.
        """
        timestamp = time.strftime("%H:%M:%S")
        status = BioThreatLevel.SAFE

        if resistance_score > 0.8:
            status = BioThreatLevel.CRITICAL
        elif resistance_score > 0.4:
            status = BioThreatLevel.MONITORED

        log_entry = f"[{timestamp}] GOVERNANCE_LOG: Strain {strain_id} | Res: {resistance_score:.2f} | Status: {status.value}"
        self.logs.append(log_entry)
        
        print(log_entry)
        
        if status == BioThreatLevel.CRITICAL:
            self.trigger_containment_protocol(strain_id, mutations)

    def trigger_containment_protocol(self, strain_id: str, mutations: List[str]):
        print(f"!!! ALERT: Strain {strain_id} has breached containment parameters.")
        print(f"!!! CAUSE: Resolved critical dependencies: {mutations[-1]}")
        print("!!! ACTION: Deploying bacteriophage countermeasures (Simulated).")

# --- 4. THE SIMULATION (Main Loop) ---
# Simulates the "Thread" of evolution over time.

def run_rift_simulation():
    print("--- INITIALIZING GOSSILANG BIO-KERNEL ---")
    print("--- LOADING SPARSE MODEL: MRSA_VARIANT_ALPHA ---")
    
    # 1. Initialize the Graph (The "Roads")
    graph = GenomicDependencyGraph()
    governor = ActiveGovernor(threshold=0.7)

    # 2. Define the "Packages" (Genes)
    # A standard Staph bacteria gene
    g_base = GeneNode(id="g01", name="CellWall_Synthesis", resistance_factor=0.1)
    
    # A minor mutation (requires base)
    g_mut1 = GeneNode(id="g02", name="Beta-Lactamase_Production", resistance_factor=0.3, dependencies=["g01"])
    
    # The Superbug mutation (requires mutation 1) - This represents mecA gene integration
    g_mrsa = GeneNode(id="mecA", name="PBP2a_Alteration (MRSA)", resistance_factor=0.95, dependencies=["g02"])

    graph.add_gene(g_base)
    graph.add_gene(g_mut1)
    graph.add_gene(g_mrsa)

    # 3. Initialize a Strain (The "User")
    strain_id = "STAPH_V1"
    genome = set()
    
    # 4. Simulation Loop (Evolution over Time)
    evolution_steps = ["g01", "g02", "mecA"]
    
    current_resistance = 0.0
    
    for step_gene_id in evolution_steps:
        time.sleep(1.0) # Simulate time passing
        
        # Try to resolve dependencies
        can_evolve = graph.resolve_dependencies(genome, step_gene_id)
        
        if can_evolve:
            print(f" > Strain {strain_id} attempting to acquire {step_gene_id}...")
            genome.add(step_gene_id)
            current_resistance = graph.nodes[step_gene_id].resistance_factor
            
            # NOTIFY GOVERNOR
            governor.observe(strain_id, current_resistance, list(genome))
        else:
            print(f" > Strain {strain_id} FAILED to acquire {step_gene_id} - Dependencies missing.")
            
    print("\n--- SIMULATION COMPLETE: RIFT CLOSED ---")

if __name__ == "__main__":
    run_rift_simulation()
