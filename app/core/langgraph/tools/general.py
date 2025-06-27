from langchain_core.tools.base import BaseTool
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
from datetime import datetime
from functools import lru_cache
import httpx

class CityTimeArgs(BaseModel):
    city: str = Field(..., description="Название города (можно кириллицей или латиницей), например: Porto, Одесса, Lisboa")

class CityTimeTool(BaseTool):
    name: str = "city_time"
    description: str = "Получает текущее локальное время и страну для указанного города."
    args_schema: type = CityTimeArgs

    def _run(self, city: str):
        geolocator = Nominatim(user_agent="agent-time-tool")
        tf = TimezoneFinder()
        try:
            location = geolocator.geocode(city, language="en", exactly_one=True, timeout=10)
            if not location:
                return f"Город '{city}' не найден."
            lat, lon = location.latitude, location.longitude
            tz_name = tf.timezone_at(lat=lat, lng=lon)
            if not tz_name:
                return f"Не удалось определить тайм-зону для города '{city}'."
            now_local = datetime.now(ZoneInfo(tz_name)).isoformat()
            country = location.address.split(",")[-1].strip()
            return f"В городе {city} ({country}) сейчас {now_local} ({tz_name})"
        except Exception as e:
            return f"Ошибка при определении времени для города {city}: {e}"

city_time_tool = CityTimeTool()
