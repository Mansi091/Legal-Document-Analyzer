import json
import logging
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

def analyze_contract(contract_text: str, user_api_key: str = None):
    logs = ["Received contract text for analysis."]
    llm = get_llm(user_api_key)

    if not llm:
        logs.append("No Groq API Key found. Operating in Demo/Mock Mode.")
        logs.append("Classified contract: SaaS Vendor Subscription Agreement (Demo)")
        logs.append("Running contract review simulations...")
        logs.append("Review complete. Report formatted successfully.")
        return {
            "contract_type": "SaaS Vendor Subscription Agreement",
            "risks": [
                {
                    "clause_type": "limitation_of_liability",
                    "section": "10. Limitation of Liability",
                    "severity": "High",
                    "explanation": "Caps vendor's liability at ₹5,00,000, which is extremely low for SaaS subscriptions.",
                    "text_found": "Vendor's total liability under this Agreement shall not exceed ₹5,00,000 under any circumstances."
                },
                {
                    "clause_type": "termination_and_renewal",
                    "section": "Clause 8. Term & Renewal",
                    "severity": "Medium",
                    "explanation": "Requires a 90-day prior written notice to prevent auto-renewal, which is an industry renewal trap.",
                    "text_found": "This Agreement will automatically renew for successive 12-month periods unless either party provides written notice of non-renewal at least 90 days prior..."
                }
            ],
            "missing_clauses": [
                {
                    "clause_type": "confidentiality",
                    "title": "Confidentiality Obligations",
                    "explanation": "Standard mutual confidentiality protections are missing from the agreement.",
                    "suggested_text": "Each party agrees to protect the other's Confidential Information with the same degree of care it uses for its own confidential info, but not less than reasonable care."
                }
            ],
            "contradictions": [
                {
                    "sections_involved": ["Section 5. IP Rights", "Section 10. Limitation of Liability"],
                    "explanation": "Section 5 specifies unlimited IP indemnification, but Section 10 caps total liability at ₹5,00,000, creating a conflict."
                }
            ],
            "logs": logs
        }

    logs.append("Groq API connection established. Initializing live analysis...")

    # Truncate contract text if it is excessively long to prevent token rate limits
    max_char_limit = 12000
    safe_contract_text = contract_text
    if len(contract_text) > max_char_limit:
        logs.append(f"Contract text length ({len(contract_text)} chars) exceeds safety limits. Truncating to {max_char_limit} chars for API compliance.")
        safe_contract_text = contract_text[:max_char_limit] + "\n\n... [Remaining text truncated] ..."

    prompt = (
        "You are an expert legal AI assistant specializing in contract review.\n"
        "Analyze the provided contract text and perform the following reviews:\n"
        "1. Classify the contract type (e.g. SaaS Agreement, NDA, Services Agreement).\n"
        "2. Identify potential high or medium risks (e.g. unfavorable liability caps, automatic renewal terms, harsh termination clauses).\n"
        "3. Identify critical missing clauses that should be included for standard buyer/customer protection.\n"
        "4. Detect any internal contradictions or conflicts in the text (e.g. unlimited IP indemnity vs a low overall liability cap).\n\n"
        "You MUST return your analysis ONLY as a raw JSON object matching the following structure:\n"
        "{\n"
        '  "contract_type": "string",\n'
        '  "risks": [\n'
        "    {\n"
        '      "clause_type": "string (e.g. limitation_of_liability, termination, renewal)",\n'
        '      "section": "string (name/number of section, e.g. Section 10)",\n'
        '      "severity": "string (High, Medium, or Low)",\n'
        '      "explanation": "string detailing the risk",\n'
        '      "text_found": "string containing the exact/excerpt of text from the contract"\n'
        "    }\n"
        "  ],\n"
        '  "missing_clauses": [\n'
        "    {\n"
        '      "clause_type": "string (e.g. confidentiality, data_privacy, governing_law)",\n'
        '      "title": "string title",\n'
        '      "explanation": "string explaining why it is missing and why it matters",\n'
        '      "suggested_text": "string containing proposed legal language to insert"\n'
        "    }\n"
        "  ],\n"
        '  "contradictions": [\n'
        "    {\n"
        '      "sections_involved": ["string (section name)", "string (section name)"],\n'
        '      "explanation": "string explaining the conflict"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Do not include any chat prefix, suffix, markdown wrapper (like ```json), or extra text outside the JSON object itself."
    )

    try:
        import time
        start_time = time.time()
        
        logs.append("Sending contract text to LLM for comprehensive review...")
        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=safe_contract_text)
        ])
        
        latency_seconds = time.time() - start_time
        token_usage = response.response_metadata.get("token_usage", {})
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get("total_tokens", 0)
        
        # Calculate cost based on Groq Llama 3.1 8B pricing: $0.05/1M input, $0.08/1M output
        input_cost = (prompt_tokens / 1_000_000) * 0.05
        output_cost = (completion_tokens / 1_000_000) * 0.08
        total_cost = input_cost + output_cost
        
        logs.append(f"LLM Latency: {latency_seconds:.2f}s")
        logs.append(f"Tokens: {prompt_tokens} input, {completion_tokens} output (Total: {total_tokens})")
        logs.append(f"Estimated API Cost: ${total_cost:.6f} USD")
        
        response_text = response.content.strip()
        
        # Clean markdown wrappers if any
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        logs.append("Parsing analysis results from LLM...")
        parsed_result = json.loads(response_text)
        parsed_result["logs"] = logs + ["Analysis parsing complete. Review successfully generated."]
        return parsed_result

    except Exception as e:
        logger.error(f"Error in direct LLM analysis: {e}")
        logs.append(f"Analysis failed with error: {str(e)}")
        return {
            "contract_type": "Unknown",
            "risks": [],
            "missing_clauses": [
                {
                    "clause_type": "error",
                    "title": "Analysis Error",
                    "explanation": f"The AI analysis pipeline encountered an error: {str(e)}",
                    "suggested_text": ""
                }
            ],
            "contradictions": [],
            "logs": logs
        }