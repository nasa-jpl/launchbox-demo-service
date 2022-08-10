import os
from util import LBCommand


class LBGit:
    @staticmethod
    def clone(path, url, branch, dirname):
        args = ["git", "clone", url, dirname, "--branch", branch, "--single-branch"]
        LBCommand.run(args, cwd=path)
        return os.path.join(path, dirname)

    @staticmethod
    def head(path):
        args = ["git", "rev-parse", "HEAD"]
        result = LBCommand.run(args, cwd=path, output=True)
        if result.returncode == 0:
            return result.stdout.decode("utf-8").strip("\n")

    @staticmethod
    def reset(path, commit):
        args = ["git", "reset", "--hard", commit]
        LBCommand.run(args, cwd=path)


url = "https://github.com/nasa-jpl/explorer-1.git"
branch = "main"
commit = "bb44f1406af7a7ae9677fb1d05baecadfdac21e1"
path = "services/explorer-1/"

# repo_path = LBGit.clone(path, url, branch, commit)
# LBGit.reset(repo_path, commit)
