import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../components/layout/AppShell";
import { expensesService } from "../services/expenses";
export function Expenses() {
  const { data } = useQuery({
    queryKey: ["expenses"],
    queryFn: () => expensesService.list(),
  });
  const expenses = data?.results ?? [];
  return (
    <AppShell>
      <h2 className="mb-6 text-3xl font-black">Expenses</h2>
      <div className="glass overflow-hidden rounded-3xl">
        <table className="w-full text-left">
          <thead className="bg-white/50 dark:bg-slate-800">
            <tr>
              <th className="p-4">Title</th>
              <th>Amount</th>
              <th>Date</th>
              <th>Split</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((e: any) => (
              <tr key={e.id} className="border-t border-white/20">
                <td className="p-4 font-medium">{e.title}</td>
                <td>{e.amount}</td>
                <td>{e.expense_date}</td>
                <td>{e.split_method}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AppShell>
  );
}
