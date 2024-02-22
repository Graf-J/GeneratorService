from fastapi import FastAPI

from app.api.routes import project_router, vertex_router, edge_router, graph_router

app = FastAPI()

app.include_router(project_router, prefix="/api/v1")
app.include_router(vertex_router, prefix='/api/v1')
app.include_router(edge_router, prefix="/api/v1")
app.include_router(graph_router, prefix="/api/v1")
