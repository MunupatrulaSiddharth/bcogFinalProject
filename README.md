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

## Data Analysis Pipeline (`analyze.py`)

### Core Functions

1.  **Data Export & Transformation**

    - Exports SQLite database tables to CSV format
    - Flattens nested JSON trial data into structured columns
    - Handles large numeric values (seeds/timestamps) as text

2.  **Quality Control Checks**

    - **Screen Validation**: Removes participants with screen resolution <800×600px
    - **Seriousness Filter**: Excludes participants with self-reported seriousness <70
    - **Reliability Check**: Drops inconsistent responders (repeat trial correlation <0)

3.  **Output Generation**

    ```text
    Data.csv                  # Raw database export
    Data_expanded.csv         # All processed trials
    participants_after_checks.csv  # Filtered participants
    data_after_checks.csv     # Filtered raw trials
    data_expanded_after_checks.csv # Filtered processed trials
    ```

4.  **Computation of IMR and TMR**:

    - Implement matrix arithmetic to compute IMR and TMR for each participant.
    - Use NumPy for matrix operations and averaging.

5.  **Visualization**:

    - Generate visual representations of IMRs and TMRs using libraries like Matplotlib.

6.  **Statistical Analysis**:

    - Compare IMRs and TMRs between experts and non-experts.
    - Perform statistical tests (e.g., t-tests), cosine similarities to determine significant differences.

7.  **Output**:
    - Save computed IMRs and TMRs to files for further analysis.
    - Generate summary reports and visualizations for presentation.

## Testing Component (`test_app_new.py`)

This script performs comprehensive testing of the experimental application and data processing pipeline:

1. **Application Testing**:

   - Verifies correct rendering of car stimuli images
   - Tests response recording functionality
   - Validates trial sequence and timing
   - Checks participant ID generation and session management

2. **Data Processing Tests**:

   - Validates JSON-to-CSV conversion accuracy
   - Tests quality control filters (screen size, seriousness, reliability)
   - Verifies correct computation of IMR/TMR values
   - Checks output file generation and formatting

3. **Statistical Testing**:

   - Validates cosine similarity calculations
   - Tests significance testing procedures
   - Verifies visualization generation

4. **Edge Case Handling**:

   - Tests handling of incomplete/malformed data
   - Verifies error handling for corrupt image files
   - Tests recovery from interrupted sessions

5. **Performance Testing**:
   - Measures processing time for large datasets
   - Tests memory usage during image rendering
   - Verifies scalability with increasing participant numbers

---

## References

- Albohn, D. N., Uddenberg, S. & Todorov, A. (2022). A data-driven, hyper-realistic method
  for visualizing individual mental representations of faces. _Frontiers in Psychology_, _13_, 997498.

- Peterson, J. C., Uddenberg, S., Griffiths, T. L., Todorov, A., & Suchow, J. W. (2022).
  Deep models of superficial face judgments. _Proceedings of the National Academy of
  Sciences_, _119_(17), e2115228119.
