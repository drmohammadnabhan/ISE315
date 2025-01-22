import numpy as np
from scipy.stats import norm, t, chi2
import matplotlib.pyplot as plt
import streamlit as st

# Function to calculate p-value based on the selected test type
def calculate_p_value(statistic, test_type, tail_type='Upper', df=1):
    if test_type == 'Z-test' or test_type == 'T-test':
        if tail_type == 'Two-tailed':
            p_value = 2 * (1 - norm.cdf(abs(statistic))) if test_type == 'Z-test' else 2 * (1 - t.cdf(abs(statistic), df))
        else:
            p_value = (1 - norm.cdf(statistic)) if tail_type == 'Upper' and test_type == 'Z-test' else norm.cdf(statistic) if tail_type == 'Lower' and test_type == 'Z-test' else (1 - t.cdf(statistic, df)) if tail_type == 'Upper' else t.cdf(statistic, df)
    elif test_type == 'Chi-square':
        if tail_type == 'Upper':
            p_value = 1 - chi2.cdf(statistic, df)
        elif tail_type == 'Lower':
            p_value = chi2.cdf(statistic, df)
        else:  # Two-tailed (conceptual, not standard)
            p_value = 2 * min(chi2.cdf(statistic, df), 1 - chi2.cdf(statistic, df))
    return p_value

# Function to plot the distribution and p-value
def plot_p_value(statistic, p_value, test_type, tail_type='Upper', df=1):
    x = np.linspace(-4, 4, 1000) if test_type in ['Z-test', 'T-test'] else np.linspace(0, max(10, statistic + 10), 1000)
    y = norm.pdf(x) if test_type == 'Z-test' else t.pdf(x, df) if test_type == 'T-test' else chi2.pdf(x, df)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'b-', lw=2)

    if test_type == 'Chi-square':
        if tail_type == 'Upper':
            ax.fill_between(x, y, where=x >= statistic, color='red', alpha=0.5)
        elif tail_type == 'Lower':
            ax.fill_between(x, y, where=x <= statistic, color='red', alpha=0.5)
    else:
        if tail_type == 'Two-tailed':
            critical_val_left = norm.ppf(p_value / 2) if test_type == 'Z-test' else t.ppf(p_value / 2, df)
            critical_val_right = norm.ppf(1 - p_value / 2) if test_type == 'Z-test' else t.ppf(1 - p_value / 2, df)
            ax.fill_between(x, y, where=(x <= critical_val_left) | (x >= critical_val_right), color='red', alpha=0.5)
        elif tail_type == 'Upper':
            critical_val = norm.ppf(1 - p_value) if test_type == 'Z-test' else t.ppf(1 - p_value, df)
            ax.fill_between(x, y, where=x >= critical_val, color='red', alpha=0.5)
        else:  # Lower
            critical_val = norm.ppf(p_value) if test_type == 'Z-test' else t.ppf(p_value, df)
            ax.fill_between(x, y, where=x <= critical_val, color='red', alpha=0.5)

    ax.set_title(f'{test_type} Distribution (Statistic = {statistic}, P-Value = {p_value:.4f})')
    ax.set_xlabel('Statistic Value')
    ax.set_ylabel('Probability Density')

    st.pyplot(fig)

# Streamlit App
st.title("P-Value Calculator and Visualization")

# Sidebar input controls
statistic = st.number_input("Enter Test Statistic:", value=0.0, step=0.1)
test_type = st.selectbox("Choose Test Type:", ['Z-test', 'T-test', 'Chi-square'])
tail_type = st.selectbox("Tail Type:", ['Upper', 'Lower', 'Two-tailed'])
df = st.number_input("Degrees of Freedom (for T-test/Chi-square):", min_value=1, value=1, step=1) if test_type in ['T-test', 'Chi-square'] else 1

# Calculate button
if st.button("Calculate P-Value"):
    p_value = calculate_p_value(statistic, test_type, tail_type, df)
    st.success(f"Calculated P-Value: {p_value:.4f}")
    plot_p_value(statistic, p_value, test_type, tail_type, df)

# Explanation Section
st.markdown("""
## How to Use This Tool
1. **Enter the test statistic:** Input your calculated statistic.
2. **Select the test type:** Choose between Z-test, T-test, or Chi-square test.
3. **Choose the tail type:** Upper, Lower, or Two-tailed.
4. **Degrees of Freedom:** Required for T-test and Chi-square tests.
5. **Click Calculate P-Value to visualize and obtain results.**

## Interpretation of Results
- **Z-Test:** Assumes normal distribution, used for large sample sizes.
- **T-Test:** Used for small sample sizes, accounts for variance in the data.
- **Chi-Square Test:** Used to test relationships between categorical variables.

The red-shaded area represents the p-value, helping you understand the significance of your test.
""")
