from pydantic import BaseModel
from pydantic import ConfigDict


class DashboardSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    conversations_today: int
    conversations_total: int
