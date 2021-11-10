from fastapi import FastAPI, Depends, Request, APIRouter, Response
from api import userql
# from database import mongodb_utils
from auth import authentication as auth
import uvicorn
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
import graphene
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
from pydantic import BaseModel

app = FastAPI()

app.mount("/files", StaticFiles(directory="files"), name="files")

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.AUTH_ROUTER, prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    auth.REGISTER_ROUTER, prefix="/auth", tags=["auth"]
)
app.include_router(
    auth.RESET_PASWORD_ROUTER,
    prefix="/auth",
    tags=["auth"],
)

graphql_app = GraphQLApp(schema=graphene.Schema(query=userql.Query, mutation=userql.Mutation), executor_class=AsyncioExecutor)

@app.get("/graphql")
@app.post("/graphql")
async def graphql(request: Request, user= Depends(auth.fastapi_users.get_optional_current_user)):
    request.state.user = user
    return await graphql_app.handle_graphql(request=request)