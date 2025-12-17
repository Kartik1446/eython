"""
Mock worker agents used by the Streamlit demo app.
These provide deterministic, offline data so the app runs without external APIs.
"""

from typing import Dict, Any, List
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class IQVIAInsightsAgent:
    def run(self, molecule: str, indication: str, geography: str = "US") -> Dict[str, Any]:
        # Mock market data
        raw_rows = [
            {"year": 2020, "sales_usd_mn": 120},
            {"year": 2021, "sales_usd_mn": 135},
            {"year": 2022, "sales_usd_mn": 150},
            {"year": 2023, "sales_usd_mn": 160},
            {"year": 2024, "sales_usd_mn": 172},
        ]
        return {
            "market_size_usd_mn": raw_rows[-1]["sales_usd_mn"],
            "cagr_3yr_pct": 4.8,
            "top_year": 2024,
            "comments": f"Mock IQVIA-style market overview for {molecule} in {geography}.",
            "raw_rows": raw_rows,
        }


class EXIMTrendsAgent:
    def run(self, molecule: str, geography: str = "US") -> Dict[str, Any]:
        # Mock trade data
        trade_rows = [
            {"country": "IN", "price_usd_per_kg": 95, "volume_kg": 12000},
            {"country": "CN", "price_usd_per_kg": 88, "volume_kg": 9000},
            {"country": "DE", "price_usd_per_kg": 110, "volume_kg": 3500},
        ]
        avg_price = round(sum(r["price_usd_per_kg"] for r in trade_rows) / len(trade_rows), 2)
        return {
            "api_import_dependency": "High",
            "avg_import_price_per_kg_usd": avg_price,
            "comments": f"Mock EXIM-style trade overview for API related to {molecule}.",
            "raw_rows": trade_rows,
        }


class PatentLandscapeAgent:
    def run(self, molecule: str) -> Dict[str, Any]:
        patents = [
            {"assignee": "PharmaCorp", "title": f"Formulations of {molecule}", "year": 2018},
            {"assignee": "GenPharm", "title": f"Use of {molecule} in neuropathic pain", "year": 2017},
        ]
        return {
            "core_patent_expiry": "2026-12-31",
            "fto_risk": "Moderate",
            "comments": "Mock patent landscape. Core filings nearing expiry; some formulation claims persist.",
            "patents": patents,
        }


class ClinicalTrialsAgent:
    def run(self, molecule: str) -> Dict[str, Any]:
        phase_distribution = {
            "Phase I": 6,
            "Phase II": 12,
            "Phase III": 8,
            "Phase IV": 5,
        }
        notable_trials = [
            {"id": "NCT00000001", "phase": "Phase III", "status": "Active"},
            {"id": "NCT00000002", "phase": "Phase II", "status": "Completed"},
        ]
        return {
            "total_trials": sum(phase_distribution.values()),
            "active_trials": 14,
            "phase_distribution": phase_distribution,
            "comments": "Mock clinical landscape derived from sample registry counts.",
            "notable_trials": notable_trials,
        }


class InternalKnowledgeAgent:
    def run(self, molecule: str) -> Dict[str, Any]:
        field_feedback = [
            "Adherence in elderly patients is challenging with current dosing.",
            "Some patients report dizziness and daytime sedation.",
            "Diabetic neuropathy subgroup may benefit from tailored regimen.",
        ]
        raw_rows = [
            {"doc": "FieldNotes_2024_Q3", "summary": "Elderly adherence concerns & sedation reports."},
            {"doc": "StrategicBrief_2025", "summary": "Focus on differentiation via formulation & dosing."},
        ]
        return {
            "strategic_priorities_match": "Medium",
            "comments": "Mock internal insights summarizing strategy fit and feedback.",
            "field_feedback": field_feedback,
            "raw_rows": raw_rows,
        }


class WebIntelligenceAgent:
    def run(self, molecule: str) -> Dict[str, Any]:
        guideline_extracts = [
            "Consider dose adjustments in elderly and renally impaired patients.",
            "Monitor CNS-related side effects and counsel patients accordingly.",
        ]
        patient_forum_highlights = [
            "Daytime sleepiness was an issue until dose timing was changed.",
            "Pain relief is good but adherence suffers with complex schedules.",
        ]
        recent_news = [
            "New formulation approaches aim to reduce CNS side effects.",
            "Real-world studies highlight adherence interventions improving outcomes.",
        ]
        raw_rows = [
            {"source": "ForumA", "snippet": "Users discuss adjusting dose timing for less sedation."},
            {"source": "GuidelineX", "snippet": "Elderly dosing considerations highlighted."},
        ]
        return {
            "guideline_extracts": guideline_extracts,
            "patient_forum_highlights": patient_forum_highlights,
            "recent_news": recent_news,
            "raw_rows": raw_rows,
        }


