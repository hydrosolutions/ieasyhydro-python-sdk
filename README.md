# IEasyHydroSDK

IEasyHydro SDK is a Python library used to simplify access to the iEasyHydro data.
It supports both iEasyHydro and iEasyHydroHF. At the moment, support for iEasyHydroHF
is limited to "static" data, but more functionalities will be added once the application becomes
fully operational.

## Installation

```shell
pip install git+https://github.com/hydrosolutions/ieasyhydro-python-sdk
```

## Usage

### Configuration

To use IEasyHydroSDK you need to configure next environment variables:

```dotenv
IEASYHYDRO_HOST=https://api.ieasyhydro.org
IEASYHYDRO_USERNAME=username
IEASYHYDRO_PASSWORD=password
ORGANIZATION_ID=1  # only fill if user is superadmin
```

For SDK for iEasyHydroHF, similar environment variables are required:

```dotenv
IEASYHYDROHF_HOST=https://api.ieasyhydro.org
IEASYHYDROHF_USERNAME=username
IEASYHYDROHF_PASSWORD=password
```

We strongly recommend to create a dedicated "machine" user for API usage.

### Initialization

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK, IEasyHydroHFSDK

# initialize SDK (configuration will be read from environment variables)
ieasyhydro_sdk = IEasyHydroSDK()
ieasyhydro_sdk_hf = IEasyHydroHFSDK()
```

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK, IEasyHydroHFSDK

# initialize and configure SDK by providing configuration on class creation
ieasyhydro_sdk = IEasyHydroSDK(
    host='https://api.ieasyhydro.org',
    username='username',
    password='password',
    organization_id=1,
)
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
from ieasyhydro_sdk.sdk import IEasyHydroSDK

ieasyhydro_sdk = IEasyHydroSDK()

discharge_sites_data = ieasyhydro_sdk.get_discharge_sites()
```

For the HF SDK, it's exactly the same:

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

discharge_sites_data = ieasyhydro_hf_sdk.get_discharge_sites()
```

The difference with the discharge stations is that due to different structure
of the database in iEasyHydroHF, the virtual stations are separated from the discharge ones.
If you need to retrieve the virtual stations, you can do it as follows:

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

virtual_sites_data = ieasyhydro_hf_sdk.get_virtual_sites()
```

Example 2: Fetch meteo sites data

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK

ieasyhydro_sdk = IEasyHydroSDK()

meteo_sites_data = ieasyhydro_sdk.get_meteo_sites()
```

The HF client works exactly the same.

Both methods are returning dictionary with the following structure (for the iEasyHydro SDK):

```python
[
  {
    'elevation': 0.0,
    'organization_id': 1,
    'longitude': 0.0,
    'site_name': 'Site name 1',
    'site_type': 'discharge',
    'region': 'Region 1',
    'is_virtual': False,
    'country': 'Kyrgyzstan',
    'latitude': 0.0,
    'basin': 'Basin 1',
    'id': 23,
    'site_code': '10000'
  },
  {
    'elevation': 0.0,
    'organization_id': 1,
    'longitude': 0.0,
    'site_name': 'Site name 2',
    'site_type': 'discharge',
    'region': 'Region 2',
    'is_virtual': False,
    'country': 'Kyrgyzstan',
    'latitude': 0.0,
    'basin': 'Basin 2',
    'id': 53,
    'site_code': '11000'
  },
]
```

Again, since iEasyHydro HF works differently "under the hood", there are some differences in the output
the SDK will return.

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
        'site_type': 'manual'
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
        'id': 97,
        'latitude': 40.214,
        'longitude': 72.529,
        'national_name': '',
        'official_name': 'Араван-Сай-к.Жаны-Ноокат',
        'region': {
            'national_name': '',
            'official_name': 'БАТКЕНСКАЯ ОБЛАСТЬ'
        },
        'site_code': '16158',
        'site_type': 'manual'
    }
]

```

You will get similar response for meteo stations with the exception that the `enabled_forecasts` will be `None`.

### Norm

The iEasyHydro has an API endpoint for fetching the norm for the next data types:

- `discharge`
- `temperature`
- `precitipation`

It's important to understand that iEasyHydro is calculating norm with the "cutoff" logic -
this logic is the legacy from the times when it was calculated manually on the paper.
This was used to avoid frequent manual recalculation of the norm, but to do a recalculation
every 5 years. The logic is just not considering the latest data in norm calculation, and
the cutoff year is calculated by the next python code (the `lowest_year` is the year of the
first data in the system):

