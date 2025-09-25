from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from job import Job
from os import getenv
import json


api_version = getenv("API_VERSION", "v1")
app = FastAPI(
    root_path=f"/api/{api_version}"
)


@app.post("/predict")
async def predict(request: Request):
    try:
        job = Job()

        loan_application_data = await request.json()
        clean_data = job.prepare_data(loan_application_data)
        prediction = job.predict(clean_data)

        return JSONResponse(content={"rate": prediction}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Exception: {e}"}, status_code=500)


@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "healthy"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
