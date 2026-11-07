import argparse
import hashlib
import importlib
import time

REALCASES = [
    # jinja, 245 KB
    (
        "0137fb05990d35f1275a587e9aee6d56da821fc83491a0fb838183be43f66d6d",
        "https://files.pythonhosted.org/packages/df/bf/f7da0350254c0ed7c72f3e33cef02e048281fec7ecec5f032d4aac52226b/jinja2-3.1.6.tar.gz",  # NOQA
    ),
    # requests, 150 KB
    (
        "f288924cae4e29463698d6d60bc6a4da69c89185ad1e0bcc4104f584e960b9ed",
        "https://files.pythonhosted.org/packages/ac/c3/e2a2b89f2d3e2179abd6d00ebd70bff6273f37fb3e0cc209f48b39d00cbf/requests-2.34.2.tar.gz",  # NOQA
    ),
    # 11.3 MB
    (
        "b5d2d9e35295065d13b1927b3f19a59bd119f737aa6299def14ccca1ae3c8c0d",
        "https://files.pythonhosted.org/packages/55/79/49a609ea76ec51404b482932e33f1e6858946b920232c11b11a25bea3032/django-6.1.3.tar.gz",  # NOQA
    ),
    # 136 KB
    (
        "a9895e6e2758b371e0545e321a3a8fd1fcfd9829ada8824a936dfb16aaaf36cd",
        "https://files.pythonhosted.org/packages/fd/11/b524cbd9bbdaca58608e4cf4053fd463417549e1959fa8d3aa18319f9555/certifi-2026.10.23.tar.gz",  # NOQA
    ),
]

SAMPLE = REALCASES[0]


def check(hashorig, result):
    try:
        hashresult = hashlib.sha256(result).hexdigest()
    except Exception:
        breakpoint()
        ok = "FAIL"
    else:
        if hashresult == hashorig:
            ok = "ok"
        else:
            ok = "FAIL"
    return ok


def test(mod):
    hashorig, url = SAMPLE
    tini = time.time()
    try:
        result = mod.run([url], print)
        with open("/tmp/prueba", "wb") as fh:
            fh.write(result[0])
    except Exception as exc:
        ok = f"ERROR: {exc!r}"
    else:
        ok = check(hashorig, result[0])
    finally:
        tfin = time.time()

    tdeltams = 1000 * (tfin - tini)
    print(f"Finished, {tdeltams:.2f}ms, {ok}")


def measure(mod):
    hashorig, url = SAMPLE
    for quant in [1, 2, 3, 5, 10]:
        tini = time.time()
        try:
            results = mod.run([url] * quant, lambda *a, **k: None)
        except Exception as exc:
            tfin = time.time()
            ok = f"ERROR: {exc!r}"
        else:
            tfin = time.time()
            ok = [check(hashorig, result) for result in results]

        tdeltams = 1000 * (tfin - tini) / quant
        print(f"Measured {quant:2d}, {tdeltams:.2f}ms per file, {ok}")


FUNCS = {"test": test, "measure": measure}

parser = argparse.ArgumentParser()
parser.add_argument(
    "mode", choices=FUNCS.keys(), help="Run once in debug or multiple times and measure"
)
parser.add_argument("name", help="Name of the dowloader module.")
args = parser.parse_args()

mod = importlib.import_module(args.name)
print("Running:", mod.run.__doc__)
func = FUNCS[args.mode]
func(mod)
