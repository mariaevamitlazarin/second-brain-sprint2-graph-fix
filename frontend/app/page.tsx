import { BrainGraph } from "../components/BrainGraph";
import { DocumentsList } from "../components/DocumentsList";
import { UploadPanel } from "../components/UploadPanel";
import "./page.css";

export default function Home() {
  return (
    <main className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Second Brain Prototype</p>
          <h1>Knowledge Graph Console</h1>
          <p>
            Sprint 2 adds the first intelligence layer: text extraction, metadata, basic summary,
            keywords, and a graph-ready API for the visual brain.
          </p>
        </div>
        <div className="brainMock" aria-label="Neural graph visual placeholder">
          <span className="node nodeA" />
          <span className="node nodeB" />
          <span className="node nodeC" />
          <span className="node nodeD" />
          <span className="line lineOne" />
          <span className="line lineTwo" />
          <span className="line lineThree" />
        </div>
      </header>

      <div className="grid topGrid">
        <UploadPanel />
        <BrainGraph />
      </div>

      <DocumentsList />
    </main>
  );
}
