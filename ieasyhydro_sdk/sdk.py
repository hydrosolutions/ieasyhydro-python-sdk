
from datetime import datetime

from ieasyhydro_sdk.sdk_endpoint_definitions import IEasyHydroSDKEndpointsBase
from ieasyhydro_sdk.filters import GetDataValueFilters


variable_variable_code_map = {
    'water_level_daily': '0001',
    'water_level_daily_average': '0002',
    'water_level_daily_estimation': '0003',
    'discharge_measurement': '0004',
    'discharge_daily': '0005',
    'free_river_area': '0006',
    'maximum_depth': '0007',
    'decade_discharge': '0008',
    'dangerous_discharge': '0009',
    'discharge_daily_average': '0010',
    'ice_phenomena': '0011',
    'water_level_measurement': '0012',
    'water_temperature': '0013',
    'air_temperature': '0014',
    'fiveday_discharge': '0015',
    'decade_temperature': '0016',
    'monthly_temperature': '0017',
    'decade_precipitation': '0018',
    'monthly_precipitation': '0019',
    'discharge_historical_decade_average': '0020',
}


class IEasyHydroSDK(IEasyHydroSDKEndpointsBase):

    def get_discharge_sites(self):
        return self._call_get_discharge_sites().json()['resources']

    def get_meteo_sites(self):
        return self._call_get_meteo_sites().json()['resources']

    def get_norm_for_site(self, site_code, data_type):
        response = self._call_get_norm_for_site(site_code, data_type)
        return response.json()['resources']

    def get_data_values_for_site(
            self,
            site_code,
            variable_type,
            filters=None,
    ):
        variable_code = variable_variable_code_map[variable_type]
        variable_codes = [variable_code]
        site_codes = [site_code]
        filters_ = GetDataValueFilters(
            site_codes=site_codes,
            variable_codes=variable_codes,
            include_meteo=True,
            data_value__is_no_data_value=False,
        )

        if filters:
            filters_.update(filters)

        all_values = self._get_all_pages(self._call_get_data_values(filters_, page_size=1000))

        values_prepared = []

        if not all_values:
            return []

        return_data = {
            'site': {
                'name': all_values[0]['site']['siteName'],
                'region': all_values[0]['site']['region'],
                'site_code': site_code,
                'basin': all_values[0]['site']['basin'],
                'longitude': all_values[0]['site']['longitude'],
                'latitude': all_values[0]['site']['latitude'],
            },
            'variable': {
                'variable_code': all_values[0]['variable']['variablecode'],
                'variable_name': all_values[0]['variable']['variableName']['term'],
                'unit': all_values[0]['variable']['variableUnit']['unitAbbv'],
                'variable_type': variable_type,
            }
        }

        for value in all_values:
            values_prepared.append({
                'data_value': value['dataValue'],
                'local_date_time': datetime.fromtimestamp(value['localDateTime']),
                'utc_date_time': datetime.fromtimestamp(value['dateTimeUtc']),
            })

        return_data['data_values'] = values_prepared

        return return_data
