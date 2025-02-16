import os.path
import subprocess

# print(os.path.isfile("save_telemetry_data.py"))

path_to_python_exe = "C:\\.venv\\python312\\Scripts\\python.exe"
# cmd_path = "C:\\WINDOWS\\system32\\cmd.exe"

proc = subprocess.Popen([path_to_python_exe, "save_telemetry_data.py"],
                        # executable=cmd_path,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=False)
print(proc.pid)
code = proc.wait()
print(proc.returncode)

# path_to_python_exe = "C:\\.venv\\python312\\Scripts\\python.exe"
# subprocess.run([path_to_python_exe, "save_telemetry_data.py"])
