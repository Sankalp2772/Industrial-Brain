import * as React from "react"
import { Activity, Database, Network, ShieldCheck } from "lucide-react"

const features = [
  {
    name: 'Predictive Maintenance',
    description: 'Analyze telemetry and vibration data in real-time to predict failures before they happen, drastically reducing unplanned downtime.',
    icon: Activity,
  },
  {
    name: 'Unified Data Ingestion',
    description: 'Connect to historians, SCADA systems, and ERPs securely. A single pane of glass for all your industrial data streams.',
    icon: Database,
  },
  {
    name: 'Knowledge Graph',
    description: 'Map complex relationships between parts, machines, maintenance logs, and operational manuals to uncover hidden insights.',
    icon: Network,
  },
  {
    name: 'Enterprise Security',
    description: 'Built with SOC2 compliance in mind. Your data remains isolated, encrypted, and governed by strict role-based access controls.',
    icon: ShieldCheck,
  },
]

export function Features() {
  return (
    <div className="py-24 sm:py-32 bg-surface">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-primary">Core Capabilities</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Everything you need to modernize plant operations
          </p>
          <p className="mt-6 text-lg leading-8 text-muted-foreground">
            Industrial Brain bridges the gap between legacy operational technology (OT) and modern AI infrastructure.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-2">
            {features.map((feature) => (
              <div key={feature.name} className="flex flex-col border border-border p-8 rounded-xl bg-card shadow-sm hover:shadow-enterprise transition-shadow duration-300">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-foreground">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                    <feature.icon className="h-6 w-6 text-primary" aria-hidden="true" />
                  </div>
                  {feature.name}
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-muted-foreground">
                  <p className="flex-auto">{feature.description}</p>
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  )
}
