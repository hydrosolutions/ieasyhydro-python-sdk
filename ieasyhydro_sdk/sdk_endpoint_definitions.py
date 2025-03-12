from typing import Optional

from ieasyhydro_sdk.sdk_base import IEasyHydroSDKBase, IEasyHydroHFSDKBase
from ieasyhydro_sdk.filters import GetDataValueFilters, GetHFDataValuesFilters


class IEasyHydroSDKEndpointsBase(IEasyHydroSDKBase):

    def _call_get_norm_for_site(
            self,
            site_code,
            data_type,
    ):
        method = 'get'
        path = '/data_values/norm'
        params = {
            'site_code': site_code,
            'data_type': data_type
        }
        return self._call_api(
            method,
            path,
            params=params,
            paginated_endpoint=False,
        )

    def _call_get_data_values(
            self,
            filters: Optional[GetDataValueFilters] = None,
            page_size=None,
            offset=None,
    ):
        method = 'get'
        path = '/data_values'
        return self._call_api(
            method,
            path,
            page_size=page_size,
            offset=offset,
            params=filters
        )

    def _call_get_discharge_sites(self, paginate=False, params=None):
        method = 'get'
        path = '/discharge_sites'
        return self._call_api(
            method,
            path,
            paginated_endpoint=paginate,
            params=params
        )

    def _call_get_meteo_sites(self, paginate=False, params=None):
        method = 'get'
        path = '/meteo_sites'
        return self._call_api(
            method,
            path,
            paginated_endpoint=paginate,
            params=params,
        )


class IEasyHydroHFSDKEndpointsBase(IEasyHydroHFSDKBase):
    def _call_get_site_for_site_code(self, site_code, site_type):
        def _get_path():
            if site_type == 'hydro':
                return f'stations/{self.organization_uuid}/hydrological'
            elif site_type == 'meteo':
                return f'stations/{self.organization_uuid}/meteo'
            elif site_type == 'virtual':
                return f'stations/{self.organization_uuid}/virtual'
            else:
                return None

        method = 'get'
        path = _get_path()
        params = {
            'station_code': site_code
        }
        return self._call_api(
            method, path, params=params, paginated_endpoint=False
        )

    def _get_site_uuid_for_site_code(self, site_code, site_type):
        site_response = self._call_get_site_for_site_code(site_code, site_type)
        if site_response.status_code == 200:
            return site_response.json()[0]["uuid"]
        else:
            return None

    def _call_get_norm_for_site(
            self,
            site_code,
            site_type,
            params
    ):
        def _get_path():
            site_uuid = self._get_site_uuid_for_site_code(site_code, site_type)

            if site_type == 'hydro' and site_uuid:
                return f'hydrological-norms/{site_uuid}'
            elif site_type == 'meteo' and site_uuid:
                return f'meteorological-norms/{site_uuid}'
            else:
                return None

        method = 'get'
        path = _get_path()
        params = params
        return self._call_api(
            method,
            path,
            params=params,
            paginated_endpoint=False,
        )

    def _call_get_discharge_norm_for_site(self, site_code, norm_type="d"):
        return self._call_get_norm_for_site(
            site_code, 'hydro', {"norm_type": norm_type}
        )

    def _call_get_meteo_norm_for_site(self, site_code, norm_type="d", norm_metric="p"):
        return self._call_get_norm_for_site(
            site_code, 'meteo', {"norm_type": norm_type, "norm_metric": norm_metric}
        )

    def _call_get_discharge_sites(self, paginate=False, params=None):
        method = 'get'
        path = f'stations/{self.organization_uuid}/hydrological'
        return self._call_api(
            method, path, paginated_endpoint=paginate, params=params
        )

    def _call_get_meteo_sites(self, paginate=False, params=None):
        method = 'get'
        path = f'stations/{self.organization_uuid}/meteo'
        return self._call_api(
            method, path, paginated_endpoint=paginate, params=params
        )

    def _call_get_virtual_sites(self, paginate=False, params=None):
        method = 'get'
        path = f'stations/{self.organization_uuid}/virtual'
        return self._call_api(
            method, path, paginated_endpoint=paginate, params=params
        )
    
    def _call_get_data_values_for_site(
        self,
        site_type: str,
        filters: Optional[GetHFDataValuesFilters] = None,
        paginate: bool = False,
    ):
        """
        Call API endpoint to get data values for a specific site.
        
        Args:
            site_type: Type of station ('hydro' or 'meteo')
            station_code: Station code
            filters: Data value filters including required timestamp_local__gte and timestamp_local__lt
            paginate: Whether to use pagination
        """
        if not filters or 'timestamp_local__gte' not in filters or 'timestamp_local__lt' not in filters:
            raise ValueError("timestamp_local__gte and timestamp_local__lt are required in filters")

        method = 'get'
        
        # Prepare parameters
        params = dict(filters) if filters else {}
        
        # Build path based on site type
        if site_type == 'hydro':
            if 'view_type' not in filters or 'display_type' not in filters:
                raise ValueError("view_type and display_type are required for hydro metrics")
            path = f'metrics/{self.organization_uuid}/hydro/{filters["view_type"]}/{filters["display_type"]}'
            # Remove these from params as they're in the path
            params.pop('view_type', None)
            params.pop('display_type', None)
        elif site_type == 'meteo':
            path = f'metrics/{self.organization_uuid}/meteo'
        else:
            return None
        
        return self._call_api(
            method,
            path,
            paginated_endpoint=paginate,
            params=params,
        )
    
    def _get_station_code_for_station_id(self, station_id, site_type):
        """Get station code for a given station ID."""
        def _get_path():
            if site_type == 'hydro':
                return f'stations/{self.organization_uuid}/hydro'
            elif site_type == 'meteo':
                return f'stations/{self.organization_uuid}/meteo'
            else:
                return None

        method = 'get'
        path = _get_path()
        
        # Get all stations of this type
        response = self._call_api(method, path, paginated_endpoint=False)
        if response.status_code == 200:
            stations = response.json()
            # Find the station with matching ID
            for station in stations:
                if station.get('id') == station_id:  # This matches the 'id' field in the response
                    station_code = station.get('station_code')
                    return station_code
                # Also check related stations
                for related in station.get('related_hydro_stations', []) + station.get('related_meteo_stations', []):
                    if related.get('id') == station_id:
                        station_code = related.get('station_code')
                        return station_code
        return None

