# =============================================================================
# ENHANCED IMPULSE BUYING BEHAVIOR ANALYSIS
# =============================================================================
# This script provides comprehensive analysis including:
# - Original 5 visualizations
# - 10+ additional charts and insights
# - Statistical tests and correlations
# - Detailed summary tables
# - Profile comparisons and recommendations
# =============================================================================

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from scipy import stats
from scipy.stats import chi2_contingency, f_oneway, kruskal
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import warnings
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
pio.renderers.default = "browser"

# =============================================================================
# 1. LOAD DATA
# =============================================================================
print("Loading data...")
df = pd.read_excel('CodebookData_SEMPLS_IBB.xlsx')
df = df.drop("Location", axis=1, errors='ignore')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {len(df.columns)}")

# =============================================================================
# 2. FEATURE ENGINEERING
# =============================================================================
print("\nEngineering features...")

df['IB_Score'] = df.filter(regex=r'^IBB').mean(axis=1)
df['Happy_Score'] = df.filter(regex=r'^H[1-4]').mean(axis=1)
df['Promo_Score'] = df.filter(regex=r'^P[1-4]').mean(axis=1)
df['Social_Score'] = df.filter(regex=r'^SI').mean(axis=1)
df['Normative_Score'] = df.filter(regex=r'^NE').mean(axis=1)
df['SC_Score'] = df.filter(regex=r'^SC').mean(axis=1)

df['Risk_SC_Penalty'] = 6 - df['SC_Score']

df['Raw_Risk'] = (
    (1.5 * df['IB_Score']) +
    df['Happy_Score'] +
    df['Promo_Score'] +
    df['Social_Score'] +
    df['Risk_SC_Penalty']
)

scaler = MinMaxScaler(feature_range=(0, 100))
df['Impulse_Risk_Score'] = scaler.fit_transform(df[['Raw_Risk']])

# Additional derived features
df['Total_Social_Influence'] = df['Social_Score'] + df['Normative_Score']
df['Emotional_Index'] = (df['Happy_Score'] + df['IB_Score']) / 2
df['Rational_Control'] = df['SC_Score']

# =============================================================================
# 3. CLUSTERING
# =============================================================================
print("Performing clustering...")

clustering_features = df[
    ['IB_Score', 'Happy_Score', 'Promo_Score',
     'Social_Score', 'Risk_SC_Penalty']
].fillna(0)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster_ID'] = kmeans.fit_predict(clustering_features)

# Dynamic Cluster Labeling
cluster_means = df.groupby('Cluster_ID')[
    ['IB_Score', 'Happy_Score', 'Promo_Score',
     'Social_Score', 'Risk_SC_Penalty']
].mean()

labels = {}
for i in range(4):
    row = cluster_means.loc[i]
    if row['Promo_Score'] > 3.5 and row['IB_Score'] > 3.5:
        labels[i] = "The Deal Chaser"
    elif row['Social_Score'] > 3.5:
        labels[i] = "The Social/Trend Shopper"
    elif row['Risk_SC_Penalty'] < 2.5:
        labels[i] = "The Rational Spender"
    else:
        labels[i] = "The Emotional Spender"

df['Behaviour_Profile'] = df['Cluster_ID'].map(labels)

# =============================================================================
# 4. PCA
# =============================================================================
print("Running PCA...")

pca = PCA(n_components=2)
pca_features = pca.fit_transform(clustering_features)

df['PCA_1'] = pca_features[:, 0]
df['PCA_2'] = pca_features[:, 1]

# =============================================================================
# 5. ORIGINAL VISUALIZATIONS
# =============================================================================
print("\nGenerating original visualizations...")

# Plot 1: Trait Deviations
question_cols = [c for c in df.columns if c.startswith(('IBB', 'P', 'SI', 'H', 'SC', 'NE'))]
melted = df.melt(id_vars=['ID#'] if 'ID#' in df.columns else [], 
                 value_vars=question_cols, 
                 var_name='Question', 
                 value_name='Response')

