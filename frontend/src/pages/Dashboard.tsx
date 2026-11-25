import { useEffect, useState } from "react";
import api from "../services/api";
import type { DashboardStats } from "../types";

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>();
  useEffect(() => { api.get("/analytics/dashboard").then(({ data }) => setStats(data)).catch(() => setStats({
    datasets: 0, tasks: 0, completed_tasks: 0, pending_tasks: 0, annotations: 0, reviewed_tasks: 0,
  })); }, []);
  const cards = [
    ["Total tasks", stats?.tasks ?? 0],
    ["Completed", stats?.completed_tasks ?? 0],
    ["Pending", stats?.pending_tasks ?? 0],
    ["Annotations", stats?.annotations ?? 0],
  ] as const;
  return (
    <div>
      <header className="page-header"><div><p className="eyebrow">Overview</p><h1>Evaluation dashboard</h1></div></header>
      <section className="stat-grid">{cards.map(([label, value]) => <article className="stat-card" key={label}><span>{label}</span><strong>{value}</strong></article>)}</section>
      <section className="panel"><h2>Recent activity</h2><p>Upload a dataset and create evaluation tasks to begin measuring quality.</p></section>
      <section className="two-col">
        <article className="panel"><h2>Human vs AI agreement</h2><div className="empty-chart">No judge labels yet</div></article>
        <article className="panel"><h2>Error distribution</h2><div className="empty-chart">No annotations yet</div></article>
      </section>
    </div>
  );
}
