from pydantic import BaseModel


class StrategicTheme(BaseModel):
    theme: str
    evidence: str
    sources: list[int]


class RiskFlag(BaseModel):
    category: str
    severity: str
    rationale: str
    sources: list[int]


class ValueCreationHypothesis(BaseModel):
    lever: str
    hypothesis: str
    evidence: str
    test: str


class Source(BaseModel):
    id: int
    title: str
    publisher: str
    published_at: str
    url: str


class InsightReport(BaseModel):
    company: str
    executive_summary: str
    investment_thesis: str
    bull_case: list[str]
    bear_case: list[str]
    strategic_themes: list[StrategicTheme]
    risk_flags: list[RiskFlag]
    value_creation_hypotheses: list[ValueCreationHypothesis]
    sources: list[Source]
    generated_at: str
    confidence_caveats: str


class InsightRequest(BaseModel):
    company: str
