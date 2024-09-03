
# IEasyHydroSDK

IEasyHydro SDK is a Python library used to simplify access to the iEasyHydro data.

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
IEASYHYDRO_PASSWORD=passwoord
ORGANIZATION_ID=1 # only fill if user is superadmin
```

We strongly recommend to create a dedicated "machine" user for API usage.

### Initialization

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK

# initialize SDK (configuration will be read from environment variables)
ieasyhydro_sdk = IEasyHydroSDK()
```

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK

# initialize and configure SDK by providing configuration on class creation
ieasyhydro_sdk = IEasyHydroSDK(
    host='https://api.ieasyhydro.org',
    username='username',
    password='password',
    organization_id=1,
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

Example 2: Fetch meteo sites data

```python
from ieasyhydro_sdk.sdk import IEasyHydroSDK

ieasyhydro_sdk = IEasyHydroSDK()

meteo_sites_data = ieasyhydro_sdk.get_meteo_sites()
```

Both methods are returning dictionary with the following structure:

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

### Data Values

We can fetch data for all data types stored in iEasyHydro database by using the `get_data_values_for_site()` method. 
We just need to specify `site_code` and `variable_type` we want to fetch, and function will automatically fetch all
data values from the API. It will take care to perform requests in chunks in order to avoid overloading of the server.

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
|-------------------------------------|-------------|
| water_level_daily                   | |
| water_level_daily_average           | |
| water_level_daily_estimation        | |
| discharge_measurement               | |
| discharge_daily                     | |
| free_river_area                     | |
| maximum_depth                       | |
| decade_discharge                    | |
| dangerous_discharge                 | |
| discharge_daily_average             | |
| ice_phenomena                       | |
| water_level_measurement             | |
| water_temperature                   | |
| air_temperature                     | |
| fiveday_discharge                   | |
| decade_temperature                  | |
| monthly_temperature                 | |
| decade_precipitation                | |
| monthly_precipitation               | |
| discharge_historical_decade_average | |


Available filters are described here:

| Parameter | Type | Description                                                           |
|-----------|------|-----------------------------------------------------------------------|
| `data_value` | `float`, optional | Only include data with specified data value                            |
| `data_value__ne` | `float`, optional | Excludes the specified data value                                     |
| `data_value__gt` | `float`, optional | Data values greater than the specified value                          |
| `data_value__gte` | `float`, optional | Data values greater than or equal to the specified value              |
| `data_value__lt` | `float`, optional | Data values less than the specified value                             |
| `data_value__lte` | `float`, optional | Data values less than or equal to the specified value                 |
| `data_value__isnull` | `bool`, optional | Whether the data value is null                                        |
| `data_value__is_no_data_value` | `bool`, optional | Whether the data value is not a data value                            |
| `local_date_time` | `datetime`, optional | Specific local date and time to filter the results                    |
| `local_date_time__gt` | `datetime`, optional | Local date and time greater than the specified value                  |
| `local_date_time__gte` | `datetime`, optional | Local date and time greater than or equal to the specified value      |
| `local_date_time__lt` | `datetime`, optional | Local date and time less than the specified value                     |
| `local_date_time__lte` | `datetime`, optional | Local date and time less than or equal to the specified value         |
| `utc_date_time` | `datetime`, optional | Specific UTC date and time to filter the results                      |
| `utc_date_time__gt` | `datetime`, optional | UTC date and time greater than the specified value                    |
| `utc_date_time__gte` | `datetime`, optional | UTC date and time greater than or equal to the specified value        |
| `utc_date_time__lt` | `datetime`, optional | UTC date and time less than the specified value                       |
| `utc_date_time__lte` | `datetime`, optional | UTC date and time less than or equal to the specified value           |
| `order_by` | `str`, optional | Name of the column we want to order data. Suported ordering `local_date_time` and `-local_date_time` |




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

