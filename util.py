import os
import subprocess


class LBCommand:
    @staticmethod
    def run(args, cwd=None, setenv={}, stdin=None, output=False):
        # Extend existing environment variables
        env = LBEnv.copy()
        env.update(setenv)
        # Check stdin (invalid stdin can cause commands that expect it to hang)
        if stdin is not None:
            if type(stdin) is not bytes:
                # WCPEvent.warn("WCPCommand", "Unable to run command: stdin value must use byte format")
                return False
        return subprocess.run(args, cwd=cwd, env=env, input=stdin, capture_output=output)


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