melted['Question'] = melted['Question'].astype(str).str.split(':', n=1).str[0].str.strip()
melted['Construct'] = melted['Question'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))

fig1 = px.box(melted, x='Question', y='Response', color='Construct', 
              points="all", 
              title="Distribution & Deviations of Specific Traits",
              labels={'Question': 'Survey Trait', 'Response': 'Likert Score (1-5)'},
              hover_data=['Question'])
fig1.update_layout(xaxis_tickangle=-45)
fig1.write_html("plot_1_trait_deviations.html")

# Plot 2: Risk Score Distribution
mean_risk = df['Impulse_Risk_Score'].mean()
fig2 = px.histogram(
    df, x='Impulse_Risk_Score', nbins=30, marginal="box",
    color_discrete_sequence=['crimson'],
    title="<b>Distribution of Impulse Risk Scores</b>",
    labels={"Impulse_Risk_Score": "Impulse Risk Score (0-100)"}
)
fig2.add_vline(x=mean_risk, line_dash="dash", line_color="black",
               annotation_text=f"Mean: {mean_risk:.1f}",
               annotation_position="top right")
fig2.write_html("plot_2_risk_score.html")

# Plot 3: Behaviour Profiles
profile_counts = df['Behaviour_Profile'].value_counts().reset_index()
profile_counts.columns = ['Behaviour_Profile', 'Count']
fig3 = px.bar(profile_counts, x='Count', y='Behaviour_Profile', orientation='h',
              color='Behaviour_Profile', text='Count',
              title="<b>Count of Behavioural Profiles</b>")
fig3.update_layout(showlegend=False)
fig3.write_html("plot_3_profiles.html")

# Plot 4: PCA Cluster Visualization
fig4 = px.scatter(
    df, x='PCA_1', y='PCA_2', color='Behaviour_Profile',
    size='Impulse_Risk_Score',
    hover_data=['IB_Score', 'Promo_Score', 'Social_Score', 'Impulse_Risk_Score'],
    title=(f"<b>Behavioral Clusters (PCA Projection)</b><br>"
           f"<sup>PC1: {pca.explained_variance_ratio_[0]:.1%} | "
           f"PC2: {pca.explained_variance_ratio_[1]:.1%}</sup>")
)
fig4.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
fig4.write_html("plot_4_clusters.html")

# Plot 5: Cluster Centers
cluster_centers = df.groupby('Behaviour_Profile')[
    ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'Risk_SC_Penalty']
].mean().reset_index()
melted_centers = cluster_centers.melt(
    id_vars='Behaviour_Profile',
    var_name='Psychological Trigger',
    value_name='Average Score'
)
fig5 = px.bar(melted_centers, x='Behaviour_Profile', y='Average Score',
              color='Psychological Trigger', barmode='group',
              title="<b>Average Psychological Triggers per Profile</b>")
fig5.write_html("plot_5_cluster_centers.html")

print("Original visualizations complete!")

# =============================================================================
# 6. NEW ANALYSIS: CORRELATION HEATMAP
# =============================================================================
print("\n📊 Creating correlation heatmap...")

correlation_cols = ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 
                    'Normative_Score', 'SC_Score', 'Impulse_Risk_Score']
corr_matrix = df[correlation_cols].corr()

fig6 = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=corr_matrix.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Correlation")
))

fig6.update_layout(
    title="<b>Correlation Matrix of Psychological Factors</b>",
    xaxis_title="", yaxis_title="",
    width=700, height=700
)
fig6.write_html("plot_6_correlation_heatmap.html")

# =============================================================================
# 7. NEW ANALYSIS: RISK CATEGORIES
# =============================================================================
print("📊 Creating risk category analysis...")

# Create risk categories
df['Risk_Category'] = pd.cut(df['Impulse_Risk_Score'], 
                              bins=[0, 33, 66, 100],
                              labels=['Low Risk', 'Medium Risk', 'High Risk'])

