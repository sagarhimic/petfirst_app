from pydantic import BaseModel
from typing import Optional

class StoreBankRequest(BaseModel):
    bank_name: str
    account_holder_name: str
    account_number: str
    ifsc: str
    is_primary: Optional[bool] = False

class UpdateBankRequest(BaseModel):
    bank_name: str
    account_holder_name: str
    account_number: str
    ifsc: str
    is_primary: Optional[bool] = False

