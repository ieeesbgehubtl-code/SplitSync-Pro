import { http } from "../api/http";
export const expensesService = {
  list: (params?: Record<string, string>) =>
    http.get("/expenses/", { params }).then((r) => r.data),
  create: (data: unknown) => http.post("/expenses/", data).then((r) => r.data),
  categories: () => http.get("/expenses/categories/").then((r) => r.data),
  payments: (data: unknown) =>
    http.post("/payments/", data).then((r) => r.data),
};
