from dataclasses import dataclass, field

@dataclass
class Task:
    user: str
    time: str
    action: str
    params: dict = field(default_factory=dict)
