# IEasyHydroSDK

IEasyHydro SDK is a Python library used to simplify access to the iEasyHydro data.


## Installation

```shell
pip install git+https://github.com/hydrosolutions/ieasyhydro-python-sdk
```

## Usage

### Configuration

To use IEasyHydroSDKHF you need to configure next environment variables:


```dotenv
IEASYHYDROHF_HOST=https://hf.ieasyhydro.org/api/v1/
IEASYHYDROHF_USERNAME=username
IEASYHYDROHF_PASSWORD=password
```

We strongly recommend to create a dedicated "machine" user for API usage.

### Initialization

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

# initialize SDK (configuration will be read from environment variables)
ieasyhydro_sdk_hf = IEasyHydroHFSDK()
```

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

# initialize and configure SDK by providing configuration on class creation
ieasyhydro_hf_sdk = IEasyHydroHFSDK(
    host='https://hf.ieasyhydro.org/api/v1/',
    username='username',
    password='password',
)
```

### Sites

We can fetch details about all available discharge and meteo sites in the organization.

Example 1: Fetch discharge sites data

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

discharge_sites_data = ieasyhydro_hf_sdk.get_discharge_sites()
```

The virtual stations are separated from the discharge ones.
If you need to retrieve the virtual stations, you can do it as follows:

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

virtual_sites_data = ieasyhydro_hf_sdk.get_virtual_sites()
```

Example 2: Fetch meteo sites data

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDKHF

ieasyhydro_sdk = IEasyHydroSDKHF()

meteo_sites_data = ieasyhydro_sdk.get_meteo_sites()
```

Response example:

```python
[
    {
        'basin': {
            'national_name': '',
            'official_name': 'Иссык-Куль'
        },
        'bulletin_order': 0,
        'country': 'Кыргызстан',
        'dangerous_discharge': 100.0,
        'elevation': 0.0,
        'enabled_forecasts': {
            'daily_forecast': False,
            'decadal_forecast': False,
            'monthly_forecast': False,
            'pentad_forecast': False,
            'seasonal_forecast': False
        },
        'historical_discharge_maximum': None,
        'historical_discharge_minimum': None,
        'id': 96,
        'latitude': 42.8746,
        'longitude': 74.5698,
        'national_name': '',
        'official_name': 'Ак-Сай - с.Көк-Сай',
        'region': {
            'national_name': '',
            'official_name': 'ИССЫК-КУЛЬСКАЯ ОБЛАСТЬ'
        },
        'site_code': '15054',
        'site_type': 'manual',
        'associations': [
            {
                "name": "Ак-Терек - с.Ак-Терек",
                "id": 9,
                "uuid": "110e8400-e29b-41d4-a716-446655440000",
                "weight": 0.9,
                "station_code": "12346"
            },
            {
                "name": "Кара-Суу - с.Кара-Суу", 
                "id": 10,
                "uuid": "119e6679-7425-40de-944b-e07fc1f90ae7",
                "weight": 0.9,
                "station_code": "12345"
            }
        ],
    },
    {
        'basin': {
            'national_name': '',
            'official_name': 'Сыр-Дарья'
        },
        'bulletin_order': 0,
        'country': 'Кыргызстан',
        'dangerous_discharge': 50.2,
        'elevation': 0.0,
        'enabled_forecasts': {
            'daily_forecast': False,
            'decadal_forecast': False,
            'monthly_forecast': False,
            'pentad_forecast': False,
            'seasonal_forecast': False
        },
        'historical_discharge_maximum': None,
        'historical_discharge_minimum': None,
        'id': 78,
        'latitude': 40.214,
        'longitude': 72.529,
        'national_name': '',
        'official_name': 'Араван-Сай-к.Жаны-Ноокат',
        'region': {
            'national_name': '',
            'official_name': 'БАТКЕНСКАЯ ОБЛАСТЬ'
        },
        'site_code': '12121',
        'site_type': 'manual',
        'associations': []
    }
]

