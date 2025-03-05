"""Obtain hardware usage data of the host"""

import asyncio
from datetime import datetime

import psutil


class HardWareMonitor:
    """Define data object for future actions"""

    def __init__(self, monitor_period: int = 5):
        """Init HardWareMonitor object

        Arguments:
        monitor_period - period (sec) to check hardware usage (default = 5)"""
        self.monitor_period = monitor_period
        self.ram_free = None
        self.set_ram_free()
        self.cpu_usage = None
        self.network_usage = None

        # тут запускаются асинхронно функции которые требуют некоторое время для своего выполнения
        asyncio.run(self.wait_data())

    def get_hw_usage_data(self):
        """Define return data as dict"""
        return {
            "ram_free": self.ram_free,
            "cpu_usage": self.cpu_usage[0],
            "network_usage": self.network_usage[0],
        }

    async def wait_data(self):
        """Create tasks with collecting data"""

        get_network_usage_task = asyncio.create_task(self.get_network_usage())
        get_cpu_usage_task = asyncio.create_task(self.get_cpu_usage())
        self.network_usage = await asyncio.gather(get_network_usage_task)
        self.cpu_usage = await asyncio.gather(get_cpu_usage_task)

    def set_ram_free(self):
        """set ram_free class attribute"""
        self.ram_free = (
            psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        )

    async def get_cpu_usage(self):
        """set cpu_usage class attribute"""

        # Need time lag to get CPU usage info
        # to get info for all cores

        try:
            cpu_usage = psutil.cpu_percent(interval=self.monitor_period, percpu=True)
            # return average value if core used more than 2%
            core_usage_list = []

            for cpu in cpu_usage:
                if cpu > 2:
                    core_usage_list.append(cpu)
            return sum(core_usage_list) / len(core_usage_list)

        except KeyboardInterrupt:
            pass

        except ZeroDivisionError:
            return 0

    async def get_network_usage(self):
        """Set class attribute - network_usage"""

        previous_state = {
            "data": psutil.net_io_counters(pernic=True),
            "timestamp": datetime.now(),
        }
        await asyncio.sleep(self.monitor_period)
        # Refresh network usage state
        current_state = {
            "data": psutil.net_io_counters(pernic=True),
            "timestamp": datetime.now(),
        }
        network_usage = {}
        for adapter in current_state["data"]:
            down_diff = getattr(current_state["data"][adapter], "bytes_recv") - getattr(
                previous_state["data"][adapter], "bytes_recv"
            )
            up_diff = getattr(current_state["data"][adapter], "bytes_sent") - getattr(
                previous_state["data"][adapter], "bytes_sent"
            )
            time_diff = current_state["timestamp"] - previous_state["timestamp"]
            time_diff_in_seconds = time_diff.total_seconds()

            # Count bytes for period
            down = down_diff / time_diff_in_seconds
            up = up_diff / time_diff_in_seconds
            network_usage.update({adapter: {"up": up, "down": down}})

        return network_usage
