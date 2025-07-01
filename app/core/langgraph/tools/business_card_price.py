import os
import requests
from langchain_core.tools.base import BaseTool
from pydantic import BaseModel, Field
from typing import Optional

class WeatherArgs(BaseModel):
    city: str = Field(..., description="Название города (например, Лиссабон, Paris, Tokyo)")

class WeatherTool(BaseTool):
    name: str = "weather"
    description: str = "Выдаёт текущую температуру в выбранном городе."
    args_schema: type = WeatherArgs

    def _run(self, city: str):
        api_key = os.getenv("WEATHER_API_KEY", "ef3798edf43a0c4908c4b8cd431a7374")
        if not api_key:
            return "Ошибка: не задан API-ключ для OpenWeatherMap (WEATHER_API_KEY)"
        # Получаем координаты города через geocoding API
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_resp = requests.get(geo_url)
        if geo_resp.status_code != 200 or not geo_resp.json():
            return f"Ошибка: не удалось найти город '{city}'"
        geo = geo_resp.json()[0]
        lat, lon = geo["lat"], geo["lon"]
        # Получаем погоду через One Call API 3.0
        weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ru"
        weather_resp = requests.get(weather_url)
        if weather_resp.status_code != 200:
            return f"Ошибка: не удалось получить погоду для '{city}' (код {weather_resp.status_code})"
        data = weather_resp.json()
        current = data.get("current")
        if not current or "temp" not in current or not current.get("weather"):
            return f"Ошибка: не удалось получить актуальную температуру для '{city}'"
        temp = current["temp"]
        desc = current["weather"][0]["description"]
        return f"Текущая температура в {city}: {temp}°C, {desc}"

weather_tool = WeatherTool()

class BusinessCardPriceArgs(BaseModel):
    size: str = Field(..., description="Business card size, e.g. '90x50 mm'")
    quantity: int = Field(..., description="Number of sets")
    paper_density: int = Field(..., description="Paper density in g/m²")
    lamination: Optional[str] = Field(None, description="Lamination type: 'glossy', 'matte', or 'none'")

class BusinessCardPriceTool(BaseTool):
    name: str = "business_card_price"
    description: str = "Calculate the price for printing a set of business cards. Requires size, quantity, paper density, and lamination type."
    args_schema: type = BusinessCardPriceArgs

    def _run(self, size: str, quantity: int, paper_density: int, lamination: Optional[str] = None):
        # Simple price calculation logic
        base_price = 200  # базовая цена за комплект
        paper_coef = (paper_density - 250) * 0.1 if paper_density > 250 else 0
        lam_coef = 0
        if lamination:
            if lamination.lower() == "glossy":
                lam_coef = 50
            elif lamination.lower() == "matte":
                lam_coef = 70
        total = (base_price + paper_coef + lam_coef) * quantity
        return f"Business card set price: {total:.2f} UAH (size: {size}, quantity: {quantity}, paper: {paper_density}g/m², lamination: {lamination or 'none'})"

business_card_price_tool = BusinessCardPriceTool() 