import * as React from "react"
import { Bell, Lock, User, Monitor, Key, Shield, Database, Save } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"

export function SettingsPage() {
  const [activeTab, setActiveTab] = React.useState("general")

  return (
    <div className="space-y-6 max-w-5xl animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground mt-1">Manage platform configuration and integrations.</p>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <div className="w-full md:w-64 flex-shrink-0">
          <nav className="flex flex-col space-y-1">
            <SettingsTab id="general" active={activeTab} onClick={setActiveTab} icon={Monitor} label="General Settings" />
            <SettingsTab id="profile" active={activeTab} onClick={setActiveTab} icon={User} label="Profile & Access" />
            <SettingsTab id="notifications" active={activeTab} onClick={setActiveTab} icon={Bell} label="Alerts & Notifications" />
            <SettingsTab id="integrations" active={activeTab} onClick={setActiveTab} icon={Database} label="System Integrations" />
            <SettingsTab id="security" active={activeTab} onClick={setActiveTab} icon={Shield} label="Security & Compliance" />
          </nav>
        </div>

        <div className="flex-1">
          <Card className="shadow-sm">
            <CardHeader>
              <CardTitle>Platform Integrations</CardTitle>
              <CardDescription>Configure connections to your existing industrial infrastructure.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b pb-4">
                  <div>
                    <h3 className="font-semibold">SAP ERP Connection</h3>
                    <p className="text-sm text-muted-foreground">Sync maintenance work orders and inventory.</p>
                  </div>
                  <Button variant="outline">Configure</Button>
                </div>
                
                <div className="flex items-center justify-between border-b pb-4">
                  <div>
                    <h3 className="font-semibold">OSIsoft PI System</h3>
                    <p className="text-sm text-muted-foreground">Connect to historian for real-time telemetry ingestion.</p>
                  </div>
                  <Button variant="secondary">Connected</Button>
                </div>

                <div className="flex items-center justify-between border-b pb-4">
                  <div>
                    <h3 className="font-semibold">Azure IoT Hub</h3>
                    <p className="text-sm text-muted-foreground">Stream sensor data directly into the knowledge graph.</p>
                  </div>
                  <Button variant="outline">Configure</Button>
                </div>
              </div>

              <div className="space-y-4 pt-4 border-t">
                 <h3 className="text-lg font-semibold mb-4">API Keys</h3>
                 <div className="space-y-2">
                   <Label>Primary Production Key</Label>
                   <div className="flex gap-2">
                     <Input readOnly type="password" value="sk-industrial-brain-1234567890abcdef" className="font-mono bg-muted" />
                     <Button variant="outline" size="icon"><Key className="w-4 h-4" /></Button>
                   </div>
                   <p className="text-xs text-muted-foreground">Used for external SCADA system webhooks.</p>
                 </div>
              </div>

              <div className="pt-6 flex justify-end">
                <Button><Save className="w-4 h-4 mr-2" /> Save Changes</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function SettingsTab({ id, active, onClick, icon: Icon, label }: { id: string, active: string, onClick: (id: string) => void, icon: any, label: string }) {
  const isActive = active === id
  return (
    <button
      onClick={() => onClick(id)}
      className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
        isActive
          ? "bg-primary/10 text-primary"
          : "text-muted-foreground hover:bg-muted hover:text-foreground"
      }`}
    >
      <Icon className={`mr-3 h-4 w-4 ${isActive ? "text-primary" : "text-muted-foreground"}`} />
      {label}
    </button>
  )
}
