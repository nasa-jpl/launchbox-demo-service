import os

import envdir


class LBEnv:
    class dir:
        @staticmethod
        def clear(envpath):
            # TODO: Walk directory and delete files directly
            with envdir.open(envpath) as env:
                for var_name in list(env.keys()):
                    del env[var_name]

        @staticmethod
        def get(envpath, var_name):
            with envdir.open(envpath) as env:
                return env.get(var_name)

        @staticmethod
        def read(envpath):
            if LBEnv.dir.valid(envpath):
                with envdir.open(envpath) as env:
                    return dict(env.items())
            return False

        @staticmethod
        def set(envpath, var_name, value):
            with envdir.open(envpath) as env:
                env[var_name] = value

        @staticmethod
        def setup(envpath):
            if LBEnv.dir.valid(envpath):
                return True
            elif os.path.exists(envpath):
                return False
            else:
                try:
                    os.mkdir(envpath)
                except Exception:
                    return False
                else:
                    return True

        @staticmethod
        def valid(envpath):
            if os.path.exists(envpath):
                return os.path.isdir(envpath)
            return False


# print(LBEnv.dir.read("env_vars"))
