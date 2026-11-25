import { useEffect, useState } from "react";
import api from "../services/api";
import type { EvaluationTask } from "../types";

const dimensions = ["Correctness", "Instruction following", "Relevance", "Completeness", "Clarity"];
const errors = ["Factual error", "Hallucination", "Logical error", "Instruction violation", "Omission", "Safety violation"];

export default function Annotation() {
  const [tasks, setTasks] = useState<EvaluationTask[]>([]);
  const [task, setTask] = useState<EvaluationTask>();
  const [preference, setPreference] = useState("A");
  const [rationale, setRationale] = useState("");
  const [confidence, setConfidence] = useState(0.8);
  const [selectedErrors, setSelectedErrors] = useState<string[]>([]);
  useEffect(() => { api.get("/tasks").then(({ data }) => { setTasks(data); if (data[0]) setTask(data[0]); }).catch(() => setTasks([])); }, []);
  const openTask = async (id: number) => {
    const { data } = await api.get(`/tasks/${id}`);
    setTask(data);
  };
  const submit = async () => {
    if (!task) return;
    await api.post("/annotations/submit", {
      task_id: task.id, preference,
      scores: dimensions.map((dimension) => ({ dimension: dimension.toLowerCase().replaceAll(" ", "_"), score: 4 })),
      errors: selectedErrors.map((category) => ({ category: category.toLowerCase().replaceAll(" ", "_") })),
      rationale, confidence,
    });
    setRationale("");
  };
  return (
    <div>
      <header className="page-header"><div><p className="eyebrow">Human evaluation</p><h1>Response annotation</h1></div>
        <select onChange={(event) => openTask(Number(event.target.value))}><option value="">Select task</option>{tasks.map((item) => <option key={item.id} value={item.id}>Task {item.id}</option>)}</select>
      </header>
      {task?.item ? (
        <>
          <section className="prompt-panel"><span>Prompt</span><p>{task.item.prompt}</p></section>
          <section className="response-grid">
            <article className="response-card"><h2>Response A</h2><p>{task.item.response_a}</p></article>
            <article className="response-card"><h2>Response B</h2><p>{task.item.response_b}</p></article>
          </section>
          <section className="panel rubric"><h2>Rubric</h2>{dimensions.map((dimension) => <label key={dimension}>{dimension}<input type="range" min="1" max="5" defaultValue="4" /></label>)}</section>
          <section className="panel"><h2>Preference</h2><div className="choice-row">{["A", "B", "Tie", "BothPoor"].map((choice) => <button key={choice} className={preference === choice ? "choice active" : "choice"} onClick={() => setPreference(choice)}>{choice === "BothPoor" ? "Both poor" : choice}</button>)}</div></section>
          <section className="panel"><h2>Error tags</h2><div className="tag-grid">{errors.map((error) => <button key={error} className={selectedErrors.includes(error) ? "tag active" : "tag"} onClick={() => setSelectedErrors((current) => current.includes(error) ? current.filter((item) => item !== error) : [...current, error])}>{error}</button>)}</div></section>
          <section className="panel"><h2>Rationale</h2><textarea value={rationale} onChange={(event) => setRationale(event.target.value)} placeholder="Explain the evidence behind your judgment..." /><label className="confidence">Confidence <input type="range" min="0" max="1" step="0.05" value={confidence} onChange={(event) => setConfidence(Number(event.target.value))} /> {Math.round(confidence * 100)}%</label></section>
          <button className="primary submit" onClick={submit}>Submit annotation</button>
        </>
      ) : <section className="panel empty-state">Create and assign a task to start annotation.</section>}
    </div>
  );
}
