import { useEffect, useState } from "react";
import api from "../services/api";

export default function Reviews() {
  const [pending, setPending] = useState<any[]>([]);
  useEffect(() => { api.get("/reviews/pending").then(({ data }) => setPending(data)).catch(() => setPending([])); }, []);
  const decide = async (annotationId: number, decision: "approve" | "reject") =>
    { await api.post(`/reviews/${decision}`, { annotation_id: annotationId, decision, comments: "" }); setPending((items) => items.filter((item) => item.id !== annotationId)); };
  return (
    <div><header className="page-header"><div><p className="eyebrow">Quality control</p><h1>Reviewer workspace</h1></div></header>
      {pending.length === 0 ? <section className="panel empty-state">No annotations awaiting review.</section> :
        pending.map((item) => <section className="panel review-card" key={item.id}><div><h2>Annotation {item.id}</h2><p>Task {item.task_id} · Preference: {item.preference}</p></div><div><button className="choice" onClick={() => decide(item.id, "reject")}>Reject</button><button className="primary" onClick={() => decide(item.id, "approve")}>Approve</button></div></section>)}
    </div>
  );
}
