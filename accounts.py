from typing import *


class UserInfo(NamedTuple):
    username: str
    password: str


def get_accounts(txt_name: str) -> List[UserInfo]:
    lines = []
    with open(txt_name, 'r') as f:
        lines = f.readlines()
        return list(map(lambda l: UserInfo(*l.split()), lines))
