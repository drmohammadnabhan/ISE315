import numpy as np
from scipy.stats import norm, t, chi2
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit App
st.title("P-Value Calculator and Visualization")

st.markdown("""
## Introduction to P-Value

The p-value is a measure that helps determine the significance of your hypothesis test. It represents the probability of obtaining results as extreme as the observed data, assuming that the null hypothesis is true.

In hypothesis testing, the p-value is compared to the significance level (\(\alpha\)) to decide whether to reject the null hypothesis (H0). A smaller p-value indicates stronger evidence against H0.
""")

# Sidebar input controls
statistic = st.number_input("Enter Test Statistic:", value=0.0, step=0.1)
test_type = st.selectbox("Choose Test Type:", ['Z-test', 'T-test', 'Chi-square'])
tail_type = st.selectbox("Tail Type:", ['Upper', 'Lower', 'Two-tailed'])
df = st.number_input("Degrees of Freedom (for T-test/Chi-square):", min_value=1, value=1, step=1) if test_type in ['T-test', 'Chi-square'] else 1

# Function to calculate p-value
def calculate_p_value(statistic, test_type, tail_type='Upper', df=1):
    if test_type == 'Z-test' or test_type == 'T-test':
        if tail_type == 'Two-tailed':
            p_value = 2 * (1 - norm.cdf(abs(statistic))) if test_type == 'Z-test' else 2 * (1 - t.cdf(abs(statistic), df))
        else:
            p_value = (1 - norm.cdf(statistic)) if tail_type == 'Upper' and test_type == 'Z-test' else norm.cdf(statistic) if tail_type == 'Lower' and test_type == 'Z-test' else (1 - t.cdf(statistic, df)) if tail_type == 'Upper' else t.cdf(statistic, df)
    elif test_type == 'Chi-square':
        p_value = 1 - chi2.cdf(statistic, df) if tail_type == 'Upper' else chi2.cdf(statistic, df)
    return p_value

# Function to plot the distribution and p-value
def plot_p_value(statistic, p_value, test_type, tail_type='Upper', df=1):
    x = np.linspace(-4, 4, 1000) if test_type in ['Z-test', 'T-test'] else np.linspace(0, max(10, statistic + 10), 1000)
    y = norm.pdf(x) if test_type == 'Z-test' else t.pdf(x, df) if test_type == 'T-test' else chi2.pdf(x, df)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'b-', lw=2)

    if tail_type == 'Two-tailed':
        critical_val = abs(statistic)
        ax.fill_between(x, y, where=(x <= -critical_val) | (x >= critical_val), color='red', alpha=0.5)
    elif tail_type == 'Upper':
        ax.fill_between(x, y, where=x >= statistic, color='red', alpha=0.5)
    else:
        ax.fill_between(x, y, where=x <= statistic, color='red', alpha=0.5)

    ax.set_title(f'{test_type} Distribution (Statistic = {statistic}, P-Value = {p_value:.4f})')
    ax.set_xlabel('Statistic Value')
    ax.set_ylabel('Probability Density')

    st.pyplot(fig)

# Calculate button
if st.button("Calculate P-Value"):
    p_value = calculate_p_value(statistic, test_type, tail_type, df)
    st.success(f"Calculated P-Value: {p_value:.4f}")
    plot_p_value(statistic, p_value, test_type, tail_type, df)

st.markdown("""
## Example of a Hypothesis Test

Suppose we want to test whether the mean weight of a certain product is 50kg. We take a sample and calculate a test statistic of 1.75 from a standard normal distribution.

- **Null Hypothesis (H0):** The mean weight is 50kg.
- **Alternative Hypothesis (H1):** The mean weight is not 50kg (Two-tailed test).
- **Test Statistic:** 1.75
- **Significance Level:** 0.05

Using the tool, we input the test statistic and select a Z-test with a two-tailed option to visualize the p-value.
""")
