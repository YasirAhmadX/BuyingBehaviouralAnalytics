# 🚀 Quick Start Guide - Enhanced Impulse Buying Analysis

## ⚡ 5-Minute Setup

### **Step 1: Install Required Packages**
```bash
pip install pandas numpy scikit-learn scipy plotly seaborn matplotlib openpyxl
```

### **Step 2: Place Your Data File**
Ensure `CodebookData_SEMPLS_IBB.xlsx` is in the same directory as the script.

### **Step 3: Run the Analysis**
```bash
python enhanced_analysis.py
```

### **Step 4: View Results**
Open any of the 15 HTML files in your browser to explore visualizations!

---

## 📁 File Structure

```
your_project_folder/
│
├── CodebookData_SEMPLS_IBB.xlsx    # Your input data (REQUIRED)
├── enhanced_analysis.py             # Main script
├── DOCUMENTATION.md                 # Detailed documentation
├── COMPARISON_GUIDE.md              # Before/after comparison
├── QUICK_START.md                   # This file
│
└── outputs/ (auto-generated)
    ├── plot_1_trait_deviations.html
    ├── plot_2_risk_score.html
    ├── ... (15 HTML files total)
    ├── analysis_results_enhanced.csv
    ├── profile_characteristics_table.csv
    ├── statistical_tests.csv
    ├── key_insights_summary.csv
    ├── profile_recommendations.csv
    └── summary_statistics_by_profile.csv
```

---

## 🎯 What to Look at First

### **For Quick Insights (5 minutes)**
1. Open `key_insights_summary.csv` - High-level findings
2. Open `plot_3_profiles.html` - See profile distribution
3. Open `plot_8_radar_profiles.html` - Compare profiles visually

### **For Deep Dive (30 minutes)**
1. Read through all visualizations (plot_1 through plot_15)
2. Review `statistical_tests.csv` for significance
3. Check `profile_recommendations.csv` for action items
4. Examine `summary_statistics_by_profile.csv` for details

### **For Academic Paper (2 hours)**
1. Use `summary_statistics_by_profile.csv` as Table 1
2. Include `plot_6_correlation_heatmap.html` as Figure 1
3. Include `plot_8_radar_profiles.html` as Figure 2
4. Report ANOVA results from `statistical_tests.csv` in text
5. Reference `key_insights_summary.csv` for abstract/discussion

### **For Business Presentation (1 hour)**
1. Start with `plot_13_sunburst.html` (overview)
2. Show `plot_3_profiles.html` (segment sizes)
3. Present `plot_7_risk_categories.html` (risk distribution)
4. Share `profile_recommendations.csv` (action plan)
5. Use `plot_10_risk_predictors.html` (prioritization)

---

## 🔧 Troubleshooting

### **Error: "No module named 'xyz'"**
**Solution**: Install missing package
```bash
pip install xyz
```

### **Error: "File not found"**
**Solution**: Make sure your Excel file is named exactly `CodebookData_SEMPLS_IBB.xlsx` and is in the same folder as the script.

### **Plots not showing?**
**Solution**: They're saved as HTML files. Open them directly in any web browser (Chrome, Firefox, Safari, Edge).

### **Script runs but no output?**
**Solution**: Check console for error messages. Make sure all packages are installed.

### **Different number of clusters?**
**Solution**: Change `n_clusters=4` in line 54 of the script to your desired number.

---

## 🎨 Customization Options

### **Change Cluster Count**
```python
# Line 54: Change from 4 to any number
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)  # Now 5 clusters
```

### **Adjust Risk Formula**
```python
# Lines 34-39: Modify weights
df['Raw_Risk'] = (
    (2.0 * df['IB_Score']) +      # Increase impulse buying weight
    df['Happy_Score'] +
    (0.5 * df['Promo_Score']) +   # Decrease promotion weight
    df['Social_Score'] +
    df['Risk_SC_Penalty']
)
```

### **Change Risk Thresholds**
```python
# Line 197: Modify cutoffs
df['Risk_Category'] = pd.cut(df['Impulse_Risk_Score'], 
                              bins=[0, 40, 70, 100],  # Changed from [0,33,66,100]
                              labels=['Low Risk', 'Medium Risk', 'High Risk'])
```

### **Add Custom Profile Labels**
```python
# Lines 59-70: Edit labeling logic
labels = {}
for i in range(4):
    row = cluster_means.loc[i]
    
    # Add your own rules here
    if row['Promo_Score'] > 4.0:
        labels[i] = "Super Shopper"  # Custom name
    elif row['Social_Score'] > 4.0:
        labels[i] = "Influencer Buyer"  # Custom name
    # ... etc
```

---

## 📊 Understanding the Outputs

### **CSV Files** (Data Tables)

