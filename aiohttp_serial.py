import asyncio

import aiohttp


def run(urls, log):
    """Serial downloader using stdlib's request."""
    results = asyncio.run(main(urls, log))
    return results


async def main(urls, log):
    log("Async!")
    results = []
    async with aiohttp.ClientSession() as session:
        log("Session ok")
        for url in urls:
            async with session.get(url) as resp:
                log("Status", resp.status)
                result = await resp.read()
                results.append(result)
    return results
