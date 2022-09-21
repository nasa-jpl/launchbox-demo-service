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
        "service": os.environ.get("LB_SERVICE_ID", False),
        "site": os.environ.get("LB_SITE_ID", False),
        "type": "demo",
        "version": version,
    }

# Env vars
@app.get("/vars")
def index():
    return os.environ.copy()
