from datetime import datetime
from typing import List, Optional, TypedDict, Literal


class BasicDataValueFilters(TypedDict, total=False):
    data_value: Optional[float]
    data_value__ne: Optional[float]
    data_value__gt: Optional[float]
    data_value__gte: Optional[float]
    data_value__lt: Optional[float]
    data_value__lte: Optional[float]
    data_value__isnull: Optional[bool]
    data_value__is_no_data_value: Optional[bool]
    local_date_time: Optional[datetime]
    local_date_time__gt: Optional[datetime]
    local_date_time__gte: Optional[datetime]
    local_date_time__lt: Optional[datetime]
    local_date_time__lte: Optional[datetime]
    utc_date_time: Optional[datetime]
    utc_date_time__gt: Optional[datetime]
    utc_date_time__gte: Optional[datetime]
    utc_date_time__lt: Optional[datetime]
    utc_date_time__lte: Optional[datetime]
    order_by: Optional[str]


class GetDataValueFilters(BasicDataValueFilters):
    site_ids: Optional[List[int]]
    site_codes: Optional[List[str]]
    include_meteo: bool
    variable_codes: Optional[List[str]]
    group_ids: Optional[List[int]]


class BasicHFDataValueFilters(TypedDict, total=False):
    local_date_time: Optional[str]
    local_date_time__gt: Optional[str]
    local_date_time__lte: Optional[str]
    local_date_time__gte: Optional[str]
    local_date_time__lt: Optional[str]
    utc_date_time: Optional[str]
    utc_date_time__gte: Optional[str]
    utc_date_time__gt: Optional[str]
    utc_date_time__lt: Optional[str]
    utc_date_time__lte: Optional[str]
    variable_names: Optional[List[str]]
    page: Optional[int]
    page_size: Optional[int]


class GetHFDataValuesFilters(BasicHFDataValueFilters):
    site_ids: Optional[List[int]]
    site_codes: Optional[List[str]]