risk_profile_crosstab = pd.crosstab(df['Risk_Category'], df['Behaviour_Profile'])

fig7 = go.Figure(data=[
    go.Bar(name=profile, x=risk_profile_crosstab.index, 
           y=risk_profile_crosstab[profile])
    for profile in risk_profile_crosstab.columns
])

fig7.update_layout(
    title="<b>Risk Categories by Behavioural Profile</b>",
    xaxis_title="Risk Category",
    yaxis_title="Count",
    barmode='stack',
    showlegend=True
)
fig7.write_html("plot_7_risk_categories.html")

# =============================================================================
# 8. NEW ANALYSIS: RADAR CHART OF PROFILES
# =============================================================================
print("📊 Creating radar chart for profiles...")

categories = ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']
profile_means = df.groupby('Behaviour_Profile')[categories].mean()

fig8 = go.Figure()

for profile in profile_means.index:
    values = profile_means.loc[profile].tolist()
    values.append(values[0])  # Close the radar
    
    fig8.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=profile
    ))

fig8.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    title="<b>Psychological Profile Comparison (Radar Chart)</b>",
    showlegend=True
)
fig8.write_html("plot_8_radar_profiles.html")

# =============================================================================
# 9. NEW ANALYSIS: DISTRIBUTION COMPARISON
# =============================================================================
print("📊 Creating distribution comparison...")

fig9 = make_subplots(
    rows=2, cols=3,
    subplot_titles=('Impulse Buying', 'Happiness', 'Promotion',
                    'Social Influence', 'Self-Control', 'Normative')
)

scores = ['IB_Score', 'Happy_Score', 'Promo_Score', 
          'Social_Score', 'SC_Score', 'Normative_Score']
positions = [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3)]

for score, (row, col) in zip(scores, positions):
    for profile in df['Behaviour_Profile'].unique():
        profile_data = df[df['Behaviour_Profile'] == profile][score]
        fig9.add_trace(
            go.Violin(y=profile_data, name=profile, showlegend=(row==1 and col==1)),
            row=row, col=col
        )

fig9.update_layout(
    title_text="<b>Score Distributions Across Behavioral Profiles</b>",
    height=600,
    showlegend=True
)
fig9.write_html("plot_9_distribution_comparison.html")

# =============================================================================
# 10. NEW ANALYSIS: STATISTICAL TESTS
# =============================================================================
print("📊 Running statistical tests...")

statistical_results = []

# ANOVA tests for each score across profiles
for score in ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']:
    groups = [df[df['Behaviour_Profile'] == p][score].dropna() 
              for p in df['Behaviour_Profile'].unique()]
    
    # ANOVA
    f_stat, p_value = f_oneway(*groups)
    
    # Kruskal-Wallis (non-parametric alternative)
    h_stat, kw_p_value = kruskal(*groups)
    
    statistical_results.append({
        'Factor': score,
        'F-Statistic': f_stat,
        'ANOVA p-value': p_value,
        'H-Statistic': h_stat,
        'Kruskal-Wallis p-value': kw_p_value,
        'Significant (α=0.05)': 'Yes' if p_value < 0.05 else 'No'
    })

stats_df = pd.DataFrame(statistical_results)
stats_df.to_csv('statistical_tests.csv', index=False)

print("\nStatistical Test Results:")
print(stats_df.to_string())

# =============================================================================
# 11. NEW ANALYSIS: IMPULSE RISK PREDICTORS
# =============================================================================
print("\n📊 Analyzing risk score predictors...")

# Correlation with risk score
risk_correlations = df[['IB_Score', 'Happy_Score', 'Promo_Score', 
                         'Social_Score', 'SC_Score', 'Normative_Score']].corrwith(
    df['Impulse_Risk_Score']
).sort_values(ascending=False)

fig10 = go.Figure(data=[
    go.Bar(x=risk_correlations.index, y=risk_correlations.values,
           marker_color=['green' if x > 0 else 'red' for x in risk_correlations.values])
])

