import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { InsightCard, type InsightCardData } from './InsightCard'

// ─── Shared mock data ─────────────────────────────────────────

const mockData: InsightCardData = {
  companyName: 'Stripe',
  ticker: 'STRIPE',
  sector: 'Fintech',
  generatedAt: new Date('2026-05-09T08:00:00Z'),
  executiveSummary:
    'Stripe is the dominant payments infrastructure layer for the internet economy, processing over $1 trillion in annualised TPV.',
  bullCase: [
    'Enterprise bookings accelerating into Q3.',
    'Stablecoin rails capturing cross-border TAM.',
  ],
  bearCase: [
    'Take-rate compression from enterprise negotiations.',
    'Regulatory fragmentation across 50+ jurisdictions.',
  ],
  strategicThemes: ['Platform expansion', 'Stablecoin infrastructure buildout'],
  riskFlags: [
    {
      label: 'Competitive',
      severity: 'HIGH',
      description: 'Adyen closing the developer-experience gap in EMEA.',
    },
    {
      label: 'Regulatory',
      severity: 'MEDIUM',
      description: 'PSD3 reserve requirements could impair capital efficiency.',
    },
    {
      label: 'Macro',
      severity: 'LOW',
      description: 'IT budget freezes at financial-services customers.',
    },
  ],
  valueCreationHypotheses: [
    'Financial services attach rate — Cross-selling Issuing to Capital users grows ARPU.',
  ],
  sources: [
    { label: 'Reuters', href: 'https://example.com/reuters-stripe' },
    { label: 'TechCrunch', href: 'https://example.com/techcrunch-stripe' },
  ],
}

// ─── Executive summary ────────────────────────────────────────

describe('InsightCard — executive summary', () => {
  it('renders the executive summary text', () => {
    render(<InsightCard data={mockData} />)

    expect(screen.getByText(mockData.executiveSummary)).toBeInTheDocument()
  })

  it('renders the "Executive Summary" section label', () => {
    render(<InsightCard data={mockData} />)

    expect(screen.getByText('Executive Summary')).toBeInTheDocument()
  })

  it('renders the company name in the header', () => {
    render(<InsightCard data={mockData} />)

    expect(screen.getByText('Stripe')).toBeInTheDocument()
  })

  it('renders the ticker when provided', () => {
    render(<InsightCard data={mockData} />)

    expect(screen.getByText('STRIPE')).toBeInTheDocument()
  })
})

// ─── Bull / bear cases ────────────────────────────────────────

describe('InsightCard — bull and bear cases', () => {
  it('renders the "Investment Thesis" section label', () => {
    render(<InsightCard data={mockData} />)

    expect(screen.getByText('Investment Thesis')).toBeInTheDocument()
  })

  it('renders all bull-case items', () => {
    render(<InsightCard data={mockData} />)

    for (const point of mockData.bullCase) {
      expect(screen.getByText(point)).toBeInTheDocument()
    }
  })

  it('renders all bear-case items', () => {
    render(<InsightCard data={mockData} />)

    for (const point of mockData.bearCase) {
      expect(screen.getByText(point)).toBeInTheDocument()
    }
  })

  it('renders the "Bull Case" column label', () => {
    render(<InsightCard data={mockData} />)

    expect(screen.getByText('Bull Case')).toBeInTheDocument()
  })

  it('renders the "Bear Case" column label', () => {
    render(<InsightCard data={mockData} />)

    expect(screen.getByText('Bear Case')).toBeInTheDocument()
  })

  it('renders bull and bear items in separate lists', () => {
    render(<InsightCard data={mockData} />)

    const lists = screen.getAllByRole('list')
    const bullList = lists.find((list) =>
      within(list).queryByText(mockData.bullCase[0]) !== null,
    )
    const bearList = lists.find((list) =>
      within(list).queryByText(mockData.bearCase[0]) !== null,
    )

    expect(bullList).toBeDefined()
    expect(bearList).toBeDefined()
    expect(bullList).not.toBe(bearList)
  })
})

// ─── Risk chips ───────────────────────────────────────────────

describe('InsightCard — risk chip severity colours', () => {
  it('renders a chip for every risk flag', () => {
    render(<InsightCard data={mockData} />)

    for (const flag of mockData.riskFlags) {
      expect(screen.getByTitle(flag.description!)).toBeInTheDocument()
    }
  })

  it('applies red (risk-red) background to HIGH severity chips', () => {
    render(<InsightCard data={mockData} />)

    const chip = screen.getByTitle('Adyen closing the developer-experience gap in EMEA.')
    expect(chip.getAttribute('style')).toContain('var(--risk-red-bg)')
    expect(chip.getAttribute('style')).toContain('var(--risk-red-text)')
  })

  it('applies amber (risk-amber) background to MEDIUM severity chips', () => {
    render(<InsightCard data={mockData} />)

    const chip = screen.getByTitle('PSD3 reserve requirements could impair capital efficiency.')
    expect(chip.getAttribute('style')).toContain('var(--risk-amber-bg)')
    expect(chip.getAttribute('style')).toContain('var(--risk-amber-text)')
  })

  it('applies green (risk-green) background to LOW severity chips', () => {
    render(<InsightCard data={mockData} />)

    const chip = screen.getByTitle('IT budget freezes at financial-services customers.')
    expect(chip.getAttribute('style')).toContain('var(--risk-green-bg)')
    expect(chip.getAttribute('style')).toContain('var(--risk-green-text)')
  })

  it('renders "HIGH" label text inside the HIGH severity chip', () => {
    render(<InsightCard data={mockData} />)

    const chip = screen.getByTitle('Adyen closing the developer-experience gap in EMEA.')
    expect(within(chip).getByText('HIGH')).toBeInTheDocument()
  })

  it('renders "MED" label text inside the MEDIUM severity chip', () => {
    render(<InsightCard data={mockData} />)

    const chip = screen.getByTitle('PSD3 reserve requirements could impair capital efficiency.')
    expect(within(chip).getByText('MED')).toBeInTheDocument()
  })

  it('renders "LOW" label text inside the LOW severity chip', () => {
    render(<InsightCard data={mockData} />)

    const chip = screen.getByTitle('IT budget freezes at financial-services customers.')
    expect(within(chip).getByText('LOW')).toBeInTheDocument()
  })

  it('renders the dot indicator inside each risk chip', () => {
    render(<InsightCard data={mockData} />)

    const highChip = screen.getByTitle('Adyen closing the developer-experience gap in EMEA.')
    const dot = highChip.querySelector('span[aria-hidden="true"]')
    expect(dot).not.toBeNull()
    expect(dot!.getAttribute('style')).toContain('var(--risk-red-dot)')
  })
})
