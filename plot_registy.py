from plots.plot_avg_bidders_by_act_type import plot_avg_bidders_by_act_type
from plots.plot_avg_effective_price_by_act_type import plot_avg_effective_price_by_act_type
from plots.plot_avg_log_price_pandemic import plot_avg_log_price_pandemic
from plots.plot_avg_price_by_environmental import plot_avg_price_by_environmental
from plots.plot_avg_price_with_quadratic import plot_avg_price_with_quadratic
from plots.plot_bidders_vs_ln_price import plot_bidders_vs_ln_price
from plots.plot_bidders_vs_log_price_pandemic import plot_bidders_vs_log_price_pandemic
from plots.plot_contracts_by_cpv_group import plot_contracts_by_cpv_group
from plots.plot_contracts_by_environmental import plot_contracts_by_environmental
from plots.plot_contracts_by_location import plot_contracts_by_location
from plots.plot_contracts_during_pandemic import plot_contracts_during_pandemic
from plots.plot_contracts_per_year import plot_contracts_per_year
from plots.plot_density_ln_effective_price_by_environmental import plot_density_ln_effective_price_by_environmental
from plots.plot_effective_price_trend import plot_effective_price_trend
from plots.plot_execution_by_act_type import plot_execution_by_act_type
from plots.plot_execution_compliance_rate import plot_execution_compliance_rate
from plots.plot_execution_pandemic_comparison import plot_execution_pandemic_comparison
from plots.plot_ln_base_vs_ln_effective import plot_ln_base_vs_ln_effective
from plots.plot_log_log_by_region import plot_log_log_by_region
from plots.plot_mean_bidders_per_cpv import plot_mean_bidders_per_cpv
from plots.plot_total_spending_by_cpv import plot_total_spending_by_cpv
from plots.plot_total_spending_by_location import plot_total_spending_by_location
from plots.plot_waffle import plot_waffle