fig10.update_layout(
    title="<b>Correlation of Factors with Impulse Risk Score</b>",
    xaxis_title="Psychological Factor",
    yaxis_title="Correlation Coefficient",
    showlegend=False
)
fig10.write_html("plot_10_risk_predictors.html")

# =============================================================================
# 12. NEW ANALYSIS: SCORE TRENDS AND OUTLIERS
# =============================================================================
print("📊 Analyzing outliers and trends...")

# Box plot with all scores
score_columns = ['IB_Score', 'Happy_Score', 'Promo_Score', 
                 'Social_Score', 'SC_Score', 'Normative_Score']

melted_scores = df.melt(value_vars=score_columns, 
                        var_name='Factor', value_name='Score')

fig11 = px.box(melted_scores, x='Factor', y='Score', 
               color='Factor', points='outliers',
               title="<b>Score Distributions and Outliers Detection</b>")
fig11.update_layout(xaxis_tickangle=-45, showlegend=False)
fig11.write_html("plot_11_outliers.html")

# =============================================================================
# 13. NEW ANALYSIS: PROFILE CHARACTERISTICS TABLE
# =============================================================================
print("📊 Creating profile characteristics table...")

profile_summary = df.groupby('Behaviour_Profile').agg({
    'Impulse_Risk_Score': ['mean', 'std', 'min', 'max'],
    'IB_Score': 'mean',
    'Happy_Score': 'mean',
    'Promo_Score': 'mean',
    'Social_Score': 'mean',
    'SC_Score': 'mean',
    'ID#': 'count'  # or just 'count' if no ID# column
}).round(2)

profile_summary.columns = ['Risk_Mean', 'Risk_Std', 'Risk_Min', 'Risk_Max',
                           'IB_Mean', 'Happy_Mean', 'Promo_Mean', 
                           'Social_Mean', 'SC_Mean', 'Count']
profile_summary.to_csv('profile_characteristics_table.csv')

print("\nProfile Characteristics:")
print(profile_summary.to_string())

# =============================================================================
# 14. NEW ANALYSIS: PERCENTILE RANKINGS
# =============================================================================
print("📊 Creating percentile rankings...")

df['Risk_Percentile'] = df['Impulse_Risk_Score'].rank(pct=True) * 100

fig12 = px.scatter(df, x=df.index, y='Risk_Percentile', 
                   color='Behaviour_Profile',
                   title="<b>Individual Risk Percentile Rankings</b>",
                   labels={'y': 'Percentile Rank', 'x': 'Participant ID'})
fig12.add_hline(y=50, line_dash="dash", line_color="gray", 
                annotation_text="Median")
fig12.add_hline(y=75, line_dash="dot", line_color="orange",
                annotation_text="75th Percentile")
fig12.add_hline(y=25, line_dash="dot", line_color="blue",
                annotation_text="25th Percentile")
fig12.write_html("plot_12_percentile_rankings.html")

# =============================================================================
# 15. NEW ANALYSIS: SUNBURST CHART
# =============================================================================
print("📊 Creating hierarchical sunburst chart...")

# Create hierarchical data
df_sunburst = df.copy()
df_sunburst['All'] = 'All Participants'

fig13 = px.sunburst(df_sunburst, 
                    path=['All', 'Risk_Category', 'Behaviour_Profile'],
                    title="<b>Hierarchical View: Risk → Profile Distribution</b>")
fig13.write_html("plot_13_sunburst.html")

# =============================================================================
# 16. NEW ANALYSIS: PARALLEL COORDINATES
# =============================================================================
print("📊 Creating parallel coordinates plot...")

# Normalize scores for better visualization
df_parallel = df.copy()
for col in ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']:
    df_parallel[col + '_norm'] = (df_parallel[col] - df_parallel[col].min()) / \
                                  (df_parallel[col].max() - df_parallel[col].min())

