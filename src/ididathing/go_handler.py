import os
import subprocess
import shutil
import sys
import tempfile


# If $GOPATH is not specified, $HOME/go will be used by default
class PythonHandler:
    def __init__(self, test_package, virtual_dir=None):
        if virtual_dir is None:
            self.virtual_dir = tempfile.mkdtemp()
        else:
            self.virtual_dir = virtual_dir
        self.test_package = test_package
        self.virtual_python = os.path.join(self.virtual_dir, "bin", "python")

    def install_virtual_env(self):
        self.pip_install("virtualenv")
        if not os.path.exists(self.virtual_python):
            import subprocess
            subprocess.call(
                [sys.executable, "-m", "virtualenv", self.virtual_dir],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # print("found virtual python: " + self.virtual_python)
            pass

    def is_venv(self):
        return sys.prefix == self.virtual_dir

    def restart_under_venv(self):
        # print("Restarting under virtual environment " + self.virtual_dir)
        subprocess.call([self.virtual_python, __file__, self.virtual_dir])
        exit(0)

    @staticmethod
    def pip_install(package):
        try:
            __import__(package)

        except ImportError:
            subprocess.call([sys.executable, "-m", "pip", "install", package, "--upgrade"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                            )

    def get_deps(self):
        self.pip_install(self.test_package)
        command = f"{sys.executable} -m pip freeze"
        ret = subprocess.run(command, capture_output=True, shell=True)
        print(ret.stdout.decode())

    def run(self):
        if not self.is_venv():
            self.install_virtual_env()
            self.restart_under_venv()
        else:
            self.get_deps()
            shutil.rmtree(self.virtual_dir)


if len(sys.argv) == 2:
    working_dir = sys.argv[1]
    py = PythonHandler("pytest", working_dir)
else:
    py = PythonHandler("pytest")
py.run()
