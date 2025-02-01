# import asyncio

# async def Name():
#     print("Deepika")
#     await FirstN("Amarapu")
# async def FirstN(text):
#     print(text)
#     await asyncio.sleep(1)
# asyncio.run(Name())

import asyncio

async def Name():
    print("Deepika")
    #await FirstN("Amarapu")
    task=asyncio.create_task(FirstN("Amarapu"))
    await asyncio.sleep(1)
    print("finished")
async def FirstN(text):
    print(text)
    await asyncio.sleep(1)
asyncio.run(Name())





