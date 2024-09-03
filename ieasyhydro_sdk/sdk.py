
from datetime import datetime

from ieasyhydro_sdk.sdk_endpoint_definitions import IEasyHydroSDKEndpointsBase, IEasyHydroHFSDKEndpointsBase
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

    def map_site_data(self, all_resources):
        response_data = []
        for resource in all_resources:
            response_data.append({
                'id': resource['id'],
                'site_code': resource['siteCode'],
                'basin': resource['basin'],
                'latitude': resource['latitude'],
                'longitude': resource['longitude'],
                'country': resource['country'],
                'is_virtual': resource['isVirtual'],
                'region': resource['region'],
                'site_type': resource['siteType'],
                'site_name': resource['siteName'],
                'organization_id': resource['sourceId'],
                'elevation': resource['elevationM'],
            })

        return response_data

    def get_discharge_sites(self):
        print(self._call_get_discharge_sites())
        all_resources = self._call_get_discharge_sites().json()['resources']
        return self.map_site_data(all_resources)

    def get_meteo_sites(self):
        all_resources = self._call_get_meteo_sites().json()['resources']
        return self.map_site_data(all_resources)

    def get_norm_for_site(self, site_code, data_type):
        response = self._call_get_norm_for_site(site_code, data_type)
        resources = response.json()['resources']
        return {
            'norm_data': resources[0]['normData'],
            'start_year': resources[0]['startYear'],
            'end_year': resources[0]['endYear'],
            'site_id': resources[0]['siteId'],
        }

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


class IEasyHydroHFSDK(IEasyHydroHFSDKEndpointsBase):
    @staticmethod
    def map_site_data(all_resources):
        response_data = []
        for resource in all_resources:
            resource_site = resource['site'] if 'site' in resource else None

            response_data.append({
                'id': resource['id'],
                'site_code': resource['station_code'],
                'site_type': resource.get('station_type'),
                'basin': {
                    'official_name': resource_site['basin']['name']
                    if resource_site else resource['basin']['name'],
                    'national_name': resource_site['basin']['secondary_name']
                    if resource_site else resource['basin']['secondary_name']
                },
                'region': {
                    'official_name': resource_site['region']['name']
                    if resource_site else resource['region']['name'],
                    'national_name': resource_site['region']['secondary_name']
                    if resource_site else resource['region']['secondary_name']
                },
                'official_name': resource['name'],
                'national_name': resource['secondary_name'],
                'country': resource_site['country'] if resource_site else resource['country'],
                'latitude': resource_site['latitude'] if resource_site else resource['latitude'],
                'longitude': resource_site['longitude'] if resource_site else resource['longitude'],
                'elevation': resource_site['country'] if resource_site else resource['country'],
                'bulletin_order': resource.get('bulletin_order'),
                'dangerous_discharge': resource.get('discharge_level_alarm'),
                'historical_discharge_minimum': resource.get('historical_discharge_minimum'),
                'historical_discharge_maximum': resource.get('historical_discharge_maximum')
            })

        return response_data

    def get_discharge_sites(self):
        print(self._call_get_discharge_sites())
        sites = self._call_get_discharge_sites().json()
        return self.map_site_data(sites)

    def get_meteo_sites(self):
        sites = self._call_get_meteo_sites().json()
        return self.map_site_data(sites)

    def get_virtual_sites(self):
        sites = self._call_get_virtual_sites().json()
        return self.map_site_data(sites)
