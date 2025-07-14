import streamlit as st

def display_policy_recommendations():  # df está aqui só para consistência com outras funções
    # Lista de recomendações
    data = [
        {
            "Variable": "Base Price",
            "Implications": "Efficiency varies non-linearly with base price. Peaks occur at log(base_price) around 9.5, 10–11, and above 12. Medium-value contracts show high volatility. At P90, contracts underperform by 33.7 percentage points on average",
            "Recommendations": "- Execution planning: Require execution plans and risk controls for contracts above €500,000.\n"
                               "- Better evaluation: Include qualitative factors such as contractor experience and capacity.\n"
                               "- Monitoring tools: Use digital systems to track execution and flag deviations in real time."
        },
        {
            "Variable": "Act Type",
            "Implications": (
                "Efficiency varies by notice type. Urgent notices perform best (0.25), while "
                "correction statements perform worst (0.18). At the 90th percentile, an efficiency "
                "gap of -0.447 suggests a strong procedural impact."
            ),
            "Recommendations": (
                "- Improve notice drafting: Standardize drafting and review to avoid procedural errors.\n"
                "- Limit corrections: Strengthen quality checks to reduce correction notices.\n"
                "- Tailored guidance: Provide training and protocols adapted to each notice type."
            )
        },
        {
            "Variable": "Contract Year",
            "Implications": (
                "Efficiency improved between 2013–2016 but declined after 2017, with scores below "
                "0.20 post-2019. At the 90th percentile, contracts from recent years underperform by "
                "38.2 percentage points, suggesting structural inefficiencies."
            ),
            "Recommendations": (
                "- Institutional learning: Retain and apply lessons through structured feedback systems.\n"
                "- Professionalization: Promote continuous training in procurement law and crisis resilience.\n"
                "- Tracking tools: Monitor performance trends over time to detect issues and assess reforms."
            )
        },
        {
            "Variable": "Pandemic Year",
            "Implications": (
                "Contracts awarded during 2020–2023 show relatively high average efficiency. The SFA model "
                "indicates a significant efficiency gain under crisis (δ₉ = –0.508), suggesting that urgency "
                "and enhanced oversight during the pandemic contributed to improved performance."
            ),
            "Recommendations": (
                "- Agile procedures: Incorporate elements of pandemic-era fast-track procurement into regular workflows.\n"
                "- Emergency protocols: Establish formal crisis procurement frameworks combining speed and accountability.\n"
                "- Digital oversight: Expand real-time monitoring tools beyond emergency contexts."
            )
        },
        {
            "Variable": "Environmental Criteria",
            "Implications": (
                "Contracts with green criteria show significantly higher efficiency (mean with criteria = 0.48 vs. mean without criteria = 0.23). "
                "The largest positive effect at P50 (+0.312) suggests broad benefits of incorporating environmental requirements into procurement."
            ),
            "Recommendations": (
                "- Mandatory green criteria: Expand obligatory inclusion of environmental requirements in tenders, especially in high-impact sectors.\n"
                "- Capacity-building: Offer training and tools to help entities design and assess environmental criteria effectively."
            )
        },
        {
            "Variable": "CPV Group",
            "Implications": (
                "Efficiency varies by CPV group. Services and equipment show higher efficiency (> 0.27), "
                "while medical and industrial goods underperform (< 0.20). The P90 gap is one of the highest (-0.423). "
                "Although the low technical efficiency scores observed in contracts related to medical equipment may initially suggest monopolistic structures or limited competition, "
                "the data reveal a relatively high average number of bidders in this category. This implies that inefficiencies may not stem from market concentration alone, "
                "but rather from factors such as regulatory constraints, complex technical specifications, or suboptimal contract design. "
                "Policy efforts must therefore address both procedural improvements and capacity building measures tailored to the specific operational challenges of this sector."
            ),
            "Recommendations": (
                "- Differentiated requirements: Adapt planning and monitoring by CPV group.\n"
                "- Sector-specific guidelines: Issue best practices tailored to each category.\n"
                "- Targeted training: Train officers in underperforming sectors (e.g., medical equipment)."
            )
        },
        {
            "Variable": "Bidders",
            "Implications": (
                "Higher bidder participation correlates with lower efficiency. "
                "Contracts with 1–3 bidders perform best (0.4–0.6), while those with more than 10 bidders drop to 0.1 or below. "
                "The SFA model confirms a positive and statistically significant marginal effect on technical inefficiency (δ₁ = 0.0907), "
                "suggesting that increased competition may be associated with procedural or strategic inefficiencies. "
                "At the 90th percentile, the efficiency gap is –0.522. "
                "These inefficiencies may arise from procedural complexity, prolonged evaluation phases, or strategic bidding behavior such as underbidding or tactical delays. "
                "Therefore, focusing on bidder quality and simplifying procedures may improve efficiency more than merely increasing the number of participants."
            ),
            "Recommendations": (
                "- Prioritize quality: Focus on bidder qualification and relevance over number.\n"
                "- Simplify evaluation: Reduce overly rigid criteria to promote execution feasibility.\n"
                "- Monitor behavior: Detect underbidding and collusion in high-competition tenders.\n"
                "- Engage market: Improve communication and early engagement with bidders.\n"
                "- Adjust thresholds: Calibrate minimum competition requirements per contract type."
            )
        },
        {
            "Variable": "Execution Dummy",
            "Implications": (
                "Contracts delivered late show higher efficiency (mean = 0.24) than those delivered on time (mean = 0.14). "
                "At the 50th percentile (P50), a positive gap of +0.146 is observed, but this turns sharply negative at the 90th percentile (–0.447). "
                "These findings imply that delayed contracts may benefit from extended implementation periods, allowing adaptive resource allocation, renegotiation, or strategic adjustments. "
                "Consequently, while deadlines remain important for accountability, performance assessments should consider contextual factors and flexibility, especially in complex or high-stakes procurement scenarios."
            ),
            "Recommendations": (
                "- Contextual evaluation: Avoid penalizing all delays; consider complexity and adaptability.\n"
                "- Flexible design: Allow justified adjustments during execution.\n"
                "- Dynamic monitoring: Replace rigid deadline control with impact-based tracking.\n"
                "- Tolerance thresholds: Set sector-specific flexibility norms.\n"
                "- Efficiency audits: Conduct post-delivery reviews to separate delays from inefficiencies."
            )
        },
        {
            "Variable": "Location",
            "Implications": (
                "Regional disparities in technical efficiency are evident. "
                "The lowest efficiency scores are recorded in Madeira (PT30 = 0.15) and the North (PT11 = 0.17), "
                "while the highest are observed in the Algarve (PT15 = 0.38) and the Azores (PT20 = 0.34). "
                "These findings suggest that regional procurement outcomes may be influenced by contextual differences "
                "in administrative capacity, market structure, or institutional efficiency. "
                "There is a significant efficiency gap, particularly at the median (0.194), which declines at higher percentiles—reaching P90 = -0.399."
            ),
            "Recommendations": (
                "- Decentralised procurement hubs: Empower regional units with autonomy and resources to address local constraints effectively.\n"
                "- Regional benchmarking and monitoring: Track efficiency trends and detect bottlenecks using region-specific metrics.\n"
                "- Market development policies: Boost supplier diversity and competition through SME support and demand aggregation.\n"
                "- Tailored national strategies: Adapt procurement policies to reflect regional differences in capacity and market conditions."
            )
        }
    ]

    # Interface Streamlit
    st.markdown("#### Policy Recommendations Explorer")
    selected_var = st.selectbox("Select a variable to explore:", [d["Variable"] for d in data])

    # Mostrar dados da variável selecionada
    for item in data:
        if item["Variable"] == selected_var:
            st.markdown(f"##### Implications for {item['Variable']}")
            st.write(item["Implications"])
            st.markdown("##### Policy Recommendations")
            st.markdown(item["Recommendations"].replace('\n', '\n\n'))