import { useEffect, useState } from "react";
import api from "../services/api";

export default function Benchmarks() {
  const [benchmark, setBenchmark] = useState<any>();
  useEffect(() => { api.get("/analytics/benchmark").then(({ data }) => setBenchmark(data)).catch(() => setBenchmark({ preference_distribution: {} })); }, []);
  const rows = Object.entries(benchmark?.preference_distribution ?? {});
  return (
    <div><header className="page-header"><div><p className="eyebrow">Experiments</p><h1>Model benchmark</h1></div></header>
      <section className="panel"><h2>Preference distribution</h2><table><thead><tr><th>Preference</th><th>Count</th></tr></thead><tbody>{rows.map(([label, count]) => <tr key={label}><td>{label}</td><td>{String(count)}</td></tr>)}</tbody></table></section>
      <section className="two-col"><article className="panel"><h2>Score distribution</h2><div className="empty-chart">Run evaluations to populate</div></article><article className="panel"><h2>Category performance</h2><div className="empty-chart">Run category benchmarks to populate</div></article></section>
    </div>
  );
}
