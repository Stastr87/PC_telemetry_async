from pprint import pprint

from stored_data_operation import DataObject

tab = DataObject("2025-01-06T00:33:00", "2025-01-08T02:07:00")
with open('output.csv', 'w', encoding="utf-8") as file:
    file.write(str(tab.get_csv_data()))

# pprint(tab.search_data())