| File | What It Contains | When to Use |
|------|------------------|-------------|
| `analysis_results_enhanced.csv` | Full dataset with all calculated features | Raw data export, further analysis |
| `profile_characteristics_table.csv` | Statistics for each profile | Profile descriptions, comparisons |
| `statistical_tests.csv` | ANOVA and Kruskal-Wallis results | Significance testing, academic papers |
| `key_insights_summary.csv` | Top-level findings | Executive summary, abstracts |
| `profile_recommendations.csv` | Intervention and marketing strategies | Action planning, decision-making |
| `summary_statistics_by_profile.csv` | Comprehensive descriptive stats | Detailed reporting, appendices |

### **HTML Files** (Interactive Visualizations)

| Plot # | Name | Best For |
|--------|------|----------|
| 1 | Trait Deviations | Data exploration, outlier check |
| 2 | Risk Distribution | Overall risk assessment |
| 3 | Profile Counts | Segment sizing |
| 4 | PCA Clusters | Cluster validation |
| 5 | Cluster Centers | Mean comparisons |
| 6 | Correlation Heatmap | Factor relationships |
| 7 | Risk Categories | Risk segmentation |
| 8 | Radar Profiles | Quick visual comparison |
| 9 | Distribution Comparison | Variance analysis |
| 10 | Risk Predictors | Prioritization |
| 11 | Outliers | Data quality |
| 12 | Percentile Rankings | Individual positioning |
| 13 | Sunburst | Hierarchical overview |
| 14 | Parallel Coordinates | Multi-dimensional patterns |
| 15 | Cumulative Distribution | Threshold setting |

---

## ⚙️ Advanced Usage

### **Batch Processing Multiple Files**
```python
import glob

excel_files = glob.glob("*.xlsx")

for file in excel_files:
    print(f"Processing {file}...")
    df = pd.read_excel(file)
    # ... rest of analysis
    # Save with unique names
    df.to_csv(f'{file[:-5]}_results.csv', index=False)
```

### **Export Plots as Static Images**
```python
# Add after each fig.write_html() line:
fig.write_image("plot_1.png", width=1200, height=800)

# Requires: pip install kaleido
```

### **Run Silently (No Console Output)**
```bash
python enhanced_analysis.py > /dev/null 2>&1
```

### **Schedule Automated Runs**
```bash
# Linux/Mac (crontab)
0 9 * * * cd /path/to/project && python enhanced_analysis.py

# Windows (Task Scheduler)
# Create new task pointing to python.exe with enhanced_analysis.py as argument
```

---

## 🎓 Learning Path

### **Beginner** (Just want results)
1. Run script as-is
2. Open HTML files
3. Read key_insights_summary.csv
4. Done! ✅

### **Intermediate** (Want to understand)
1. Run script
2. Review DOCUMENTATION.md
3. Compare COMPARISON_GUIDE.md
4. Modify risk formula
5. Re-run and compare results

### **Advanced** (Want to extend)
1. Add new features (demographics, etc.)
2. Try different clustering algorithms
3. Build predictive models (regression, classification)
4. Create interactive dashboard (Dash/Streamlit)
5. Integrate with business systems

---

## 📧 Getting Help

### **Check These First:**
1. **DOCUMENTATION.md** - Detailed explanations of every feature
2. **COMPARISON_GUIDE.md** - Before/after comparison and use cases
3. **Script comments** - Inline explanations in the code

### **Common Questions:**

**Q: How many participants do I need?**  
A: Minimum 100 for meaningful clustering, 200+ recommended.

**Q: What if I have missing data?**  
A: Currently filled with 0. Check data quality in Plot 11 (outliers).

**Q: Can I use different survey questions?**  
A: Yes! Modify the regex patterns in lines 25-30 to match your column names.

**Q: How do I cite this analysis?**  
A: Include methodology description from DOCUMENTATION.md in your paper.

**Q: Can I share these files?**  
A: Yes, but ensure you have permission to share the underlying data.

---

## ✅ Pre-Flight Checklist

Before running the analysis, ensure:

- [ ] Data file is in correct location
- [ ] Data file is named `CodebookData_SEMPLS_IBB.xlsx` (or update script)
- [ ] All packages installed (`pip list` to check)
- [ ] Python version 3.7 or higher (`python --version`)
- [ ] At least 100 MB free disk space for outputs
- [ ] No other programs have the Excel file open

---

## 🎉 You're Ready!

**Just run:**
```bash
python enhanced_analysis.py
```

**Expected runtime:** 30-60 seconds  
**Expected output:** 21 files (15 HTML + 6 CSV)  
**Next step:** Open HTML files in browser and explore!

---

## 📚 Additional Resources

- **Plotly Documentation**: https://plotly.com/python/
- **Scikit-learn Clustering**: https://scikit-learn.org/stable/modules/clustering.html
- **Pandas Guide**: https://pandas.pydata.org/docs/user_guide/index.html
- **Statistical Tests**: https://docs.scipy.org/doc/scipy/reference/stats.html

---

**Happy Analyzing! 🚀📊**

*For detailed feature explanations, see DOCUMENTATION.md*  
*For before/after comparison, see COMPARISON_GUIDE.md*
