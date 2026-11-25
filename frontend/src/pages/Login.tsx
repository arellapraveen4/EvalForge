import { useState } from "react";
import api from "../services/api";

export default function Login({ onAuthenticated }: { onAuthenticated: () => void }) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("annotator");
  const [error, setError] = useState("");

  const submit = async () => {
    setError("");
    try {
      const endpoint = mode === "login" ? "/auth/login" : "/auth/register";
      const payload = mode === "login"
        ? { email, password }
        : { email, name: name || email.split("@")[0], password, role };
      const { data } = await api.post(endpoint, payload);
      localStorage.setItem("evalforge_token", data.access_token);
      onAuthenticated();
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? "Authentication failed");
    }
  };

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={(event) => { event.preventDefault(); void submit(); }}>
        <div className="brand login-brand"><span>EF</span><strong>EvalForge</strong></div>
        <p className="eyebrow">Human and AI evaluation lab</p>
        <h1>{mode === "login" ? "Sign in" : "Create account"}</h1>
        {mode === "register" && <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Full name" />}
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Email" required />
        <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Password" required />
        {mode === "register" && <select value={role} onChange={(event) => setRole(event.target.value)}><option value="annotator">Annotator</option><option value="reviewer">Reviewer</option><option value="admin">Admin</option></select>}
        {error && <p className="login-error">{error}</p>}
        <button type="button" className="primary" onClick={submit}>{mode === "login" ? "Sign in" : "Register"}</button>
        <button type="button" className="text-button" onClick={() => setMode(mode === "login" ? "register" : "login")}>{mode === "login" ? "Create an account" : "Use an existing account"}</button>
      </form>
    </div>
  );
}
