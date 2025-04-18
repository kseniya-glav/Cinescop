from fastapi import FastAPI
from datetime import datetime
import pytz

app = FastAPI()

@app.get("/ping")
def ping():
    return "PONG!"


@app.get("/fake/worldclockapi/api/json/utc/now")
def get_current_utc_time():
    now = datetime.now(pytz.utc)
    response = {
        "$id": "1",
        "currentDateTime": now.strftime("%Y-%m-%dT%H:%MZ"),
        "utcOffset": "00:00:00",
        "isDayLightSavingsTime": False,
        "dayOfTheWeek": now.strftime("%A"),
        "timeZoneName": "UTC",
        "currentFileTime": int(now.timestamp() * 10**7),  # Преобразуем в FILETIME (100-наносекундные интервалы с 1 января 1601)
        "ordinalDate": now.strftime("%Y-%j"),  # Год и день года (001-366)
        "serviceResponse": None
    }
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=16001)
    