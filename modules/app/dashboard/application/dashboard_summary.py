from dataclasses import dataclass


@dataclass
class DashboardSummary:
    conversations_today: int
    conversations_total: int
