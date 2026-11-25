import { useEffect, useState } from "react";
import api from "../services/api";

export default function Analytics() {
  const [agreement, setAgreement] = useState<any>();
  const [errors, setErrors] = useState<any>();
  useEffect(() => {
    api.get("/analytics/agreement").then(({ data }) => setAgreement(data)).catch(() => setAgreement({}));
    api.get("/analytics/error-distribution").then(({ data }) => setErrors(data)).catch(() => setErrors({ categories: {} }));
  }, []);
  return (
    <div><header className="page-header"><div><p className="eyebrow">Reliability</p><h1>Quality analytics</h1></div></header>
      <section className="stat-grid"><article className="stat-card"><span>Task agreement</span><strong>{agreement?.task_count ?? 0}</strong></article><article className="stat-card"><span>Error categories</span><strong>{Object.keys(errors?.categories ?? {}).length}</strong></article></section>
      <section className="two-col"><article className="panel"><h2>Inter-annotator agreement</h2><pre>{JSON.stringify(agreement?.task_agreement ?? {}, null, 2)}</pre></article><article className="panel"><h2>Error distribution</h2><pre>{JSON.stringify(errors?.categories ?? {}, null, 2)}</pre></article></section>
    </div>
  );
}
