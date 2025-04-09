from pydantic import BaseModel
from typing import Union

class ErrorResponse(BaseModel):
    message: Union[str , list[str]]
    error: str
    statusCode: int
    