export interface ApiStrategicTheme {
  theme: string
  evidence: string
  sources: number[]
}

export interface ApiRiskFlag {
  category: string
  severity: 'High' | 'Medium' | 'Low'
  rationale: string
  sources: number[]
}

export interface ApiValueCreationHypothesis {
  lever: string
  hypothesis: string
  evidence: string
  test: string
}

export interface ApiSource {
  id: number
  title: string
  publisher: string
  published_at: string
  url: string
}

export interface InsightReport {
  company: string
  executive_summary: string
  investment_thesis: string
  bull_case: string[]
  bear_case: string[]
  strategic_themes: ApiStrategicTheme[]
  risk_flags: ApiRiskFlag[]
  value_creation_hypotheses: ApiValueCreationHypothesis[]
  sources: ApiSource[]
  generated_at: string
  confidence_caveats: string
}
