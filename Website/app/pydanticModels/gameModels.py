from pydantic import BaseModel
from typing import Optional

class createGame(BaseModel):

	side: str
	name: Optional[str] = ''
	limit: Optional[int] = 0
	increment: Optional[int] = 0

