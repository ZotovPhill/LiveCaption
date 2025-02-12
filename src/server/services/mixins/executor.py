from asyncio import get_running_loop
from typing import Any, Callable


class AsyncExecutorMixin:
    async def _run_in_executor(self, func: Callable[..., Any], *args: Any) -> Any:
        return await get_running_loop().run_in_executor(None, func, *args)
