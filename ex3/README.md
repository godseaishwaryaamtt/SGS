# Smart Grid Systems (SGS) - Complete Experimental Framework

## **Project Overview**

This repository contains three interconnected experiments demonstrating critical smart grid technologies for India's energy transition. Each experiment addresses fundamental challenges in grid modernization, consumer privacy, and environmental sustainability.

### **Experiments Summary**
1. **Dynamic Tariff Explorer** - Demand response and behavioral economics
2. **Privacy-Preserving Synthetic Energy Data** - Data privacy and analytics
3. **Carbon-Intensity Aware Task Scheduler** - Environmental optimization

***

## **Experiment 1: Dynamic Tariff Explorer**

### **Objective**
Demonstrate how different electricity pricing schemes affect consumer behavior and enable demand response through load shifting and behavioral nudging.

### **Key Concepts**
- **Time-of-Use (ToU) Pricing**: Variable rates based on demand periods
- **Critical Peak Pricing (CPP)**: Extreme pricing during grid stress
- **Load Shifting**: Moving consumption from peak to off-peak hours
- **Behavioral Nudging**: Information-based interventions to influence choices
- **Demand Response**: Changes in usage patterns responding to price signals

### **Indian Context - Maharashtra Focus**
- **MSEDCL Tariff Structure**: ₹4.71-16.64/unit across consumption slabs
- **ToD Implementation**: Government mandate from April 2025
- **Solar Hour Discounts**: 20% reduction during 10 AM-6 PM
- **BPL Special Rates**: ₹1.56/unit for economically disadvantaged

### **How It Works**
1. **Generate Consumption Profiles**: Realistic household usage patterns
2. **Apply Pricing Schemes**: Flat, ToU, and CPP tariffs
3. **Simulate Behavioral Response**: Load shifting based on price thresholds
4. **Calculate Savings**: Compare bills before/after optimization

### **Key Results**
- **25% flexible load assumption**: Typical household shifting potential
- **15-30% bill reduction**: Through optimal timing of usage
- **Peak demand reduction**: Flattened load curves benefit grid stability

### **Graph Explanations**
- **Consumption Timeline**: Shows original vs. shifted usage patterns
- **Pricing Comparison**: Visualizes rate differences across 24 hours
- **Savings Metrics**: Quantifies financial benefits of load shifting

***

## **Experiment 2: Privacy-Preserving Synthetic Energy Data**

### **Objective**
Generate realistic but artificial energy consumption datasets that preserve analytical utility while protecting individual privacy under India's DPDP 2023.

### **Key Concepts**
- **Synthetic Data**: Artificially generated data mimicking real patterns
- **k-Anonymity**: Privacy measure ensuring individuals cannot be distinguished from k-1 others
- **Quasi-Identifiers (QI)**: Attributes that could identify individuals when combined
- **Data Minimization**: DPDP 2023 principle of collecting minimal necessary data
- **Re-identification Risk**: Probability of linking anonymous data to individuals

### **Privacy Framework**
- **QI Selection**: Home type, occupants, tariff type as identifying factors
- **k-Anonymity Target**: Minimum k=5 for energy data protection
- **Bucketing Strategy**: Group similar values to enhance anonymity
- **Utility Validation**: Ensure synthetic data maintains analytical value

### **Indian Regulatory Context**
- **DPDP 2023 Compliance**: ₹500 crore penalties for violations
- **250 Million Smart Meters**: Unprecedented data generation scale
- **Cultural Sensitivity**: Joint families, economic stratification concerns
- **Cross-border Restrictions**: Limitations on international data sharing

### **How It Works**
1. **Statistical Analysis**: Study real consumption patterns and distributions
2. **Synthetic Generation**: Create new records following same patterns
3. **Privacy Assessment**: Measure k-anonymity and re-identification risk
4. **Utility Comparison**: Validate analytical value preservation

### **Key Results**
- **Distribution Matching**: Synthetic data preserves real consumption statistics
- **Privacy Enhancement**: k-anonymity improved from 2 to 5+ through bucketing
- **Research Enablement**: Safe datasets for AI/ML development and policy studies

### **Graph Explanations**
- **Tariff Distribution**: Bar charts comparing real vs synthetic data proportions
- **Consumption Histograms**: Overlapping distributions showing pattern preservation
- **Privacy Metrics**: k-anonymity measurements and improvement strategies

