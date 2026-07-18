import * as React from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { AppShell } from "@/components/layout/AppShell"
import { LandingPage } from "@/pages/LandingPage"
import { LoginPage } from "@/pages/LoginPage"
import { DashboardPage } from "@/pages/DashboardPage"
import { DocumentsLibraryPage } from "@/pages/DocumentsLibraryPage"
import { UploadCenterPage } from "@/pages/UploadCenterPage"
import { KnowledgeGraphPage } from "@/pages/KnowledgeGraphPage"
import { AssetsPage } from "@/pages/AssetsPage"
import { CopilotPage } from "@/pages/CopilotPage"
import { AnalyticsPage } from "@/pages/AnalyticsPage"
import { SettingsPage } from "@/pages/SettingsPage"
import { ErrorBoundary } from "@/components/ui/ErrorBoundary"
import { RegisterPage } from "@/pages/RegisterPage"
import { useAuthStore } from "@/store/useAuthStore"

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected App Routes */}
        <Route path="/app" element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
          <Route index element={<Navigate to="/app/dashboard" replace />} />
          <Route path="dashboard" element={<ErrorBoundary><DashboardPage /></ErrorBoundary>} />
          <Route path="documents" element={<ErrorBoundary><DocumentsLibraryPage /></ErrorBoundary>} />
          <Route path="documents/upload" element={<ErrorBoundary><UploadCenterPage /></ErrorBoundary>} />
          <Route path="knowledge-graph" element={<ErrorBoundary><KnowledgeGraphPage /></ErrorBoundary>} />
          <Route path="assets" element={<ErrorBoundary><AssetsPage /></ErrorBoundary>} />
          <Route path="copilot" element={<ErrorBoundary><CopilotPage /></ErrorBoundary>} />
          <Route path="analytics" element={<ErrorBoundary><AnalyticsPage /></ErrorBoundary>} />
          <Route path="settings" element={<ErrorBoundary><SettingsPage /></ErrorBoundary>} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
