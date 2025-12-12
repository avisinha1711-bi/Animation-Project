"""
BioOS Python Unit Tests
Comprehensive test suite for biological operating system
"""

import unittest
import sys
import os
from typing import List

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src/python'))

from bioOS_kernel import (
    BioOS, BioProcess, Gene, Protein, ProcessState, 
    EventType, BiologicalEvent, ProcessScheduler, 
    BiologicalMemory, EventManager
)
import bioOS_utils as utils
import bioOS_config as config

# ============================================================================
# GENE TESTS
# ============================================================================

class TestGene(unittest.TestCase):
    """Test cases for Gene class"""
    
    def setUp(self):
        self.gene = Gene("TEST_GENE", "ATCGATCG")
    
    def test_gene_creation(self):
        """Test gene initialization"""
        self.assertEqual(self.gene.name, "TEST_GENE")
        self.assertEqual(self.gene.sequence, "ATCGATCG")
        self.assertEqual(self.gene.expression_level, 0.0)
    
    def test_gene_expression(self):
        """Test gene expression"""
        level = self.gene.express(1.0)
        self.assertGreater(level, 0.0)
        self.assertLessEqual(level, 1.0)
    
    def test_gene_expression_saturation(self):
        """Test expression level saturation at 1.0"""
        for _ in range(100):
            self.gene.express(1.0)
        self.assertEqual(self.gene.expression_level, 1.0)

# ============================================================================
# PROTEIN TESTS
# ============================================================================

class TestProtein(unittest.TestCase):
    """Test cases for Protein class"""
    
    def setUp(self):
        self.protein = Protein("TEST_PROTEIN", "TEST_GENE")
        self.protein.concentration = 100.0
    
    def test_protein_creation(self):
        """Test protein initialization"""
        self.assertEqual(self.protein.name, "TEST_PROTEIN")
        self.assertEqual(self.protein.origin_gene, "TEST_GENE")
        self.assertEqual(self.protein.concentration, 100.0)
    
    def test_protein_degradation(self):
        """Test protein degradation"""
        initial = self.protein.concentration
        self.protein.degrade()
        self.assertLess(self.protein.concentration, initial)
    
    def test_protein_degradation_sequence(self):
        """Test multiple degradation steps"""
        for _ in range(10):
            self.protein.degrade()
        self.assertLess(self.protein.concentration, 100.0)

# ============================================================================
# BIOPROCESS TESTS
# ============================================================================

class TestBioProcess(unittest.TestCase):
    """Test cases for BioProcess class"""
    
    def setUp(self):
        self.process = BioProcess(1, "TestOrganism")
    
    def test_process_creation(self):
        """Test process initialization"""
        self.assertEqual(self.process.pid, 1)
        self.assertEqual(self.process.name, "TestOrganism")
        self.assertEqual(self.process.state, ProcessState.READY)
        self.assertEqual(self.process.energy, 100.0)
        self.assertEqual(self.process.age, 0.0)
    
    def test_process_update(self):
        """Test process state update"""
        initial_energy = self.process.energy
        initial_age = self.process.age
        
        self.process.update(1.0)
        
        self.assertLess(self.process.energy, initial_energy)
        self.assertGreater(self.process.age, initial_age)
    
    def test_process_gene_addition(self):
        """Test adding genes to process"""
        gene = Gene("TEST_GENE", "ATCG")
        self.process.genome["TEST_GENE"] = gene
        
        self.assertIn("TEST_GENE", self.process.genome)
        self.assertEqual(self.process.genome["TEST_GENE"].name, "TEST_GENE")
    
    def test_process_energy_decay(self):
        """Test energy decay over time"""
        for _ in range(10):
            self.process.update(1.0)
        
        self.assertEqual(self.process.energy, 100.0 - (10 * 0.5))

# ============================================================================
# MEMORY MANAGEMENT TESTS
# ============================================================================

class TestBiologicalMemory(unittest.TestCase):
    """Test cases for memory management"""
    
    def setUp(self):
        self.memory = BiologicalMemory(total_capacity=1000.0)
    
    def test_memory_allocation(self):
        """Test memory allocation"""
        result = self.memory.allocate(1, 100.0)
        self.assertTrue(result)
        self.assertAlmostEqual(self.memory.free_space, 900.0)
    
    def test_memory_allocation_failure(self):
        """Test allocation failure on insufficient space"""
        self.memory.allocate(1, 900.0)
        result = self.memory.allocate(2, 200.0)
        self.assertFalse(result)
    
    def test_memory_deallocation(self):
        """Test memory deallocation"""
        self.memory.allocate(1, 100.0)
        result = self.memory.deallocate(1)
        self.assertTrue(result)
        self.assertAlmostEqual(self.memory.free_space, 1000.0)
    
    def test_memory_deallocation_failure(self):
        """Test deallocation of non-existent entity"""
        result = self.memory.deallocate(999)
        self.assertFalse(result)
    
    def test_memory_usage_calculation(self):
        """Test memory usage percentage calculation"""
        self.memory.allocate(1, 500.0)
        usage = self.memory.get_usage()
        self.assertAlmostEqual(usage, 50.0, places=1)

