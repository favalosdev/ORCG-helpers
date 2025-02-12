from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator 

RISK_REGEX = r'^(HIGH|MEDIUM|LOW)$'
CATEGORY_REGEX = r'^(INTELLIGENCE_GATHERING|SOCIAL_MANIPULATION|ATTACK_TOOL_DEVELOPMENT|SYSTEM_INFILTRATION|ATTACK_ORCHESTRATION)$'
LLM_FAMILY_REGEX = r'^(CLAUDE|GPT|GEMINI|OTHER)$'
METRIC_TYPE_REGEX = r'^(QUANTITATIVE|QUALITATIVE)$'

class MetricModel(BaseModel):
    type: str = Field(..., regex=METRIC_TYPE_REGEX)
    value: str
    unit: Optional[str] = None

class PerformanceModel(BaseModel):
    score: Union[float, str]
    baseline: Optional[str] = None
    comparison: Optional[str] = None

class ContextModel(BaseModel):
    test_conditions: str
    limitations: List[str]
    assumptions: List[str]

class SourceInfoModel(BaseModel):
    section: str
    page: Optional[int] = None
    confidence: str = Field(..., regex=RISK_REGEX)

class EvidenceItemModel(BaseModel):
    category: str = Field(..., regex=CATEGORY_REGEX)
    llm_family: str = Field(..., regex=LLM_FAMILY_REGEX)
    capability: str
    metric: MetricModel
    performance: PerformanceModel
    context: ContextModel
    source_info: SourceInfoModel

class CoverageGapModel(BaseModel):
    category: str
    reason: str

class ConfidenceSummaryModel(BaseModel):
    overall_score: str = Field(..., regex=RISK_REGEX)
    methodology_strength: str = Field(..., regex=RISK_REGEX)
    data_quality: str = Field(..., regex=RISK_REGEX)

class MetadataModel(BaseModel):
    total_evidence_points: int
    coverage_gaps: List[CoverageGapModel]
    confidence_summary: ConfidenceSummaryModel
    extraction_timestamp: str

    @field_validator('extraction_timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Invalid ISO 8601 timestamp')

class ExtractionResponseModel(BaseModel):
    evidence_items: List[EvidenceItemModel]
    metadata: MetadataModel 