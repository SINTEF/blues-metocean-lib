from pathlib import Path
from dmtpygen import generator as pygen
from dmttsgen import generator as tsgen

def __generate_python(root):
    config = {
        "source" : True,
        "cleanup" : cleanup,
        "version" : "0.1.0",
        "license" : "UNKNOWN"
    }
    output_dir = Path("./src/bluesmet")
    pygen.generate(root,output_dir,config)

def __generate_typescript(root):
    config = {
        "source" : True,
        "cleanup" : cleanup,
        "minimal" : True,
        "version" : "0.1.0",
        "license" : "UNKNOWN"
    }
    output_dir = Path("./output/ts")
    tsgen.generate(root,output_dir,config)

cleanup = True
for module_name in ["met"]:
    package_root = Path("./models/" + module_name)
    __generate_python(package_root)
    __generate_typescript(package_root)
    