```

You will get similar response for meteo stations with the exception that the `enabled_forecasts` will be `None`.

### Norm

You can specify:

- The norm type (`discharge`, `water_level`, `precipitation`, or `temperature`)
- The norm period:
  - `d` for daily (default)
  - `p` for pentad (5-day)
  - `m` for monthly
- Whether to get norms for automatic or manual stations

Example for retrieving norms with iEasyHydroHF:

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

# Get decadal discharge norm (default)
decadal_discharge_norm = ieasyhydro_hf_sdk.get_norm_for_site("11194", "discharge")

# Get decadal water level norm (default)
decadal_water_level_norm = ieasyhydro_hf_sdk.get_norm_for_site("11194", "water_level")

# Get monthly discharge norm
monthly_norm = ieasyhydro_hf_sdk.get_norm_for_site("11194", "discharge", norm_period="m")

# Get pentad norms for automatic station
norm_data = ieasyhydro_hf_sdk.get_norm_for_site(
    site_code="11194",
    norm_type="discharge",
    norm_period="p",  # pentad (5-day) norms
    automatic=True
)

# Get monthly norms for temperature
norm_data = ieasyhydro_hf_sdk.get_norm_for_site(
    site_code="15194",
    norm_type="temperature",
    norm_period="m",  # monthly norms
    automatic=False
)

```

The data returned is a list of float values representing the norm for each period. The length of the list depends on the norm_period:

- Decadal: 36 values (3 values per month)
- Monthly: 12 values (1 value per month)
- Pentadal: 72 values (6 values per month)

Example norm data:

```python
[
    11.76306,
    11.69184,
    11.64643,
    11.61071,
    11.57296,
    11.5401,
    11.5451,
    11.54677,
    11.53255,
    11.53218,
    11.60733,
    11.7696,
    21.27225,
    31.08059,
    41.1617,
    61.32663,
    81.14099,
    110.01703,
    111.67733,
    113.4458,
    114.639,
    115.05198,
    113.84901,
    111.10554,
    81.11796,
    51.90596,
    41.43908,
    31.43042,
    21.89649,
    21.53247,
    21.32948,
    21.1932,
    21.08865,
    21.00885,
    11.92897,
    11.85072
]
```

If no norm is uploaded for the requested site code, an empty list will be returned.
If the requested site code has only partially uploaded norm data, the missing norm will
be replaced with `None` values. For example:

```
monthly_norm = ieasyhydro_hf_sdk.get_norm_for_site("12345", "discharge", norm_period="m")

print(montly_norm)

[
    2.50,
    None,
    3.75,
    0.23,
    None,
    None,
    None,
    0.45,
    0.50,
    None,
    None,
    None
]
```

### Data Values

We can fetch data for all data types stored in iEasyHydro database by using the `get_data_values_for_site()` method.
We just need to specify `site_codes` and `variable_names` we want to fetch, and function will automatically fetch all
data values from the API. It will take care to perform requests in chunks in order to avoid overloading of the server.



For iEasyHydroHF SDK, the method works slightly differently.

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK
from ieasyhydro_sdk.filters import GetHFDataValuesFilters

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

# Example 1: Get data values for multiple sites and variables
filters = {
    "site_codes": ["11159", "11100", "11200"],  # Multiple stations
    "variable_names": ["WLD", "WDD", "WLDA"],   # Multiple variables
    "local_date_time__gte": "2024-03-01T00:00:00Z",
    "local_date_time__lt": "2024-04-02T00:00:00Z"
}

response_data = ieasyhydro_hf_sdk.get_data_values_for_site(filters=filters)

# Example 2: Get temperature and precipitation measurements
meteo_filters = {
    "site_codes": ["11159", "11160"],
    "variable_names": ["ATDCA", "PDCA"],  # Air temperature and precipitation decade averages
    "local_date_time__gte": "2024-03-01T00:00:00Z"
}

