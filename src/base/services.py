from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_session


class APIServiceMixin:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
