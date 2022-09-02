import os
import pprint
import yaml


class LBEnv:
    @staticmethod
    def copy():
        return os.environ.copy()

    @staticmethod
    def get(name, default=None):
        if value := os.getenv(name, False):
            return value
        elif default is None:
            # WCPEvent.exit("LBEnv", f"Requested environment variable is not set: {name}")
            pass
        return default

    @staticmethod
    def aws():
        return LBEnv.type() != "local"

    @staticmethod
    def local():
        return LBEnv.type() == "local"

    @staticmethod
    def git_branch():
        return LBEnv.get("GIT_BRANCH", "N/A")

    @staticmethod
    def git_sha():
        return LBEnv.get("GIT_SHA", "N/A")

    @staticmethod
    def type():
        if environment := LBEnv.get("ENVIRONMENT", False):
            return environment.lower()
        else:
            # line1 = "Environment not specified, assuming: local."
            # line2 = "Please add ENVIRONMENT=local to your .env file."
            # WCPEvent.warn("LBEnv", f"{line1} {line2}")
            return "local"


class LBDeployment:
    def __init__(self, service_id, commit, status):
        # Params
        self.commit = commit
        self.service_id = service_id
        self.status = status
        # Setup
        self.path = f"services/{service_id}/{commit}/"

    @property
    def active(self):
        return self.status == "active"


class LBService:
    def __init__(self, identifier):
        self.identifier = identifier
        self.git_repo = "https://github.jpl.nasa.gov/18x/WCP"
        self.git_branch = "develop"
        self.deployments = []

    @property
    def deployed(self):
        for deployment in self.deployments:
            if deployment.active:
                return deployment

    @property
    def path(self):
        if self.deployed:
            return self.deployed.path


class LBSite:
    def __init__(self, identifier, service):
        self.identifier = identifier
        self.service = service


class LBConfig:
    def __init__(self, site):
        # Params
        self.site = site
        # Setup
        self.path = os.path.join(site.service.path, "launch.yaml")
        self.data = self.load()

    def load(self):
        if os.path.isfile(self.path):
            with open(self.path, "r") as fd:
                return yaml.safe_load(fd)
        return {}

    @property
    def env(self):
        if env := self.data.get("env"):
            # Environment
            result = env.get("base", {})
            if specific := env.get(LBEnv.type()):
                result.update(specific)
            # Resources
            for name, config in self.resources.items():
                for key, value in config["values"].items():
                    result[f"LB_{name}_{key}"] = value
            return result
        return {}

    @property
    def resources(self):
        if resources := self.data.get("resources"):
            for name, config in resources.items():
                match config.get("type"):
                    case "postgres":
                        config["values"] = {
                            "hostname": "postgres.example.localhost",
                            "name": f"{self.site.identifier}_{name}",
                            "username": self.site.identifier,
                            "password": "example",
                            "port": 5342,
                        }
                    case "redis":
                        config["values"] = {
                            "url": "redis.example.localhost",
                            "prefix": f"{self.site.identifier}_{name}",
                        }
                    case _:
                        print(f"[LBConfig.resources]: Resource type not recognized")
            return resources
        return {}


deployment1 = LBDeployment("wcp-wagtail", "f4e34db690308848c5e7ea4851c12d0daf49332b", "active")

service1 = LBService("wcp-wagtail")
service1.deployments.append(deployment1)

site1 = LBSite("example", service1)

config = LBConfig(site1)
pprint.pprint(config.env)
