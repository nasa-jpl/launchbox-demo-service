import requests

from util import LBEvent


class LBGitHub:
    # max 100
    per_page = 30

    @staticmethod
    def branches(url, token=None):
        # Call
        if response := LBGitHub.query(url, resource="branches", token=token):
            # Results
            return [{
                "name": val["name"],
                "sha": val["commit"]["sha"],
                "url": val["commit"]["url"],
            } for val in response]

    @staticmethod
    def commits(url, branch="", token=None):
        if response := LBGitHub.query(url, branch, "commits", token):
            return [{
                "sha": val["sha"],
                "date": val["commit"]["author"]["date"],
                "author": val["author"]["login"],
                "url": val["html_url"],
            } for val in response]

    @staticmethod
    def repos(url, token=None):
        if response := LBGitHub.query(url, token=token):
            return {
                "name": response["name"],
                "owner": response["owner"]["login"],
                "description": response["description"],
                "url": response["html_url"],
                "created_at": response["created_at"],
                "updated_at": response["updated_at"],
                "pushed_at": response["pushed_at"],
            }

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
    def endpoint(repo, resource):
        endpoint = f"https://{repo['base_url']}/repos/{repo['owner']}/{repo['name']}"
        if resource:
            endpoint += f"/{resource}"
        return endpoint

    @staticmethod
    def query(url, branch="", resource="", token=None):
        # Parse
        if repo := LBGitHub.parse(url):
            # Call
            if response := requests.get(
                LBGitHub.endpoint(repo, resource),
                headers=LBGitHub.auth(token),
                params={"per_page": LBGitHub.per_page, "sha": branch},
                timeout=15,
            ):
                # Results
                if response.status_code == 200:
                    return response.json()
                else:
                    LBEvent.error("LBGitHub.query", f"[{response.status_code}] {response.reason}")
                    return False
            else:
                LBEvent.error("LBGitHub.query", "Response Error")
                return False
        else:
            LBEvent.error("LBGitHub.query", "Parse Error")
            return False
