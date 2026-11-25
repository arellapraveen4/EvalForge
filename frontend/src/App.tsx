import { NavLink, Route, Routes } from "react-router-dom";
import { BarChart3, ClipboardCheck, Database, FlaskConical, LayoutDashboard, Settings, Users } from "lucide-react";
import Dashboard from "./pages/Dashboard";
import Datasets from "./pages/Datasets";
import Annotation from "./pages/Annotation";
import Reviews from "./pages/Reviews";
import Benchmarks from "./pages/Benchmarks";
import Analytics from "./pages/Analytics";
import Login from "./pages/Login";
import { useState } from "react";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/datasets", label: "Datasets", icon: Database },
  { to: "/annotation", label: "Annotation Tasks", icon: ClipboardCheck },
  { to: "/reviews", label: "Reviews", icon: Users },
  { to: "/benchmarks", label: "Benchmarks", icon: FlaskConical },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
];

export default function App() {
  const [authenticated, setAuthenticated] = useState(Boolean(localStorage.getItem("evalforge_token")));
  if (!authenticated) return <Login onAuthenticated={() => setAuthenticated(true)} />;
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span>EF</span><strong>EvalForge</strong></div>
        <nav>
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} end={to === "/"} className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
              <Icon size={18} /> {label}
            </NavLink>
          ))}
        </nav>
        <button className="settings"><Settings size={18} /> Settings</button>
      </aside>
      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/annotation" element={<Annotation />} />
          <Route path="/reviews" element={<Reviews />} />
          <Route path="/benchmarks" element={<Benchmarks />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
    </div>
  );
}
