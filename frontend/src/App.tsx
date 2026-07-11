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

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />

        {/* Protected App Routes */}
        <Route path="/app" element={<AppShell />}>
          <Route index element={<Navigate to="/app/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="documents" element={<DocumentsLibraryPage />} />
          <Route path="documents/upload" element={<UploadCenterPage />} />
          <Route path="knowledge-graph" element={<KnowledgeGraphPage />} />
          <Route path="assets" element={<AssetsPage />} />
          <Route path="copilot" element={<CopilotPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