***

## **Experiment 3: Carbon-Intensity Aware Task Scheduler**

### **Objective**
Optimize timing of flexible computing tasks and energy-intensive activities to minimize carbon emissions by leveraging grid carbon intensity variations.

### **Key Concepts**
- **Carbon Intensity**: gCO₂ emitted per kWh of electricity generated
- **Temporal Carbon Footprint**: How emissions vary throughout the day
- **Grid Mix**: Proportion of coal, gas, nuclear, renewable generation
- **Marginal Emissions**: Additional CO₂ from consuming one extra unit
- **Optimal Window**: Time period with lowest carbon intensity for task execution

### **Indian Grid Reality**
- **713 gCO₂/kWh**: India's grid intensity (48% above global average)
- **72.5% Coal Dependency**: Creates high-carbon baseload
- **Solar Opportunity**: 30-40% emission reduction during 11 AM-4 PM
- **Maharashtra Specifics**: ~800 gCO₂/kWh with growing renewable capacity

### **Applications**
- **Computing**: Data backups, ML training, cloud workloads
- **Manufacturing**: Production scheduling, equipment maintenance
- **Smart Cities**: Water treatment, traffic management, street lighting
- **Residential**: EV charging, HVAC systems, appliance automation

### **How It Works**
1. **Carbon Modeling**: Simulate realistic 24-hour intensity patterns
2. **Constraint Processing**: User-defined task duration and time windows
3. **Optimization Algorithm**: Find minimum carbon intensity window
4. **Impact Quantification**: Calculate emission savings vs immediate execution

### **Key Results**
- **50-55% Emission Reduction**: Compared to conventional scheduling
- **Maharashtra Potential**: 15-25% reduction in state's 111 million tCO₂e
- **Economic Benefits**: Lower ToD rates align with carbon optimization
- **Grid Stability**: Peak demand reduction through coordinated scheduling

### **Interactive Controls**
- **Task Duration**: 1-6 hours affecting optimization flexibility
- **Start/End Constraints**: Business requirements vs environmental optimization
- **Time Comparison**: Immediate vs optimal execution carbon costs

***

## **Why These Experiments Matter for India**

### **Scale and Urgency**
- **1.4 billion people**: Largest population requiring energy access
- **250 million smart meters**: World's biggest deployment by 2026-27
- **500 GW renewable target**: By 2030 requiring advanced grid management
- **Net-zero by 2070**: Every efficiency gain contributes to climate goals

### **Regulatory Drivers**
- **DPDP 2023**: Legal framework requiring privacy-preserving technologies
- **ToD Mandate**: Government requirement for time-based pricing from 2025
- **Carbon Commitments**: NDCs and COP obligations for emission reductions
- **Smart City Mission**: Municipal infrastructure optimization needs

### **Economic Impact**
- **₹500 crore penalties**: Privacy violation costs making compliance critical
- **Infrastructure savings**: Demand response reduces need for new capacity
- **Technology export**: Global market for Indian smart grid solutions
- **Energy security**: Reduced import dependence through optimization

***

## **Technical Integration**

### **How Experiments Connect**
1. **Dynamic Tariff Explorer** creates economic incentives for behavioral change
2. **Privacy-Preserving Data** enables research and optimization without privacy risks
3. **Carbon Scheduler** provides environmental optimization framework

### **Shared Technologies**
- **Real-time data processing**: All experiments require timely information
- **Behavioral modeling**: Understanding consumer response patterns
- **Optimization algorithms**: Finding optimal solutions within constraints
- **Policy integration**: Aligning with regulatory and business requirements

***

## **Common Viva Questions and Answers**

### **Q1: Why is India specifically mentioned in all experiments?**
**A:** India faces unique challenges - world's most carbon-intensive grid, largest smart meter deployment, strict privacy laws (DPDP 2023), and massive scale (1.4 billion people). Solutions must work at unprecedented scale while respecting cultural and economic diversity.

### **Q2: How do you ensure synthetic data is truly anonymous?**
**A:** We use k-anonymity (ensuring each record matches ≥k-1 others), identify quasi-identifiers (home type, occupants, tariff), apply bucketing (grouping similar values), and validate that statistical properties are preserved while individuals cannot be re-identified.

