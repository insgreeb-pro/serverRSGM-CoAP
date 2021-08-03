import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    
    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = b"2|1625167982.002157-24-70-50|6"
    request = Message(code=PUT, payload=payload, uri="coap://103.83.5.67/BMS_RSGM")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload.decode("utf-8")))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())