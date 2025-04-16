from ieasyhydro_sdk.sdk import IEasyHydroHFSDK
from pprint import pprint

import pandas as pd

hf = IEasyHydroHFSDK()

filters = {
    "site_codes": ["15212"],
    "variable_name": ["WLD", "ATO", "WTO"],
    "local_date_time__gte": "2025-04-01T00:00:00Z",
    "local_date_time__lte": "2025-04-15T00:00:00Z",
    "view_type": "measurements",
    "display_type": "individual",
    "page_size": 100,
    "page": 1
}

data = hf.get_data_values_for_site('hydro', filters=filters)
pprint(data)

