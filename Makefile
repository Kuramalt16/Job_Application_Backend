# Makefile to run event consumer and propagator concurrently on Windows

# Python interpreter (ensure python is available in PATH or provide full path)
PYTHON := python  # You can replace this with the full path to python if necessary, e.g., C:/Python39/python.exe

# Scripts
CONSUMER_SCRIPT := Consumer.py
PROPAGATOR_SCRIPT := Propagator.py

REQUIREMENTS := requirements.txt

# Files to store PIDs
CONSUMER_PID_FILE := consumer_pid.txt
PROPAGATOR_PID_FILE := propagator_pid.txt

all: install run

# Install dependencies
install:
	@echo "Installing dependencies..."
	@$(PYTHON) -m pip install -r $(REQUIREMENTS)

# Target for consumer and propagator
run:
	@echo "Starting Consumer..."
	@start /B $(PYTHON) $(CONSUMER_SCRIPT) &
	@$(PYTHON) $(PROPAGATOR_SCRIPT)

clean:
	@echo "Cleaning up..."
	@taskkill /F /IM python.exe || echo "No Python processes found"  # Kill all Python processes

