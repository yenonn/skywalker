import aiohttp
import asyncio
import requests


async def getResponse(session, i):
    # requests.get("http://localhost:8080/execute")
    async with session.get(f"http://localhost:8080/execute") as response:
        html = await response.text()
        await asyncio.sleep(0)
        print("done" + str(i))


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [getResponse(session, i) for i in range(10)]  # create list of tasks
        await asyncio.gather(*tasks)  # execute them in concurrent manner


asyncio.run(main())
