import threading
from urllib.request import urlopen


class Downloader(threading.Thread):
    def __init__(self, log, url):
        self.log = log
        self.url = url
        self.result = None
        super().__init__()

    def run(self):
        self.log("Opening", self.url)
        resp = urlopen(self.url)
        self.log("About to read")
        self.result = resp.read()
        self.log("Done")


def run(urls, log):
    """Threaded downloader using stdlib's request."""
    threads = []
    for url in urls:
        th = Downloader(log, url)
        threads.append(th)

    for th in threads:
        th.start()
    for th in threads:
        th.join()

    return [th.result for th in threads]
