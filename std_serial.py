from urllib.request import urlopen


def run(urls, log):
    """Serial downloader using stdlib's request."""
    results = []
    for url in urls:
        log("Opening", url)
        resp = urlopen(url)
        log("About to read")
        result = resp.read()
        log("Done")
        results.append(result)
    return results
