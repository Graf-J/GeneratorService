from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import project_router, vertex_router, edge_router, graph_router, build_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router, prefix="/api/v1")
app.include_router(vertex_router, prefix='/api/v1')
app.include_router(edge_router, prefix="/api/v1")
app.include_router(graph_router, prefix="/api/v1")
app.include_router(build_router, prefix="/api/v1")
