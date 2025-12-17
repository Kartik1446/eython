# app.py

import streamlit as st
import pandas as pd

from graph import build_master_agent
from agents.worker_agents import ReportGeneratorAgent


# ----------------- Page Config & Custom CSS -----------------

st.set_page_config(
    page_title="Agentic Pharma Innovation Explorer",
    layout="wide",
    page_icon=" ",
)

st.markdown(
    """
    <style>
    /* Overall background */
    .main {
        background-color: #9e9a57;
    }
    body {
        background-color: #9e9a57;
    }
    /* Target stMain section */
    [data-testid="stMain"] {
        background-color: #000000 !important;
    }
    /* Remove ugly wide padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }
    /* Card style */
    .card {
        background: #0d3c3d;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 8px 20px rgba(0,0,0,0.45);
    }
    .card h3, .card h4, .card p, .card li {
        color: #f4f4f8 !important;
    }
    .card-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #8f9bb8;
    }
    .pill {
        display: inline-block;
        padding: 0.15rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        background: rgba(76, 161, 255, 0.16);
        color: #a9c7ff;
        border: 1px solid rgba(76, 161, 255, 0.5);
        margin-right: 0.4rem;
    }
    .pill-green {
        background: rgba(0, 200, 140, 0.16);
        color: #9cebd2;
        border-color: rgba(0, 200, 140, 0.5);
    }
    .pill-orange {
        background: rgba(255, 179, 71, 0.18);
        color: #ffd9a0;
        border-color: rgba(255, 179, 71, 0.65);
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #97a0c2;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .kpi-value {
        font-size: 1.4rem;
        font-weight: 600;
        color: #ffffff;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #838cb0;
    }
    /* Tabs background tweak */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #cfcc9f;
        border-radius: 999px;
        padding: 6px 14px;
        color: black; /* Unselected tab text color */
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(207,204,159,0.9), rgba(255,255,255,0.6)) !important;
        color: white !important;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #E37434; /* Updated sidebar color */
        border-right: 1px solid rgba(255,255,255,0.04);
    }
    /* Pills on sidebar */
    [data-testid="stSidebar"] .pill {
        background: #F6F3C2; /* Updated pill background */
        color: black; /* Updated pill text color */
    }
    /* Text on sidebar */
    [data-testid="stSidebar"] {
        color: black; /* Text color in sidebar */
    }
    /* Buttons in sidebar */
    [data-testid="stSidebar"] button {
        background-color: #d6d39f; /* Secondary color for buttons in sidebar */
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------- Main App -----------------

def main():
    # Header
    st.markdown(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.4rem;">
          <div>
            <h1 style="color:#ffffff; margin-bottom:0.2rem;"> Agentic Pharma Innovation Explorer</h1>
            <p style="color:#a0a8c8; font-size:0.95rem; max-width:720px;">
              Rapidly evaluate innovation opportunities for generic molecules using an agent-style orchestration of
              market, clinical, patent, internal and web intelligence.
            </p>
          </div>
          <div style="text-align:right;">
            <div class="pill">Master Agent Orchestrator</div><br/>
            <div class="pill pill-green">6 Worker Agents</div>
            <div class="pill pill-orange">Offline · Mock Data</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Sidebar
    st.sidebar.markdown("###  Query Configuration")
    molecule = st.sidebar.text_input("Molecule", value="pregabalin")
    indication = st.sidebar.text_input("Primary indication", value="neuropathic pain")
    geography = st.sidebar.text_input("Target geography", value="US")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        **How this demo works:**
        - Master Agent calls worker agents  
        - Uses mock IQVIA, EXIM, patent, clinical, internal & web data  
        - Synthesizes unmet needs & an innovation story  
        - Builds a downloadable TXT + PDF report  
        """
    )

    run_clicked = st.sidebar.button(" Run Innovation Search", use_container_width=True)

    if not run_clicked:
        st.info("Enter molecule, indication & geography in the left panel, then click **Run Innovation Search**.")
        return

    if not molecule.strip():
        st.error("Please enter a molecule name.")
        return

    master = build_master_agent()

    with st.spinner("Running Master + Worker Agents..."):
        result = master.run(molecule.strip(), indication.strip(), geography.strip())

    st.success("Analysis complete ")

    # --------- KPI STRIP ---------
    cols_kpi = st.columns(4)

    market = result["market_overview"]
    trials = result["clinical_trials_landscape"]
    patents = result["patent_landscape"]
    exim = result["exim_overview"]

    with cols_kpi[0]:
        ms = market.get("market_size_usd_mn")
        cagr = market.get("cagr_3yr_pct")
        st.markdown(
            f"""
            <div class="card">
                <div class="kpi-label">Market Size</div>
                <div class="kpi-value">{ms if ms is not None else "NA"} {"" if ms is None else "M USD"}</div>
                <div class="kpi-sub">CAGR: {cagr if cagr is not None else "NA"}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with cols_kpi[1]:
        st.markdown(
            f"""
            <div class="card">
                <div class="kpi-label">Clinical Activity</div>
                <div class="kpi-value">{trials.get("total_trials", 0)}</div>
                <div class="kpi-sub">Active trials: {trials.get("active_trials", 0)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with cols_kpi[2]:
        st.markdown(
            f"""
            <div class="card">
                <div class="kpi-label">FTO Risk</div>
                <div class="kpi-value">{patents.get("fto_risk", "Unknown")}</div>
                <div class="kpi-sub">Core expiry: {patents.get("core_patent_expiry", "NA")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with cols_kpi[3]:
        st.markdown(
            f"""
            <div class="card">
                <div class="kpi-label">API Sourcing</div>
                <div class="kpi-value">{exim.get("api_import_dependency", "NA")}</div>
                <div class="kpi-sub">Avg import price: {exim.get("avg_import_price_per_kg_usd", "NA")} USD/kg</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # --------- Tabs ---------
    overview_tab, market_tab, clinical_tab, insights_tab, report_tab = st.tabs(
        [" Overview", " Market & Trade", " Clinical & Patents", " Insights & Web", " Report"]
    )

    # ============ OVERVIEW TAB ============
    with overview_tab:
        st.markdown(
            f"""
            <div class="card">
              <div class="card-label">Search context</div>
              <h3 style="margin-top:0.3rem;">{result["molecule"]} – {result["primary_indication"]} ({result["target_geography"]})</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")

        col_o1, col_o2 = st.columns([1.3, 1])

        with col_o1:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">Innovation hypothesis</div>
                    <p style='margin-top:0.5rem; font-size:0.95rem;'>{result['innovation_hypothesis']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_o2:
            unmet = result.get("unmet_needs", [])
            if unmet:
                unmet_content = (
                    "<ul style='padding-left:1.1rem; margin-top:0.4rem;'>"
                    + "".join([f"<li>{u}</li>" for u in unmet])
                    + "</ul>"
                )
            else:
                unmet_content = "<p style='margin-top:0.5rem; color:#a0a8c8;'>No specific unmet needs inferred from mock data.</p>"

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">Unmet needs</div>
                    {unmet_content}
                    <p style='margin-top:0.8rem; font-size:0.85rem; color:#9da7ce;'><b>Clinical rationale:</b> {result['clinical_rationale']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ============ MARKET & TRADE TAB ============
    with market_tab:
        col_m1, col_m2 = st.columns([1.3, 1])

        with col_m1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            m = result["market_overview"]
            st.markdown(
                f"""
                <h3>IQVIA-like Market Overview</h3>
                <p><b>Market size (USD Mn):</b> {m.get('market_size_usd_mn')}</p>
                <p><b>CAGR (3-yr %):</b> {m.get('cagr_3yr_pct')}</p>
                <p><b>Top year:</b> {m.get('top_year')}</p>
                <p style='font-size:0.8rem; color:#838cb0;'>{m.get("comments", "")}</p>
                """,
                unsafe_allow_html=True
            )
            if m.get("raw_rows"):
                df_sales = pd.DataFrame(m["raw_rows"])
                st.markdown("**Raw view:**")
                st.dataframe(df_sales, use_container_width=True)
                if "year" in df_sales.columns and "sales_usd_mn" in df_sales.columns:
                    df_sales_sorted = df_sales.sort_values("year")
                    st.markdown("**Sales trend (USD Mn by year):**")
                    st.line_chart(df_sales_sorted.set_index("year")["sales_usd_mn"])


        with col_m2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            e = result["exim_overview"]
            st.markdown(
                f"""
                <h3>EXIM-like Trade Overview</h3>
                <p><b>API import dependency:</b> {e.get('api_import_dependency')}</p>
                <p><b>Avg import price (USD/kg):</b> {e.get('avg_import_price_per_kg_usd')}</p>
                <p style='font-size:0.8rem; color:#838cb0;'>{e.get("comments", "")}</p>
                """,
                unsafe_allow_html=True
            )
            if e.get("raw_rows"):
                st.markdown("**Trade rows:**")
                st.dataframe(pd.DataFrame(e["raw_rows"]), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ============ CLINICAL & PATENTS TAB ============
    with clinical_tab:
        col_c1, col_c2 = st.columns([1.3, 1])

        with col_c1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            c = result["clinical_trials_landscape"]
            st.markdown(
                f"""
                <h3>Clinical Trials Landscape</h3>
                <p><b>Total trials:</b> {c.get('total_trials')}</p>
                <p><b>Active trials:</b> {c.get('active_trials')}</p>
                <p><b>Phase distribution:</b> {c.get('phase_distribution')}</p>
                <p style='font-size:0.8rem; color:#838cb0;'>{c.get("comments", "")}</p>
                """,
                unsafe_allow_html=True
            )
            if c.get("notable_trials"):
                st.markdown("**Notable trials:**")
                st.dataframe(pd.DataFrame(c["notable_trials"]), use_container_width=True)

            phase_dist = c.get("phase_distribution", {})
            if phase_dist:
                df_phase = pd.DataFrame(
                    list(phase_dist.items()), columns=["Phase", "Trials"]
                ).set_index("Phase")
                st.markdown("**Trials by Phase:**")
                st.bar_chart(df_phase)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_c2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            p = result["patent_landscape"]
            st.markdown(
                f"""
                <h3>Patent Landscape</h3>
                <p><b>Core patent expiry:</b> {p.get('core_patent_expiry')}</p>
                <p><b>FTO risk:</b> {p.get('fto_risk')}</p>
                <p style='font-size:0.8rem; color:#838cb0;'>{p.get("comments", "")}</p>
                """,
                unsafe_allow_html=True
            )
            if p.get("patents"):
                st.markdown("**Patent list:**")
                st.dataframe(pd.DataFrame(p["patents"]), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ============ INSIGHTS & WEB TAB ============
    with insights_tab:
        col_i1, col_i2 = st.columns([1.3, 1])

        with col_i1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            i = result["internal_insights"]
            st.markdown(
                f"""
                <h3>Internal Insights</h3>
                <p><b>Strategic priority match:</b> {i.get('strategic_priorities_match')}</p>
                <p style='font-size:0.8rem; color:#838cb0;'>{i.get("comments", "")}</p>
                """,
                unsafe_allow_html=True
            )
            if i.get("field_feedback"):
                st.markdown("**Field feedback:**")
                for fb in i["field_feedback"]:
                    st.markdown(f"- {fb}")
            if i.get("raw_rows"):
                st.markdown("**Raw internal docs:**")
                st.dataframe(pd.DataFrame(i["raw_rows"]), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_i2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            w = result["web_insights"]
            guideline_extracts_html = "".join([f"<li>{g}</li>" for g in w.get("guideline_extracts", [])])
            patient_forum_highlights_html = "".join([f"<li>{p}</li>" for p in w.get("patient_forum_highlights", [])])
            st.markdown(
                f"""
                <h3>Web Intelligence</h3>
                <p><b>Guideline extracts:</b></p>
                <ul>{guideline_extracts_html}</ul>
                <p><b>Patient forum highlights:</b></p>
                <ul>{patient_forum_highlights_html}</ul>
                """,
                unsafe_allow_html=True
            )

            st.write("**Recent news / journals:**")
            for rn in w.get("recent_news", []):
                st.markdown(f"- {rn}")

            if w.get("raw_rows"):
                st.markdown("**Raw web snippets:**")
                st.dataframe(pd.DataFrame(w["raw_rows"]), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ============ REPORT TAB ============
    with report_tab:
        payload = {
            "molecule": result["molecule"],
            "primary_indication": result["primary_indication"],
            "target_geography": result["target_geography"],
            "unmet_needs": result.get("unmet_needs", []),
            "clinical_rationale": result.get("clinical_rationale", ""),
            "market_overview": result.get("market_overview", {}),
            "exim_overview": result.get("exim_overview", {}),
            "patent_landscape": result.get("patent_landscape", {}),
            "clinical_trials_landscape": result.get("clinical_trials_landscape", {}),
            "internal_insights": result.get("internal_insights", {}),
            "web_insights": result.get("web_insights", {}),
            "innovation_hypothesis": result.get("innovation_hypothesis", ""),
        }

        report_agent = ReportGeneratorAgent()
        report_text = report_agent.generate_text_report(payload)
        pdf_bytes = report_agent.generate_pdf_report(payload)

        st.markdown(
            f"""
            <div class="card">
                <h3>Downloadable Report</h3>
                <p><b>Text preview:</b></p>
                <pre>{report_text[:1500] + ("\n...\n" if len(report_text) > 1500 else "")}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_txt, col_pdf = st.columns(2)
        with col_txt:
            st.download_button(
                label="Download full report (.txt)",
                data=report_text.encode("utf-8"),
                file_name=f"{result['molecule']}_{result['primary_indication']}_innovation_report.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_pdf:
            st.download_button(
                label="Download full report (.pdf)",
                data=pdf_bytes,
                file_name=f"{result['molecule']}_{result['primary_indication']}_innovation_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )


if __name__ == "__main__":
    main()