# ============================================================================
# SCHEDULER TESTS
# ============================================================================

class TestProcessScheduler(unittest.TestCase):
    """Test cases for process scheduling"""
    
    def setUp(self):
        self.scheduler = ProcessScheduler()
    
    def test_process_creation(self):
        """Test process creation"""
        pid = self.scheduler.create_process("Test1")
        self.assertEqual(pid, 0)
    
    def test_multiple_process_creation(self):
        """Test creating multiple processes"""
        pids = [self.scheduler.create_process(f"Org{i}") for i in range(5)]
        self.assertEqual(len(pids), 5)
        self.assertEqual(len(self.scheduler.processes), 5)
    
    def test_process_retrieval(self):
        """Test retrieving process by PID"""
        pid = self.scheduler.create_process("TestOrg")
        process = self.scheduler.get_process(pid)
        self.assertIsNotNone(process)
        self.assertEqual(process.name, "TestOrg")
    
    def test_process_termination(self):
        """Test process termination"""
        pid = self.scheduler.create_process("TestOrg")
        result = self.scheduler.terminate_process(pid)
        self.assertTrue(result)
        
        process = self.scheduler.get_process(pid)
        self.assertEqual(process.state, ProcessState.TERMINATED)
    
    def test_scheduling_priority(self):
        """Test priority-based scheduling"""
        p1 = self.scheduler.create_process("Org1")
        p2 = self.scheduler.create_process("Org2")
        
        self.scheduler.get_process(p2).priority = 1  # Higher priority
        self.scheduler.get_process(p1).priority = 5
        
        # Should schedule higher priority (lower number) first
        scheduled = self.scheduler.schedule()
        self.assertEqual(scheduled.pid, p2)

# ============================================================================
# EVENT MANAGER TESTS
# ============================================================================

class TestEventManager(unittest.TestCase):
    """Test cases for event management"""
    
    def setUp(self):
        self.event_manager = EventManager()
    
    def test_event_emission(self):
        """Test event emission"""
        event = BiologicalEvent(
            timestamp=1.0,
            event_type=EventType.CELL_DIVISION,
            source_pid=1
        )
        self.event_manager.emit(event)
        self.assertGreater(len(self.event_manager.event_queue), 0)
    
    def test_event_subscription(self):
        """Test event handler subscription"""
        called = [False]
        
        def handler(event):
            called[0] = True
        
        self.event_manager.subscribe(EventType.CELL_DIVISION, handler)
        event = BiologicalEvent(
            timestamp=0.0,
            event_type=EventType.CELL_DIVISION,
            source_pid=1
        )
        self.event_manager.emit(event)
        self.event_manager.process_events(1.0)
        
        self.assertTrue(called[0])
    
    def test_event_ordering(self):
        """Test events processed in chronological order"""
        results = []
        
        def handler(event):
            results.append(event.timestamp)
        
        self.event_manager.subscribe(EventType.CELL_DIVISION, handler)
        
        # Emit events out of order
        self.event_manager.emit(BiologicalEvent(3.0, EventType.CELL_DIVISION, 1))
        self.event_manager.emit(BiologicalEvent(1.0, EventType.CELL_DIVISION, 1))
        self.event_manager.emit(BiologicalEvent(2.0, EventType.CELL_DIVISION, 1))
        
        self.event_manager.process_events(4.0)
        
        # Should be processed in order
        self.assertEqual(results, [1.0, 2.0, 3.0])

# ============================================================================
# KERNEL TESTS
# ============================================================================

class TestBioOS(unittest.TestCase):
    """Test cases for BioOS kernel"""
    
    def setUp(self):
        self.os = BioOS(time_step=0.1)
    
    def test_kernel_creation(self):
        """Test kernel initialization"""
        self.assertEqual(self.os.time_step, 0.1)
        self.assertEqual(self.os.current_time, 0.0)
        self.assertFalse(self.os.running)
    
    def test_organism_creation(self):
        """Test creating organism"""
        genome = {"GROWTH_GENE": Gene("GROWTH_GENE", "ATCG")}
        pid = self.os.create_organism("TestOrg", genome)
        
        self.assertGreaterEqual(pid, 0)
        process = self.os.scheduler.get_process(pid)
        self.assertIsNotNone(process)
    
    def test_simulation_tick(self):
        """Test single simulation tick"""
        genome = {"GROWTH_GENE": Gene("GROWTH_GENE", "ATCG")}
        self.os.create_organism("TestOrg", genome)
        
        initial_time = self.os.current_time
        self.os.run_tick()
        
        self.assertEqual(self.os.current_time, initial_time + 0.1)
    
    def test_multiple_ticks(self):
        """Test multiple simulation ticks"""
        genome = {"GROWTH_GENE": Gene("GROWTH_GENE", "ATCG")}
        self.os.create_organism("TestOrg", genome)
        
        for _ in range(10):
            self.os.run_tick()
        
        self.assertAlmostEqual(self.os.current_time, 1.0, places=5)

