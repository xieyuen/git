import os
import json
import yaml

from loguru import logger

from utils import sha256


config: dict = {}
userdata: list = []