class ReportGeneratorAgent:
    def _compose_text(self, payload: Dict[str, Any]) -> str:
        lines: List[str] = []
        lines.append(f"Innovation Report: {payload.get('molecule','')} – {payload.get('primary_indication','')} ({payload.get('target_geography','')})")
        lines.append("")
        lines.append("Unmet Needs:")
        for u in payload.get("unmet_needs", []):
            lines.append(f"- {u}")
        lines.append("")
        lines.append(f"Clinical Rationale: {payload.get('clinical_rationale','')}")
        lines.append("")

        m = payload.get("market_overview", {})
        lines.append("Market Overview:")
        lines.append(f"- Market size (USD Mn): {m.get('market_size_usd_mn','NA')}")
        lines.append(f"- CAGR (3-yr %): {m.get('cagr_3yr_pct','NA')}")
        lines.append(f"- Top year: {m.get('top_year','NA')}")
        lines.append("")

        e = payload.get("exim_overview", {})
        lines.append("Trade Overview:")
        lines.append(f"- API import dependency: {e.get('api_import_dependency','NA')}")
        lines.append(f"- Avg import price (USD/kg): {e.get('avg_import_price_per_kg_usd','NA')}")
        lines.append("")

        c = payload.get("clinical_trials_landscape", {})
        lines.append("Clinical Trials:")
        lines.append(f"- Total trials: {c.get('total_trials','NA')}")
        lines.append(f"- Active trials: {c.get('active_trials','NA')}")
        lines.append(f"- Phase distribution: {c.get('phase_distribution','NA')}")
        lines.append("")

        p = payload.get("patent_landscape", {})
        lines.append("Patent Landscape:")
        lines.append(f"- Core patent expiry: {p.get('core_patent_expiry','NA')}")
        lines.append(f"- FTO risk: {p.get('fto_risk','NA')}")
        lines.append("")

        i = payload.get("internal_insights", {})
        lines.append("Internal Insights:")
        lines.append(f"- Strategic priority match: {i.get('strategic_priorities_match','NA')}")
        for fb in i.get("field_feedback", []):
            lines.append(f"  • {fb}")
        lines.append("")

        w = payload.get("web_insights", {})
        lines.append("Web Intelligence:")
        for g in w.get("guideline_extracts", []):
            lines.append(f"- {g}")
        for rn in w.get("recent_news", []):
            lines.append(f"- {rn}")
        lines.append("")

        lines.append("Innovation Hypothesis:")
        lines.append(payload.get("innovation_hypothesis", ""))
        lines.append("")
        lines.append("Generated by mock agents (offline demo).")
        return "\n".join(lines)

    def generate_text_report(self, payload: Dict[str, Any]) -> str:
        return self._compose_text(payload)

    def generate_pdf_report(self, payload: Dict[str, Any]) -> bytes:
        # Render the text into a simple PDF using Pillow (no external deps)
        text = self._compose_text(payload)

        # Create a white A4-ish image and draw text
        img_w, img_h = 1240, 1754  # ~A4 at ~150 DPI
        margin = 40
        line_height = 22
        img = Image.new("RGB", (img_w, img_h), "white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Wrap text to fit width
        def wrap_line(s: str, max_width: int) -> List[str]:
            words = s.split(" ")
            lines: List[str] = []
            current = ""
            for w in words:
                test = w if not current else current + " " + w
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = w
            if current:
                lines.append(current)
            return lines

        max_text_width = img_w - 2 * margin
        y = margin
        for raw_line in text.split("\n"):
            wrapped = wrap_line(raw_line, max_text_width)
            for wl in wrapped:
                if y + line_height > img_h - margin:
                    # Stop if page would overflow; indicate truncation
                    draw.text((margin, y), "...", fill=(0, 0, 0), font=font)
                    y += line_height
                    break
                draw.text((margin, y), wl, fill=(0, 0, 0), font=font)
                y += line_height

        bio = BytesIO()
        img.save(bio, format="PDF")
        return bio.getvalue()