```python
    def get_norm_cutoff_year(cls, lowest_year):
        current_year = datetime.datetime.now().year
        if current_year - lowest_year < 10:
            return current_year

        return (current_year / 5) * 5
```

Example 1:

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK

ieasyhydro_sdk = IEasyHydroSDK()

norm_data = ieasyhydro_sdk.get_norm_for_site(
    site_code='15212',
    data_type='discharge')
```

The method is returning dictionary with the following structure:

```python
{
    'norm_data': [
      2.02,
      1.88,
      1.69,
      1.65,
      1.72,
      1.6,
      1.69,
      1.61,
      1.5,
      1.42,
      1.51,
      1.61,
      1.64,
      2.31,
      3.76,
      10.2,
      13.3,
      13.6,
      13.9,
      11.0,
      12.1,
      12.6,
      9.21,
      6.13,
      4.68,
      3.7,
      2.6,
      2.82,
      2.36,
      2.09,
      2.05,
      2.3,
      2.5,
      2.44,
      2.35,
      2.02
    ],
    'end_year': 2020,
    'site_id': 10,
    'start_year': 2013
}

```

As norms also work differently in iEasyHydroHF, the output you get when requesting norms from its SDK is slightly different.
iEasyHydroHF only works with the current norm values, instead of calculating it from norm data for all the previous years
which also means the "cutoff" logic described above isn't relevant here.
For iEasyHydroHF, you can specify:

- The norm type (`discharge`, `precipitation`, or `temperature`)
- The norm period:
  - `d` for daily (default)
  - `p` for pentad (5-day)
  - `m` for monthly
- Whether to get norms for automatic or manual stations

Example for retrieving norms with iEasyHydroHF:

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

# Get decadal norm (default)
decadal_norm = ieasyhydro_hf_sdk.get_norm_for_site("15194", "discharge")

# Get monthly norm
monthly_norm = ieasyhydro_hf_sdk.get_norm_for_site("15194", "discharge", norm_period="m")

# Get pentad norms for automatic station
norm_data = ieasyhydro_hf_sdk.get_norm_for_site(
    site_code="15194",
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
    1.76306,
    1.69184,
    1.64643,
    1.61071,
    1.57296,
    1.5401,
    1.5451,
    1.54677,
    1.53255,
    1.53218,
    1.60733,
    1.7696,
    2.27225,
    3.08059,
    4.1617,
    6.32663,
    8.14099,
    10.01703,
    11.67733,
    13.4458,
    14.639,
    15.05198,
    13.84901,
    11.10554,
    8.11796,
    5.90596,
    4.43908,
    3.43042,
    2.89649,
    2.53247,
    2.32948,
    2.1932,
    2.08865,
    2.00885,
    1.92897,
    1.85072
]
```

If no norm is uploaded for the requested site code, an empty list will be returned.
If the requested site code has only partially uploaded norm data, the missing norm will
be replaced with `None` values. For example:

```
monthly_norm = ieasyhydro_hf_sdk.get_norm_for_site("15194", "discharge", norm_period="m")

print(montly_norm)

[
    1.50,
    None,
    1.75,
    2.23,
    None,
    None,
    None,
    6.45,
    7.50,
    None,
    None,
    None
]
```

### Data Values

We can fetch data for all data types stored in iEasyHydro database by using the `get_data_values_for_site()` method.
We just need to specify `site_code` and `variable_type` we want to fetch, and function will automatically fetch all
data values from the API. It will take care to perform requests in chunks in order to avoid overloading of the server.

**IMPORTANT
At this time, iEasyHydro HF still doesn't provide the interface for retrieving the data values. As soon as it is in
operational use, the library will be updated to provide support for this as well.**

Examples 1: Fetch all daily discharge values

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK

ieasyhydro_sdk = IEasyHydroSDK()

response_data = ieasyhydro_sdk.get_data_values_for_site('15212', 'discharge_daily')
```

Example 2: Fetch all historical decade averages

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK

ieasyhydro_sdk = IEasyHydroSDK()

response_data = ieasyhydro_sdk.get_data_values_for_site('15212', 'discharge_historical_decade_average')
```

Example 3: Fetch all discharge measurements measured after 2018-01-01

