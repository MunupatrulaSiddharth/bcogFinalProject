# bcog-Final-Project

This is an experiment to study capacity of expertise knowledge vs non-expertise to identify the impression from objects.

## Project Overview

This project is part of a research study aimed at investigating how design experts and non-experts form impressions of inanimate objects, using synthetic cars as a case study. The goal is to determine whether and to what degree experts’ impression models differ from those of non-experts in terms of quality.

### Key Research Question

- **Do experts and non-experts differ in their mental representations of synthetic cars?**
- Specifically, we aim to measure the **Idiosyncratic Mental Representation (IMR)** and **Target Mental Representation (TMR)** for each participant.

---

## Experiment Design

### Task Description

- Participants will view **300 computer-generated images of cars** across multiple trials.
- For each image, participants must select one of three options:
  - `{X}` (e.g., a specific judgment assigned to the participant)
  - `not {X}`
  - `not sure`
- The judgment `{X}` is assigned to each participant based on the experimental condition.

### Dependent Variable

- The **Idiosyncratic Mental Representation (IMR)** is calculated based on participants' choices:
  - For each participant, the IMR is derived by averaging the latent representations of all images selected in each category.
  - The IMR is computed as:  
    `IMR = X - N`  
    where:
    - `X` = average of images selected as `{X}`
    - `N` = average of images selected as `not {X}`
- The **Target Mental Representation (TMR)** is calculated as:  
  `TMR = X - N + U`  
  where `U` = average of images selected as `not sure`.

### Sample Size

- The aim is to recruit **60 participants per experimental condition**.
- The total target sample size is **60 experts and 60 non-experts**.

---

## Python Component: Data Analysis

The primary focus of this project is the **analysis of participant data** to compute and visualize IMRs and TMRs. The Python component will involve the following steps:

### Key Tasks

1. **Data Preprocessing**:

   - Load and clean participant response data.
   - Organize data into structured formats for analysis (e.g., Pandas DataFrames).

2. **Computation of IMR and TMR**:

   - Implement matrix arithmetic to compute IMR and TMR for each participant.
   - Use NumPy for matrix operations and averaging.

3. **Visualization**:

   - Generate visual representations of IMRs and TMRs using libraries like Matplotlib.

4. **Statistical Analysis**:

   - Compare IMRs and TMRs between experts and non-experts.
   - Perform statistical tests (e.g., t-tests), cosine similarities to determine significant differences.

5. **Output**:
   - Save computed IMRs and TMRs to files for further analysis.
   - Generate summary reports and visualizations for presentation.

---
