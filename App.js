import React, { useState, useEffect } from "react";
import { signup, login, createProject, listProjects, createIssue, listIssues } from "./api";

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [projects, setProjects] = useState([]);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");

  useEffect(() => { fetchProjects(); }, []);

  async function fetchProjects() {
    const res = await listProjects();
    setProjects(res);
  }

  async function handleSignup() {
    await signup("dev1", "password123");
    const t = await login("dev1", "password123");
    setToken(t.access_token);
  }

  async function handleCreateProject() {
    if (!token) return alert("Login first");
    await createProject(token, title, desc);
    setTitle(""); setDesc("");
    fetchProjects();
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Issue Tracker</h1>
      {!token ? (
        <div>
          <button onClick={handleSignup}>Quick Signup & Login</button>
        </div>
      ) : <div>Logged in (token present)</div>}

      <hr />
      <h2>Create Project</h2>
      <input placeholder="title" value={title} onChange={e=>setTitle(e.target.value)} />
      <br />
      <textarea placeholder="description" value={desc} onChange={e=>setDesc(e.target.value)} />
      <br />
      <button onClick={handleCreateProject}>Create Project</button>

      <hr />
      <h2>Projects</h2>
      {projects.map(p => (
        <div key={p.id} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8 }}>
          <h3>{p.title}</h3>
          <p>{p.description}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
