# -*- coding: utf-8 -*-
from Mandark.project.app import create_app
from Mandark.project.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(debug=True)
