# -*- coding: utf-8 -*-
from flask.helpers import get_debug_flag
from Mandark.project.app import create_app
from Mandark.project.config import DevelopmentConfig, ProductionConfig

CONFIG = DevelopmentConfig if get_debug_flag() else ProductionConfig

app = create_app(CONFIG)
