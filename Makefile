# BioOS Makefile
# Build configuration for BioOS project

.PHONY: help build clean test run python cpp docs install

# Variables
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -pthread
PYTHON = python3
SRC_CPP = src/cpp
BUILD_DIR = build
BIN_DIR = bin

help:
	@echo "BioOS Build System"
	@echo "=================="
	@echo ""
	@echo "Available targets:"
	@echo "  make build          - Build all components (C++ and Python)"
	@echo "  make cpp            - Build C++ components only"
	@echo "  make python         - Setup Python environment"
	@echo "  make test           - Run all tests"
	@echo "  make test-cpp       - Run C++ tests"
	@echo "  make test-python    - Run Python tests"
	@echo "  make run-cpp        - Run C++ simulator"
	@echo "  make run-python     - Run Python simulator"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make install        - Install dependencies"
	@echo "  make docs           - Generate documentation"
	@echo "  make format         - Format code"
	@echo "  make lint           - Run linters"
	@echo ""

# Create build directories
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(BIN_DIR)

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Installation complete!"

# Python setup
python: install
	@echo "Python environment ready"
	@echo "Run: cd src/python && python3 bioOS_main.py"

# Build C++ components
cpp: $(BUILD_DIR)
	@echo "Building C++ components..."
	$(CXX) $(CXXFLAGS) $(SRC_CPP)/bioOS_kernel.cpp $(SRC_CPP)/bioOS_main.cpp \
		-o $(BIN_DIR)/bioOS_simulator
	@echo "C++ build complete!"
	@echo "Binary: $(BIN_DIR)/bioOS_simulator"

# Build all
build: cpp python
	@echo "All components built successfully!"

# Run C++ simulator
run-cpp: cpp
	@echo "Running C++ BioOS simulator..."
	./$(BIN_DIR)/bioOS_simulator

# Run Python simulator
run-python: python
	@echo "Running Python BioOS simulator..."
	cd src/python && $(PYTHON) bioOS_main.py

# Test C++
test-cpp: cpp
	@echo "Running C++ tests..."
	$(CXX) $(CXXFLAGS) $(SRC_CPP)/bioOS_kernel.cpp tests/test_bioOS_cpp.cpp \
		-o $(BUILD_DIR)/test_bioOS_cpp
	./$(BUILD_DIR)/test_bioOS_cpp

# Test Python
test-python: python
	@echo "Running Python tests..."
	cd src/python && $(PYTHON) -m pytest ../../tests/test_bioOS_python.py -v

# Run all tests
test: test-cpp test-python
	@echo "All tests completed!"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(BUILD_DIR)
	rm -rf $(BIN_DIR)
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.o" -delete
	find . -type f -name "*.so" -delete
	@echo "Clean complete!"

# Generate documentation
docs:
	@echo "Generating documentation..."
	@mkdir -p docs/generated
	$(PYTHON) -c "import sys; sys.path.insert(0, 'src/python'); \
		from bioOS_kernel import BioOS; help(BioOS)" > docs/generated/bioOS_api.txt
	@echo "Documentation generated in docs/generated/"

# Code formatting
format:
	@echo "Formatting Python code..."
	$(PYTHON) -m black src/python/ --line-length=100
	@echo "Formatting C++ code..."
	find $(SRC_CPP) -name "*.cpp" -o -name "*.h" | xargs clang-format -i 2>/dev/null || true
	@echo "Formatting complete!"

# Linting
lint:
	@echo "Running Python linter..."
	$(PYTHON) -m flake8 src/python/ --max-line-length=100 --ignore=E203,W503
	@echo "Running C++ linter..."
	cppcheck $(SRC_CPP) --enable=all --suppress=missingIncludeSystem 2>/dev/null || true
	@echo "Linting complete!"

# Generate profiling info
profile-cpp: cpp
	@echo "Running C++ profiling..."
	$(CXX) $(CXXFLAGS) -pg $(SRC_CPP)/bioOS_kernel.cpp $(SRC_CPP)/bioOS_main.cpp \
		-o $(BIN_DIR)/bioOS_profile
	./$(BIN_DIR)/bioOS_profile
	gprof ./$(BIN_DIR)/bioOS_profile gmon.out > bioOS_profile.txt
	@echo "Profile saved to bioOS_profile.txt"

# CMake build alternative
cmake-build: $(BUILD_DIR)
	@echo "Building with CMake..."
	cd $(BUILD_DIR) && cmake .. && make
	@echo "CMake build complete!"

# Memory check (Valgrind)
memory-check: cpp
	@echo "Running memory check..."
	valgrind --leak-check=full --show-leak-kinds=all \
		./$(BIN_DIR)/bioOS_simulator 2>&1 | tee memory_report.txt
	@echo "Memory report saved to memory_report.txt"

# Development watch mode
watch:
	@echo "Watching for changes..."
	while true; do \
		clear; \
		$(MAKE) cpp; \
		sleep 2; \
	done

# Debugging
debug: $(BUILD_DIR)
	@echo "Building with debug symbols..."
	$(CXX) -std=c++17 -Wall -Wextra -g -pthread $(SRC_CPP)/bioOS_kernel.cpp \
		$(SRC_CPP)/bioOS_main.cpp -o $(BIN_DIR)/bioOS_debug
	@echo "Running debugger..."
	gdb ./$(BIN_DIR)/bioOS_debug

# Statistics
stats:
	@echo "Code Statistics"
	@echo "==============="
	@echo "Python files:"
	wc -l src/python/*.py
	@echo ""
	@echo "C++ files:"
	wc -l $(SRC_CPP)/*.cpp $(SRC_CPP)/*.h
	@echo ""
	@echo "Total lines:"
	find src -name "*.py" -o -name "*.cpp" -o -name "*.h" | xargs wc -l | tail -1

# Version info
version:
	@echo "BioOS v1.0.0"
	@echo "Build system: Make"
	@echo "C++ Standard: C++17"
	@echo "Python Version: 3.8+"

.DEFAULT_GOAL := help
