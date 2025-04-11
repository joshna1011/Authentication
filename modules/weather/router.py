from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import RedirectResponse
from ..user.utils.response import success_response, failure_response
from .weather_util import Weather
from datetime import datetime

router = APIRouter()

def get_weather():
    return Weather()

@router.get("/")
async def get_weather_data(weather: Weather = Depends(get_weather)):
    
    data = await weather.get_weather_data()
    stations = data["metadata"]["stations"]
    readings = data["items"][0]["readings"]

    # Create a station lookup map: {id: {name, lat, long}}
    station_map = {
        station["id"]: {
            "name": station["name"],
            "latitude": station["location"]["latitude"],
            "longitude": station["location"]["longitude"]
        }
        for station in stations
    }

    result = []
    for reading in readings:
        station_id = reading["station_id"]
        temperature = reading["value"]
        station_info = station_map.get(station_id)

        if station_info:
            result.append({
                "place": station_info["name"],
                "latitude": station_info["latitude"],
                "longitude": station_info["longitude"],
                "temperature": temperature
            })

    return result

