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
    def _call_get_site_for_site_code(self, site_code, site_type, station_type=None):
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
        
        # Add station_type to params if provided
        if station_type:
            params['station_type'] = station_type
        
        return self._call_api(
            method, path, params=params, paginated_endpoint=False
        )

    def _get_site_uuid_for_site_code(self, site_code, site_type, station_type="M"):
        """Get site UUID for a given site code and type.
        
        Args:
            site_code: Station code
            site_type: Type of site ('hydro' or 'meteo')
            station_type: Type of station ('A' for automatic or 'M' for manual, default 'M')
        """
        site_response = self._call_get_site_for_site_code(site_code, site_type, station_type)
        if site_response.status_code == 200:
            sites = site_response.json()
            # Filter by station type
            for site in sites:
                if site.get('station_type') == station_type:
                    return site.get('uuid')
            # If no match with station_type, return first site's UUID as fallback
            if sites:
                print(f"Warning: No site found with station_type={station_type}, using first available site")
                return sites[0].get('uuid')
        return None

    def _call_get_norm_for_site(
            self,
            site_code,
            site_type,
            params,
            station_type="M"
    ):
        def _get_path():
            site_uuid = self._get_site_uuid_for_site_code(site_code, site_type, station_type)

            if site_type == 'hydro' and site_uuid:
                return f'hydrological-norms/{site_uuid}'
            elif site_type == 'meteo' and site_uuid:
                return f'meteorological-norms/{site_uuid}'
            else:
                return None

        method = 'get'
        path = _get_path()
        return self._call_api(
            method,
            path,
            params=params,
            paginated_endpoint=False,
        )

    def _call_get_discharge_norm_for_site(self, site_code, norm_type="d", station_type="M"):
        return self._call_get_norm_for_site(
            site_code, 'hydro', {"norm_type": norm_type}, station_type
        )

    def _call_get_meteo_norm_for_site(self, site_code, norm_type="d", norm_metric="p", station_type="M"):
        return self._call_get_norm_for_site(
            site_code, 'meteo', {"norm_type": norm_type, "norm_metric": norm_metric}, station_type
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
            filters: Data value filters
            paginate: Whether to use pagination
        """
        if not filters:
            raise ValueError("Filters are required")
        
        # Check if at least one timestamp filter is present
        timestamp_filters = [f for f in filters if f.startswith('timestamp')]
        if not timestamp_filters:
            raise ValueError("At least one timestamp filter is required")

        method = 'get'
        
        # Prepare parameters
        params = dict(filters) if filters else {}
        
        # todo construct path based on site type and variable names
        # or even better move the complexity to the backend and handle it there
        
        return self._call_api(
            method,
            path,
            paginated_endpoint=paginate,
            params=params,
        )
    
    def _ensure_norm_data_has_correct_length(self, norm_data, norm_period):
        period_lengths = {
            'd': 36,  # Daily - 36 values (3 per month)
            'm': 12,  # Monthly - 12 values
            'p': 72   # Pentad - 72 values (6 per month)
        }

        if not norm_data:
            return []
        
        if norm_period not in period_lengths:
            raise ValueError(f"Invalid norm period '{norm_period}'. Must be one of: {', '.join(period_lengths.keys())}")
            
        target_length = period_lengths[norm_period]
        
        normalized_data = [None] * target_length
        
        for i, value in enumerate(norm_data[:target_length]):
            normalized_data[i] = value
            
        return normalized_data
            