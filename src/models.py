from typing import Optional

from pydantic import Field, BaseModel


class NowWeather(BaseModel):
    observation_time: str = Field(alias='obsTime', description='数据时间')
    temperature: int = Field(alias='temp', description='温度，摄氏度')
    feels_temperature: int = Field(
        alias='feelsLike',
        description='体感温度，默认单位：摄氏度',
    )
    icon: int = Field(alias='icon', description='天气状况的图标代码')
    weather_description: str = Field(alias='text', description='天气状况')
    wind_degress: int = Field(alias='wind360', description='风向360角度')
    wind_direction: str = Field(alias='windDir', description='风向')
    wind_scale: int = Field(alias='windScale', description='风力等级')
    wind_speed: int = Field(alias='windSpeed', description='风速，公里/小时')
    humidity: int = Field(alias='humidity', description='相对湿度，百分比')
    precipitation: float = Field(
        alias='precip',
        description='当前小时累计降水量，默认单位：毫米',
    )
    pressure: int = Field(alias='pressure', description='大气压强，百帕')
    visual_distance: int = Field(alias='vis', description='能见度，公里')
    cloud_amount: Optional[int] = Field(
        default=None,
        alias='cloud',
        description='云量，百分比数值。可能为空',
    )
    dew_temperature: Optional[int] = Field(
        default=None,
        alias='dew',
        description='露点温度。可能为空',
    )


class CityInfo(BaseModel):
    name: str = Field(description='地区/城市名称')
    city_id: int = Field(description='地区/城市ID')
    latitude: float = Field(alias='lat', description='地区/城市纬度')
    logtitude: float = Field(alias='lon', description='地区/城市经度')
    superior_adm: str = Field(alias='adm2', description='上级行政区划名称')
    self_adm: str = Field(alias='adm1', description='所属一级行政区域')
    country: str = Field(description='地区/城市所属国家名称')
    timezone: str = Field(alias='tz', description='地区/城市所在时区')
    utc_offset: str = Field(
        alias='utcOffset',
        description='地区/城市目前与UTC时间偏移的小时数',
    )
    is_daylight_saving: bool = Field(
        alias='isDst',
        description='地区/城市是否当前处于夏令时',
    )
    city_type: str = Field(description='地区/城市的属性')
    rank: int = Field(description='地区评分')
    fix_link: str = Field(alias='fxLink', description='天气预报网页链接')
