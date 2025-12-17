# graph.py

from dataclasses import dataclass
from typing import Dict, Any, List

from agents.worker_agents import (
    IQVIAInsightsAgent,
    EXIMTrendsAgent,
    PatentLandscapeAgent,
    ClinicalTrialsAgent,
    InternalKnowledgeAgent,
    WebIntelligenceAgent,
)


@dataclass
class MasterAgent:
    iqvia_agent: IQVIAInsightsAgent
    exim_agent: EXIMTrendsAgent
    patent_agent: PatentLandscapeAgent
    clinical_agent: ClinicalTrialsAgent
    internal_agent: InternalKnowledgeAgent
    web_agent: WebIntelligenceAgent

    def run(self, molecule: str, indication: str, geography: str = "US") -> Dict[str, Any]:
        # 1. Call worker agents
        market = self.iqvia_agent.run(molecule, indication, geography)
        exim = self.exim_agent.run(molecule, geography)
        patents = self.patent_agent.run(molecule)
        trials = self.clinical_agent.run(molecule)
        internal = self.internal_agent.run(molecule)
        web = self.web_agent.run(molecule)

        # 2. Derive unmet needs (rule-based)
        unmet_needs: List[str] = []

        for fb in internal.get("field_feedback", []):
            fbl = fb.lower()
            if "dizziness" in fbl:
                unmet_needs.append("Reduce dizziness / CNS side effects.")
            if "adherence" in fbl:
                unmet_needs.append("Improve adherence in elderly / complex regimens.")
            if "elderly" in fbl:
                unmet_needs.append("Design regimen better suited to elderly patients.")
            if "diabet" in fbl:
                unmet_needs.append("Target neuropathic pain in diabetic patients more specifically.")

        for p in web.get("patient_forum_highlights", []):
            pl = p.lower()
            if "sleepy" in pl or "sedation" in pl:
                unmet_needs.append("Minimize daytime sedation while maintaining pain relief.")

        unmet_needs = list(dict.fromkeys(unmet_needs))

        clinical_rationale = (
            "Internal feedback and external snippets indicate scope for differentiation via "
            "formulation, dosing regimen or population targeting (e.g., elderly, diabetic neuropathy)."
        )

        # 3. Simple template-based innovation hypothesis
        base_pop = "elderly patients" if any("elderly" in n.lower() for n in unmet_needs) else "high-risk patients"
        innovation = (
            f"Develop a differentiated formulation of {molecule} for {indication}, "
            f"focusing on {base_pop} and aiming to reduce side effects while improving adherence."
        )

        return {
            "molecule": molecule,
            "primary_indication": indication,
            "target_geography": geography,
            "unmet_needs": unmet_needs,
            "clinical_rationale": clinical_rationale,
            "market_overview": market,
            "exim_overview": exim,
            "patent_landscape": patents,
            "clinical_trials_landscape": trials,
            "internal_insights": internal,
            "web_insights": web,
            "innovation_hypothesis": innovation,
        }


def build_master_agent() -> MasterAgent:
    return MasterAgent(
        iqvia_agent=IQVIAInsightsAgent(),
        exim_agent=EXIMTrendsAgent(),
        patent_agent=PatentLandscapeAgent(),
        clinical_agent=ClinicalTrialsAgent(),
        internal_agent=InternalKnowledgeAgent(),
        web_agent=WebIntelligenceAgent(),
    )
