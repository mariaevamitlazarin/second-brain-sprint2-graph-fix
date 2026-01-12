"use client";

import { useEffect, useMemo, useState } from "react";

type GraphNode = {
  id: string;
  type: string;
  label: string;
  color: string;
  size: number;
  metadata: Record<string, unknown>;
};

type GraphEdge = {
  id: string;
  source: string;
  target: string;
  relationship_type: string;
  weight: number;
};

type GraphResponse = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};

type PositionedNode = GraphNode & {
  x: number;
  y: number;
};

function getRadius(type: string) {
  // Keep every ring inside the canvas. The first Sprint 2 version used
  // radii above 50, which pushed nodes outside the 0-100 SVG/absolute
  // coordinate system and visually cut the graph.
  if (type === "brain") return 0;
  if (type === "area") return 13;
  if (type === "subject") return 22;
  if (type === "document") return 31;
  if (type === "keyword") return 39;
  return 43;
}

function clampPosition(value: number) {
  // Extra margin protects labels and node borders from being clipped.
  return Math.min(92, Math.max(8, value));
}

export function BrainGraph() {
  const [graph, setGraph] = useState<GraphResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadGraph() {
    try {
      const response = await fetch("http://localhost:8000/api/graph");
      const payload = await response.json();
      setGraph(payload);
      setError(null);
    } catch {
      setError("Could not load graph API.");
    }
  }

  useEffect(() => {
    loadGraph();
    window.addEventListener("second-brain-refresh", loadGraph);
    return () => window.removeEventListener("second-brain-refresh", loadGraph);
  }, []);

  const positionedNodes = useMemo<PositionedNode[]>(() => {
    if (!graph) return [];

    const groups: Record<string, GraphNode[]> = {};
    for (const node of graph.nodes) {
      groups[node.type] = groups[node.type] || [];
      groups[node.type].push(node);
    }

    const positioned: PositionedNode[] = [];
    const typeOrder = ["brain", "area", "subject", "document", "keyword", "file_type"];

    for (const type of typeOrder) {
      const nodes = groups[type] || [];
      const radius = getRadius(type);
      nodes.forEach((node, index) => {
        if (type === "brain") {
          positioned.push({ ...node, x: 50, y: 50 });
          return;
        }
        const angle = (2 * Math.PI * index) / Math.max(nodes.length, 1) - Math.PI / 2;
        positioned.push({
          ...node,
          x: clampPosition(50 + radius * Math.cos(angle)),
          y: clampPosition(50 + radius * Math.sin(angle)),
        });
      });
    }

    return positioned;
  }, [graph]);

  const nodeMap = useMemo(() => {
    const map = new Map<string, PositionedNode>();
    positionedNodes.forEach((node) => map.set(node.id, node));
    return map;
  }, [positionedNodes]);

  return (
    <section className="panel graphPanel">
      <div className="panelHeader">
        <div>
          <h2>Brain Graph</h2>
          <p>First graph API: areas, subjects, documents, file types, keywords, and duplicates.</p>
        </div>
        <button type="button" onClick={loadGraph}>Refresh</button>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="graphCanvas">
        <svg className="graphSvg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
          {graph?.edges.map((edge) => {
            const source = nodeMap.get(edge.source);
            const target = nodeMap.get(edge.target);
            if (!source || !target) return null;
            return (
              <line
                key={edge.id}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                className="graphLine"
              />
            );
          })}
        </svg>

        {positionedNodes.map((node) => (
          <div
            key={node.id}
            className={`graphNode ${node.type} ${node.y > 78 ? "labelAbove" : ""}`}
            style={{
              left: `${node.x}%`,
              top: `${node.y}%`,
              width: `${Math.max(node.size, 12)}px`,
              height: `${Math.max(node.size, 12)}px`,
              backgroundColor: node.color,
              color: node.color,
            }}
            title={`${node.type}: ${node.label}`}
          >
            <span>{node.label}</span>
          </div>
        ))}

        {graph && graph.nodes.length === 1 && (
          <p className="emptyGraph">Upload files to expand the graph.</p>
        )}
      </div>

      {graph && (
        <div className="graphStats">
          <span>{graph.nodes.length} nodes</span>
          <span>{graph.edges.length} edges</span>
        </div>
      )}
    </section>
  );
}
