import { useMutation } from '@tanstack/react-query'
import { AlertCircle, Search } from 'lucide-react'
import { useState } from 'react'
import type { InsightReport } from '../types'
import { InsightCard, type InsightCardData, type RiskSeverity } from './InsightCard'

// ─── API ──────────────────────────────────────────────────────

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

async function fetchInsights(company: string): Promise<InsightReport> {
  const response = await fetch(`${BASE_URL}/api/insights`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company }),
  })
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}))
    throw new Error(detail?.detail ?? `Request failed with status ${response.status}`)
  }
  return response.json()
}

// ─── Mapper ───────────────────────────────────────────────────

function mapToInsightCardData(report: InsightReport): InsightCardData {
  const severityMap: Record<string, RiskSeverity> = {
    High: 'HIGH',
    Medium: 'MEDIUM',
    Low: 'LOW',
  }

  return {
    companyName: report.company,
    generatedAt: new Date(report.generated_at),
    executiveSummary: report.executive_summary,
    bullCase: report.bull_case,
    bearCase: report.bear_case,
    strategicThemes: report.strategic_themes.map((t) => t.theme),
    riskFlags: report.risk_flags.map((r) => ({
      label: r.category,
      severity: severityMap[r.severity] ?? 'MEDIUM',
      description: r.rationale,
    })),
    valueCreationHypotheses: report.value_creation_hypotheses.map(
      (v) => `${v.lever} — ${v.hypothesis}`,
    ),
    sources: report.sources.map((s) => ({
      label: s.publisher,
      href: s.url,
    })),
  }
}

// ─── Skeleton ─────────────────────────────────────────────────

function SkeletonBar({ width = '100%', height = 'h-3' }: { width?: string; height?: string }) {
  return (
    <div
      className={`rounded ${height} animate-pulse`}
      style={{ width, backgroundColor: 'var(--border)' }}
      aria-hidden="true"
    />
  )
}

function SkeletonCard({ index }: { index: number }) {
  const widths: [string, string, string][] = [
    ['55%', '100%', '75%'],
    ['40%', '90%', '60%'],
    ['48%', '95%', '82%'],
  ]
  const [head, body, tail] = widths[index % 3]

  return (
    <div
      className="rounded overflow-hidden"
      style={{ border: '1px solid var(--border)', borderRadius: '4px' }}
    >
      <div
        className="h-1"
        style={{ backgroundColor: 'var(--navy)', opacity: 0.18 + index * 0.06 }}
        aria-hidden="true"
      />
      <div className="px-5 py-4 space-y-2.5" style={{ backgroundColor: 'var(--card)' }}>
        <SkeletonBar width={head} height="h-3" />
        <SkeletonBar width={body} height="h-2.5" />
        <SkeletonBar width={tail} height="h-2.5" />
      </div>
    </div>
  )
}

// ─── Main component ───────────────────────────────────────────

