import json
import os
import subprocess
import shutil
import sys
import tempfile


class JavaScriptHandler:
    def __init__(self, test_package, virtual_dir=None):
        if virtual_dir is None:
            self.virtual_dir = tempfile.mkdtemp()
        else:
            self.virtual_dir = virtual_dir
        self.test_package = test_package

    def npm_install(self, package):
        subprocess.call(["npm", "install", package],
                        cwd=self.virtual_dir,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                        )

    def get_deps(self):
        self.npm_install(self.test_package)
        command = "cat package-lock.json"
        ret = subprocess.run(command, capture_output=True, shell=True, cwd=self.virtual_dir)
        data = json.loads(ret.stdout.decode())
        for dep, data in data["dependencies"].items():
            print(f"{dep}=={data['version']}")

    def run(self):
        self.get_deps()
        shutil.rmtree(self.virtual_dir)


js = JavaScriptHandler("coffee-middle")
js.run()
