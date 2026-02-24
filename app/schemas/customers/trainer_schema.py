from pydantic import BaseModel, Field, condecimal
from decimal import Decimal
from typing import Optional


class GetTrainersRequest(BaseModel):
    latitude: condecimal(max_digits=10, decimal_places=8)
    longitude: condecimal(max_digits=11, decimal_places=8)
    service_id: Optional[int] = None
    trainer_id: Optional[int] = None
