import requests

from util import LBEvent


class LBGitHub:
    # max 100
    per_page = 30

    @staticmethod
    def commits(repo_url, branch="", token=None):
        if repo := LBGitHub.parse(repo_url):
            if response := LBGitHub.API.request(
                endpoint=LBGitHub.endpoint(repo, "repos", "commits"),
                headers=LBGitHub.auth(token),
                params={"per_page": LBGitHub.per_page, "sha": branch},
            ):
                return [{
                    "sha": val["sha"],
                    "date": val["commit"]["author"]["date"],
                    "author": val["author"]["login"],
                    "url": val["html_url"]
                } for val in response]
        else:
            LBEvent.error("LBGitHub.commits", "Error parsing URL")
            return False

    @staticmethod
    def parse(url):
        # Start
        for prefix in ["http://", "https://", "git@"]:
            if url.startswith(prefix):
                url = url[len(prefix):]
        # End
        if url.endswith(".git"):
            url = url[:-4]
        # Split
        parts = url.split("/")
        if len(parts) >= 3:
            # Params
            base_url = parts[0]
            owner = parts[1]
            name = parts[2]
            # Check
            if base_url == "github.com":
                base_url = f"api.{base_url}"
            else:
                base_url = f"{base_url}/api/v3"
            # Result
            return {
                "base_url": base_url,
                "owner": owner,
                "name": name,
            }

    @staticmethod
    def auth(token):
        return {"Authorization": f"token {token}"} if token else {}

    @staticmethod
    def endpoint(repo, parent, child):
        return f"https://{repo['base_url']}/{parent}/{repo['owner']}/{repo['name']}/{child}"

    class API:
        @staticmethod
        def request(endpoint, headers, params):
            try:
                response = requests.get(
                    endpoint,
                    headers=headers,
                    params=params,
                    timeout=15,
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    LBEvent.error("LBGitHub.API", f"[{response.status_code}] {response.reason}")
                    return False
            except Exception as e:
                LBEvent.error("LBGitHub.API", e)
                return False
