import { Building2, Clock, ExternalLink, TrendingDown, TrendingUp } from 'lucide-react'

// ─── Data types ───────────────────────────────────────────────

export type RiskSeverity = 'HIGH' | 'MEDIUM' | 'LOW'

export interface RiskFlag {
  label: string
  severity: RiskSeverity
  description?: string
}

export interface Source {
  label: string
  href: string
}

export interface InsightCardData {
  companyName: string
  ticker?: string
  sector?: string
  generatedAt: Date
  executiveSummary: string
  bullCase: string[]
  bearCase: string[]
  strategicThemes: string[]
  riskFlags: RiskFlag[]
  valueCreationHypotheses: string[]
  sources: Source[]
}

// ─── Sub-components ───────────────────────────────────────────

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <span
        className="text-[10px] font-semibold tracking-[0.12em] uppercase"
        style={{ color: 'var(--navy)' }}
      >
        {children}
      </span>
      <div className="flex-1 h-px" style={{ backgroundColor: 'var(--navy)', opacity: 0.15 }} />
    </div>
  )
}

function RiskChip({ flag }: { flag: RiskFlag }) {
  const map: Record<RiskSeverity, { bg: string; text: string; dot: string; label: string }> = {
    HIGH:   { bg: 'var(--risk-red-bg)',   text: 'var(--risk-red-text)',   dot: 'var(--risk-red-dot)',   label: 'HIGH' },
    MEDIUM: { bg: 'var(--risk-amber-bg)', text: 'var(--risk-amber-text)', dot: 'var(--risk-amber-dot)', label: 'MED'  },
    LOW:    { bg: 'var(--risk-green-bg)', text: 'var(--risk-green-text)', dot: 'var(--risk-green-dot)', label: 'LOW'  },
  }
  const c = map[flag.severity]
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded"
      style={{ backgroundColor: c.bg, color: c.text }}
      title={flag.description}
    >
      <span
        className="w-1.5 h-1.5 rounded-full flex-shrink-0"
        style={{ backgroundColor: c.dot }}
        aria-hidden="true"
      />
      <span>{flag.label}</span>
      <span className="ml-0.5 text-[10px] font-semibold tracking-wider opacity-60">{c.label}</span>
    </span>
  )
}

function ThemeTag({ label }: { label: string }) {
  return (
    <span
      className="inline-block px-2.5 py-1 text-xs font-medium tracking-wide rounded border"
      style={{
        backgroundColor: 'var(--navy-light)',
        color: 'var(--navy)',
        borderColor: 'rgba(0,52,120,0.2)',
      }}
    >
      {label}
    </span>
  )
}

function SourceChip({ source }: { source: Source }) {
  return (
    <a
      href={source.href}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1 px-2 py-0.5 text-[11px] font-medium rounded border transition-colors hover:opacity-80"
      style={{
        backgroundColor: 'var(--navy-light)',
        color: 'var(--navy)',
        borderColor: 'rgba(0,52,120,0.2)',
      }}
    >
      {source.label}
      <ExternalLink className="w-2.5 h-2.5" aria-hidden="true" />
    </a>
  )
}

// ─── Main InsightCard ─────────────────────────────────────────

