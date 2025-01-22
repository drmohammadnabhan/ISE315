import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit App Title
st.title("Hypothesis Testing Interactive Visualization")

# Introduction
st.markdown("""
## Introduction

Understanding statistical hypothesis testing can be challenging, as it couples abstract statistical theory with practical data analysis methods. This interactive visualization tool aims to aid your understanding of hypothesis testing in a more intuitive manner by adjusting key concepts such as alpha level, sample size, and effect size. The tool generates simulated data and performs two-sided, larger, and smaller hypothesis testing.
""")

# Sidebar Controls
st.sidebar.header("Adjust Parameters")
alpha = st.sidebar.slider("Alpha Level", 0.01, 0.2, 0.05, 0.01)
sample_size = st.sidebar.slider("Sample Size", 3, 30, 5, 1)
effect_size = st.sidebar.slider("Effect Size", 0.25, 3.0, 1.0, 0.25)
alternative = st.sidebar.selectbox("Alternative Hypothesis", ['two-sided', 'larger', 'smaller'])

# Function to visualize hypothesis testing
def visualize_hypothesis_in_original_domain(alpha, sample_size, effect_size, alternative):
    plt.figure(figsize=(8, 5))
    population_std_dev = 1
    std_error = population_std_dev / np.sqrt(sample_size)

    x = np.linspace(-3 * population_std_dev, 3 * population_std_dev, 1000)
    y_null = norm.pdf(x, loc=0, scale=std_error)

    effect_size_scaled = effect_size * population_std_dev

    if alternative == 'two-sided':
        y_alt = norm.pdf(x, loc=effect_size_scaled, scale=std_error)
    elif alternative == 'larger':
        y_alt = norm.pdf(x, loc=effect_size_scaled, scale=std_error)
    elif alternative == 'smaller':
        y_alt = norm.pdf(x, loc=-effect_size_scaled, scale=std_error)

    plt.plot(x, y_null, label='Null Hypothesis')
    plt.plot(x, y_alt, label='Alternative Hypothesis')

    if alternative == 'two-sided':
        reject = np.abs(x) >= norm.ppf(1 - alpha / 2, loc=0, scale=std_error)
    elif alternative == 'larger':
        reject = x >= norm.ppf(1 - alpha, loc=0, scale=std_error)
    elif alternative == 'smaller':
        reject = x <= norm.ppf(alpha, loc=0, scale=std_error)

    plt.fill_between(x, y_null, where=reject, alpha=0.3, color='red', label='Reject H0')
    plt.fill_between(x, y_alt, where=~reject, alpha=0.3, color='green', label='Accept H0')

    plt.ylim(0, max(max(y_null), max(y_alt)) * 1.1)
    plt.ylabel("Probability")
    plt.xlabel("Mean Difference (or relevant test statistic)")
    plt.title("Hypothesis Testing")
    plt.grid(True)
    plt.legend()

    st.pyplot(plt)

# Call the visualization function
visualize_hypothesis_in_original_domain(alpha, sample_size, effect_size, alternative)

# Explanation and Interpretation
st.markdown("""
## Key Concepts

**1. Alpha Level**: The probability of rejecting the null hypothesis when it is true. A smaller alpha reduces the chance of a Type I error (false positive).

**2. Sample Size**: The number of observations in the sample. A larger sample size provides more accurate estimates.

**3. Effect Size**: The magnitude of the experimental effect. Larger effect sizes result in stronger relationships.

**4. Null Hypothesis (H0)**: The assumption that there is no effect or difference in the population.

**5. Alternative Hypothesis (H1)**: Contradicts the null hypothesis by stating an effect or difference exists.

**6. Standard Error**: The measure of statistical accuracy, equal to the standard deviation divided by the square root of the sample size.

**7. Type I Error (α)**: Incorrect rejection of a true null hypothesis (false positive).

**8. Type II Error (β)**: Failure to reject a false null hypothesis (false negative).

## How to Use the Tool

1. Adjust the `Alpha` slider to change the significance level of the hypothesis test.
2. Modify the `Sample Size` slider to change the sample size and see its effect on the distributions.
3. Adjust the `Effect Size` slider to observe the separation between null and alternative distributions.
4. Select the type of `Alternative Hypothesis` - 'two-sided', 'larger', or 'smaller'.
5. Observe how these changes impact the visualization of Type I and Type II errors.

## Interpreting the Visualization

- **Red Area**: Represents the probability of committing a Type I error (false positive).
- **Green Area**: Represents the probability of committing a Type II error (false negative).
- The visualization dynamically updates based on your inputs to show how hypothesis testing is affected by various parameters.

## Understanding Trade-offs in Hypothesis Testing

1. **Type I and Type II Errors**: Balancing these errors is crucial in hypothesis testing. Lowering the alpha level reduces Type I errors but increases Type II errors.

2. **Sample Size and Effect Size**: Increasing sample size reduces standard error, making tests more sensitive to small effects.

3. **Effect Size and Test Sensitivity**: Smaller effect sizes require larger samples for meaningful detection.

4. **One-sided vs. Two-sided Tests**: One-sided tests have more power in one direction, while two-sided tests detect effects in both directions.

Understanding these trade-offs helps design and interpret hypothesis tests effectively.
""")
