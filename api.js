import axios from "axios";
const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function signup(username, password) {
  const res = await axios.post(`${API}/signup`, { username, password });
  return res.data;
}

export async function login(username, password) {
  const res = await axios.post(`${API}/token`, new URLSearchParams({ username, password }));
  return res.data;
}

export async function createProject(token, title, description) {
  const res = await axios.post(`${API}/projects`, { title, description }, { headers: { Authorization: `Bearer ${token}` } });
  return res.data;
}

export async function listProjects() {
  const res = await axios.get(`${API}/projects`);
  return res.data;
}
export async function createIssue(token, projectId, issue) {
  const res = await axios.post(`${API}/projects/${projectId}/issues`, issue, { headers: { Authorization: `Bearer ${token}` } });
  return res.data;
}
export async function listIssues(projectId) {
  const res = await axios.get(`${API}/projects/${projectId}/issues`);
  return res.data;
}
