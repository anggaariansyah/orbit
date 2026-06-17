# Task Scheduler Refactoring

## Overview

This project refactors the legacy task scheduling system into a modular and extensible architecture.

### Improvements

* Converted procedural code into OOP design
* Added user quota management
* Added task data model
* Added scheduler component
* Added task executor component
* Added logging support
* Added Strategy Pattern for task actions

## Architecture

```text
Scheduler
    |
    v
TaskExecutor
    |
    +--> UserManager
    |
    +--> Action Strategies
```

## Components

### UserManager

Responsible for:

* User lookup
* Quota validation
* Execution tracking

### Task

Represents a scheduled task.

### Scheduler

Finds tasks scheduled for the current time.

### TaskExecutor

Executes tasks and updates quota usage.

### Action Strategies

Current supported actions:

* sync
* backup
* delete

## Running

```bash
python main.py
```

## Future Improvements

* Async execution
* Persistent storage (PostgreSQL)
* Distributed scheduler
* Queue-based workers
