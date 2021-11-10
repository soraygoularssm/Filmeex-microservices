from fastapi import FastAPI
from api import discovery
# from database import mongodb_utils
# import uvicorn

app = FastAPI()

# app.add_event_handler("startup", mongodb_utils.connect_to_mongo)
# app.add_event_handler("shutdown", mongodb_utils.close_mongo_connection)

app.include_router(discovery.router, prefix='/discovery' , tags=['discovery'])

# uvicorn.run(app, port=8001)