meteo_data = ieasyhydro_hf_sdk.get_data_values_for_site(filters=meteo_filters)
```

### Important API Requirements

The API has specific requirements for the filters:

1. **At least one timestamp filter must be present** - You must include at least one of the timestamp filters (local or UTC) to limit the time range of the data.
2. **At least one variable name must be specified** - You must include at least one metric name in the `variable_names` parameter.

### Error Handling Examples

The SDK handles various error scenarios:

```python
# Example 3: Missing timestamp filter
filters_without_timestamp = {
    "site_codes": ["11159"],
    "variable_name": ["WLD"]
}
# This will raise an error: "At least one timestamp filter must be present"

# Example 4: Missing variable names
filters_without_variables = {
    "site_codes": ["11159"],
    "local_date_time__gte": "2024-03-01T00:00:00Z"
}
# This will raise an error: "You must specify at least one metric name"

# Example 5: Invalid variable names
filters_with_invalid_variables = {
    "site_codes": ["11159"],
    "variable_names": ["INVALID_CODE"],
    "local_date_time__gte": "2024-03-01T00:00:00Z"
}
# This will raise an error: "Invalid metric names: ['INVALID_CODE']"

# Example 6: API error response
# If the API returns an error, the SDK will return a dictionary with status code and error text
error_response = {
    'status_code': 400,
    'text': 'Bad Request: Invalid parameters'
}
```

### Response Examples

The HF SDK returns data in a paginated structure:

```python
# Example 7: Successful response with data
{
    "count": 42,  # Total number of results
    "next": "https://api.example.com/data?page=2",  # URL for next page, if available
    "previous": None,  # URL for previous page, if available
    "results": [
        {
            "station_id": 123,
            "station_uuid": "abc-123-def-456",
            "station_code": "16159",
            "station_name": "Station Name",
            "station_type": "hydro",
            "data": [
                {
                    "variable_code": "WLD",
                    "unit": "cm",
                    "values": [
                        {
                            "value": 156.0,
                            "value_type": "M",  # Manual measurement
                            "timestamp_local": "2024-03-01T08:00:00",
                            "timestamp_utc": "2024-03-01T02:00:00Z",
                            "value_code": None
                        },
                        # ... more values ...
                    ]
                },
                # ... more variables ...
            ]
        },
        # ... more stations ...
    ]
}

# Example 8: Response with non-existent station
# If a station code doesn't exist, it won't appear in the results
filters = {
    "site_codes": ["16159", "99999"],  # 99999 doesn't exist
    "variable_names": ["WLD"],
    "local_date_time__gte": "2024-03-01T00:00:00Z"
}
# Response will only include data for station 16159, 99999 will be omitted

