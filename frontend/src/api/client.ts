import { http } from "./http";
export async function api<T>(path: string, init?: RequestInit) {
  const method = (init?.method ?? "GET").toLowerCase();
  const body = init?.body ? JSON.parse(init.body as string) : undefined;
  const res = await http.request<T>({ url: path, method, data: body });
  return res.data;
}
