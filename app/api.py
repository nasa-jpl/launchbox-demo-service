import json
import os

import bottle

# Application
app = bottle.Bottle()
version = 1.0

# Debugging
bottle.debug(LBEnv.local())

# Index
@app.get("/")
def index():
    return {
        "api": "lb",
        "env": os.environ.copy(),
        "type": "demo",
        "version": version,
    }
