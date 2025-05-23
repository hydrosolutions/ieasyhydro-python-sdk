from datetime import datetime

from ieasyhydro_sdk.sdk_endpoint_definitions import IEasyHydroSDKEndpointsBase, IEasyHydroHFSDKEndpointsBase
from ieasyhydro_sdk.filters import GetDataValueFilters, GetHFDataValuesFilters


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
    def _resolve_station_type(station_type):
        match station_type:
            case 'M':
                return 'manual'
            case 'A':
                return 'automatic'
            case 'V':
                return 'virtual'
            case None:
                return 'meteo'
            case _:
                return None

    @staticmethod
    def _resolve_forecast_status(station):
        if station.get("station_type") in ['A', 'M', 'V']:
            return {
                'daily_forecast': station['daily_forecast'],
                'pentad_forecast': station['pentad_forecast'],
                'decadal_forecast': station['decadal_forecast'],
                'monthly_forecast': station['monthly_forecast'],
                'seasonal_forecast': station['seasonal_forecast'],
            }

        return None

    def map_site_data(self, all_resources):
        response_data = []
        for index, resource in enumerate(all_resources):
            resource_site = resource['site'] if 'site' in resource else None
            site_type = self._resolve_station_type(resource.get('station_type'))

            response_data.append({
                'id': resource['id'],
                'site_code': resource['station_code'],
                'site_type': site_type,
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
                'elevation': resource_site['elevation'] if resource_site else resource['elevation'],
                'bulletin_order': resource.get('bulletin_order'),
                'dangerous_discharge': resource.get('discharge_level_alarm'),
                'historical_discharge_minimum': resource.get('historical_discharge_minimum'),
                'historical_discharge_maximum': resource.get('historical_discharge_maximum'),
                'enabled_forecasts': self._resolve_forecast_status(resource),
            })

            if site_type == 'virtual':
                response_data[index]['associations'] = resource.get('associations')

        return response_data

    def get_discharge_sites(self):
        sites_response = self._call_get_discharge_sites()
        if sites_response.status_code == 200:
            return self.map_site_data(sites_response.json())
        else:
            raise ValueError(f"Could not retrieve discharge sites, got status code {sites_response.status_code}")

    def get_meteo_sites(self):
        sites_response = self._call_get_meteo_sites()
        if sites_response.status_code == 200:
            return self.map_site_data(sites_response.json())
        else:
            raise ValueError(f"Could not retrieve meteo sites, got status code {sites_response.status_code}")

    def get_virtual_sites(self):
        sites_response = self._call_get_virtual_sites()
        if sites_response.status_code == 200:
            return self.map_site_data(sites_response.json())
        else:
            raise ValueError(f"Could not retrieve virtual sites, got status code {sites_response.status_code}")

    def get_norm_for_site(self, site_code, norm_type, norm_period="d", automatic=False):
        """
        Get norm data for a site.
        
        Args:
            site_code: Station code
            norm_type: Type of norm ('discharge', 'precipitation', or 'temperature')
            norm_period: Period for norm data ('d' for daily, default)
            automatic: If True, get norms for automatic stations, if False for manual (default False)
        """
        station_type = 'A' if automatic else 'M'
        
        match norm_type:
            case 'discharge':
                norm_response = self._call_get_discharge_norm_for_site(site_code, norm_period, station_type)
            case 'precipitation':
                norm_response = self._call_get_meteo_norm_for_site(site_code, norm_period, 'p', station_type)
            case 'temperature':
                norm_response = self._call_get_meteo_norm_for_site(site_code, norm_period, 't', station_type)
            case _:
                raise ValueError(f"Can only retrieve discharge, precipitation or temperature norms, got {norm_type}")

        if norm_response.status_code == 200:
            return self._ensure_norm_data_has_correct_length(
                [float(entry["value"]) for entry in norm_response.json()],
                norm_period
            )
        else:
            raise ValueError(
                f"Could not retrieve {norm_type} norm for site {site_code}, got status code {norm_response.status_code}"
            )

    def get_data_values_for_site(self, filters: GetHFDataValuesFilters = None):
        filters = {
            'view_type': 'measurements',
            'display_type': 'individual',
            **filters
        }
        api_filters = self._map_filters(filters) if filters else {}
        response = self._call_get_data_values_for_site(filters=api_filters)
        if not response or response.status_code != 200:
            return {
                'status_code': response.status_code,
                'text': response.text
            }

        return response.json()
