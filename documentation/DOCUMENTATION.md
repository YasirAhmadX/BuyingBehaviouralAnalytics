# 📊 Enhanced Impulse Buying Behavior Analysis - Documentation

## Overview
This enhanced analysis expands your original 5 visualizations to **15+ comprehensive charts** plus multiple statistical tables and actionable insights.

---

## 🎯 What's New: Complete Enhancement List

### **NEW VISUALIZATIONS (10 Additional Charts)**

#### **Plot 6: Correlation Heatmap** 📈
- **Purpose**: Identifies relationships between all psychological factors
- **Key Insights**: 
  - Which factors move together
  - Positive vs. negative correlations
  - Multicollinearity detection
- **Use Case**: Understanding factor interdependencies for intervention design

#### **Plot 7: Risk Categories by Profile** 🎲
- **Purpose**: Shows how behavioral profiles distribute across risk levels (Low/Medium/High)
- **Key Insights**:
  - Which profiles are highest risk
  - Proportion of high-risk individuals per profile
  - Segmentation effectiveness
- **Use Case**: Targeting interventions to specific profile-risk combinations

#### **Plot 8: Radar Chart of Profiles** 🕸️
- **Purpose**: Compares all profiles across all dimensions simultaneously
- **Key Insights**:
  - Visual "fingerprint" of each profile
  - Quickly spot profile extremes
  - Identify overlapping vs. distinct profiles
- **Use Case**: Client presentations and quick profile comparison

#### **Plot 9: Distribution Comparison (Violin Plots)** 🎻
- **Purpose**: Shows full distribution shape for each score across profiles
- **Key Insights**:
  - Not just means, but variance and outliers
  - Bimodal distributions
  - Profile overlap
- **Use Case**: Understanding within-profile heterogeneity

#### **Plot 10: Risk Score Predictors** 📊
- **Purpose**: Ranks factors by their correlation with impulse risk
- **Key Insights**:
  - Top positive drivers (increase risk)
  - Top negative drivers (decrease risk)
  - Relative importance of each factor
- **Use Case**: Prioritizing intervention targets

#### **Plot 11: Outliers Detection** 🔍
- **Purpose**: Identifies extreme responses across all factors
- **Key Insights**:
  - Data quality check
  - Unusual response patterns
  - Potential edge cases
- **Use Case**: Data cleaning and identifying unique individuals

#### **Plot 12: Percentile Rankings** 📍
- **Purpose**: Shows each participant's risk relative to the full sample
- **Key Insights**:
  - Individual risk positioning
  - Quartile breakdowns
  - Distribution spread
- **Use Case**: Individual reporting and benchmarking

#### **Plot 13: Sunburst Hierarchical Chart** ☀️
- **Purpose**: Shows nested relationship: Risk Category → Behavioral Profile
- **Key Insights**:
  - Hierarchical composition
  - Proportional representation
  - Drill-down capability
- **Use Case**: Executive dashboards and high-level overviews

#### **Plot 14: Parallel Coordinates** 🎵
- **Purpose**: Multi-dimensional view of all factors simultaneously
- **Key Insights**:
  - Individual patterns across dimensions
  - Cluster validation
  - Complex interactions
- **Use Case**: Identifying complex behavioral patterns

#### **Plot 15: Cumulative Distribution Function** 📈
- **Purpose**: Shows what percentage of people fall below each risk score
- **Key Insights**:
  - Percentile lookup
  - Distribution shape
  - Threshold analysis
- **Use Case**: Setting risk cutoffs and policy decisions

---

### **NEW STATISTICAL ANALYSES (5 Tables)**

#### **1. Statistical Tests (statistical_tests.csv)**
Contains:
- **ANOVA F-statistics**: Tests if profiles differ significantly on each factor
- **p-values**: Statistical significance (p < 0.05 = significant)
- **Kruskal-Wallis H-statistics**: Non-parametric alternative for non-normal data
- **Significance flags**: Quick Yes/No indicators

**Interpretation Guide**:
- p < 0.05 = Profiles ARE meaningfully different on this factor
- p > 0.05 = Profiles are NOT significantly different (clustering may be weak here)

#### **2. Profile Characteristics Table (profile_characteristics_table.csv)**
Contains per profile:
- **Risk Statistics**: Mean, Std Dev, Min, Max
- **Factor Means**: Average scores for IB, Happiness, Promotion, Social, Self-Control
- **Sample Size**: Count of individuals in each profile

**Use Cases**:
- Profile descriptions for papers/reports
- Identifying high-risk profiles
- Sample size adequacy check

