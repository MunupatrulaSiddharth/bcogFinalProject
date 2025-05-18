# Abstract

Mental health stigma remains a pervasive societal issue, influencing interpersonal behavior, access to care, and policy support. While explicit attitudes have been widely studied, less is known about how individuals visually conceptualize mental illness in others. This study aims to investigate the mental representations people hold of various psychological disorders by leveraging a reverse correlation approach to face perception.

Participants will complete a categorization task in which they judge AI-generated faces for their resemblance to individuals with specific mental health conditions, including depression, anxiety, bipolar disorder, and post-traumatic stress disorder. The images are randomly sampled from a generative adversarial network trained on neutral human faces, allowing for systematic mapping of participants’ visual intuitions. From these responses, individual-level visual prototypes will be estimated.

These prototypes will then be analyzed using computational models of social perception to assess how visual representations align with attributes such as trustworthiness, dominance, and attractiveness. Importantly, the strength and valence of these impressions will be related to participants’ self-reported stigma toward mental illness, as measured by a validated scale.

It is expected that visual representations of mental illness will systematically differ from those of non-illness categories along socially relevant dimensions, and that these differences will scale with individual variation in stigma. By making implicit visual stereotypes explicit, this study offers a novel framework for quantifying how social bias becomes encoded in mental imagery.

The findings have implications for understanding the visual basis of stigma and may inform future interventions aimed at reducing misperceptions of mental illness.

## Experiment Design

### Task Description

- Participants will view **300 computer-generated images of faces** across multiple trials.
- For each image, participants must select one of three options:
  - `{X}` (e.g., a specific judgment assigned to the participant)
  - `not {X}`
  - `not sure`
- The judgment `{X}` is assigned to each participant based on the experimental condition.

### Dependent Variable

- The **Target Mental Representation (TMR)** is calculated as:  
  `TMR = X - N + U`  
  where `U` = average of images selected as `not sure`.

### Sample Size

- The aim is to recruit **30 participants per experimental condition**.
- The total target sample size is **120-150 participants across all conditions**.

---

## Python Component: Data Analysis

The primary focus of this project is the **analysis of participant data** to compute and visualize TMRs. The Python component will involve the following steps:

### Implementation Plan

## Data Analysis Pipeline (`analyze.ipynb`)

### Core Functions

1.  **Data Export & Transformation** -- Done

    - Exports SQLite database tables to CSV format
    - Flattens nested JSON trial data into structured columns
    - Handles large numeric values (seeds/timestamps) as text

2.  **Quality Control Checks** -- Done

    - **Screen Validation**: Removes participants with screen resolution <800×600px
    - **Seriousness Filter**: Excludes participants with self-reported seriousness <70
    - **Reliability Check**: Drops inconsistent responders (repeat trial correlation <0)

3.  **Output Generation** -- Done

    ```text
    Data.csv                  # Raw database export
    Data_expanded.csv         # All processed trials
    participants_after_checks.csv  # Filtered participants
    data_after_checks.csv     # Filtered raw trials
    data_expanded_after_checks.csv # Filtered processed trials
    ```

4.  **Computation of TMR**: -- ToDo

    - Implement matrix arithmetic to compute TMR for each participant.
    - Use NumPy for matrix operations and averaging.
    - Then do the same for across all participants.

5.  **Visualization**: -- ToDo

    - Generate visual representations of TMRs using libraries like Matplotlib.

6.  **Statistical Analysis**: -- ToDo

    - Perform statistical tests (e.g., t-tests), cosine similarities to determine significant differences.
    - Visualize TMRs.

7.  **Output**: -- ToDo
    - Save computed TMRs to files for further analysis.
    - Generate summary reports and visualizations for presentation.

## Testing Component (`test_app_new.py`)

This script performs comprehensive testing of the experimental application and data processing pipeline:

1. **Generate Dummy Data**: -- Done

   - Generates dummy data for participant table
   - Generates dummy data for data table
   - This data is generated exactly in the format that the frontend is saving data

2. **Data Processing Tests**: -- Done first two

   - Validates JSON-to-CSV conversion accuracy
   - Tests quality control filters (screen size, seriousness, reliability)
   - Verifies correct computation of TMR values
   - Checks output file generation and formatting

3. **Statistical Testing**: -- ToDo

   - Validates cosine similarity calculations
   - Tests significance testing procedures
   - Verifies visualization generation

---

## References

- Albohn, D. N., Uddenberg, S. & Todorov, A. (2022). A data-driven, hyper-realistic method
  for visualizing individual mental representations of faces. _Frontiers in Psychology_, _13_, 997498.

- Peterson, J. C., Uddenberg, S., Griffiths, T. L., Todorov, A., & Suchow, J. W. (2022).
  Deep models of superficial face judgments. _Proceedings of the National Academy of
  Sciences_, _119_(17), e2115228119.
