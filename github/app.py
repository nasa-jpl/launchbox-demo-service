import json

import bottle
import requests

# Application
app = application = bottle.Bottle()

# Debugging
bottle.debug(True)


@app.get("/")
def index():
    manifest = {
        "name": "Launchbox-Test",
        "url": "http://wcpdev.jplweb.net:8001",
        "hook_attributes": {
            "url": "http://wcpdev.jplweb.net:8001/events",
        },
        "redirect_url": "http://wcpdev.jplweb.net:8001/redirect",
        "callback_urls": [
            "http://wcpdev.jplweb.net:8001/callback",
        ],
        "public": False,
        "default_permissions": {
            "contents": "read",
        },
        "default_events": [
            "push",
        ]
    }
    return f"""
        <html>
            <body>
                <form action="https://github.com/settings/apps/new" method="POST">
                    <input id="manifest" type="hidden" name="manifest">
                    <input id="state" type="hidden" name="state" value="fejwaofejiwafjw">
                    <input type="submit" value="Register">
                </form>
                <script>
                    input = document.getElementById("manifest")
                    input.value = JSON.stringify({json.dumps(manifest)})
                </script>
            </body>
        </html>
    """

@app.route("/events")
def events():
    if body := bottle.request.body:
        data = json.loads(body)
        print(data)
    return {"api": "launchbox"}

@app.get("/redirect")
def redirect():
    if code := bottle.request.params.get("code"):
        print(f"Code: {code}")
        response = requests.post(f"https://api.github.com/app-manifests/{code}/conversions")
        if response.status_code == 201:
            data = response.json()
            print(data)
            return data

@app.get("/callback")
def callback():
    print(bottle.request.body)
    return {"endpoint": "callback"}


if __name__ == "__main__":
    # Run webserver
    bottle.run(
        app=app,
        host="0.0.0.0",
        port=8001,
    )
