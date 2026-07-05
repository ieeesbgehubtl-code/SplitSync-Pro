import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import "./index.css";
import {
  SearchUsers,
  Friends,
  FriendRequests,
  TripInvitations,
  Notifications,
} from "./pages/Pages";
import { Dashboard } from "./pages/Dashboard";
import { Trips } from "./pages/Trips";
import { Expenses } from "./pages/Expenses";
import { Login, Register } from "./pages/Auth";
const queryClient = new QueryClient();
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Toaster position="top-right" />
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/trips" element={<Trips />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/search" element={<SearchUsers />} />
          <Route path="/friends" element={<Friends />} />
          <Route path="/requests" element={<FriendRequests />} />
          <Route path="/invitations" element={<TripInvitations />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route
            path="*"
            element={
              <div className="grid min-h-screen place-items-center">
                <h1 className="text-4xl font-black">404</h1>
              </div>
            }
          />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
