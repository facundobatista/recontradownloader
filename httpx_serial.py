import httpx


def run(urls, log):
    """Serial downloader using stdlib's request."""
    client = httpx.Client(http2=True)
    results = []
    for url in urls:
        log("Opening", url)
        resp = client.get(url)
        log("About to read")
        result = resp.content
        log("Done")
        results.append(result)
    return results

