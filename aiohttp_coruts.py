import asyncio

import aiohttp


async def download(log, session, url):
    async with session.get(url) as resp:
        log("Status", resp.status)
        return await resp.read()


async def main(urls, log):
    log("Async!")
    async with aiohttp.ClientSession() as session:
        log("Session ok")
        coruts = (download(log, session, url) for url in urls)
        results = await asyncio.gather(*coruts)
    return results


def run(urls, log):
    """Serial downloader using stdlib's request."""
    results = asyncio.run(main(urls, log))
    return results
