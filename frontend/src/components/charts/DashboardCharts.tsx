import {
  BarChart,
  Bar,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";
const COLORS = ["#4f46e5", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"];
export function MonthlyChart({ data }: { data: any[] }) {
  return (
    <div className="glass h-80 rounded-3xl p-5">
      <h3 className="font-bold">Monthly spending</h3>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="total" fill="#4f46e5" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
export function CategoryPie({ data }: { data: any[] }) {
  return (
    <div className="glass h-80 rounded-3xl p-5">
      <h3 className="font-bold">Category spending</h3>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="total"
            nameKey="category__name"
            outerRadius={90}
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
