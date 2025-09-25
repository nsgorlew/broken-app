from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from os import getenv
import json


api_version = getenv("API_VERSION", "v1")
app = FastAPI(
    root_path=f"/api/{api_version}"
)


@app.post("/predict")
async def predict(request: Request):
    try:
        data = json.loads(request.model_dump_json())
        result = data["message"]
        return JSONResponse(content={"message": result}, status_code=200)
    except KeyError as ke:
        return JSONResponse(content={"message": f"KeyError: {ke}"}, status_code=200)
    except ValueError as ve:
        return JSONResponse(content={"message": f"ValueError: {ve}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Exception: {e}"}, status_code=200)


@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "healthy"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
