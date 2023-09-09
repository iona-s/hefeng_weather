from datetime import datetime
from typing import Literal, Optional

from pydantic import Field, BaseModel


class ConfigedBaseModel(BaseModel):
    """配置化的基础模型"""

    class Config:
        """配置"""

        allow_population_by_field_name = True


class CityInfo(ConfigedBaseModel):
    """城市信息"""

    name: str = Field(description='地区/城市名称')
    city_id: str = Field(alias='id', description='地区/城市ID')
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
    city_type: str = Field(alias='type', description='地区/城市的属性')
    rank: int = Field(description='地区评分')
    fix_link: str = Field(alias='fxLink', description='天气预报网页链接')


class CityWeatherApi:
    """城市天气系列api"""

    class NowWeather(ConfigedBaseModel):
        """当前天气"""

        observation_time: datetime = Field(
            alias='obsTime',
            description='数据时间',
        )
        temperature: int = Field(alias='temp', description='温度，摄氏度')
        feels_temperature: int = Field(
            alias='feelsLike',
            description='体感温度，摄氏度',
        )
        icon: int = Field(alias='icon', description='天气状况的图标代码')
        weather_description: str = Field(alias='text', description='天气状况')
        wind_degress: int = Field(alias='wind360', description='风向360角度')
        wind_direction: str = Field(alias='windDir', description='风向')
        wind_scale: int = Field(alias='windScale', description='风力等级')
        wind_speed: int = Field(
            alias='windSpeed',
            description='风速，公里/小时',
        )
        humidity: int = Field(alias='humidity', description='相对湿度，百分比')
        precipitation: float = Field(
            alias='precip',
            description='当前小时累计降水量，毫米',
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

    class DailyWeather(ConfigedBaseModel):
        """每日天气"""

        date: datetime = Field(alias='fxDate', description='预报日期')
        sunrise: Optional[datetime] = Field(
            default=None,
            alias='sunrise',
            description='日出时间，在高纬度地区可能为空',
        )
        sunset: Optional[datetime] = Field(
            default=None,
            alias='sunset',
            description='日落时间，在高纬度地区可能为空',
        )
        moonrise: Optional[datetime] = Field(
            default=None,
            alias='moonrise',
            description='当天月升时间，可能为空',
        )
        moonset: Optional[datetime] = Field(
            default=None,
            alias='moonset',
            description='当天月落时间，可能为空',
        )
        moon_phase: str = Field(alias='moonPhase', description='月相名称')
        moon_phase_icon: int = Field(
            alias='moonPhaseIcon',
            description='月相图标代码',
        )
        temperature_max: int = Field(
            alias='tempMax',
            description='预报当天最高温度',
        )
        temperature_min: int = Field(
            alias='tempMin',
            description='预报当天最低温度',
        )
        icon_day: int = Field(
            alias='iconDay',
            description='预报白天天气状况的图标代码',
        )
        weather_description_day: str = Field(
            alias='textDay',
            description='预报白天天气状况文字描述，包括阴晴雨雪等天气状态的描述',
        )
        icon_night: int = Field(
            alias='iconNight',
            description='预报夜间天气状况的图标代码',
        )
        weather_description_night: str = Field(
            alias='textNight',
            description='预报晚间天气状况文字描述，包括阴晴雨雪等天气状态的描述',
        )
        wind_degress_day: int = Field(
            alias='wind360Day',
            description='预报白天风向360角度',
        )
        wind_direction_day: str = Field(
            alias='windDirDay',
            description='预报白天风向',
        )
        wind_scale_day: int = Field(
            alias='windScaleDay',
            description='预报白天风力等级',
        )
        wind_speed_day: int = Field(
            alias='windSpeedDay',
            description='预报白天风速，公里/小时',
        )
        wind_degress_night: int = Field(
            alias='wind360Night',
            description='预报夜间风向360角度',
        )
        wind_direction_night: str = Field(
            alias='windDirNight',
            description='预报夜间当天风向',
        )
        wind_scale_night: int = Field(
            alias='windScaleNight',
            description='预报夜间风力等级',
        )
        wind_speed_night: int = Field(
            alias='windSpeedNight',
            description='预报夜间风速，公里/小时',
        )
        precipitation: float = Field(
            alias='precip',
            description='预报当天总降水量，毫米',
        )
        uv_index: int = Field(alias='uvIndex', description='紫外线强度指数')
        humidity: int = Field(
            alias='humidity',
            description='相对湿度，百分比数值',
        )
        pressure: int = Field(
            alias='pressure',
            description='大气压强，百帕',
        )
        visual_distance: int = Field(
            alias='vis',
            description='能见度，公里',
        )
        cloud_amount: Optional[int] = Field(
            default=None,
            alias='cloud',
            description='云量，百分比数值。可能为空',
        )

    class HourlyWeather(ConfigedBaseModel):
        """小时天气"""

        time: datetime = Field(alias='fxTime', description='预报时间')
        temperature: int = Field(alias='temp', description='温度，摄氏度')
        icon: int = Field(alias='icon', description='天气状况的图标代码')
        weather_description: str = Field(alias='text', description='天气状况')
        wind_degress: int = Field(alias='wind360', description='风向360角度')
        wind_direction: str = Field(alias='windDir', description='风向')
        wind_scale: int = Field(alias='windScale', description='风力等级')
        wind_speed: int = Field(
            alias='windSpeed',
            description='风速，公里/小时',
        )
        humidity: int = Field(alias='humidity', description='相对湿度，百分比')
        precipitation: float = Field(
            alias='precip',
            description='当前小时累计降水量，毫米',
        )
        precipitation_probability: Optional[int] = Field(
            default=None,
            alias='pop',
            description='逐小时预报降水概率，百分比数值，可能为空',
        )
        pressure: int = Field(alias='pressure', description='大气压强，百帕')
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


class BlockWeatherApi:
    """格点天气系列api"""

    class NowWeather(ConfigedBaseModel):
        """当前天气"""

        time: datetime = Field(alias='obsTime', description='数据观测时间')
        temperature: int = Field(
            alias='temp',
            description='温度，默认单位：摄氏度',
        )
        icon: int = Field(
            alias='icon',
            description='天气状况的图标代码',
        )
        weather_description: str = Field(
            alias='text',
            description='天气状况的文字描述，包括阴晴雨雪等天气状态的描述',
        )
        wind_degress: int = Field(alias='wind360', description='风向360角度')
        wind_direction: str = Field(alias='windDir', description='风向')
        wind_scale: int = Field(alias='windScale', description='风力等级')
        wind_speed: int = Field(
            alias='windSpeed',
            description='风速，公里/小时',
        )
        humidity: int = Field(
            alias='humidity',
            description='相对湿度，百分比数值',
        )
        precipitation: float = Field(
            alias='precip',
            description='当前小时累计降水量，毫米',
        )
        pressure: int = Field(
            alias='pressure',
            description='大气压强，百帕',
        )
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

    class DailyWeather(ConfigedBaseModel):
        """每日天气"""

        date: datetime = Field(alias='fxDate', description='预报日期')
        temperature_max: int = Field(
            alias='tempMax',
            description='预报当天最高温度',
        )
        temperature_min: int = Field(
            alias='tempMin',
            description='预报当天最低温度',
        )
        icon_day: int = Field(
            alias='iconDay',
            description='预报白天天气状况的图标代码',
        )
        weather_description_day: str = Field(
            alias='textDay',
            description='预报白天天气状况文字描述，包括阴晴雨雪等天气状态的描述',
        )
        icon_night: int = Field(
            alias='iconNight',
            description='预报夜间天气状况的图标代码',
        )
        weather_description_night: str = Field(
            alias='textNight',
            description='预报晚间天气状况文字描述，包括阴晴雨雪等天气状态的描述',
        )
        wind_degress_day: int = Field(
            alias='wind360Day',
            description='预报白天风向360角度',
        )
        wind_direction_day: str = Field(
            alias='windDirDay',
            description='预报白天风向',
        )
        wind_scale_day: int = Field(
            alias='windScaleDay',
            description='预报白天风力等级',
        )
        wind_speed_day: int = Field(
            alias='windSpeedDay',
            description='预报白天风速，公里/小时',
        )
        wind_degress_night: int = Field(
            alias='wind360Night',
            description='预报夜间风向360角度',
        )
        wind_direction_night: str = Field(
            alias='windDirNight',
            description='预报夜间当天风向',
        )
        wind_scale_night: int = Field(
            alias='windScaleNight',
            description='预报夜间风力等级',
        )
        wind_speed_night: int = Field(
            alias='windSpeedNight',
            description='预报夜间风速，公里/小时',
        )
        precipitation: float = Field(
            alias='precip',
            description='预报当天总降水量，毫米',
        )
        humidity: int = Field(
            alias='humidity',
            description='相对湿度，百分比数值',
        )
        pressure: int = Field(
            alias='pressure',
            description='大气压强，百帕',
        )

    class HourlyWeather(ConfigedBaseModel):
        """小时天气"""

        time: datetime = Field(alias='fxTime', description='预报时间')
        temperature: int = Field(
            alias='temp',
            description='温度，摄氏度',
        )
        icon: int = Field(
            alias='icon',
            description='天气状况的图标代码',
        )
        weather_description: str = Field(
            alias='text',
            description='天气状况的文字描述，包括阴晴雨雪等天气状态的描述',
        )
        wind_degress: int = Field(alias='wind360', description='风向360角度')
        wind_direction: str = Field(alias='windDir', description='风向')
        wind_scale: int = Field(alias='windScale', description='风力等级')
        wind_speed: int = Field(
            alias='windSpeed',
            description='风速，公里/小时',
        )
        humidity: int = Field(
            alias='humidity',
            description='相对湿度，百分比数值',
        )
        precipitation: float = Field(
            alias='precip',
            description='当前小时累计降水量，毫米',
        )
        pressure: int = Field(
            alias='pressure',
            description='大气压强，百帕',
        )
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


class MinutePrecipitation(ConfigedBaseModel):
    """分钟降雨量"""

    time: datetime = Field(alias='fxTime', description='预报时间')
    precipitation: float = Field(
        alias='precip',
        description='5分钟累计降水量，毫米',
    )
    type: Literal['rain', 'snow'] = Field(  # noqa: A003
        description='降水类型：rain = 雨，snow = 雪',
    )


class WeatherIndex(ConfigedBaseModel):
    """天气指数"""

    date: datetime = Field(alias='fxDate', description='预报日期')
    type: str = Field(description='生活指数类型ID')  # noqa: A003
    name: str = Field(description='生活指数类型的名称')
    level: str = Field(description='生活指数预报等级')
    category: str = Field(description='生活指数预报级别名称')
    text: Optional[str] = Field(
        default=None,
        description='生活指数预报的详细描述，可能为空',
    )


class AirQuality:
    """空气质量"""

    class AirQualityNow(ConfigedBaseModel):
        """当前空气质量"""

        time: datetime = Field(
            alias='pubTime',
            description='空气质量数据发布时间',
        )
        aqi: str = Field(description='空气质量指数')
        level: str = Field(description='空气质量指数等级')
        category: str = Field(description='空气质量指数级别')
        primary: str = Field(
            description='空气质量的主要污染物，空气质量为优时，返回值为NA',
        )
        pm10: str = Field(description='PM10')
        pm2p5: str = Field(description='PM2.5')
        no2: str = Field(description='二氧化氮')
        so2: str = Field(description='二氧化硫')
        co: str = Field(description='一氧化碳')
        o3: str = Field(description='臭氧')

    class AirQualityStation(ConfigedBaseModel):
        """空气质量检测站信息"""

        time: datetime = Field(
            alias='pubTime',
            description='空气质量数据发布时间',
        )
        name: str = Field(description='监测站名称')
        id: str = Field(description='监测站ID')  # noqa: A003
        aqi: str = Field(description='空气质量指数')
        level: str = Field(description='空气质量指数等级')
        category: str = Field(description='空气质量指数级别')
        primary: str = Field(
            description='空气质量的主要污染物，空气质量为优时，返回值为NA',
        )
        pm10: str = Field(description='PM10')
        pm2p5: str = Field(description='PM2.5')
        no2: str = Field(description='二氧化氮')
        so2: str = Field(description='二氧化硫')
        co: str = Field(description='一氧化碳')
        o3: str = Field(description='臭氧')


class WeatherAlert(ConfigedBaseModel):
    """天气预警"""

    id: str = Field(  # noqa: A003
        description='本条预警的唯一标识，可判断本条预警是否已经存在',
    )
    sender: str = Field(description='预警发布单位，可能为空')
    publish_time: datetime = Field(description='预警发布时间')
    title: str = Field(description='预警信息标题')
    start_time: datetime = Field(description='预警开始时间，可能为空')
    end_time: datetime = Field(description='预警结束时间，可能为空')
    status: str = Field(description='预警信息的发布状态')
    severity: str = Field(description='预警严重等级')
    severity_color: str = Field(description='预警严重等级颜色，可能为空')
    type: str = Field(description='预警类型ID')  # noqa: A003
    type_name: str = Field(description='预警类型名称')
    urgency: str = Field(description='预警信息的紧迫程度，可能为空')
    certainty: str = Field(description='预警信息的确定性，可能为空')
    text: str = Field(description='预警详细文字描述')
    related: str = Field(
        description=(
            '与本条预警相关联的预警ID，当预警状态为cancel或update时返回。可能为空'
        ),
    )
