#Load test script to generate N concurrent requests to an API end point

import asyncio
import aiohttp

async def fetch(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()

async def main():
    url = "https://google-generative-ai-samples-rk3ighzk6q-uc.a.run.app/embeddings"  # Replace with your actual URL
    num_requests = 1000  # Number of parallel requests
    data = {"num1": 10, "num2": 5, "text": "['search_query: What is Liferay?', 'search_query: What is Google?']"}  # Sample POST data

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, data) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response)

if __name__ == "__main__":
    asyncio.run(main())