fig14 = px.parallel_coordinates(
    df_parallel,
    dimensions=['IB_Score_norm', 'Happy_Score_norm', 'Promo_Score_norm', 
                'Social_Score_norm', 'SC_Score_norm'],
    color='Impulse_Risk_Score',
    labels={
        'IB_Score_norm': 'Impulse',
        'Happy_Score_norm': 'Happiness',
        'Promo_Score_norm': 'Promotion',
        'Social_Score_norm': 'Social',
        'SC_Score_norm': 'Self-Control'
    },
    title="<b>Parallel Coordinates: Multi-dimensional Profile Analysis</b>",
    color_continuous_scale=px.colors.diverging.Tealrose
)
fig14.write_html("plot_14_parallel_coordinates.html")

# =============================================================================
# 17. NEW ANALYSIS: TIME/SEQUENCE PATTERNS (if applicable)
# =============================================================================
print("📊 Creating cumulative distribution...")

sorted_risk = df['Impulse_Risk_Score'].sort_values().reset_index(drop=True)
cumulative_pct = np.arange(1, len(sorted_risk) + 1) / len(sorted_risk) * 100

fig15 = go.Figure()
fig15.add_trace(go.Scatter(x=sorted_risk, y=cumulative_pct, 
                          mode='lines', name='Cumulative %',
                          line=dict(color='royalblue', width=3)))

fig15.update_layout(
    title="<b>Cumulative Distribution of Impulse Risk Scores</b>",
    xaxis_title="Impulse Risk Score",
    yaxis_title="Cumulative Percentage",
    showlegend=False
)
fig15.add_hline(y=50, line_dash="dash", annotation_text="Median")
fig15.write_html("plot_15_cumulative_distribution.html")

# =============================================================================
# 18. NEW ANALYSIS: KEY INSIGHTS SUMMARY TABLE
# =============================================================================
print("📊 Generating key insights...")

insights = {
    'Metric': [],
    'Value': [],
    'Interpretation': []
}

# Sample size
insights['Metric'].append('Total Participants')
insights['Value'].append(str(len(df)))
insights['Interpretation'].append('Sample size for analysis')

# Risk statistics
insights['Metric'].append('Mean Risk Score')
insights['Value'].append(f"{df['Impulse_Risk_Score'].mean():.2f}")
insights['Interpretation'].append('Average impulse buying risk')

insights['Metric'].append('Risk Score Std Dev')
insights['Value'].append(f"{df['Impulse_Risk_Score'].std():.2f}")
insights['Interpretation'].append('Variability in risk levels')

# Dominant profile
dominant_profile = df['Behaviour_Profile'].value_counts().idxmax()
insights['Metric'].append('Most Common Profile')
insights['Value'].append(dominant_profile)
insights['Interpretation'].append('Largest behavioral segment')

# High risk percentage
high_risk_pct = (df['Impulse_Risk_Score'] > 66).sum() / len(df) * 100
insights['Metric'].append('High Risk %')
insights['Value'].append(f"{high_risk_pct:.1f}%")
insights['Interpretation'].append('Participants with risk > 66')

# Strongest predictor
strongest_predictor = risk_correlations.idxmax()
insights['Metric'].append('Strongest Risk Predictor')
insights['Value'].append(strongest_predictor)
insights['Interpretation'].append(f'Correlation: {risk_correlations.max():.3f}')

# Cluster separation
insights['Metric'].append('PCA Variance Explained')
insights['Value'].append(f"{(pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]):.1%}")
insights['Interpretation'].append('How well 2D captures variance')

insights_df = pd.DataFrame(insights)
insights_df.to_csv('key_insights_summary.csv', index=False)

print("\nKey Insights Summary:")
print(insights_df.to_string())

# =============================================================================
# 19. RECOMMENDATIONS TABLE
# =============================================================================
print("📊 Generating recommendations by profile...")

recommendations = {
    'Behaviour_Profile': [],
    'Risk_Level': [],
    'Key_Characteristics': [],
    'Intervention_Strategy': [],
    'Marketing_Approach': []
}

