import os
import sys
import subprocess

cwd = os.path.dirname(os.path.realpath(__file__))
mocks = os.path.join(cwd, "../mocks")
src = os.path.join(cwd, "../src")
main = os.path.join(cwd, "../src/main.py")

env = os.environ.copy()
env["PYTHONPATH"] = f"{src}:{mocks}"

subprocess.run([sys.executable, main], env=env)