#### **3. Key Insights Summary (key_insights_summary.csv)**
Top-level findings:
- Sample size
- Overall risk statistics
- Dominant behavioral profile
- Percentage in high-risk category
- Strongest risk predictor
- Model quality metrics (PCA variance explained)

**Use Cases**:
- Executive summary
- Abstract/introduction material
- Quick reference

#### **4. Profile Recommendations (profile_recommendations.csv)**
Actionable strategies per profile:
- **Risk Level**: Low/Medium/High classification
- **Key Characteristics**: Defining traits
- **Intervention Strategy**: Personalized tools/techniques
- **Marketing Approach**: How to reach this segment

**Use Cases**:
- Intervention design
- Marketing segmentation
- Policy recommendations

#### **5. Summary Statistics by Profile (summary_statistics_by_profile.csv)**
Comprehensive stats table with:
- Count, mean, median, std dev, min, max for risk scores
- Mean and std dev for all psychological factors
- Grouped by behavioral profile

**Use Cases**:
- Academic papers
- Detailed comparisons
- Validating clustering quality

---

## 📋 How the New Features Enhance Your Analysis

### **1. Deeper Insights**
- Original: Shows WHAT the clusters are
- Enhanced: Shows WHY they're different (correlations, distributions, predictors)

### **2. Statistical Rigor**
- Original: Descriptive clustering
- Enhanced: Hypothesis testing with ANOVA/Kruskal-Wallis, effect sizes

### **3. Actionability**
- Original: Identifies segments
- Enhanced: Provides specific intervention strategies and marketing approaches

### **4. Multiple Perspectives**
- Original: 2D PCA view
- Enhanced: 15 different analytical lenses (radar, parallel, hierarchical, etc.)

### **5. Individual-Level Analysis**
- Original: Group-level only
- Enhanced: Percentile rankings and individual positioning

---

## 🎯 Key Questions Each New Analysis Answers

| Analysis | Question Answered |
|----------|-------------------|
| Correlation Heatmap | Which psychological factors influence each other? |
| Risk Categories | Are certain profiles concentrated in high-risk zones? |
| Radar Chart | What's the psychological "signature" of each profile? |
| Violin Plots | Is there more variation WITHIN or BETWEEN profiles? |
| Risk Predictors | What factor should we target first to reduce risk? |
| Outliers | Are there unusual cases skewing results? |
| Percentile Ranks | Where does each person stand relative to others? |
| Sunburst | How do risk levels nest within behavioral profiles? |
| Parallel Coords | What multi-factor patterns exist? |
| CDF | What risk score separates top 25% from others? |

---

## 💡 How to Use These Results

### **For Academic Papers**
1. Use **statistical_tests.csv** for reporting significance
2. Use **summary_statistics_by_profile.csv** for Table 1
3. Use **correlation heatmap** and **radar chart** as figures
4. Reference **key insights** in abstract/conclusion

### **For Business Presentations**
1. Start with **sunburst chart** (hierarchy overview)
2. Show **profile bar chart** (segment sizes)
3. Use **radar chart** for profile comparison
4. Present **recommendations table** as action items

### **For Interventions**
1. Identify high-risk profiles from **risk categories chart**
2. Check **risk predictors** to prioritize targets
3. Use **recommendations table** for strategies
4. Monitor using **percentile rankings**

### **For Marketing**
1. Use **profile characteristics** for persona development
2. Apply **marketing approaches** from recommendations
3. Size segments using **profile counts**
4. Target using **risk categories**

---

## 🔍 Interpreting the Results

### **High-Risk Profiles**
- Mean risk score > 66
- Low self-control (SC_Score < 2.5)
- High on multiple triggers (IB, Happiness, Promotion, Social)
- **Action**: Priority intervention group

### **Medium-Risk Profiles**
- Mean risk score 33-66
- Mixed characteristics
- **Action**: Preventive education

### **Low-Risk Profiles**
- Mean risk score < 33
- High self-control (SC_Score > 3.5)
- Low on trigger factors
- **Action**: Maintain healthy habits

### **Statistical Significance**
- **p < 0.001**: Very strong evidence of differences
- **p < 0.05**: Statistically significant
- **p > 0.05**: No evidence of meaningful differences

---

## 📊 Quick Reference: All Output Files

