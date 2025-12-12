"""
BioOS Configuration File
Central configuration for biological operating system parameters
"""

# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================

# Simulation timing
TIME_STEP = 0.1  # Seconds per simulation tick
SIMULATION_DURATION = 10.0  # Total simulation duration in seconds
MAX_PROCESSES = 1000  # Maximum concurrent processes

# ============================================================================
# MEMORY CONFIGURATION
# ============================================================================

MEMORY_TOTAL_CAPACITY = 10000.0  # Total system memory units
MEMORY_PER_ORGANISM = 100.0  # Memory allocated per organism
MEMORY_ALLOCATION_THRESHOLD = 80.0  # Trigger garbage collection at 80%

# ============================================================================
# PROCESS CONFIGURATION
# ============================================================================

PROCESS_INITIAL_ENERGY = 100.0  # Initial energy per organism
PROCESS_ENERGY_COST_PER_TICK = 0.5  # Energy consumed per update tick
PROCESS_MIN_ENERGY = 0.0  # Minimum energy before termination
PROCESS_PRIORITY_LEVELS = 10  # Number of priority levels (1-10)

# ============================================================================
# BIOLOGICAL CONFIGURATION
# ============================================================================

# Gene expression
GENE_EXPRESSION_RATE = 0.1  # Base expression rate per tick
GENE_EXPRESSION_MAX = 1.0  # Maximum expression level

# Protein dynamics
PROTEIN_DEFAULT_HALFLIFE = 10.0  # Default protein half-life in ticks
PROTEIN_DEGRADATION_RATE = 0.1  # Degradation rate per tick
PROTEIN_CONCENTRATION_MAX = 100.0  # Maximum protein concentration

# Cell division
CELL_DIVISION_ENERGY_COST = 50.0  # Energy cost for cell division
CELL_DIVISION_ENERGY_THRESHOLD = 80.0  # Minimum energy to divide
CELL_DIVISION_PROBABILITY = 0.05  # Base probability per tick

# Mutation
MUTATION_RATE = 0.01  # Probability of mutation per gene per division
MUTATION_SEVERITY = 0.1  # Magnitude of expression level change

# ============================================================================
# EVENT CONFIGURATION
# ============================================================================

EVENT_QUEUE_MAX_SIZE = 10000  # Maximum events in queue
EVENT_PROCESSING_BATCH = 100  # Events processed per tick

# Event probabilities
EVENT_PROB_CELL_DIVISION = 0.01
EVENT_PROB_APOPTOSIS = 0.005
EVENT_PROB_MUTATION = 0.002
EVENT_PROB_GENE_EXPRESSION = 0.1
EVENT_PROB_SIGNAL_RECEPTION = 0.05

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "bioOS.log"
LOG_TO_CONSOLE = True
LOG_TO_FILE = True
LOG_TICK_INTERVAL = 100  # Log every N ticks
LOG_PROCESS_STATS = True
LOG_MEMORY_STATS = True

# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

ENABLE_VISUALIZATION = True
VISUALIZATION_TICK_INTERVAL = 10  # Update visualization every N ticks
VISUALIZATION_PROCESS_LIMIT = 100  # Max processes to visualize
VISUALIZATION_PORT = 8000  # Web server port for visualization

# ============================================================================
# THREADING CONFIGURATION
# ============================================================================

NUM_WORKER_THREADS = 4  # Number of worker threads
THREAD_POOL_ENABLED = True
THREAD_SAFE_OPERATIONS = True

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

PERFORMANCE_PROFILING = False
PERFORMANCE_LOG_FILE = "bioOS_profile.log"
ENABLE_OPTIMIZATION = True
CACHE_GENOME_EXPRESSIONS = True

# ============================================================================
# EXPERIMENTAL FEATURES
# ============================================================================

ENABLE_NEURAL_SIMULATION = False  # Enable neural network-based organisms
ENABLE_PHEROMONE_SYSTEM = False  # Enable pheromone signaling
ENABLE_HORIZONTAL_GENE_TRANSFER = False  # Enable gene transfer between organisms
ENABLE_EPIGENETIC_MARKS = False  # Enable epigenetic modifications

# ============================================================================
# DEBUG CONFIGURATION
# ============================================================================

DEBUG_MODE = False
DEBUG_RANDOM_SEED = None  # Set for reproducible simulations
DEBUG_VERBOSE_LOGGING = False
DEBUG_MEMORY_TRACKING = False
DEBUG_EVENT_TRACING = False
