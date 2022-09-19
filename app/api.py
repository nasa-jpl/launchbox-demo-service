import json
import os

import bottle

# Application
app = bottle.Bottle()
version = 1.0

# Debug
bottle.debug(False)

# Index
@app.get("/")
def index():
    return {
        "api": "lb",
        "env": os.environ["ENVIRONMENT"],
        "service": os.environ["SERVICE_ID"],
        "site": os.environ["SITE_ID"],
        "type": "demo",
        "version": version,
    }

# Env vars
@app.get("/vars")
def index():
    return os.environ.copy()
