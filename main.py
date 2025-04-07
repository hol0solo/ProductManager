import asyncio
import time
from POST.post_create_product import create_product_function


async def main():
    first_part = time.time()
    await create_product_function()
    final_part = time.time()
    print(f"Программа выполняется за {final_part-first_part} сек")


asyncio.run(main())