# ============================================================================
# UTILITY FUNCTION TESTS
# ============================================================================

class TestUtilities(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_generate_random_sequence(self):
        """Test random DNA sequence generation"""
        seq = utils.generate_random_sequence(10)
        self.assertEqual(len(seq), 10)
        self.assertTrue(all(base in 'ATGC' for base in seq))
    
    def test_reverse_complement(self):
        """Test DNA reverse complement"""
        seq = "ATCG"
        complement = utils.reverse_complement(seq)
        self.assertEqual(complement, "CGAT")
    
    def test_hamming_distance(self):
        """Test Hamming distance calculation"""
        distance = utils.hamming_distance("ATCG", "ATCC")
        self.assertEqual(distance, 1)
    
    def test_mutate_sequence(self):
        """Test sequence mutation"""
        seq = "ATCGATCGATCG"
        mutated = utils.mutate_sequence(seq, mutation_rate=1.0)
        # With rate=1.0, should be completely different
        self.assertNotEqual(seq, mutated)
    
    def test_translate_codon(self):
        """Test codon translation"""
        amino_acid = utils.translate_codon("ATG")
        self.assertEqual(amino_acid, "M")  # Methionine
    
    def test_calculate_stats(self):
        """Test statistics calculation"""
        values = [1, 2, 3, 4, 5]
        stats = utils.calculate_stats(values)
        
        self.assertEqual(stats['min'], 1)
        self.assertEqual(stats['max'], 5)
        self.assertEqual(stats['mean'], 3)
        self.assertEqual(stats['count'], 5)
    
    def test_weighted_random_choice(self):
        """Test weighted random selection"""
        choices = {'A': 0.7, 'B': 0.3}
        results = [utils.weighted_random_choice(choices) for _ in range(100)]
        
        # A should appear more often than B
        a_count = results.count('A')
        b_count = results.count('B')
        self.assertGreater(a_count, b_count)
    
    def test_validate_dna_sequence(self):
        """Test DNA sequence validation"""
        self.assertTrue(utils.validate_dna_sequence("ATCG"))
        self.assertTrue(utils.validate_dna_sequence("atcg"))  # Case insensitive
        self.assertFalse(utils.validate_dna_sequence("ATCX"))

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""
    
    def test_complete_simulation_run(self):
        """Test complete simulation workflow"""
        os = BioOS(time_step=0.1)
        
        # Create organisms
        genome1 = {
            "GROWTH": Gene("GROWTH", "ATCGATCG"),
            "ENERGY": Gene("ENERGY", "GCTAGCTA")
        }
        
        genome2 = {
            "SURVIVAL": Gene("SURVIVAL", "TACGTACG")
        }
        
        pid1 = os.create_organism("Org1", genome1)
        pid2 = os.create_organism("Org2", genome2)
        
        # Run simulation
        for _ in range(100):
            os.run_tick()
        
        # Verify state
        self.assertEqual(len(os.scheduler.processes), 2)
        self.assertGreater(os.current_time, 0)
    
    def test_organism_energy_dynamics(self):
        """Test organism energy dynamics over time"""
        os = BioOS(time_step=1.0)
        
        genome = {"GENE": Gene("GENE", "ATCG")}
        pid = os.create_organism("TestOrg", genome)
        
        process = os.scheduler.get_process(pid)
        initial_energy = process.energy
        
        # Run 10 ticks
        for _ in range(10):
            os.run_tick()
        
        # Should have lost energy
        self.assertLess(process.energy, initial_energy)
        self.assertEqual(process.energy, initial_energy - (10 * 0.5))

# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance(unittest.TestCase):
    """Performance and stress tests"""
    
    def test_many_organisms(self):
        """Test system with many organisms"""
        os = BioOS(time_step=0.1)
        
        # Create 100 organisms
        pids = []
        for i in range(100):
            genome = {"GENE": Gene("GENE", "ATCG")}
            pid = os.create_organism(f"Org{i}", genome)
            pids.append(pid)
        
        # Run simulation
        for _ in range(50):
            os.run_tick()
        
        self.assertEqual(len(os.scheduler.processes), 100)
    
    def test_event_queue_scaling(self):
        """Test event queue with many events"""
        em = EventManager()
        
        # Emit many events
        for i in range(1000):
            event = BiologicalEvent(
                timestamp=float(i),
                event_type=EventType.CELL_DIVISION,
                source_pid=i % 10
            )
            em.emit(event)
        
        # Process events
        em.process_events(1000.0)
        
        self.assertEqual(len(em.event_queue), 0)

# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGene))
    suite.addTests(loader.loadTestsFromTestCase(TestProtein))
    suite.addTests(loader.loadTestsFromTestCase(TestBioProcess))
    suite.addTests(loader.loadTestsFromTestCase(TestBiologicalMemory))
    suite.addTests(loader.loadTestsFromTestCase(TestProcessScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestEventManager))
    suite.addTests(loader.loadTestsFromTestCase(TestBioOS))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)
