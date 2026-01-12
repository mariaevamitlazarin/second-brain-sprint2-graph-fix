import re
from typing import Dict, List

from app.models.document import DocumentRecord, GraphEdge, GraphNode, GraphResponse
from app.services.registry import registry


AREA_COLORS = {
    "ai": "#885BD6",
    "artificial intelligence": "#885BD6",
    "business": "#F8E26C",
    "research": "#2EBCB6",
    "smart cities": "#467CD9",
    "finance": "#51E697",
    "healthcare": "#BFE081",
    "legal": "#F89570",
}

DEFAULT_COLORS = {
    "brain": "#D463E6",
    "area": "#885BD6",
    "subject": "#2EBCB6",
    "document": "#FFFFFF",
    "file_type": "#467CD9",
    "duplicate": "#F89570",
    "keyword": "#51E697",
}


def slug(value: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return clean or "unknown"


def get_area_color(area: str) -> str:
    return AREA_COLORS.get(area.strip().lower(), DEFAULT_COLORS["area"])


def add_node(nodes: Dict[str, GraphNode], node: GraphNode) -> None:
    if node.id not in nodes:
        nodes[node.id] = node


def add_edge(edges: Dict[str, GraphEdge], edge: GraphEdge) -> None:
    if edge.id not in edges:
        edges[edge.id] = edge


def build_graph() -> GraphResponse:
    documents: List[DocumentRecord] = registry.all()
    nodes: Dict[str, GraphNode] = {}
    edges: Dict[str, GraphEdge] = {}

    brain_id = "brain:second-brain"
    add_node(
        nodes,
        GraphNode(
            id=brain_id,
            type="brain",
            label="Second Brain",
            color=DEFAULT_COLORS["brain"],
            size=36,
            metadata={"description": "Central knowledge system"},
        ),
    )

    for document in documents:
        area = document.area or "Unclassified"
        subject = document.subject or "General"
        extension = document.file_extension or "unknown"

        area_id = f"area:{slug(area)}"
        subject_id = f"subject:{slug(area)}:{slug(subject)}"
        file_type_id = f"file-type:{extension.replace('.', '') or 'unknown'}"
        document_id = f"document:{document.id}"

        add_node(
            nodes,
            GraphNode(
                id=area_id,
                type="area",
                label=area,
                color=get_area_color(area),
                size=28,
                metadata={"area": area},
            ),
        )
        add_edge(
            edges,
            GraphEdge(
                id=f"edge:{brain_id}->{area_id}",
                source=brain_id,
                target=area_id,
                relationship_type="HAS_AREA",
                weight=1.0,
            ),
        )

        add_node(
            nodes,
            GraphNode(
                id=subject_id,
                type="subject",
                label=subject,
                color=DEFAULT_COLORS["subject"],
                size=22,
                metadata={"area": area, "subject": subject},
            ),
        )
        add_edge(
            edges,
            GraphEdge(
                id=f"edge:{area_id}->{subject_id}",
                source=area_id,
                target=subject_id,
                relationship_type="HAS_SUBJECT",
                weight=1.0,
            ),
        )

        add_node(
            nodes,
            GraphNode(
                id=file_type_id,
                type="file_type",
                label=extension.upper().replace(".", ""),
                color=DEFAULT_COLORS["file_type"],
                size=18,
                metadata={"extension": extension},
            ),
        )

        color = DEFAULT_COLORS["duplicate"] if document.duplicate_of else DEFAULT_COLORS["document"]
        add_node(
            nodes,
            GraphNode(
                id=document_id,
                type="document",
                label=document.original_filename,
                color=color,
                size=16 if document.duplicate_of else 20,
                metadata={
                    "document_id": document.id,
                    "status": document.status,
                    "sha256": document.sha256,
                    "keywords": document.keywords,
                    "summary": document.summary,
                    "text_length": document.extraction_metadata.text_length,
                },
            ),
        )
        add_edge(
            edges,
            GraphEdge(
                id=f"edge:{subject_id}->{document_id}",
                source=subject_id,
                target=document_id,
                relationship_type="CONTAINS_DOCUMENT",
                weight=1.0,
            ),
        )
        add_edge(
            edges,
            GraphEdge(
                id=f"edge:{document_id}->{file_type_id}",
                source=document_id,
                target=file_type_id,
                relationship_type="HAS_FILE_TYPE",
                weight=0.5,
            ),
        )

        if document.duplicate_of:
            original_id = f"document:{document.duplicate_of}"
            add_edge(
                edges,
                GraphEdge(
                    id=f"edge:{document_id}->{original_id}:duplicate",
                    source=document_id,
                    target=original_id,
                    relationship_type="DUPLICATE_OF",
                    weight=2.0,
                ),
            )

        for keyword in document.keywords[:5]:
            keyword_id = f"keyword:{slug(keyword)}"
            add_node(
                nodes,
                GraphNode(
                    id=keyword_id,
                    type="keyword",
                    label=keyword,
                    color=DEFAULT_COLORS["keyword"],
                    size=12,
                    metadata={"keyword": keyword},
                ),
            )
            add_edge(
                edges,
                GraphEdge(
                    id=f"edge:{document_id}->{keyword_id}",
                    source=document_id,
                    target=keyword_id,
                    relationship_type="MENTIONS_KEYWORD",
                    weight=0.4,
                ),
            )

    return GraphResponse(nodes=list(nodes.values()), edges=list(edges.values()))