export function SearchInterface() {
  const [query, setQuery] = useState('')

  const { mutate, isPending, data, isError, error, isSuccess } = useMutation({
    mutationFn: fetchInsights,
  })

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!query.trim()) return
    mutate(query.trim())
  }

  const cardData = data ? mapToInsightCardData(data) : null
  const hasResult = isSuccess || isError || isPending

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: 'var(--background)' }}>

      {/* ── Top bar ── */}
      <header
        className="w-full px-6 py-3.5 flex items-center justify-between"
        style={{ backgroundColor: 'var(--navy)' }}
      >
        <div className="flex items-center gap-3">
          <span className="text-white font-semibold text-sm tracking-tight leading-none">
            Bain {'&'} Company
          </span>
          <span
            className="w-px h-4 flex-shrink-0"
            style={{ backgroundColor: 'rgba(255,255,255,0.2)' }}
            aria-hidden="true"
          />
          <span className="text-sm font-medium tracking-wide" style={{ color: 'rgba(255,255,255,0.65)' }}>
            Intelligence
          </span>
        </div>
        <span
          className="text-[10px] font-semibold tracking-[0.18em] uppercase px-2 py-0.5 rounded"
          style={{ color: 'rgba(255,255,255,0.45)', border: '1px solid rgba(255,255,255,0.15)' }}
        >
          Internal
        </span>
      </header>

      {/* ── Main content ── */}
      <main className="flex-1 flex flex-col items-center px-4 pt-24 pb-16">

        {/* Heading */}
        <div className="w-full max-w-xl text-center mb-8">
          <h1
            className="text-2xl font-semibold tracking-tight text-balance mb-2"
            style={{ color: 'var(--foreground)' }}
          >
            Intelligence Search
          </h1>
          <p className="text-sm leading-relaxed" style={{ color: 'var(--muted-foreground)' }}>
            Generate an on-demand briefing for any company.
          </p>
        </div>

        {/* Search form */}
        <form
          onSubmit={handleSubmit}
          className="w-full max-w-xl"
          role="search"
          aria-label="Company intelligence search"
        >
          <div className="flex gap-2">
            <label htmlFor="company-search" className="sr-only">Company name</label>
            <div className="relative flex-1">
              <Search
                className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
                style={{ color: 'var(--muted-foreground)' }}
                aria-hidden="true"
              />
              <input
                id="company-search"
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter company name (e.g. Stripe, Shopify)"
                autoComplete="off"
                spellCheck={false}
                disabled={isPending}
                className="w-full pl-9 pr-3 py-2.5 text-sm rounded outline-none transition-shadow disabled:opacity-60"
                style={{
                  borderRadius: '4px',
                  border: '1px solid var(--border)',
                  backgroundColor: 'var(--card)',
                  color: 'var(--foreground)',
                  boxShadow: 'none',
                }}
                onFocus={(e) => {
                  e.currentTarget.style.boxShadow = '0 0 0 2px rgba(0,52,120,0.25)'
                  e.currentTarget.style.borderColor = 'var(--navy)'
                }}
                onBlur={(e) => {
                  e.currentTarget.style.boxShadow = 'none'
                  e.currentTarget.style.borderColor = 'var(--border)'
                }}
              />
            </div>
            <button
              type="submit"
              disabled={!query.trim() || isPending}
              className="flex items-center gap-2 px-4 py-2.5 text-sm font-semibold text-white transition-opacity disabled:opacity-40 disabled:cursor-not-allowed"
              style={{ borderRadius: '4px', backgroundColor: 'var(--navy)', flexShrink: 0 }}
            >
              <Search className="w-3.5 h-3.5" aria-hidden="true" />
              {isPending ? 'Searching…' : 'Search'}
            </button>
          </div>
        </form>

        {/* Keyboard hint — only before first search */}
        {!hasResult && (
          <p className="mt-3 text-[11px]" style={{ color: 'var(--muted-foreground)' }}>
            Press{' '}
            <kbd
              className="font-mono px-1 py-0.5 rounded text-[10px]"
              style={{ border: '1px solid var(--border)', color: 'var(--muted-foreground)' }}
            >
              Enter
            </kbd>
            {' '}to generate a briefing
          </p>
        )}

        {/* ── Skeleton ── */}
        {isPending && (
          <div
            className="w-full max-w-xl mt-10"
            aria-live="polite"
            aria-label="Loading intelligence brief"
          >
            <div className="flex items-center gap-2 mb-4" style={{ color: 'var(--muted-foreground)' }}>
              <span className="flex gap-0.5" aria-hidden="true">
                {[0, 1, 2].map((i) => (
                  <span
                    key={i}
                    className="w-1 h-1 rounded-full animate-bounce"
                    style={{ backgroundColor: 'var(--navy)', opacity: 0.5, animationDelay: `${i * 120}ms` }}
                  />
                ))}
              </span>
              <span className="text-xs font-medium">
                Generating intelligence brief for{' '}
                <span className="font-semibold" style={{ color: 'var(--navy)' }}>{query}</span>
                &hellip;
              </span>
            </div>
            <div className="space-y-3">
              {[0, 1, 2].map((i) => (
                <SkeletonCard key={i} index={i} />
              ))}
            </div>
          </div>
        )}

        {/* ── Error ── */}
        {isError && (
          <div
            className="w-full max-w-xl mt-10 flex items-start gap-3 px-4 py-3.5 rounded text-sm"
            style={{
              backgroundColor: 'var(--risk-red-bg)',
              border: '1px solid var(--bear-border)',
              color: 'var(--risk-red-text)',
              borderRadius: '4px',
            }}
            role="alert"
          >
            <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" aria-hidden="true" />
            <span>{error instanceof Error ? error.message : 'Something went wrong. Please try again.'}</span>
          </div>
        )}

        {/* ── Result ── */}
        {isSuccess && cardData && (
          <div className="w-full max-w-3xl mt-10">
            <InsightCard data={cardData} />
          </div>
        )}

      </main>

      {/* ── Footer ── */}
      <footer
        className="w-full py-3 text-center text-[11px]"
        style={{ color: 'var(--muted-foreground)', borderTop: '1px solid var(--border)' }}
      >
        Bain Intelligence Platform &mdash; For internal use only &middot; Not for distribution
      </footer>

    </div>
  )
}
