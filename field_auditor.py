import asyncio
import time

async def generate_sensitive_query(summary_str, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with Agent(config) as agent:
                response = await agent.prompt(f"Generate a targeted sensitive GraphQL query based on this schema: {summary_str}")
                return str(response)
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    print(f"[*] Model provider busy (503). Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
            raise e