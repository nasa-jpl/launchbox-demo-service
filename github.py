import requests

from util import LBEvent


class LBGitHub:
    # max 100
    per_page = 30

    @staticmethod
    def branches(url, token=None):
        if response := LBGitHub.query(url, resource="branches", token=token):
            return [{
                "name": val["name"],
                "sha": val["commit"]["sha"],
                "url": val["commit"]["url"],
            } for val in response]

    @staticmethod
    def commits(url, branch=None, token=None):
        if response := LBGitHub.query(url, branch=branch, resource="commits", token=token):
            return [{
                "sha": val["sha"],
                "date": val["commit"]["author"]["date"],
                "author": val["author"]["login"],
                "url": val["html_url"],
            } for val in response]

    @staticmethod
    def repo(url, token=None):
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
    def clean(url):
        # Start
        for prefix in ["http://", "https://", "git@"]:
            if url.startswith(prefix):
                url = url[len(prefix):]
        # End
        if url.endswith(".git"):
            url = url[:-4]
        # Result
        return url

    @staticmethod
    def parse(url):
        # Split
        url = LBGitHub.clean(url)
        parts = url.split("/")
        if len(parts) >= 3:
            # Result
            return {
                "url": parts[0],
                "owner": parts[1],
                "name": parts[2],
            }

    @staticmethod
    def auth(token):
        return {"Authorization": f"token {token}"} if token else {}

    @staticmethod
    def endpoint(repo, resource):
        # Check
        if repo['url'] == "github.com":
            base_url = f"api.{repo['url']}"
        else:
            base_url = f"{repo['url']}/api/v3"
        # Result
        endpoint = f"https://{base_url}/repos/{repo['owner']}/{repo['name']}"
        if resource:
            endpoint += f"/{resource}"
        return endpoint

    @staticmethod
    def query(url, branch=None, resource=None, token=None):
        # Parse
        if repo := LBGitHub.parse(url):
            # Call
            if response := requests.get(
                LBGitHub.endpoint(repo, resource),
                headers=LBGitHub.auth(token),
                params={"per_page": LBGitHub.per_page, "sha": branch or ""},
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
