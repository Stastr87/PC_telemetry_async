"""Saving telemetry data to local path"""

import sys

import data_operation

if __name__ == "__main__":
    while True:
        try:
            data_operation.init_collect_hw_data()
        except KeyboardInterrupt:
            sys.exit(0)
