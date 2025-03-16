# Abstract

This study explores how design expertise influences the formation and articulation of impressions of inanimate objects, using synthetic car images as a case study. Impressions, which are automatic and often visceral, play a critical role in emotional design, particularly in fields like product and automotive design, where visual form is used to evoke specific emotions such as aggressiveness or friendliness. While prior research has examined impression formation in faces and other stimuli, little is known about how expertise shapes these processes in the context of object perception. This study addresses this gap by comparing the mental representations of design experts and non-experts using reverse correlation and computational modeling techniques.

We hypothesize that design experts, due to their training in form-giving and emotional communication, will demonstrate more nuanced and higher-quality mental representations compared to non-experts. This study builds on foundational work in reverse correlation (Albohn et al., 2022) and computational modeling of perceptual judgments (Peterson et al., 2022), extending these methods to the domain of object perception.

The findings will advance psychological theories of impression formation while offering practical insights for design disciplines, where understanding the relationship between form and emotion is crucial for creating emotionally resonant products. By bridging psychological research and design practice, this study highlights the role of expertise in shaping how we perceive and interpret the visual world.

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

## References

- Albohn, D. N., Uddenberg, S. & Todorov, A. (2022). A data-driven, hyper-realistic method
  for visualizing individual mental representations of faces. *Frontiers in Psychology*, *13*, 997498.

- Peterson, J. C., Uddenberg, S., Griffiths, T. L., Todorov, A., & Suchow, J. W. (2022).
  Deep models of superficial face judgments. *Proceedings of the National Academy of
  Sciences*, *119*(17), e2115228119.
