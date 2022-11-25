from typing import List

from pydantic import BaseModel
class Doctor(BaseModel):
    uid: str
    nickName: str
    token: str

class Char(BaseModel):
    name: str 
    rarity: int 
    isNew: bool

class Gacha(BaseModel):
    uid: str
    ts: int
    pool: str
    chars: List[Char]
