import { http } from "../api/http";
export const reportsService = {
  dashboard: () => http.get("/reports/dashboard/").then((r) => r.data),
};
