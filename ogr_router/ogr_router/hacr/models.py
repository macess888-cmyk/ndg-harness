from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

class Posture(str, Enum):
    OBSERVE = "observe"
    DISCUSS = "discuss"
    SUPPORT = "support"
    PUBLISH = "publish"
    COMPATIBLE_BUT_INDEPENDENT = "compatible_but_independent"
    HOLD = "hold"
    ROLLBACK = "rollback"
    REJECT = "reject"


class Status(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    HOLD = "hold"
    PROVISIONAL = "provisional"


@dataclass
class CheckResult:
    name: str
    status: Status
    notes: List[str] = field(default_factory=list)


@dataclass
class RouterInput:
    object_id: str
    object_type: str
    title: str
    scope: Dict[str, Any]
    authorship: Dict[str, Any]
    assumptions: List[str]
    invariant: Dict[str, Any]
    boundaries: Dict[str, Any]
    reversibility: Dict[str, Any]
    commitment_surface: Dict[str, Any]
    transition: Dict[str, Any]
    evidence: Dict[str, Any]
    cross_scale: Dict[str, Any]
    separation_integrity: Dict[str, Any]


@dataclass
class RouterOutput:
    object_id: str
    posture: Posture
    summary_status: str
    results: List[CheckResult]
    constraints: List[str] = field(default_factory=list)