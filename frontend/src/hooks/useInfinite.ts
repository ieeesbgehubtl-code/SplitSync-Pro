import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Page } from "../types";
export function useInfinite<T>(path: string) {
  const [items, setItems] = useState<T[]>([]);
  const [next, setNext] = useState<string | null>(path);
  const [loading, setLoading] = useState(false);
  async function load(url = next) {
    if (!url || loading) return;
    setLoading(true);
    const normalized = url.startsWith("http")
      ? new URL(url).pathname.replace(/^\/api/, "") + new URL(url).search
      : url;
    const data = await api<Page<T>>(normalized);
    setItems((v) => (url === path ? data.results : [...v, ...data.results]));
    setNext(data.next);
    setLoading(false);
  }
  useEffect(() => {
    setItems([]);
    setNext(path);
    load(path);
  }, [path]);
  return { items, loading, load, hasMore: !!next, setItems };
}
