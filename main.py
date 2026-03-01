# =============================================================================
# IMPULSE BUYING BEHAVIOR ANALYSIS DASHBOARD
# OrgX Behavioural Analytics Hackathon (Feb 28 - Mar 1)
# Developed by: Yasir Ahmad
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from scipy.stats import f_oneway, kruskal
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Impulse Buying Analytics | OrgX Hackathon",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown("""
<style>
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .dashboard-title {
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
    }
    
    .dashboard-subtitle {
        font-size: 1.2em;
        margin-top: 10px;
        opacity: 0.9;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 15px 0;
    }
    
    .warning-box {
        background: #fff3e0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 15px 0;
    }
    
    .success-box {
        background: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING AND PROCESSING
# =============================================================================
@st.cache_data
def load_and_process_data():
    """Load and process the impulse buying behavior data"""
    try:
        df = pd.read_excel('CodebookData_SEMPLS_IBB.xlsx')
        df = df.drop("Location", axis=1, errors='ignore')
        
        # Feature Engineering
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
        
        # Additional features
        df['Total_Social_Influence'] = df['Social_Score'] + df['Normative_Score']
        df['Emotional_Index'] = (df['Happy_Score'] + df['IB_Score']) / 2
        df['Rational_Control'] = df['SC_Score']
        
        # Clustering
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
        
        # PCA
        pca = PCA(n_components=2)
        pca_features = pca.fit_transform(clustering_features)
        df['PCA_1'] = pca_features[:, 0]
        df['PCA_2'] = pca_features[:, 1]
        
        # Risk Categories
        df['Risk_Category'] = pd.cut(df['Impulse_Risk_Score'], 
                                      bins=[0, 33, 66, 100],
                                      labels=['Low Risk', 'Medium Risk', 'High Risk'],
                                      include_lowest=True)
        
        df['Risk_Percentile'] = df['Impulse_Risk_Score'].rank(pct=True) * 100
        
        return df, pca, clustering_features, kmeans
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

# Load data
df, pca, clustering_features, kmeans = load_and_process_data()

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
        <h2 style='margin: 0;'>🛍️ IBB Analytics</h2>
        <p style='margin: 5px 0 0 0; font-size: 0.9em;'>OrgX Hackathon 2024</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 👤 Developer")
    st.info("**Yasir Ahmad**  \nBehavioural Analytics Specialist")
    
    st.markdown("---")
    
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "Select Page:",
        ["🏠 Dashboard", "📈 Risk Analysis", "👥 Profile Analysis", 
         "🔍 Deep Dive", "📋 Statistical Tests", "💡 Recommendations"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if df is not None:
        st.markdown("### 📌 Quick Stats")
        st.metric("Total Participants", len(df))
        st.metric("Avg Risk Score", f"{df['Impulse_Risk_Score'].mean():.1f}/100")
        st.metric("Profiles Identified", df['Behaviour_Profile'].nunique())
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🎚️ Filters")
        selected_profiles = st.multiselect(
            "Select Profiles:",
            options=df['Behaviour_Profile'].unique(),
            default=df['Behaviour_Profile'].unique()
        )
        
        risk_range = st.slider(
            "Risk Score Range:",
            0, 100, (0, 100)
        )
        
        # Apply filters
        df_filtered = df[
            (df['Behaviour_Profile'].isin(selected_profiles)) &
            (df['Impulse_Risk_Score'] >= risk_range[0]) &
            (df['Impulse_Risk_Score'] <= risk_range[1])
        ]
    else:
        df_filtered = None

# =============================================================================
# MAIN CONTENT
# =============================================================================

if df is None:
    st.error("⚠️ Please upload 'CodebookData_SEMPLS_IBB.xlsx' to proceed.")
    st.stop()

# Header
st.markdown("""
<div class='dashboard-header'>
    <div class='dashboard-title'>🛍️ Impulse Buying Behavior Analytics</div>
    <div class='dashboard-subtitle'>OrgX Behavioural Analytics Hackathon | Feb 28 - Mar 1, 2024</div>
    <div style='margin-top: 15px; font-size: 0.95em;'>
        Developed by <strong>Yasir Ahmad</strong> | Advanced ML-Powered Consumer Psychology Analysis
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# PAGE: DASHBOARD
# =============================================================================
if page == "🏠 Dashboard":
    st.markdown("## 📊 Executive Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #667eea; margin: 0;'>👥 Participants</h3>
            <h1 style='margin: 10px 0;'>{}</h1>
            <p style='color: #666; margin: 0;'>Total analyzed</p>
        </div>
        """.format(len(df_filtered)), unsafe_allow_html=True)
    
    with col2:
        avg_risk = df_filtered['Impulse_Risk_Score'].mean()
        risk_color = "#d32f2f" if avg_risk > 66 else "#ff9800" if avg_risk > 33 else "#4CAF50"
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: {}; margin: 0;'>⚠️ Avg Risk Score</h3>
            <h1 style='margin: 10px 0;'>{:.1f}/100</h1>
            <p style='color: #666; margin: 0;'>Population average</p>
        </div>
        """.format(risk_color, avg_risk), unsafe_allow_html=True)
    
    with col3:
        high_risk_count = (df_filtered['Impulse_Risk_Score'] > 66).sum()
        high_risk_pct = (high_risk_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #d32f2f; margin: 0;'>🔴 High Risk</h3>
            <h1 style='margin: 10px 0;'>{}</h1>
            <p style='color: #666; margin: 0;'>{:.1f}% of sample</p>
        </div>
        """.format(high_risk_count, high_risk_pct), unsafe_allow_html=True)
    
    with col4:
        dominant_profile = df_filtered['Behaviour_Profile'].value_counts().idxmax()
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #4CAF50; margin: 0;'>🎯 Top Profile</h3>
            <h1 style='margin: 10px 0; font-size: 1.3em;'>{}</h1>
            <p style='color: #666; margin: 0;'>Most common</p>
        </div>
        """.format(dominant_profile[:20]), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Dashboard Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Risk Score Distribution")
        fig = px.histogram(
            df_filtered, x='Impulse_Risk_Score', nbins=30,
            color_discrete_sequence=['#667eea'],
            labels={"Impulse_Risk_Score": "Risk Score"}
        )
        fig.add_vline(x=df_filtered['Impulse_Risk_Score'].mean(), 
                     line_dash="dash", line_color="red",
                     annotation_text="Mean")
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 👥 Behavioural Profiles")
        profile_counts = df_filtered['Behaviour_Profile'].value_counts().reset_index()
        profile_counts.columns = ['Profile', 'Count']
        fig = px.pie(profile_counts, values='Count', names='Profile',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 PCA Cluster Visualization")
        fig = px.scatter(
            df_filtered, x='PCA_1', y='PCA_2', 
            color='Behaviour_Profile',
            size='Impulse_Risk_Score',
            hover_data=['Impulse_Risk_Score'],
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='white')))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🔥 Risk by Profile")
        risk_by_profile = df_filtered.groupby('Behaviour_Profile')['Impulse_Risk_Score'].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(risk_by_profile, x='Impulse_Risk_Score', y='Behaviour_Profile',
                    orientation='h',
                    color='Impulse_Risk_Score',
                    color_continuous_scale='Reds',
                    labels={'Impulse_Risk_Score': 'Avg Risk Score'})
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: RISK ANALYSIS
# =============================================================================
elif page == "📈 Risk Analysis":
    st.markdown("## 📈 Risk Analysis Deep Dive")
    
    tab1, tab2, tab3 = st.tabs(["Risk Distribution", "Risk Predictors", "Risk Categories"])
    
    with tab1:
        st.markdown("### 📊 Detailed Risk Score Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=df_filtered['Impulse_Risk_Score'],
                nbinsx=40,
                name='Risk Distribution',
                marker_color='#667eea',
                opacity=0.7
            ))
            
            fig.add_vline(x=df_filtered['Impulse_Risk_Score'].mean(),
                         line_dash="dash", line_color="red", line_width=2,
                         annotation_text=f"Mean: {df_filtered['Impulse_Risk_Score'].mean():.1f}")
            fig.add_vline(x=df_filtered['Impulse_Risk_Score'].median(),
                         line_dash="dot", line_color="green", line_width=2,
                         annotation_text=f"Median: {df_filtered['Impulse_Risk_Score'].median():.1f}")
            
            fig.update_layout(
                title="Risk Score Distribution with Central Tendencies",
                xaxis_title="Impulse Risk Score",
                yaxis_title="Frequency",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Statistics")
            stats_df = pd.DataFrame({
                'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Q1', 'Q3', 'IQR'],
                'Value': [
                    f"{df_filtered['Impulse_Risk_Score'].mean():.2f}",
                    f"{df_filtered['Impulse_Risk_Score'].median():.2f}",
                    f"{df_filtered['Impulse_Risk_Score'].std():.2f}",
                    f"{df_filtered['Impulse_Risk_Score'].min():.2f}",
                    f"{df_filtered['Impulse_Risk_Score'].max():.2f}",
                    f"{df_filtered['Impulse_Risk_Score'].quantile(0.25):.2f}",
                    f"{df_filtered['Impulse_Risk_Score'].quantile(0.75):.2f}",
                    f"{df_filtered['Impulse_Risk_Score'].quantile(0.75) - df_filtered['Impulse_Risk_Score'].quantile(0.25):.2f}"
                ]
            })
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
        
        # Cumulative Distribution
        st.markdown("### 📈 Cumulative Distribution Function")
        sorted_risk = df_filtered['Impulse_Risk_Score'].sort_values().reset_index(drop=True)
        cumulative_pct = np.arange(1, len(sorted_risk) + 1) / len(sorted_risk) * 100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sorted_risk, y=cumulative_pct,
            mode='lines', name='CDF',
            line=dict(color='royalblue', width=3),
            fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        fig.add_hline(y=50, line_dash="dash", annotation_text="50th Percentile")
        fig.add_hline(y=75, line_dash="dot", annotation_text="75th Percentile", line_color="orange")
        fig.add_hline(y=25, line_dash="dot", annotation_text="25th Percentile", line_color="green")
        fig.update_layout(
            xaxis_title="Impulse Risk Score",
            yaxis_title="Cumulative Percentage",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔍 Risk Predictors & Correlations")
        
        risk_correlations = df_filtered[['IB_Score', 'Happy_Score', 'Promo_Score', 
                                'Social_Score', 'SC_Score', 'Normative_Score']].corrwith(
            df_filtered['Impulse_Risk_Score']
        ).sort_values(ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    x=risk_correlations.index, 
                    y=risk_correlations.values,
                    marker_color=['#4CAF50' if x > 0 else '#f44336' for x in risk_correlations.values],
                    text=[f"{x:.3f}" for x in risk_correlations.values],
                    textposition='outside'
                )
            ])
            fig.update_layout(
                title="Correlation with Impulse Risk Score",
                xaxis_title="Psychological Factor",
                yaxis_title="Correlation Coefficient",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Key Insights")
            strongest = risk_correlations.idxmax()
            weakest = risk_correlations.idxmin()
            
            st.success(f"**Strongest Predictor:**  \n{strongest}  \n({risk_correlations.max():.3f})")
            st.info(f"**Weakest Correlation:**  \n{weakest}  \n({risk_correlations.min():.3f})")
            
            st.markdown("#### 📊 Interpretation")
            st.write(f"Factors with positive correlation increase risk, while negative correlations (like Self-Control) reduce it.")
        
        # Correlation Heatmap
        st.markdown("### 🔥 Correlation Matrix")
        correlation_cols = ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 
                            'Normative_Score', 'SC_Score', 'Impulse_Risk_Score']
        corr_matrix = df_filtered[correlation_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
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
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎯 Risk Categories Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_counts = df_filtered['Risk_Category'].value_counts().reset_index()
            risk_counts.columns = ['Category', 'Count']
            fig = px.pie(risk_counts, values='Count', names='Category',
                        color='Category',
                        color_discrete_map={
                            'Low Risk': '#4CAF50',
                            'Medium Risk': '#ff9800',
                            'High Risk': '#f44336'
                        })
            fig.update_layout(title="Risk Category Distribution", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            risk_profile_crosstab = pd.crosstab(df_filtered['Risk_Category'], 
                                                df_filtered['Behaviour_Profile'])
            fig = go.Figure(data=[
                go.Bar(name=profile, x=risk_profile_crosstab.index, 
                      y=risk_profile_crosstab[profile])
                for profile in risk_profile_crosstab.columns
            ])
            fig.update_layout(
                title="Risk Categories by Profile",
                xaxis_title="Risk Category",
                yaxis_title="Count",
                barmode='stack',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Percentile Rankings
        st.markdown("### 📊 Individual Risk Percentile Rankings")
        fig = px.scatter(
            df_filtered.reset_index(), x='index', y='Risk_Percentile',
            color='Behaviour_Profile',
            hover_data=['Impulse_Risk_Score'],
            labels={'index': 'Participant ID', 'Risk_Percentile': 'Percentile Rank'}
        )
        fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Median")
        fig.add_hline(y=75, line_dash="dot", line_color="orange", annotation_text="75th")
        fig.add_hline(y=25, line_dash="dot", line_color="blue", annotation_text="25th")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: PROFILE ANALYSIS
# =============================================================================
elif page == "👥 Profile Analysis":
    st.markdown("## 👥 Behavioural Profile Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Profile Overview", "Profile Comparison", "Profile Characteristics"])
    
    with tab1:
        st.markdown("### 📊 Profile Distribution & Characteristics")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            profile_counts = df_filtered['Behaviour_Profile'].value_counts().reset_index()
            profile_counts.columns = ['Profile', 'Count']
            fig = px.bar(profile_counts, y='Profile', x='Count', orientation='h',
                        color='Profile', text='Count')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            cluster_centers = df_filtered.groupby('Behaviour_Profile')[
                ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']
            ].mean().reset_index()
            melted_centers = cluster_centers.melt(
                id_vars='Behaviour_Profile',
                var_name='Factor',
                value_name='Score'
            )
            fig = px.bar(melted_centers, x='Behaviour_Profile', y='Score',
                        color='Factor', barmode='group')
            fig.update_layout(
                title="Average Psychological Scores per Profile",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Radar Chart
        st.markdown("### 🎯 Multi-dimensional Profile Comparison (Radar Chart)")
        categories = ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']
        profile_means = df_filtered.groupby('Behaviour_Profile')[categories].mean()
        
        fig = go.Figure()
        for profile in profile_means.index:
            values = profile_means.loc[profile].tolist()
            values.append(values[0])
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=profile
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 Score Distributions Across Profiles")
        
        scores = ['IB_Score', 'Happy_Score', 'Promo_Score', 
                  'Social_Score', 'SC_Score', 'Normative_Score']
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Impulse Buying', 'Happiness', 'Promotion',
                            'Social Influence', 'Self-Control', 'Normative')
        )
        
        positions = [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3)]
        
        for score, (row, col) in zip(scores, positions):
            for profile in df_filtered['Behaviour_Profile'].unique():
                profile_data = df_filtered[df_filtered['Behaviour_Profile'] == profile][score]
                fig.add_trace(
                    go.Violin(y=profile_data, name=profile, showlegend=(row==1 and col==1)),
                    row=row, col=col
                )
        
        fig.update_layout(height=700, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Box plots for outlier detection
        st.markdown("### 🔍 Outlier Detection by Profile")
        score_columns = ['IB_Score', 'Happy_Score', 'Promo_Score', 
                        'Social_Score', 'SC_Score', 'Normative_Score']
        melted_scores = df_filtered.melt(value_vars=score_columns, 
                                        var_name='Factor', value_name='Score')
        fig = px.box(melted_scores, x='Factor', y='Score', 
                    color='Factor', points='outliers')
        fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 📋 Detailed Profile Characteristics")
        
        profile_summary = df_filtered.groupby('Behaviour_Profile').agg({
            'Impulse_Risk_Score': ['mean', 'std', 'min', 'max', 'count'],
            'IB_Score': 'mean',
            'Happy_Score': 'mean',
            'Promo_Score': 'mean',
            'Social_Score': 'mean',
            'SC_Score': 'mean'
        }).round(2)
        
        profile_summary.columns = ['Risk_Mean', 'Risk_Std', 'Risk_Min', 'Risk_Max', 'Count',
                                   'IB_Mean', 'Happy_Mean', 'Promo_Mean', 'Social_Mean', 'SC_Mean']
        
        st.dataframe(profile_summary, use_container_width=True)
        
        # Profile characteristics table with styling
        st.markdown("### 🎯 Profile Risk Assessment")
        
        risk_assessment = []
        for profile in df_filtered['Behaviour_Profile'].unique():
            profile_data = df_filtered[df_filtered['Behaviour_Profile'] == profile]
            avg_risk = profile_data['Impulse_Risk_Score'].mean()
            
            risk_level = 'High' if avg_risk > 66 else 'Medium' if avg_risk > 33 else 'Low'
            risk_color = '🔴' if avg_risk > 66 else '🟡' if avg_risk > 33 else '🟢'
            
            risk_assessment.append({
                'Profile': profile,
                'Risk Level': f"{risk_color} {risk_level}",
                'Avg Risk Score': f"{avg_risk:.1f}",
                'Count': len(profile_data),
                'Top Trait': profile_data[['IB_Score', 'Happy_Score', 'Promo_Score', 
                                          'Social_Score']].mean().idxmax()
            })
        
        risk_df = pd.DataFrame(risk_assessment)
        st.dataframe(risk_df, hide_index=True, use_container_width=True)

# =============================================================================
# PAGE: DEEP DIVE
# =============================================================================
elif page == "🔍 Deep Dive":
    st.markdown("## 🔍 Advanced Analytics Deep Dive")
    
    tab1, tab2, tab3 = st.tabs(["Parallel Coordinates", "Sunburst Hierarchy", "3D Analysis"])
    
    with tab1:
        st.markdown("### 📊 Parallel Coordinates: Multi-dimensional View")
        
        df_parallel = df_filtered.copy()
        for col in ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']:
            df_parallel[col + '_norm'] = (df_parallel[col] - df_parallel[col].min()) / \
                                         (df_parallel[col].max() - df_parallel[col].min())
        
        fig = px.parallel_coordinates(
            df_parallel.head(200),  # Limit for performance
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
            color_continuous_scale=px.colors.diverging.Tealrose
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("🔍 **How to read:** Each line represents one participant. Follow the lines to see how different psychological factors relate to each other.")
    
    with tab2:
        st.markdown("### 🌟 Hierarchical Distribution: Risk → Profile")
        
        df_sunburst = df_filtered.copy()
        df_sunburst['All'] = 'All Participants'
        
        fig = px.sunburst(
            df_sunburst,
            path=['All', 'Risk_Category', 'Behaviour_Profile'],
            color='Impulse_Risk_Score',
            color_continuous_scale='RdYlGn_r',
            hover_data={'Impulse_Risk_Score': ':.1f'}
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("🔍 **Interactive Tip:** Click on any segment to zoom in and explore that category in detail.")
    
    with tab3:
        st.markdown("### 🎲 3D Psychological Space")
        
        fig = px.scatter_3d(
            df_filtered, x='IB_Score', y='Social_Score', z='SC_Score',
            color='Behaviour_Profile',
            size='Impulse_Risk_Score',
            hover_data=['Impulse_Risk_Score', 'Promo_Score'],
            labels={
                'IB_Score': 'Impulse Buying',
                'Social_Score': 'Social Influence',
                'SC_Score': 'Self Control'
            }
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📈 Feature Importance by Profile")
        
        feature_importance = []
        for profile in df_filtered['Behaviour_Profile'].unique():
            profile_data = df_filtered[df_filtered['Behaviour_Profile'] == profile]
            scores = profile_data[['IB_Score', 'Happy_Score', 'Promo_Score', 
                                   'Social_Score', 'SC_Score']].mean()
            feature_importance.append({
                'Profile': profile,
                **{f: scores[f] for f in scores.index}
            })
        
        fi_df = pd.DataFrame(feature_importance).set_index('Profile')
        fig = px.imshow(fi_df.T, 
                       labels=dict(x="Profile", y="Factor", color="Score"),
                       color_continuous_scale='Viridis',
                       aspect="auto")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: STATISTICAL TESTS
# =============================================================================
elif page == "📋 Statistical Tests":
    st.markdown("## 📋 Statistical Testing & Validation")
    
    st.markdown("### 🧪 ANOVA & Kruskal-Wallis Tests")
    st.info("Testing whether psychological factors differ significantly across behavioural profiles.")
    
    statistical_results = []
    
    for score in ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']:
        groups = [df_filtered[df_filtered['Behaviour_Profile'] == p][score].dropna() 
                  for p in df_filtered['Behaviour_Profile'].unique()]
        
        if all(len(g) > 0 for g in groups):
            f_stat, p_value = f_oneway(*groups)
            h_stat, kw_p_value = kruskal(*groups)
            
            statistical_results.append({
                'Factor': score.replace('_Score', ''),
                'F-Statistic': f"{f_stat:.3f}",
                'ANOVA p-value': f"{p_value:.6f}",
                'H-Statistic': f"{h_stat:.3f}",
                'Kruskal p-value': f"{kw_p_value:.6f}",
                'Significant': '✅ Yes' if p_value < 0.05 else '❌ No'
            })
    
    stats_df = pd.DataFrame(statistical_results)
    
    st.dataframe(stats_df, hide_index=True, use_container_width=True)
    
    # Visualization of p-values
    st.markdown("### 📊 Statistical Significance Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(stats_df, x='Factor', y='ANOVA p-value',
                    color='Significant',
                    color_discrete_map={'✅ Yes': '#4CAF50', '❌ No': '#f44336'})
        fig.add_hline(y=0.05, line_dash="dash", line_color="red",
                     annotation_text="α = 0.05")
        fig.update_layout(height=400, yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(stats_df, x='Factor', y='Kruskal p-value',
                    color='Significant',
                    color_discrete_map={'✅ Yes': '#4CAF50', '❌ No': '#f44336'})
        fig.add_hline(y=0.05, line_dash="dash", line_color="red",
                     annotation_text="α = 0.05")
        fig.update_layout(height=400, yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📊 Effect Sizes & Group Comparisons")
    
    # Calculate effect sizes
    for score in ['IB_Score', 'Happy_Score', 'Promo_Score', 'Social_Score', 'SC_Score']:
        st.markdown(f"#### {score.replace('_Score', '')} by Profile")
        
        profile_means = df_filtered.groupby('Behaviour_Profile')[score].mean().sort_values()
        
        fig = px.bar(profile_means.reset_index(), x='Behaviour_Profile', y=score,
                    color=score, color_continuous_scale='Viridis')
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Interpretation
    st.markdown("### 💡 Interpretation Guide")
    st.success("""
    **Statistical Significance (p < 0.05):**
    - ✅ **Significant**: The psychological factor varies meaningfully across profiles
    - ❌ **Not Significant**: No strong evidence of differences between profiles
    
    **ANOVA F-Statistic:** Higher values indicate greater between-group variance
    **Kruskal-Wallis H-Statistic:** Non-parametric alternative, robust to outliers
    """)

# =============================================================================
# PAGE: RECOMMENDATIONS
# =============================================================================
elif page == "💡 Recommendations":
    st.markdown("## 💡 Strategic Recommendations")
    
    tab1, tab2 = st.tabs(["Profile-Based Strategies", "Key Insights"])
    
    with tab1:
        st.markdown("### 🎯 Targeted Interventions by Profile")
        
        recommendations = []
        for profile in df_filtered['Behaviour_Profile'].unique():
            profile_data = df_filtered[df_filtered['Behaviour_Profile'] == profile]
            avg_risk = profile_data['Impulse_Risk_Score'].mean()
            
            # Characteristics
            characteristics = []
            if profile_data['Promo_Score'].mean() > 3.5:
                characteristics.append('Promotion-sensitive')
            if profile_data['Social_Score'].mean() > 3.5:
                characteristics.append('Socially influenced')
            if profile_data['SC_Score'].mean() < 2.5:
                characteristics.append('Low self-control')
            
            # Interventions
            if avg_risk > 66:
                intervention = '🔴 Budget apps, cooling-off periods, impulse blockers'
            elif avg_risk > 33:
                intervention = '🟡 Spending awareness tools, goal-setting'
            else:
                intervention = '🟢 Maintain current healthy habits'
            
            # Marketing
            if 'Deal Chaser' in profile:
                marketing = '🎯 Limited-time offers, flash sales, exclusivity'
            elif 'Social' in profile:
                marketing = '👥 Social proof, influencer partnerships, trending items'
            elif 'Emotional' in profile:
                marketing = '❤️ Emotional storytelling, aspirational messaging'
            else:
                marketing = '💎 Value propositions, quality assurance, practical benefits'
            
            recommendations.append({
                'Profile': profile,
                'Risk Level': '🔴 High' if avg_risk > 66 else '🟡 Medium' if avg_risk > 33 else '🟢 Low',
                'Key Traits': ', '.join(characteristics) if characteristics else 'Balanced',
                'Intervention': intervention,
                'Marketing Strategy': marketing,
                'Count': len(profile_data)
            })
        
        rec_df = pd.DataFrame(recommendations)
        
        for _, row in rec_df.iterrows():
            with st.expander(f"**{row['Profile']}** ({row['Count']} participants) - {row['Risk Level']}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🎯 Key Characteristics:**")
                    st.write(row['Key Traits'])
                    
                    st.markdown("**🛡️ Recommended Interventions:**")
                    st.write(row['Intervention'])
                
                with col2:
                    st.markdown("**📢 Marketing Approach:**")
                    st.write(row['Marketing Strategy'])
                    
                    # Profile-specific metrics
                    profile_data = df_filtered[df_filtered['Behaviour_Profile'] == row['Profile']]
                    st.metric("Average Risk Score", f"{profile_data['Impulse_Risk_Score'].mean():.1f}/100")
    
    with tab2:
        st.markdown("### 📊 Key Insights & Findings")
        
        # Generate insights
        total_participants = len(df_filtered)
        avg_risk = df_filtered['Impulse_Risk_Score'].mean()
        high_risk_pct = (df_filtered['Impulse_Risk_Score'] > 66).sum() / len(df_filtered) * 100
        dominant_profile = df_filtered['Behaviour_Profile'].value_counts().idxmax()
        
        risk_correlations = df_filtered[['IB_Score', 'Happy_Score', 'Promo_Score', 
                                'Social_Score', 'SC_Score', 'Normative_Score']].corrwith(
            df_filtered['Impulse_Risk_Score']
        ).sort_values(ascending=False)
        strongest_predictor = risk_correlations.idxmax()
        
        # Display insights in cards
        st.markdown("#### 🔍 Population Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='success-box'>
                <h4>📊 Sample Size</h4>
                <h2>{}</h2>
                <p>Total participants analyzed</p>
            </div>
            """.format(total_participants), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='warning-box'>
                <h4>⚠️ Average Risk</h4>
                <h2>{:.1f}/100</h2>
                <p>Population mean risk score</p>
            </div>
            """.format(avg_risk), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='info-box'>
                <h4>🎯 Dominant Profile</h4>
                <h2 style='font-size: 1.2em;'>{}</h2>
                <p>Most common behavioral type</p>
            </div>
            """.format(dominant_profile[:25]), unsafe_allow_html=True)
        
        st.markdown("#### 🎯 Critical Findings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h4>🔴 High-Risk Segment</h4>
                <h2>{:.1f}%</h2>
                <p>Participants with risk score > 66</p>
                <p style='margin-top: 10px;'><strong>Recommendation:</strong> Priority intervention group requiring immediate attention and behavioral modification strategies.</p>
            </div>
            """.format(high_risk_pct), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-card'>
                <h4>🎯 Primary Risk Driver</h4>
                <h2>{}</h2>
                <p>Correlation: {:.3f}</p>
                <p style='margin-top: 10px;'><strong>Implication:</strong> This factor shows the strongest relationship with impulse buying risk and should be targeted in interventions.</p>
            </div>
            """.format(strongest_predictor.replace('_Score', ''), risk_correlations.max()), unsafe_allow_html=True)
        
        # Actionable recommendations
        st.markdown("#### 💼 Actionable Recommendations")
        
        st.markdown("""
        <div class='success-box'>
            <h4>🎯 For Businesses:</h4>
            <ul>
                <li><strong>Segment Marketing:</strong> Tailor messaging to each behavioral profile</li>
                <li><strong>Ethical Considerations:</strong> Balance conversion optimization with consumer wellbeing</li>
                <li><strong>Personalization:</strong> Use profile characteristics to customize user experience</li>
                <li><strong>Timing Strategies:</strong> Target high-risk profiles during optimal decision-making periods</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-box'>
            <h4>🛡️ For Consumers:</h4>
            <ul>
                <li><strong>Self-Awareness:</strong> Understand your behavioral profile and triggers</li>
                <li><strong>Tools & Apps:</strong> Use budget tracking and impulse control applications</li>
                <li><strong>Cooling-Off Periods:</strong> Implement waiting periods before major purchases</li>
                <li><strong>Social Support:</strong> Share financial goals with accountability partners</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='warning-box'>
            <h4>🔬 For Researchers:</h4>
            <ul>
                <li><strong>Validation Studies:</strong> Test interventions on high-risk profiles</li>
                <li><strong>Longitudinal Analysis:</strong> Track behavioral changes over time</li>
                <li><strong>Cross-Cultural:</strong> Examine profile differences across demographics</li>
                <li><strong>Predictive Modeling:</strong> Develop early warning systems for at-risk individuals</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>🛍️ Impulse Buying Behavior Analytics Dashboard</strong></p>
    <p>OrgX Behavioural Analytics Hackathon | February 28 - March 1, 2024</p>
    <p>Developed by <strong>Yasir Ahmad</strong> | Advanced ML-Powered Consumer Psychology Analysis</p>
    <p style='font-size: 0.9em; margin-top: 10px;'>
        Built with Streamlit • Powered by Python & Plotly • Machine Learning with scikit-learn
    </p>
</div>
""", unsafe_allow_html=True)