```python
import datetime

from ieasyhydro_sdk.sdk import IEasyHydroSDK
from ieasyhydro_sdk.filters import BasicDataValueFilters

ieasyhydro_sdk = IEasyHydroSDK()

filters = BasicDataValueFilters(
    local_date_time__gt=datetime.datetime(2018, 1, 1)
)

response_data = ieasyhydro_sdk.get_data_values_for_site(
    '15212',
    'discharge_historical_decade_average',
    filters=filters
)
```

You can find all variable types listed here:

| Variable type                       | Description |
| ----------------------------------- | ----------- |
| water_level_daily                   |             |
| water_level_daily_average           |             |
| water_level_daily_estimation        |             |
| discharge_measurement               |             |
| discharge_daily                     |             |
| free_river_area                     |             |
| maximum_depth                       |             |
| decade_discharge                    |             |
| dangerous_discharge                 |             |
| discharge_daily_average             |             |
| ice_phenomena                       |             |
| water_level_measurement             |             |
| water_temperature                   |             |
| air_temperature                     |             |
| fiveday_discharge                   |             |
| decade_temperature                  |             |
| monthly_temperature                 |             |
| decade_precipitation                |             |
| monthly_precipitation               |             |
| discharge_historical_decade_average |             |

Available filters are described here:

| Parameter                      | Type                 | Description                                                                                          |
| ------------------------------ | -------------------- | ---------------------------------------------------------------------------------------------------- |
| `data_value`                   | `float`, optional    | Only include data with specified data value                                                          |
| `data_value__ne`               | `float`, optional    | Excludes the specified data value                                                                    |
| `data_value__gt`               | `float`, optional    | Data values greater than the specified value                                                         |
| `data_value__gte`              | `float`, optional    | Data values greater than or equal to the specified value                                             |
| `data_value__lt`               | `float`, optional    | Data values less than the specified value                                                            |
| `data_value__lte`              | `float`, optional    | Data values less than or equal to the specified value                                                |
| `data_value__isnull`           | `bool`, optional     | Whether the data value is null                                                                       |
| `data_value__is_no_data_value` | `bool`, optional     | Whether the data value is not a data value                                                           |
| `local_date_time`              | `datetime`, optional | Specific local date and time to filter the results                                                   |
| `local_date_time__gt`          | `datetime`, optional | Local date and time greater than the specified value                                                 |
| `local_date_time__gte`         | `datetime`, optional | Local date and time greater than or equal to the specified value                                     |
| `local_date_time__lt`          | `datetime`, optional | Local date and time less than the specified value                                                    |
| `local_date_time__lte`         | `datetime`, optional | Local date and time less than or equal to the specified value                                        |
| `utc_date_time`                | `datetime`, optional | Specific UTC date and time to filter the results                                                     |
| `utc_date_time__gt`            | `datetime`, optional | UTC date and time greater than the specified value                                                   |
| `utc_date_time__gte`           | `datetime`, optional | UTC date and time greater than or equal to the specified value                                       |
| `utc_date_time__lt`            | `datetime`, optional | UTC date and time less than the specified value                                                      |
| `utc_date_time__lte`           | `datetime`, optional | UTC date and time less than or equal to the specified value                                          |
| `order_by`                     | `str`, optional      | Name of the column we want to order data. Suported ordering `local_date_time` and `-local_date_time` |

The method is returning dictionary with the following structure:

```python
{
  'site': {
    'name': 'р.Ак-Суу с.Чон-Арык',
    'region': 'ЧУЙСКАЯ ОБЛАСТЬ',
    'site_code': '15212',
    'basin': 'Чу',
    'longitude': 74.008333,
    'latitude': 42.613889
  },
  'variable': {
    'variable_code': '0020',
    'variable_name': 'Discharge',
    'unit': 'm^3/s',
    'variable_type': 'discharge_historical_decade_average'
  },
  'data_values': [
    {
      'data_value': 2.02,
      'local_date_time': datetime .datetime (2013, 1, 5, 13, 0),
      'utc_date_time': datetime .datetime (2013, 1, 5, 13, 0)
    },
    {
      'data_value': 1.88,
      'local_date_time': datetime .datetime (2013, 1, 15, 13, 0),
      'utc_date_time': datetime .datetime (2013, 1, 15, 13, 0)
    },
    {
      'data_value': 1.69,
      'local_date_time': datetime .datetime (2013, 1, 25, 13, 0),
      'utc_date_time': datetime .datetime (2013, 1, 25, 13, 0)
    },
  ]
}
```

For iEasyHydroHF SDK, the method works slightly differently. You specify the site type ('hydro' or 'meteo') and can use filters to narrow down the results:

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK
from ieasyhydro_sdk.filters import GetHFDataValuesFilters

