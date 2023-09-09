# 和风天气

一个使用和风天气API提供天气查询和定时预报的HoshinoBot插件

## 使用方法
1. 将插件放入Hoshino中，具体方法就不赘述了
2. 申请一个和风天气API的KEY https://dev.heweather.com/docs/api/weather
3. 初次启动会在插件文件夹下生成`config.yml`文件，将拿到的KEY填入，其余按照需求填写即可

## 配置项
| 配置项名称                 | 值的类型  | 说明                      |
|-----------------------|-------|-------------------------|
| HEFENG_KEY            | str   | 和风天气API的KEY             |
| FREE_SUBSCRIBE        | bool  | 是否为免费订阅                 |
| CITY_INFO_TTL         | str   | 城市信息缓存TTL，单位为s          |
| WEATHER_INFO_TTL      | bool  | 天气信息缓存TTL，单位为s          |
| SEND_MESSAGE_INTERVAL | float | 插件内部消息发送频率限制，单位为s ，意义不大 |

## 功能
- [x] 基本的天气查询
- [x] 小时天气查询
- [x] 定时天气预报
- [ ] 天气灾害预警
- [ ] 空气质量查询
- [ ] 生活指数查询
- [ ] 其余可能有用的功能

插件是一时兴起搓的，主要是自用，想到什么有用的功能~~可能~~就会加，欢迎提出建议