for profile in df['Behaviour_Profile'].unique():
    profile_data = df[df['Behaviour_Profile'] == profile]
    avg_risk = profile_data['Impulse_Risk_Score'].mean()
    
    recommendations['Behaviour_Profile'].append(profile)
    recommendations['Risk_Level'].append('High' if avg_risk > 66 else 'Medium' if avg_risk > 33 else 'Low')
    
    # Characteristics
    characteristics = []
    if profile_data['Promo_Score'].mean() > 3.5:
        characteristics.append('Promotion-sensitive')
    if profile_data['Social_Score'].mean() > 3.5:
        characteristics.append('Socially influenced')
    if profile_data['SC_Score'].mean() < 2.5:
        characteristics.append('Low self-control')
    recommendations['Key_Characteristics'].append(', '.join(characteristics) if characteristics else 'Balanced')
    
    # Intervention
    if avg_risk > 66:
        intervention = 'Budget apps, cooling-off periods, impulse blockers'
    elif avg_risk > 33:
        intervention = 'Spending awareness tools, goal-setting'
    else:
        intervention = 'Maintain current healthy habits'
    recommendations['Intervention_Strategy'].append(intervention)
    
    # Marketing
    if 'Deal Chaser' in profile:
        marketing = 'Limited-time offers, flash sales, exclusivity'
    elif 'Social' in profile:
        marketing = 'Social proof, influencer partnerships, trending items'
    elif 'Emotional' in profile:
        marketing = 'Emotional storytelling, aspirational messaging'
    else:
        marketing = 'Value propositions, quality assurance, practical benefits'
    recommendations['Marketing_Approach'].append(marketing)

recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('profile_recommendations.csv', index=False)

print("\nProfile-Based Recommendations:")
print(recommendations_df.to_string())

# =============================================================================
# 20. EXPORT COMPREHENSIVE RESULTS
# =============================================================================
print("\n📊 Exporting comprehensive results...")

# Enhanced dataset
df.to_csv('analysis_results_enhanced.csv', index=False)

# Summary statistics by profile
summary_stats = df.groupby('Behaviour_Profile').agg({
    'Impulse_Risk_Score': ['count', 'mean', 'median', 'std', 'min', 'max'],
    'IB_Score': ['mean', 'std'],
    'Happy_Score': ['mean', 'std'],
    'Promo_Score': ['mean', 'std'],
    'Social_Score': ['mean', 'std'],
    'SC_Score': ['mean', 'std']
}).round(2)

summary_stats.to_csv('summary_statistics_by_profile.csv')

print("\n" + "="*70)
print("✅ ANALYSIS COMPLETE!")
print("="*70)
print(f"\n📁 Generated Files:")
print(f"   • 15 Interactive HTML Visualizations (plot_*.html)")
print(f"   • analysis_results_enhanced.csv - Full dataset with all features")
print(f"   • profile_characteristics_table.csv - Detailed profile metrics")
print(f"   • statistical_tests.csv - ANOVA and Kruskal-Wallis results")
print(f"   • key_insights_summary.csv - High-level findings")
print(f"   • profile_recommendations.csv - Actionable recommendations")
print(f"   • summary_statistics_by_profile.csv - Comprehensive stats")
print("\n" + "="*70)

# Print final summary
print("\n📊 QUICK SUMMARY:")
print(f"   Total Participants: {len(df)}")
print(f"   Behavioral Profiles Identified: {df['Behaviour_Profile'].nunique()}")
print(f"   Average Risk Score: {df['Impulse_Risk_Score'].mean():.2f}/100")
print(f"   High-Risk Individuals (>66): {(df['Impulse_Risk_Score'] > 66).sum()} ({(df['Impulse_Risk_Score'] > 66).sum()/len(df)*100:.1f}%)")
print(f"   Dominant Profile: {df['Behaviour_Profile'].value_counts().idxmax()}")
print(f"   Strongest Risk Factor: {risk_correlations.idxmax()} (r={risk_correlations.max():.3f})")
print("\n" + "="*70)
