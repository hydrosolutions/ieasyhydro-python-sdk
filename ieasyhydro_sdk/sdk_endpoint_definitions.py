
from typing import Optional

from ieasyhydro_sdk.sdk_base import IEasyHydroSDKBase, IEasyHydroHFSDKBase
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

    def _get_norm_for_site(
            self,
            site_code,
            site_type,
            norm_type
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
        params = {
            'norm_type': norm_type
        }
        return self._call_api(
            method,
            path,
            params=params,
            paginated_endpoint=False,
        )

    def _call_get_discharge_norm_for_site(self, site_code, norm_type):
        return self._get_norm_for_site(site_code, 'hydro', norm_type)

    def _call_get_meteo_norm_for_site(self, site_code, norm_type):
        return self._get_norm_for_site(site_code, 'meteo', norm_type)

    def _call_get_discharge_sites(self, paginate=False, params=None):
        method = 'get'
        path = f'{self.organization_uuid}/hydrological'
        return self._call_gapi(
            method, path, paginated_endpoint=paginate, params=params
        )

    def _call_get_meteo_sites(self, paginate=False, params=None):
        method = 'get'
        path = f'{self.organization_uuid}/meteo'
        return self._call_api(
            method, path, paginated_endpoint=paginate, params=params
        )

    def _call_get_virtual_sites(self, paginate=False, params=None):
        method = 'get'
        path = f'{self.organization_uuid}/virtual'
        return self._call_api(
            method, path, paginated_endpoint=paginate, params=params
        )