plot_registry = {
    'effective_total_price': [
        {
            'title': "Trend of Log(Effective Total Price) Over Time",
            'insight': """
- **Average effective prices** decreased consistently between **2011 and 2018**.
- From **2019 onward**, a **slight upward trend** is observed, suggesting possible **stabilization** or a **market shift**.
- Years with **higher contract volumes** (post-2018) tend to show **lower average prices**.
- Indicates potential **efficiency gains** or **economies of scale** in procurement.
""",
            'func': plot_effective_price_trend
        },
    ],
    'environmental': [
        {
            'title': "Distribution of Log(Effective Price) by Environmental Criteria",
            'insight': """
- Contracts **with environmental criteria** show a **more concentrated and right-skewed** price distribution.
- These contracts are associated with **higher average log-prices**, suggesting more **standardized pricing**.
- Contracts **without environmental criteria** exhibit **greater price variability** and a **broader range** of values.
- The presence of environmental requirements may indicate **higher compliance demands** or the use of **specialized suppliers**.
""",
            'func': plot_density_ln_effective_price_by_environmental
        },
         {
            'title': "Environmental Contracts Over Time",
            'insight': """
- **Contracts without environmental criteria** increased sharply after **2018**, reaching over **660 contracts by 2023**.
- **Contracts with environmental criteria** remained **rare and sporadic**, never exceeding a few per year.
- The trend highlights a **systemic underutilization** of **green public procurement** practices in the healthcare sector.
""",
            'func': plot_contracts_by_environmental
        },
        {
            'title': "Average Effective Price by Environmental Criteria",
            'insight': """
- **Contracts without environmental criteria** exhibit a **stable and lower** average price trend across years.
- **Contracts with environmental criteria** show **substantially higher average prices**, especially in **recent years**.
- This suggests that **green public procurement** may involve **higher compliance costs** or the use of **specialized suppliers**.
""",
            'func': plot_avg_price_by_environmental
        },
    ],
    'base_price': [
        {
            'title': "Relationship between Log(Base Price) and Log(Effective Price)",
            'insight': """
- Shows a **strong positive correlation** between base and effective prices.
- The trend line lies **consistently below** the 45-degree identity line, indicating that **most contracts were executed below their base price**.
- There is a **widening spread** at higher base prices, suggesting **heteroskedasticity**.
- Supports the **log-transformation** to stabilize variance and validate base price as a **key explanatory variable**.
""",
            'func': plot_ln_base_vs_ln_effective
        },
    ],

    'act_type': [
        {
            'title': "Distribution of Procurement Notice Types",
            'insight': """
- **Standard Procedure Notices** represent the vast majority (**86.5%**), indicating a **high degree of standardization** in procurement processes.
- **Urgent Tender Notices** (5.7%) and **Deadline Extension Notices** (5.6%) occur infrequently, suggesting that **exceptions or disruptions are rare**.
- **Notice Correction Statements** are minimal (**2.2%**), reinforcing the view that **most procedures proceed as initially planned**.
""",
            'func': plot_waffle
        },
        {
            'title': "Execution Rate by Procurement Notice Type",
            'insight': """
- **Deadline Extension Notices** have the **highest execution rate**, suggesting that **adjusting deadlines** supports successful contract completion.
- **Notice Correction Statements** show the **lowest execution success**, potentially reflecting **higher uncertainty or procedural issues**.
- **Standard** and **Urgent Tender Notices** fall in between, with **moderate execution rates**.
- The pattern indicates that **procedural deviations**, such as corrections, may compromise execution outcomes.
""",
            'func': plot_execution_by_act_type
        },
         {
            'title': "Average Number of Bidders by Procurement Notice Type",
            'insight': """
- **Urgent Tender Notices** attract the **highest average number of bidders** (20.6), indicating **strong competition despite time constraints**.
- **Standard Procedure Notices** also show high bidder participation (19.8), reinforcing their widespread adoption.
- **Deadline Extension Notices** register the **lowest average bidder count** (14.7), possibly due to **planning uncertainty**.
- Differences in bidder numbers highlight how **announcement type impacts competition and efficiency**.
""",
            'func': plot_avg_bidders_by_act_type
        },
        {
            'title': "Average Effective Price by Procurement Notice Type",
            'insight': """
- **Standard Procedure Notices** exhibit the **highest average price** (€104,703), indicating **larger-scale acquisitions** and greater procedural complexity.
- **Urgent Tender Notices** have a **moderate average price** (€53,938), reflecting **rapid procurement needs** but still significant budgets.
- **Deadline Extension Notices** (€28,955) and **Notice Correction Statements** (€25,903) show **much lower average prices**, likely associated with **simpler or revised contracts**.
- This pattern suggests a **clear link between announcement type and contract size**.
""",
            'func': plot_avg_effective_price_by_act_type
        },
    ],

    'contract_year': [
        {
            'title': "Number of Contracts per Year",
            'insight': """
- Between **2011 and 2017**, the number of contracts remained **consistently low**, with no more than **21 contracts/year**.
- A **sharp increase** began in **2018**, rising to **126 contracts in 2019**.
- The most notable surge occurred in **2021**, reaching **556 contracts**, a **400.9% increase** from 2020.
- The upward trend continued in **2022** and **2023**, with **636 and 668 contracts**, respectively.
- The data suggests a **structural shift** in procurement volume, possibly due to policy changes or digital transformation.
""",
            'func': plot_contracts_per_year
        },
         {
            'title': "Average Effective Price Over Time",
            'insight': """
- **Strong decline** in average effective prices from **2011 to 2019**, indicating reduced per-contract expenditure.
- **Reversal in trend** observed **after 2020**, with prices rising moderately.
- The **quadratic trendline** confirms a **non-linear pattern** over time, with the **minimum** around **2019**.
- This supports the use of **year-squared terms** in econometric modeling to account for **curvature in the time-price relationship**.
""",
            'func': plot_avg_price_with_quadratic
        },
        
    ],


    'CPV_agrupado': [
        {
            'title': "Contracts by CPV Group Over Time",
            'insight': """
- **Medical Equipment** showed a **sharp increase** in contract volume from **2020 onward**, aligned with the **COVID-19 pandemic response**.
- **Services** and **Equipment & Materials** also rose during 2020–2021, likely supporting **logistics, hospital operations, and IT**.
- **Group Not Specified** grew moderately, possibly due to **emergency procurement classifications** or incomplete codifications.
- **Industrial Products** remained consistently **low in volume**, suggesting limited relevance to the health crisis.
- Overall, **Medical Equipment dominated** procurement priorities, highlighting a **significant shift in public spending** during the health emergency.
""",
            'func': plot_contracts_by_cpv_group
        },
         
        {
            'title': "Total Spending by CPV Group",
            'insight': """
- The top three CPV groups by total expenditure were **Services**, **Medical Equipment**, and **Equipment & Materials**.
- These categories represented the **most financially intensive areas** of public procurement.
- In contrast, **Industrial Products** and **Group Not Specified** accounted for a **negligible share of total spending**.
- The distribution reflects **strategic investment priorities** in healthcare delivery and infrastructure.
""",
            'func': plot_total_spending_by_cpv
        },
        {
            'title': "Average Number of Bidders per CPV Group",
            'insight': """
- There is **significant heterogeneity** in bidder participation across CPV categories.
- The **“Group Not Specified”** shows the **highest average number of bidders**, above 30.
- The **“Medical Equipment”** category also reveals **strong competition**, with an average of around 22 bidders.
- In contrast, **“Industrial Products”** and **“Services”** record **fewer than 10 bidders on average**, suggesting **market concentration or barriers to entry**.
- The **“Equipment and Materials”** group lies in between, averaging around 12 bidders.
- These differences **highlight potential areas for policy intervention** to improve market access and **enhance procurement efficiency**.
""",
            'func': plot_mean_bidders_per_cpv
        },
    ],

   
    'bidders': [
        {
            'title': "Bidders vs. Log-Effective Price",
            'insight': """
- A **clear inverse relationship** is observed: more bidders are associated with **lower effective prices**.
- This aligns with standard economic theory—**increased competition** drives prices down.
- **Low-participation procedures** show greater price dispersion, suggesting **uncertainty and inefficiency**.
- When participation is broader, prices are **more concentrated and predictable**, indicating **higher procurement efficiency**.
""",
            'func': plot_bidders_vs_ln_price
        },
    ],



   

    'covid_pandemic': [
        {
            'title': "Number of Contracts During the COVID-19 Pandemic (2020–2023)",
            'insight': """
- In **2020**, only about **90 contracts** were signed, likely due to initial **institutional disruption** and delays in launching procedures.
- In **2021**, contracts rose sharply to over **550**, reflecting **emergency adaptation** and increased **public spending**.
- In **2022**, the volume peaked at around **640 contracts**, indicating **consolidated operational response** to the pandemic.
- In **2023**, contracts dropped to about **410**, aligning with the **official end of the pandemic** and suggesting a return to **standard procurement practices**.
""", 
            'func': plot_contracts_during_pandemic
        },
         {
            'title': "Average Log Effective Contract Price During and Outside the Pandemic",
            'insight': """
- A **negative relationship** between the **number of bidders** and the **contract price** persists across both pandemic and non-pandemic periods.
- This supports the theory that **higher competition leads to lower prices**, reinforcing efficiency in procurement.
- Although the general pattern is consistent, **some differences** are observed between periods, suggesting that the **pandemic context may have influenced market dynamics** and supplier behavior.
""", 
            'func': plot_bidders_vs_log_price_pandemic  
        },
          {
            'title': "Relationship Between Number of Bidders and Log Effective Price by Pandemic Period",
            'insight': """
- The **negative relationship between the number of bidders and contract price** remains visible in both pandemic and non-pandemic periods.
- During the **pandemic**, contracts with **fewer bidders** are associated with **higher and more dispersed prices**, suggesting **inefficiencies driven by urgency and institutional uncertainty**.
- In **non-pandemic periods**, prices are more **concentrated**, with **fewer extreme values**, reflecting greater predictability.
- When there are **more than 20 bidders**, **price levels converge** across periods, reinforcing the notion that **greater competition smooths disparities even under adverse conditions**.
""",
            'func': plot_avg_log_price_pandemic
        },
    ],
 

   
    'loc': [
        {
            'title': "Number of Contracts by Location (NUTS II)",
            'insight': """
- The **PT17 region (Lisboa Metropolitan Area)** stands out with approximately **1,050 contracts**, reflecting its **central role in public administration and healthcare procurement**.
- Regions such as **PT16 (Centro)**, **PT11 (Norte)**, and **PT18 (Alentejo)** show similar levels of contracting activity (between 300 and 400 contracts).
- **PT30 (Autonomous Region of Madeira)** and **PT15 (Algarve)** display significantly lower volumes.
- The **PT20 (Autonomous Region of the Azores)** recorded **almost no contracting activity** in the analysed dataset.
- These figures point to **significant regional disparities** in public healthcare procurement volume.
""",
            'func': plot_contracts_by_location
        },
        {
            'title': "Total Spending by Location (NUTS II)",
            'insight': """
- The **PT17 region (Lisboa Metropolitan Area)** records the **highest expenditure**, around **€70.1 million**, reaffirming its position as the **main national contracting hub**.
- **PT11 (Norte)** and **PT16 (Centro)**, despite having similar contract volumes, show **different expenditure levels**: **€18.1M** vs. **€16.0M**, potentially reflecting **differences in contract types or scale**.
- **PT18 (Alentejo)** has about **150 contracts**, but only **€7.6M in total expenditure**, suggesting **lower average contract values**.
- Both **PT15 (Algarve)** and **PT20 (Autonomous Region of the Azores)** maintain **minimal expenditure levels**, respectively **€2.3M** and **€0.25M**.
- This pattern highlights **regional inequalities** not only in contract volume but also in the **average and total value of public procurement**.
""",
            'func': plot_total_spending_by_location
        },
        {
            'title': "Log-Log Relationship between Base Price and Effective Total Price by Region (NUTS II)",
            'insight': """
- In almost all regions (PT11, PT16, PT17, PT18, PT15, and PT30), a **clear positive linear relationship** is observed between the base price and the effective total price (log-log scale).
- The **PT17 region (Lisboa Metropolitan Area)** stands out with the **steepest slope**, indicating a **strong alignment between initial estimates and final contracted amounts**.
- The **PT20 region (Autonomous Region of the Azores)** shows a **slightly negative trend**, possibly due to a **statistical artifact** caused by the **limited number of observations** or **distinct procurement dynamics** in the autonomous region.
- The consistency of the positive relationship in the other regions reflects a **nationwide trend of proportionality between estimated and actual contract prices**, which may serve as an indicator of predictability or alignment in public procurement practices.
""",
            'func': plot_log_log_by_region
        },
    ],
    'execution_dummy': [
       {
            'title': "Execution Compliance Rate by Contract Year",
            'insight': """
- The chart shows **year-to-year variability** in execution compliance.
- **Higher compliance rates** are observed in **2013 and 2023**, with over **70% of contracts** meeting deadlines.
- **Lower performance** is noted in **2015 and 2021**, when **less than half of the contracts** met execution time targets.
- These variations may be driven by **contract complexity**, **administrative inefficiencies**, or **external shocks** such as the **COVID-19 pandemic (2020–2022)**.
- The analysis suggests that **execution performance is not stable over time**, requiring further investigation into root causes for delays in specific years.
""",
            'func': plot_execution_compliance_rate  
        },
        
    {
        'title': "Execution Rate During Pandemic and Non-Pandemic Periods",
        'insight': """
- Execution compliance rates are **similar** between pandemic and non-pandemic periods.
- In both periods, **slightly more than 60%** of contracts met execution requirements.
- This suggests that the **COVID-19 pandemic did not substantially impact** execution performance.
- Reinforces the notion that contract execution was **robust** to the crisis conditions.
""",
        'func': plot_execution_pandemic_comparison  # <- garante que tens esta função definida
    }

    ]
}