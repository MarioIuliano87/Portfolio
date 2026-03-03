# Linear Regression & Mixed-Effects Models — Key Notes

This document summarizes the main points about **linear regression** and **mixed-effects models**, 
with emphasis on the areas that were initially unclear.

---

## 🔹 Linear Regression (Ordinary Least Squares)

**What it does:**  
Estimates how the target variable (Y) changes with predictors (X), assuming a linear relationship.

**Key points:**
- Coefficients represent the *average effect* of a variable, **holding all others constant**.
- Example: `response_time = -0.03` → each additional minute reduces CSAT by 0.03 points.
- For categorical variables (like customer tier), one category is the **reference group**.  
  Example: `premium = +0.32` means *premium customers score 0.32 higher than basic, on average*.
- Effects are **independent** unless you add **interaction terms** (`X1 * X2`).

**Misunderstanding clarified:**  
Linear regression tells you **associations** (marginal effects), not **drivers/causes**.

---

## 🔹 Mixed-Effects Models

**What they add:**  
Linear regression **plus random effects** to handle *grouped or hierarchical data* (e.g., tickets within agents).

**Mathematical form:**  
\[
y_{ij} = \beta_0 + \beta_1 x_{ij} + u_j + \varepsilon_{ij}, \\ 
u_j \sim N(0, \tau^2), \ arepsilon_{ij} \sim N(0, \sigma^2)
\]

- **Fixed effects (β):** same interpretation as in linear regression (average effect of predictors).
- **Random effects (u_j):** account for group-specific variation (e.g., each agent has its own baseline).
- This is the **randomization**: agent intercepts are treated as random draws from a population distribution.

**Why use them?**
- Controls for unobserved differences between groups (e.g., some agents are always higher/lower CSAT scorers).
- Prevents bias if data is clustered (tickets not independent).
- Produces **generalizable fixed-effect estimates**.

**Misunderstanding clarified:**  
- Mixed-effects models still give isolated effects for fixed variables.  
- The random effect (`agent_id`) is *not the focus* — it’s there to **reduce bias** and make estimates more robust.  
- Without `agent_id`, the model assumes each row is independent, which is false if tickets repeat by agent.

---

## 🔹 Key Insights for Business Use

- Coefficients ≠ importance directly. Importance = *effect size × actionability*.  
  Example: Tier has a bigger coefficient, but response time is more actionable.
- Adding **interactions** lets you test if different groups respond differently.  
  Example: basic customers may be more sensitive to delays than enterprise.
- Random effects mean the model accounts for team composition. If 90% of agents change, the model needs retraining.

---

## 🧭 Summary

- **Linear regression**: baseline tool for associations.  
- **Mixed-effects**: regression + random structure → handles hierarchical data.  
- **Key clarification**: Mixed models don’t tell you “what drives” CSAT; they tell you *marginal effects*, while accounting for clustering.  
- **Next step**: To prove causation, move to **causal inference methods** (A/B tests, matching, IVs).

