from dataclasses import dataclass, field
from typing import List

from bigbytes.services.spark.models.base import BaseSparkModel
from bigbytes.shared.enum import StrEnum


class ThreadState(StrEnum):
    RUNNABLE = 'RUNNABLE'
    TIMED_WAITING = 'TIMED_WAITING'
    WAITING = 'WAITING'


@dataclass
class StackTrace(BaseSparkModel):
    # "java.base@11.0.20/jdk.internal.misc.Unsafe.park(Native Method)",
    # "java.base@11.0.20/java.util.concurrent.locks.LockSupport.parkNanos(LockSupport.java:234)",
    # "java.base@11.0.20/java.lang.Thread.run(Thread.java:829)",
    elems: List[str] = field(default_factory=list)


@dataclass
class Thread(BaseSparkModel):
    #  "Lock(java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject@1086697356)"
    blocked_by_lock: str = None
    holding_locks: List[int] = field(default_factory=list)  # []
    stack_trace: StackTrace = None
    thread_id: int = None  # 54
    thread_name: str = None  # "context-cleaner-periodic-gc"
    thread_state: ThreadState = None  # "TIMED_WAITING"

    def __post_init__(self):
        if self.stack_trace and isinstance(self.stack_trace, dict):
            self.stack_trace = StackTrace.load(**self.stack_trace)

        if self.thread_state and isinstance(self.thread_state, str):
            try:
                self.thread_state = ThreadState(self.thread_state)
            except ValueError as err:
                print(f'[WARNING] Thread: {err}')
                self.thread_state = self.thread_state
