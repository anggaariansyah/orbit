# Task Scheduler Refactoring

## Overview

Refactored the legacy task scheduling script into a modular OOP-based design.

## Improvements

* User quota management
* Task data model using dataclass
* Task executor abstraction
* Scheduler component
* Logging support
* Strategy Pattern for task actions
* Multiple tasks per user
* Configurable task parameters

## Architecture

```text
Scheduler
    |
    v
TaskExecutor
    |
    +--> UserManager
    |
    +--> StrategyFactory
            |
            +--> SyncStrategy
            +--> BackupStrategy
            +--> DeleteStrategy
```

## Run

```bash
python main.py
```

## Future Improvements

* Async execution
* Database persistence
* Message queue integration
* Distributed scheduling