# Example 9: Response with station that has no data
# If a station exists but has no data for the requested variables, the variables will still be included with empty values
{
    "count": 1,
    "next": None,
    "previous": None,
    "results": [
        {
            "station_id": 123,
            "station_uuid": "abc-123-def-456",
            "station_code": "16159",
            "station_name": "Station Name",
            "station_type": "hydro",
            "data": [
                {
                    "variable_code": "WLD",
                    "unit": "cm",
                    "values": []  # Empty list when no data is available
                }
            ]
        }
    ]
}
```

Available filters for the HF SDK include:

| Parameter              | Type        | Description                                 |
| ---------------------- | ----------- | ------------------------------------------- |
| `site_codes`           | `List[str]` | List of station codes to filter             |
| `site_ids`             | `List[int]` | List of station IDs to filter               |
| `variable_names`       | `List[str]` | List of metric names to filter              |
| `local_date_time__gte` | `str`       | Local timestamp greater than or equal to    |
| `local_date_time__gt`  | `str`       | Local timestamp greater than                |
| `local_date_time__lte` | `str`       | Local timestamp less than or equal to       |
| `local_date_time__lt`  | `str`       | Local timestamp less than                   |
| `local_date_time`      | `str`       | Exact local timestamp match                 |
| `utc_date_time__gte`   | `str`       | UTC timestamp greater than or equal to      |
| `utc_date_time__gt`    | `str`       | UTC timestamp greater than                  |
| `utc_date_time__lte`   | `str`       | UTC timestamp less than or equal to         |
| `utc_date_time__lt`    | `str`       | UTC timestamp less than                     |
| `utc_date_time`        | `str`       | Exact UTC timestamp match                   |
| `page`                 | `int`       | Page number for pagination                  |
| `page_size`            | `int`       | Number of items per page                    |

ATTENTION: local_date_time shouldn't include the local timezone but rather act as if it's in UTC zone so to get 8AM local metrics, use filter
local_date_time = datetime.datetime(2025, 9, 25, 8, 0, tzinfo=datetime.timezone.utc).isoformat()
To get evening 8PM metrics:
local_date_time = datetime.datetime(2025, 9, 25, 20, 0, tzinfo=datetime.timezone.utc).isoformat()

#### Available Metric Names

For hydrological measurements:

| Metric Code | Description                               | Usage                                                                    |
| ----------- | ----------------------------------------- | ------------------------------------------------------------------------ |
| `WLD`       | Water level daily                         | Most common, 8AM or 8PM water level values from KN-15 telegram           |
| `WLDA`      | Water level daily average                 | Average daily water level value, calculated from the 8AM and 8PM values  |
| `WLDC`      | Water level decadal                       | Water level value from KN-15 subgroup 966                                |
| `WLDCA`     | Water level decade average                | Decadal average water level value for a period                           |
| `WDD`       | Water discharge daily                     | Discharge value, can be an estimation based on the rating curve and water level or a measured discharge point from KN-15 telegram subgroup 966 | 
| `WDDA`      | Water discharge daily average             | Daily average discharge value calculated from the daily average water level and the rating curve |
| `WDFA`      | Water discharge fiveday average           | Pentadal average discharge value                                         |
| `WDDCA`     | Water discharge decade average            | Decadal average discharge value                                          |
| `WTO`       | Water temperature observation             | Daily water temperature from section 4 of subgroup 1 of a KN-15 telegram |
| `ATO`       | Air temperature observation               | Daily air temperature from section 4 of subgroup 1 of a KN-15 telegram   |
| `IPO`       | Ice phenomena observation                 | Complex value containing a intensity and a value code describing the phenomena |
| `PD`        | Precipitation daily                       | Complex value containing the precipitation value and a value code describing the duration of the event |
| `WTDA`      | Water temperature daily average           | Average daily water temperature                                          |
| `ATDA`      | Air temperature daily average             | Average daily air temperature                                            |
| `RCSA`      | River cross section area                  | From the subgroup 966 of the KN-15 telegram                              |

For meteorological measurements:

| Metric Code | Description                     | Usage                                                                              |
| ----------- | --------------------------------| ---------------------------------------------------------------------------------- |
| `ATDCA`     | Air temperature decade average  | Either from a manual entry or KN-15 telegram subgroup 988                          |
| `PDCA`      | Precipitation decade average    | Either from a manual entry or KN-15 telegram subgroup 988                          |
| `ATMA`      | Air temperature monthly average | Either from a manual entry or KN-15 telegram subgroup 988                          |
| `PMA`       | Precipitation monthly average   | Either from a manual entry or KN-15 telegram subgroup 988                          |

The value code can be:

| Value Code | Description                                        |
| ---------- | -------------------------------------------------  |
| `M`        | Manual measurement                                 |
| `A`        | Automatic measurement                              |
| `E`        | Estimated value                                    |
| `I`        | Imported value                                     |
| `U`        | Unknown source                                     |
| `O`        | Override value manually entered by the hydrologist |
