
import logging
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod

# ==================================================
# Logging Configuration
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ==================================================
# User Management
# ==================================================

class UserManager:
    def __init__(self, users):
        self.users = users

    def can_execute(self, username):
        user = self.users.get(username)

        if not user:
            logger.error(f"User '{username}' not found")
            return False

        return user["executed"] < user["quota"]

    def record_execution(self, username):
        self.users[username]["executed"] += 1


# ==================================================
# Task Model
# ==================================================

@dataclass
class Task:
    user: str
    time: str
    action: str
    params: dict = field(default_factory=dict)


# ==================================================
# Strategy Pattern
# ==================================================

class ActionStrategy(ABC):

    @abstractmethod
    def execute(self, params):
        pass


class SyncStrategy(ActionStrategy):

    def execute(self, params):
        logger.info(
            f"Syncing target: {params.get('target')}"
        )


class BackupStrategy(ActionStrategy):

    def execute(self, params):
        logger.info(
            f"Backing up target: {params.get('target')}"
        )


class DeleteStrategy(ActionStrategy):

    def execute(self, params):
        logger.info(
            f"Deleting target: {params.get('target')}"
        )


class StrategyFactory:

    strategies = {
        "sync": SyncStrategy(),
        "backup": BackupStrategy(),
        "delete": DeleteStrategy(),
    }

    @classmethod
    def get_strategy(cls, action):
        if action not in cls.strategies:
            raise ValueError(
                f"Unsupported action: {action}"
            )

        return cls.strategies[action]


# ==================================================
# Task Executor
# ==================================================

class TaskExecutor:

    def __init__(self, user_manager):
        self.user_manager = user_manager

    def execute(self, task):

        if not self.user_manager.can_execute(task.user):
            logger.warning(
                f"{task.user} has exceeded quota"
            )
            return

        try:
            strategy = StrategyFactory.get_strategy(
                task.action
            )

            logger.info(
                f"Executing action={task.action} "
                f"for user={task.user}"
            )

            strategy.execute(task.params)

            self.user_manager.record_execution(
                task.user
            )

        except Exception as e:
            logger.exception(
                f"Execution failed: {e}"
            )


# ==================================================
# Scheduler
# ==================================================

class Scheduler:

    def __init__(self, executor):
        self.executor = executor
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def run_pending(self):

        now = datetime.now().strftime("%H:%M")

        logger.info(
            f"Checking tasks for {now}"
        )

        for task in self.tasks:
            if task.time == now:
                self.executor.execute(task)


# ==================================================
# Bootstrap
# ==================================================

def main():

    users = {
        "alice": {
            "quota": 3,
            "executed": 0
        },
        "bob": {
            "quota": 5,
            "executed": 0
        }
    }

    user_manager = UserManager(users)

    executor = TaskExecutor(user_manager)

    scheduler = Scheduler(executor)

    scheduler.add_task(
        Task(
            user="alice",
            time="12:00",
            action="sync",
            params={
                "target": "/data/x"
            }
        )
    )

    scheduler.add_task(
        Task(
            user="bob",
            time="12:00",
            action="backup",
            params={
                "target": "/srv/y"
            }
        )
    )

    scheduler.add_task(
        Task(
            user="alice",
            time="12:00",
            action="delete",
            params={
                "target": "/tmp/z"
            }
        )
    )

    scheduler.run_pending()


if __name__ == "__main__":
    main()

