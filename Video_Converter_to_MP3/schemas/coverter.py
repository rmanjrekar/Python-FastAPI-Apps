from pydantic import BaseModel
from typing import Optional

class ConversionResponse(BaseModel):
    filename: str
    converted_to: str
    message: Optional[str] = None