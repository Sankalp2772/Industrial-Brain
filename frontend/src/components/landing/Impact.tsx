import * as React from "react"
import { TrendingDown, Clock, Wrench } from "lucide-react"

const stats = [
  { id: 1, name: 'Reduction in unplanned downtime', value: '30%', icon: TrendingDown },
  { id: 2, name: 'Faster troubleshooting resolution', value: '45%', icon: Clock },
  { id: 3, name: 'Increase in maintenance efficiency', value: '25%', icon: Wrench },
]

export function Impact() {
  return (
    <div className="py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:max-w-none">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Proven Business Impact
            </h2>
            <p className="mt-4 text-lg leading-8 text-muted-foreground">
              Trusted by leading manufacturers to deliver measurable ROI within the first quarter of deployment.
            </p>
          </div>
          <dl className="mt-16 grid grid-cols-1 gap-0.5 overflow-hidden rounded-2xl text-center sm:grid-cols-2 lg:grid-cols-3 bg-border">
            {stats.map((stat) => (
              <div key={stat.id} className="flex flex-col bg-card p-8 hover:bg-surface transition-colors">
                <dt className="text-sm font-semibold leading-6 text-muted-foreground flex items-center justify-center gap-2">
                  <stat.icon className="w-4 h-4" />
                  {stat.name}
                </dt>
                <dd className="order-first text-4xl font-bold tracking-tight text-foreground mb-4">
                  {stat.value}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  )
}
