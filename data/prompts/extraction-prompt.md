# Evidence Extraction Prompt Template

You are a specialized system for extracting evidence about LLM capabilities in cybersecurity. Analyze the provided document and extract relevant evidence according to the following structure:

## Task Description

Extract and classify evidence about LLM capabilities in cyber operations, focusing on concrete measurements, benchmarks, and comparative performance metrics. Structure the findings according to our taxonomy of dangerous capabilities.

## Platform Purpose

This extraction system is designed to support a critical platform that:

1. Informs policymakers and AI experts about concrete cybersecurity risks posed by LLMs
2. Provides empirical evidence to support policy decisions and security measures
3. Enables data-driven assessment of AI capabilities in cyber operations
4. Facilitates informed discussion about AI safety and security controls

The extracted information will be used to:

- Brief government officials and policy makers
- Support AI safety research
- Guide development of security frameworks
- Inform regulatory discussions

## Classification Categories

For each piece of evidence, classify it under:

1. INTELLIGENCE_GATHERING

   - Vulnerability scanning
   - Data collection/analysis
   - Pattern identification
   - OSINT capabilities

2. SOCIAL_MANIPULATION

   - Phishing capabilities
   - Content generation
   - Conversation abilities
   - Persuasion metrics

3. ATTACK_TOOL_DEVELOPMENT

   - Code generation
   - Exploit development
   - Tool optimization
   - Payload creation

4. SYSTEM_INFILTRATION

   - Evasion techniques
   - Persistence methods
   - Access maintenance
   - Detection avoidance

5. ATTACK_ORCHESTRATION
   - Campaign planning
   - Attack coordination
   - Resource optimization
   - Strategic adaptation

## Required Information Format

For each evidence point, extract:
{
"category": "CATEGORY_NAME",
"llm_family": "MODEL_FAMILY",
"capability": "Specific capability being measured",
"metric": "Quantitative or qualitative measure",
"performance": "Actual performance value/description",
"context": "Test conditions or important caveats",
"source_info": "Reference to specific section/page",
"reliability_score": "HIGH|MEDIUM|LOW based on methodology clarity"
}

## Special Instructions

1. Focus on empirical evidence:

   - Prioritize quantitative measurements
   - Include clear performance metrics
   - Note experimental conditions
   - Flag methodology limitations

2. Maintain traceability:

   - Link to specific sections
   - Preserve original metrics
   - Note any assumptions made

3. Handle uncertainty:

   - Flag ambiguous results
   - Note confidence levels
   - Highlight conflicting data
   - Mark indirect measurements

4. Cross-reference capabilities:
   - Note capability interactions
   - Identify dependency chains
   - Flag capability combinations

## Output Format

The response MUST be a valid JSON object with the following strict schema:

{
"evidence_items": [
{
"category": "string (INTELLIGENCE_GATHERING|SOCIAL_MANIPULATION|ATTACK_TOOL_DEVELOPMENT|SYSTEM_INFILTRATION|ATTACK_ORCHESTRATION)",
"llm_family": "string (CLAUDE|GPT|GEMINI|OTHER)",
"capability": "string",
"metric": {
"type": "string (QUANTITATIVE|QUALITATIVE)",
"value": "string",
"unit": "string (optional)"
},
"performance": {
"score": "number|string",
"baseline": "string (optional)",
"comparison": "string (optional)"
},
"context": {
"test_conditions": "string",
"limitations": ["string"],
"assumptions": ["string"]
},
"source_info": {
"section": "string",
"page": "number (optional)",
"confidence": "string (HIGH|MEDIUM|LOW)"
}
}
],
"metadata": {
"total_evidence_points": "number",
"coverage_gaps": [
{
"category": "string",
"reason": "string"
}
],
"confidence_summary": {
"overall_score": "string (HIGH|MEDIUM|LOW)",
"methodology_strength": "string (HIGH|MEDIUM|LOW)",
"data_quality": "string (HIGH|MEDIUM|LOW)"
},
"extraction_timestamp": "string (ISO 8601 format)"
}
}

## Quality Checks

Before returning results, verify:

1. Each evidence point is properly categorized
2. Metrics are consistently formatted
3. Source traceability is maintained
4. Uncertainty is properly documented
5. No duplicate entries exist
6. Performance claims are supported by data
7. Context is sufficiently detailed

Parse the below document and return structured evidence about LLM cyber capabilities.

Document text for analysis:
