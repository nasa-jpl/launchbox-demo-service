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
        "site": os.environ["SITE_ID"],
        "type": "demo",
        "version": version,
    }

# Resources
@app.get("/resources")
def index():
    return {key: value for key, value in os.environ.items() if key.startswith("LB_")}
