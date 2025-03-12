import sys,time
import traceback
import asyncio
from rich import print as rpn

lock = asyncio.Lock()

async def LongTask():
    # async with lock:
    rpn('start LongTask')
    await asyncio.sleep(9)

async def ProgressBar():
    i=0
    rpn('[',end = '')
    try:
        while True:
            i += 1
            if i%5:rpn('#',end = '')
            else:rpn(f'{i}',end = '')
            await asyncio.sleep(1)
    finally:
        rpn(']')

async def main():
    asyncio.create_task(ProgressBar())
    await LongTask()
    # rpn(']')
    # await LongTask()
    # await asyncio.gather(taskPB,taskLT)

start_time = time.perf_counter()
asyncio.run(main())
stop_time =  time.perf_counter()
Inetrval = stop_time - start_time
print(f'\nОбщее время выполнения {Inetrval:.7f}')
if not (len(sys.argv) > 1 and sys.argv[1] == 'cons'):input(':-> ')
sys.exit(0)