### **Q3: What makes carbon-aware scheduling different from just peak-shaving?**
**A:** Peak-shaving focuses on demand management for grid stability. Carbon-aware scheduling optimizes for environmental impact by targeting periods when electricity is cleanest (high renewable generation), which may not align with peak demand periods.

### **Q4: How do behavioral nudges actually change consumption?**
**A:** Price signals create economic incentives. Time-of-Use rates make peak consumption expensive, encouraging load shifting. Studies show 5% peak demand reduction can create 50% price reductions, demonstrating the effectiveness of economic behavioral incentives.

### **Q5: What's the business case for utilities to implement these technologies?**
**A:** Reduced infrastructure investment (demand response avoids new capacity), regulatory compliance (DPDP 2023, ToD mandates), customer satisfaction (lower bills through optimization), and competitive advantage (advanced services attract customers).

### **Q6: How do you validate that synthetic data maintains utility?**
**A:** Compare statistical distributions (means, variances, correlations) between real and synthetic datasets. Verify that analytical conclusions drawn from synthetic data match those from real data. Test with actual research applications to ensure scientific validity.

### **Q7: What are the limitations of these approaches?**
**A:** Consumer adoption challenges (digital literacy, trust), infrastructure requirements (smart meters, communication networks), regulatory uncertainty (evolving policies), and scale complexity (coordinating millions of devices).

### **Q8: How do these experiments address energy justice and equity?**
**A:** BPL tariffs protect economically disadvantaged households, privacy preservation prevents discrimination based on consumption patterns, and behavioral programs are opt-in rather than mandatory, ensuring equitable access to benefits.

### **Q9: What's the difference between carbon intensity and carbon footprint?**
**A:** Carbon intensity is gCO₂ per kWh of electricity generated (grid characteristic). Carbon footprint is total emissions from an activity (consumption × intensity). Intensity varies by time/location; footprint depends on when/how much you consume.

### **Q10: How do you handle the trade-off between privacy and utility?**
**A:** Synthetic data generation breaks this traditional trade-off by preserving statistical utility while providing mathematical privacy guarantees. Instead of choosing between privacy OR utility, we achieve both through advanced data generation techniques.

***

## **Technical Implementation Details**

### **Required Libraries**
- **Streamlit**: Interactive web interface
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations and random generation
- **Plotly**: Interactive visualizations and graphs

### **Key Algorithms**
- **Load shifting optimization**: Greedy algorithm finding minimum cost windows
- **Synthetic data generation**: Statistical sampling preserving distributions
- **Carbon scheduling**: Constraint satisfaction with emission minimization

### **Data Structures**
- **Time series**: Hourly consumption and pricing data
- **Household profiles**: Demographics and consumption characteristics
- **Carbon intensity curves**: Grid emission factors by time

***

## **Future Extensions**

### **Advanced Features**
- **Real-time API integration**: Live grid data and carbon intensity feeds
- **Machine learning models**: Predictive optimization and demand forecasting
- **Geographic expansion**: Multi-state implementation with regional variations
- **Blockchain integration**: Secure, transparent data sharing mechanisms

### **Research Opportunities**
- **Community-level optimization**: Neighborhood-scale demand response coordination
- **Cross-sector integration**: Industrial, commercial, residential optimization
- **International collaboration**: Technology transfer to other developing nations
- **Policy impact assessment**: Quantifying regulatory intervention effectiveness

***

## **Key Takeaways for Viva**

1. **Integration**: All three experiments work together to enable smart grid transformation
2. **Scale**: India's unique challenges require innovative solutions at unprecedented scale
3. **Privacy**: DPDP 2023 makes privacy-preserving techniques legally essential
4. **Environment**: Carbon optimization supports net-zero commitments
5. **Economics**: Market mechanisms drive behavioral change better than mandates
6. **Technology**: Advanced algorithms enable win-win outcomes (consumer + grid benefits)
7. **Policy**: Regulatory frameworks must evolve to support technological innovation

These experiments demonstrate that smart grid technologies can simultaneously achieve economic efficiency, environmental sustainability, and privacy protection when properly designed for India's specific context and requirements.