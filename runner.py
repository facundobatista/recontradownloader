import argparser
import importlib

HEADER = "https://files.pythonhosted.org/packages/"

FILES = [
    # 150 KB
    "ac/c3/e2a2b89f2d3e2179abd6d00ebd70bff6273f37fb3e0cc209f48b39d00cbf/requests-2.34.2.tar.gz",
    # 245 KB
    "df/bf/f7da0350254c0ed7c72f3e33cef02e048281fec7ecec5f032d4aac52226b/jinja2-3.1.6.tar.gz",
    # 11.3 MB
    "55/79/49a609ea76ec51404b482932e33f1e6858946b920232c11b11a25bea3032/django-6.1.3.tar.gz",
    # 136 KB
    "fd/11/b524cbd9bbdaca58608e4cf4053fd463417549e1959fa8d3aa18319f9555/certifi-2026.10.23.tar.gz",
]

parser = argparser.ArgumentParser()
parser.add_argument(
    "mode", choices=["test", "measure"], help="Run once in debug or multiple times and measure"
)
parser.add_argument("name", help="Name of the dowloader module.")
args = parser.parse_args()

mod = importlib.importlib(args.name)
if parser.mode == "test":
    mod.run(FILES[:1], verbose=True)
else:
    mod.run(FILES)
