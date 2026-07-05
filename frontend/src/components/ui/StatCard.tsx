import { motion } from "framer-motion";
export function StatCard({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-3xl p-5"
    >
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-3xl font-black text-indigo-600">{value}</p>
    </motion.div>
  );
}
