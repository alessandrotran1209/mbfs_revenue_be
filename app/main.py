from fastapi import FastAPI
from starlette.responses import JSONResponse

from models.RevenueTarget import RevenueTarget
from controllers import Controller as controller
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from typing import List

from models.RevenueUpdate import RevenueUpdate

import api

import logging
import string
import time
import random

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

app = FastAPI()
origins = [
    # "http://localhost:4200",
    # "https://mobi-hatang.herokuapp.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.auth.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    log_file = open('log.log', 'a')
    log_file.write(
        f"rid={idem} start request path={request.url.path} completed_in={formatted_process_time}ms status_code={response.status_code}\n")
    log_file.close()
    return response


@app.post("/insert")
async def insert_revenue(revenue_target: RevenueTarget):
    completed = controller.insert(revenue_target.__dict__)
    if completed:
        return JSONResponse(status_code=200, content={"data": completed})
    return JSONResponse(status_code=500, content={"data": completed})


@app.post("/update-week")
async def update_week_revenue(revenue_update: RevenueUpdate):
    completed = controller.update(revenue_update.__dict__)

    if completed:
        return JSONResponse(status_code=200, content={"data": completed})
    return JSONResponse(status_code=500, content={"data": completed})


@app.get("/revenue/q")
async def get_revenue_from_sources(branch: str, source: str):
    categories = controller.get_revenue_from_source(
        branch=branch, source_value=source)
    return JSONResponse(status_code=200, content={"data": categories})


@app.get("/category/q")
async def get_category_suggestion(source: str):
    categories = controller.get_category_suggestion(source)
    return JSONResponse(status_code=200, content={"data": categories})


@app.get("/subcategory/q")
async def get_subcategory_suggestion(source: str, category: str):
    subcategories = controller.get_subcategory_suggestion(source, category)
    return JSONResponse(status_code=200, content={"data": subcategories})


@app.get("/detail/q")
async def get_detail_suggestion(source: str, category: str, subcategory: str):
    details = controller.get_detail_suggestion(source, category, subcategory)
    return JSONResponse(status_code=200, content={"data": details})


@app.post("/insert-excel")
async def insert_revenue_excel(revenue_target: List[RevenueTarget], target: str):
    completed = controller.insert_excel(revenue_target, target)
    if completed:
        return JSONResponse(status_code=200, content={"data": True})
    return JSONResponse(status_code=500, content={"data": completed})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
