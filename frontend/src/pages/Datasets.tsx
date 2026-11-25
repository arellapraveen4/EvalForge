import { useEffect, useState } from "react";
import api from "../services/api";
import type { Dataset } from "../types";

export default function Datasets() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [file, setFile] = useState<File>();
  const [message, setMessage] = useState("");
  const load = () => api.get("/datasets").then(({ data }) => setDatasets(data)).catch(() => setDatasets([]));
  useEffect(load, []);
  const upload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    const { data } = await api.post("/datasets/upload", form);
    setMessage(`Uploaded ${data.name} with ${data.items} valid items`);
    load();
  };
  return (
    <div>
      <header className="page-header"><div><p className="eyebrow">Data</p><h1>Dataset management</h1></div></header>
      <section className="panel upload-panel">
        <div><h2>Upload evaluation data</h2><p>CSV, JSON and JSONL formats supported.</p></div>
        <input type="file" accept=".csv,.json,.jsonl" onChange={(event) => setFile(event.target.files?.[0])} />
        <button className="primary" onClick={upload}>Upload dataset</button>
      </section>
      {message && <p className="success">{message}</p>}
      <section className="panel"><h2>Datasets</h2>
        <table><thead><tr><th>Name</th><th>Format</th><th>Created</th></tr></thead>
          <tbody>{datasets.map((dataset) => <tr key={dataset.id}><td>{dataset.name}</td><td>{dataset.format}</td><td>{dataset.created_at}</td></tr>)}</tbody>
        </table>
      </section>
    </div>
  );
}
