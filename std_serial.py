from urllib.request import urlopen


def run(urls, verbose=False):
    """Serial downloader using stdlib's request."""
    results = []
    for url in urls:
        resp = urlopen(url)
        results.append(resp.read())
    return results
