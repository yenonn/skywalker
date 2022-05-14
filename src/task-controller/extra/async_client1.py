import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        local_url = "http://localhost:8080/execute"
        async with session.get(local_url) as resp:
            await asyncio.sleep(0)
            result = await resp.text()
            print(result)


asyncio.run(main())