ieasyhydro_hf_sdk = IEasyHydroHFSDK()

# Example 1: Get multiple types of water level and discharge measurements
filters = {
    "site_codes": ["16159", "16100", "16200"],  # Multiple stations
    "variable_name": [
        "WLD",   # Water level daily
        "WDD",   # Water discharge daily
        "WLDA",  # Water level daily average
    ],
    "local_date_time__gte": "2024-03-01",
    "local_date_time__lt": "2024-04-01",
    "view_type": "measurements",
    "display_type": "individual"
}

response_data = ieasyhydro_hf_sdk.get_data_values_for_site("hydro", filters=filters)

# Example 2: Get temperature and precipitation measurements
meteo_filters = {
    "site_codes": ["16159", "16160"],
    "variable_name": [
        "ATDCA",   # Air temperature decade average
        "PDCA",   # Precipitation decade average
    ],
    "local_date_time__gte": "2024-03-01"
}

meteo_data = ieasyhydro_hf_sdk.get_data_values_for_site("meteo", filters=meteo_filters)
```

The HF SDK returns data in a similar structure but with some differences:

```python
[
    {
        'site': {
            'site_id': 123,
            'site_code': '16159',
            'site_uuid': 'abc-123-def-456',
        },
        'variable': {
            'variable_code': 'WLD',
            'unit': 'cm',
            'variable_type': 'M',
        },
        'data_values': [
            {
                'data_value': 156.0,
                'local_date_time': datetime(2024, 3, 1, 8, 0),
                'value_code': None,
            },
            // ... more values ...
        ]
    },
    // ... more stations ...
]
```

Available filters for the HF SDK include:

| Parameter              | Type        | Description                                 |
| ---------------------- | ----------- | ------------------------------------------- |
| `view_type`            | `str`       | Type of view ('daily' or 'measurements')    |
| `display_type`         | `str`       | Type of display ('individual' or 'grouped') |
| `site_codes`           | `List[str]` | List of station codes to filter             |
| `site_ids`             | `List[int]` | List of station IDs to filter               |
| `variable_name`        | `List[str]` | List of metric names to filter              |
| `local_date_time__gte` | `str`       | Timestamp greater than or equal to          |
| `local_date_time__lt`  | `str`       | Timestamp less than                         |
| `local_date_time`      | `str`       | Exact timestamp match                       |
| `data_value__gt`       | `float`     | Value greater than                          |
| `data_value__gte`      | `float`     | Value greater than or equal to              |
| `data_value__lt`       | `float`     | Value less than                             |
| `data_value__lte`      | `float`     | Value less than or equal to                 |
| `order_by`             | `str`       | Field to order by                           |
| `order_direction`      | `str`       | Direction of ordering                       |
| `page`                 | `int`       | Page number for pagination                  |
| `page_size`            | `int`       | Number of items per page                    |

#### Available Metric Names

For hydrological measurements:

| Metric Code | Description                               |
| ----------- | ----------------------------------------- |
| `WLD`       | Water level daily                         |
| `WLDA`      | Water level daily average                 |
| `WLDC`      | Water level decadal                       |
| `WLDCA`     | Water level decade average                |
| `WDD`       | Water discharge daily                     |
| `WDDA`      | Water discharge daily average             |
| `WDFA`      | Water discharge fiveday average           |
| `WDDCA`     | Water discharge decade average            |
| `WDDCAH`    | Water discharge decade average historical |
| `WTO`       | Water temperature observation             |
| `ATO`       | Air temperature observation               |
| `IPO`       | Ice phenomena observation                 |
| `PD`        | Precipitation daily                       |
| `WTDA`      | Water temperature daily average           |
| `ATDA`      | Air temperature daily average             |
| `RCSA`      | River cross section area                  |
| `MD`        | Maximum depth                             |

For meteorological measurements:

| Metric Code | Description                     |
| ----------- | ------------------------------- |
| `ATDCA`     | Air temperature decade average  |
| `PDCA`      | Precipitation decade average    |
| `ATMA`      | Air temperature monthly average |
| `PMA`       | Precipitation monthly average   |

The value code can be:

| Value Code | Description           |
| ---------- | --------------------- |
| `M`        | Manual measurement    |
| `A`        | Automatic measurement |
| `E`        | Estimated value       |
| `I`        | Imported value        |
| `U`        | Unknown source        |
