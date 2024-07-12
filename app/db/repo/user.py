from db import orm, model
from ._base import BaseRepository


class AccountRepository(BaseRepository[orm.User, model.User]):
    ...
