
from typing import Optional

from ieasyhydro_sdk.sdk_base import IEasyHydroSDKBase
from ieasyhydro_sdk.filters import GetDataValueFilters


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