### **Interactive Visualizations (HTML)**
1. `plot_1_trait_deviations.html` - Original boxplots
2. `plot_2_risk_score.html` - Risk distribution histogram
3. `plot_3_profiles.html` - Profile counts
4. `plot_4_clusters.html` - PCA scatter
5. `plot_5_cluster_centers.html` - Mean triggers by profile
6. `plot_6_correlation_heatmap.html` - ⭐ NEW: Factor correlations
7. `plot_7_risk_categories.html` - ⭐ NEW: Risk × Profile crosstab
8. `plot_8_radar_profiles.html` - ⭐ NEW: Multi-dimensional comparison
9. `plot_9_distribution_comparison.html` - ⭐ NEW: Violin plots
10. `plot_10_risk_predictors.html` - ⭐ NEW: Correlation with risk
11. `plot_11_outliers.html` - ⭐ NEW: Outlier detection
12. `plot_12_percentile_rankings.html` - ⭐ NEW: Individual percentiles
13. `plot_13_sunburst.html` - ⭐ NEW: Hierarchical view
14. `plot_14_parallel_coordinates.html` - ⭐ NEW: Multi-dimensional
15. `plot_15_cumulative_distribution.html` - ⭐ NEW: CDF curve

### **Data Tables (CSV)**
1. `analysis_results_enhanced.csv` - Full dataset with all features
2. `profile_characteristics_table.csv` - ⭐ NEW: Profile metrics
3. `statistical_tests.csv` - ⭐ NEW: ANOVA/Kruskal-Wallis
4. `key_insights_summary.csv` - ⭐ NEW: Top findings
5. `profile_recommendations.csv` - ⭐ NEW: Actionable strategies
6. `summary_statistics_by_profile.csv` - ⭐ NEW: Detailed stats

---

## 🚀 Running the Enhanced Analysis

```bash
python enhanced_analysis.py
```

**Requirements**:
- pandas
- numpy
- scikit-learn
- scipy
- plotly
- seaborn
- matplotlib

**Input**: `CodebookData_SEMPLS_IBB.xlsx`

**Output**: 15 HTML files + 6 CSV files

**Runtime**: ~30-60 seconds (depending on data size)

---

## 📈 Next Steps & Extensions

### **Potential Future Enhancements**
1. **Predictive Modeling**: Build ML models to predict risk scores
2. **Temporal Analysis**: If you collect follow-up data, track changes over time
3. **Demographic Integration**: Add age, gender, income as covariates
4. **A/B Testing Framework**: Test interventions on high-risk profiles
5. **Interactive Dashboard**: Convert to Dash/Streamlit for real-time exploration
6. **Network Analysis**: Explore social influence networks if applicable
7. **Text Analysis**: Analyze open-ended survey responses (if any)

### **Validation Steps**
1. **Cross-validation**: Split data, re-run clustering, check stability
2. **Silhouette Score**: Measure cluster quality
3. **External Validation**: Compare to real purchase behavior (if available)
4. **Sensitivity Analysis**: Test different k values for clustering

---

## 📚 Suggested Reading & Citations

### **Methodological References**
- **K-Means Clustering**: MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations.
- **PCA**: Jolliffe, I. T. (2002). Principal component analysis.
- **ANOVA**: Fisher, R. A. (1925). Statistical methods for research workers.

### **Impulse Buying Literature**
- Rook, D. W. (1987). The Buying Impulse. Journal of Consumer Research, 14(2), 189-199.
- Beatty, S. E., & Ferrell, M. E. (1998). Impulse buying: Modeling its precursors. Journal of Retailing, 74(2), 169-191.

---

## ❓ FAQ

**Q: Why 4 clusters?**  
A: Can be optimized using elbow method or silhouette score. Try 3-6 clusters and compare.

**Q: What if profiles overlap?**  
A: Check PCA plot and distribution comparison. Overlap is normal; focus on central tendencies.

**Q: How to handle missing data?**  
A: Currently filled with 0. Consider mean imputation or deletion if >5% missing.

**Q: Can I change profile names?**  
A: Yes! Edit the labeling logic in lines 53-66 of the script.

**Q: How to export for SPSS/Stata?**  
A: Save as .csv, then import. All variables are numeric.

---

## 📧 Contact & Support

For questions about:
- **Methodology**: Review this documentation and statistical tests output
- **Code Issues**: Check Python version (3.8+) and library installations
- **Interpretation**: Consult domain experts in consumer psychology

---

**Document Version**: 1.0  
**Last Updated**: March 2026  
**Analysis Framework**: Impulse Buying Behavior Study  
**Data Privacy**: Ensure compliance with IRB/ethics guidelines when sharing results
