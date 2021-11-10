from fastapi import FastAPI
from api import genre , category , slider
from database import mongodb_utils
import uvicorn

app = FastAPI()

app.add_event_handler("startup", mongodb_utils.connect_to_mongo)
app.add_event_handler("shutdown", mongodb_utils.close_mongo_connection)

app.include_router(genre.router)
app.include_router(category.router)
app.include_router(slider.router)

if __name__ == '__main__':
    uvicorn.run(app)
