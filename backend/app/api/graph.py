from fastapi import APIRouter

from app.models.document import GraphResponse
from app.services.graph import build_graph

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("", response_model=GraphResponse)
def get_graph() -> GraphResponse:
    return build_graph()
