from typing import Callable
from argparse import Namespace

import yaml
# from anabel import interface 
interface = lambda x: x

class Config:
    def __init__(self,filename="~/.local/share/rendre/rendre.yaml"):
        pass


@interface 
class InitOperation:
    args: Namespace

@interface 
class ItemOperation:
    args: Namespace

@interface 
class EndOperation:
    accum: Callable
    args: Namespace
    config: Config