export function InsightCard({ data }: { data: InsightCardData }) {
  const ts = data.generatedAt.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short',
  })

  return (
    <article
      className="w-full max-w-3xl mx-auto shadow-lg overflow-hidden"
      style={{ borderRadius: '4px', border: '1px solid rgba(0,52,120,0.15)' }}
    >
      {/* ── Header ── */}
      <header className="px-6 py-4" style={{ backgroundColor: 'var(--navy)' }}>
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div
              className="flex items-center justify-center w-8 h-8 rounded flex-shrink-0"
              style={{ backgroundColor: 'rgba(255,255,255,0.12)' }}
              aria-hidden="true"
            >
              <Building2 className="w-4 h-4 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2.5 flex-wrap">
                <h1 className="text-white font-semibold text-lg leading-tight tracking-tight">
                  {data.companyName}
                </h1>
                {data.ticker && (
                  <span
                    className="text-[11px] font-mono font-semibold px-1.5 py-0.5 rounded tracking-widest"
                    style={{ backgroundColor: 'rgba(255,255,255,0.15)', color: 'rgba(255,255,255,0.9)' }}
                  >
                    {data.ticker}
                  </span>
                )}
                {data.sector && (
                  <span
                    className="text-[10px] font-medium tracking-wider uppercase"
                    style={{ color: 'rgba(255,255,255,0.5)' }}
                  >
                    {data.sector}
                  </span>
                )}
              </div>
              <p
                className="text-[11px] mt-0.5 font-medium tracking-wide"
                style={{ color: 'rgba(255,255,255,0.55)' }}
              >
                INTELLIGENCE BRIEF · BAIN {'&'} COMPANY
              </p>
            </div>
          </div>

          <div
            className="flex items-center gap-1.5 flex-shrink-0 text-[11px] font-medium"
            style={{ color: 'rgba(255,255,255,0.55)' }}
          >
            <Clock className="w-3 h-3" aria-hidden="true" />
            <time dateTime={data.generatedAt.toISOString()}>{ts}</time>
          </div>
        </div>

        <div
          className="mt-4 h-px"
          style={{ backgroundColor: 'rgba(255,255,255,0.12)' }}
          aria-hidden="true"
        />
      </header>

      {/* ── Body ── */}
      <div style={{ backgroundColor: 'var(--card)', color: 'var(--foreground)' }}>

        {/* Executive Summary */}
        <section className="px-6 pt-5 pb-5" style={{ borderBottom: '1px solid var(--border)' }}>
          <SectionLabel>Executive Summary</SectionLabel>
          <p
            className="text-sm leading-relaxed font-normal"
            style={{
              color: 'var(--foreground)',
              borderLeft: '3px solid var(--navy)',
              paddingLeft: '0.875rem',
            }}
          >
            {data.executiveSummary}
          </p>
        </section>

        {/* Investment Thesis — bull / bear */}
        <section className="px-6 pt-5 pb-5" style={{ borderBottom: '1px solid var(--border)' }}>
          <SectionLabel>Investment Thesis</SectionLabel>
          <div className="grid grid-cols-2 gap-3">
            {/* Bull */}
            <div
              className="rounded p-3.5"
              style={{ backgroundColor: 'var(--bull-bg)', border: '1px solid rgba(22,163,74,0.3)' }}
            >
              <div className="flex items-center gap-1.5 mb-2.5">
                <TrendingUp className="w-3.5 h-3.5" style={{ color: 'var(--bull-border)' }} aria-hidden="true" />
                <span className="text-[10px] font-bold tracking-[0.1em] uppercase" style={{ color: 'var(--bull-border)' }}>
                  Bull Case
                </span>
              </div>
              <ul className="space-y-1.5" role="list">
                {data.bullCase.map((point, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs leading-relaxed" style={{ color: 'var(--bull-text)' }}>
                    <span className="mt-1.5 w-1 h-1 rounded-full flex-shrink-0" style={{ backgroundColor: 'var(--bull-border)' }} aria-hidden="true" />
                    {point}
                  </li>
                ))}
              </ul>
            </div>

            {/* Bear */}
            <div
              className="rounded p-3.5"
              style={{ backgroundColor: 'var(--bear-bg)', border: '1px solid rgba(220,38,38,0.3)' }}
            >
              <div className="flex items-center gap-1.5 mb-2.5">
                <TrendingDown className="w-3.5 h-3.5" style={{ color: 'var(--bear-border)' }} aria-hidden="true" />
                <span className="text-[10px] font-bold tracking-[0.1em] uppercase" style={{ color: 'var(--bear-border)' }}>
                  Bear Case
                </span>
              </div>
              <ul className="space-y-1.5" role="list">
                {data.bearCase.map((point, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs leading-relaxed" style={{ color: 'var(--bear-text)' }}>
                    <span className="mt-1.5 w-1 h-1 rounded-full flex-shrink-0" style={{ backgroundColor: 'var(--bear-border)' }} aria-hidden="true" />
                    {point}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* Strategic Themes */}
        <section className="px-6 pt-5 pb-5" style={{ borderBottom: '1px solid var(--border)' }}>
          <SectionLabel>Strategic Themes</SectionLabel>
          <div className="flex flex-wrap gap-2" role="list" aria-label="Strategic themes">
            {data.strategicThemes.map((theme, i) => (
              <div key={i} role="listitem">
                <ThemeTag label={theme} />
              </div>
            ))}
          </div>
        </section>

        {/* Risk Flags */}
        <section className="px-6 pt-5 pb-5" style={{ borderBottom: '1px solid var(--border)' }}>
          <SectionLabel>Risk Flags</SectionLabel>
          <div className="flex flex-wrap gap-2" role="list" aria-label="Risk flags by severity">
            {data.riskFlags.map((flag, i) => (
              <div key={i} role="listitem">
                <RiskChip flag={flag} />
              </div>
            ))}
          </div>
        </section>

        {/* Value Creation Hypotheses */}
        <section className="px-6 pt-5 pb-5" style={{ borderBottom: '1px solid var(--border)' }}>
          <SectionLabel>Value Creation Hypotheses</SectionLabel>
          <ol className="space-y-2.5 list-none" role="list">
            {data.valueCreationHypotheses.map((hyp, i) => (
              <li key={i} className="flex items-start gap-3 text-sm leading-relaxed">
                <span
                  className="flex-shrink-0 flex items-center justify-center w-5 h-5 rounded text-[11px] font-bold mt-0.5"
                  style={{ backgroundColor: 'var(--navy)', color: '#ffffff', minWidth: '1.25rem' }}
                  aria-hidden="true"
                >
                  {i + 1}
                </span>
                <span style={{ color: 'var(--foreground)' }}>{hyp}</span>
              </li>
            ))}
          </ol>
        </section>

        {/* Sources */}
        <footer className="px-6 pt-4 pb-5">
          <SectionLabel>Sources</SectionLabel>
          <div className="flex flex-wrap gap-1.5" role="list" aria-label="Source citations">
            {data.sources.map((src, i) => (
              <div key={i} role="listitem">
                <SourceChip source={src} />
              </div>
            ))}
          </div>
        </footer>
      </div>
    </article>
  )
}
