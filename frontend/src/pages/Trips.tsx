import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../components/layout/AppShell";
import { tripsService } from "../services/trips";
import { EmptyState } from "../components/Cards";
export function Trips() {
  const { data } = useQuery({
    queryKey: ["trips"],
    queryFn: tripsService.list,
  });
  const trips = data?.results ?? [];
  return (
    <AppShell>
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-3xl font-black">Trips</h2>
        <button className="btn bg-indigo-600 text-white">Create Trip</button>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {trips.map((t: any) => (
          <article key={t.id} className="glass rounded-3xl p-5">
            <h3 className="text-xl font-bold">{t.name}</h3>
            <p className="text-slate-500">{t.destination}</p>
            <p className="mt-3 text-sm">{t.description}</p>
            <span className="mt-4 inline-block rounded-full bg-indigo-100 px-3 py-1 text-xs text-indigo-700">
              {t.status}
            </span>
          </article>
        ))}
      </div>
      {!trips.length && (
        <EmptyState
          title="No trips yet"
          body="Create a trip and invite friends to start splitting expenses."
        />
      )}
    </AppShell>
  );
}
