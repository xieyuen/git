import os
import json
import yaml

from .. import logger
from ..utils import sha256


default_config: dict = {
    'logger':
}
default_user_data: list[dict] = [
    {
        'username': 'root',
        'password': sha256('root'),
        'enable': False,
    }
]


def create_default_config():
    with open('./config.yml', 'w', encoding='utf-8') as cfg_file:
        yaml.safe_dump(default_config, cfg_file, default_flow_style=False, allow_unicode=True)


def create_default_user_data():
    if not os.path.exists('/'):
        os.mkdir('/')
    with open("./data/user_data.json", "w", encoding='utf-8') as user_data_file:
        json.dump(default_user_data, user_data_file, indent=4)





def save_user_data(new):
    with open("./data/user_data.json", "w", encoding='utf-8') as user_data_file:
        json.dump(new, user_data_file, indent=4)
