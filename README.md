# My name's Gui—welcome to my portfolio!

## Table of Contents

- [Introduction](https://github.com/galguibra/galguibra/blob/main/README.md#introduction)

- [Overview](https://github.com/galguibra/galguibra/blob/main/README.md#overview)

    - [Python](https://github.com/galguibra/galguibra/blob/main/README.md#python)
 
        - [Batch CSV Loader](https://github.com/galguibra/galguibra/blob/main/README.md#batch-csv-loader)
     
        - [Permuted, Non-Parametric Hypothesis Testing](https://github.com/galguibra/galguibra/blob/main/README.md#permuted-non-parametric-hypothesis-testing)
     
        - [Interactive Data-Visualization Dashboard](https://github.com/galguibra/galguibra/blob/main/README.md#interactive-data-visualization-dashboard)
     
    - [LaTeX](https://github.com/galguibra/galguibra/blob/main/README.md#latex)
 
        - [Statistical Appendix](https://github.com/galguibra/galguibra/blob/main/README.md#statistical-appendix)

    - [Excel](https://github.com/galguibra/galguibra/blob/main/README.md#excel)
 
        - [Tracking Participants Awaiting Follow-Up Eligibility](https://github.com/galguibra/galguibra/blob/main/README.md#tracking-participants-awaiting-follow-up-eligibility)
     
        - [Participant Record Query Tool](https://github.com/galguibra/galguibra/blob/main/README.md#participant-record-query-tool)


## Introduction

&emsp; &emsp; This is where you can find some samples of original code I've written for various projects: standalone scripts, modules taken from larger packages, key functions and routines—you 
get the idea. I chose these samples both to represent useful, transferrable skillsets in statistics and data science, as well as to highlight code that I felt was well-structured and/or 
demonstrated creative problem-solving. See something you like? Looking for something you'd hoped to see, but didn't find? Consider this repository an evolving work in progress, and consider me 
excited for feedback! Whether you're a recruiter or just an interested observer, I'm always open to constructive critique. That said, here's hoping you leave at least a little more intrigued 
than you arrived :)


## Overview

&emsp; &emsp; At the moment, my featured content includes work in Python, LaTex, and Excel. These samples came from a research project on father-inclusive pre-natal care and parenting-readiness 
interventions, making use of a variety of scientific computing libraries like numpy, pandas, scipy, the HoloViz ecosystem, and JupyterLab. There's a mix of quantitative analyses, interactive 
vizualizations, data-management and querying tools, and more. Included below are the broad strokes of each sample's purpose, as well as some additional context.


> ### Python

>> &emsp; &emsp; These samples were written to help process, analyze, and visualize ordinal, Likert-scale data from a series of REDCap surveys. The pre-existing data management system only made the 
>> data available in raw CSV files—each measure, timepoint, and participant record completely unlinked—so it needed a lot of processing before I could work with it effectively. Likewise, because of 
>> the non-Gaussian distribution of the data, differently shaped distributions across factor levels, and very small sample sizes *within* factor levels, most typical statistical tools like, e.g. 
>> ANOVA, wouldn't be valid. These scripts were all written with these issues in mind, and I made sure to include lots of tools to make the data and its complications as legible as possible.


#### Batch CSV Loader

&emsp; &emsp; I coded the load_csv module to handle the majority of that process on its own, and to prepare datasets for easy collation and joining during later steps in the analysis process. I 
also wanted to future-proof the module for use in the reproduction distribution of the project files, so I made sure to include robust, modular import tools rather than just relying on local 
file paths. The module made it very straightforward to just list whichever data files I needed in the moment and lazy load them in an easily workable format, with each dataset already set up to 
combine with others for joint analysis, data binning, visualization, etc.


#### Permuted, Non-Parametric Hypothesis Testing

&emsp; &emsp; Ordinal data doesn't admit measures like the mean and standard deviation, so I already knew I'd need a non-parametric test. We also had heavily skewed, multi-modal data, so any 
test I chose would need to be very robust. In particular, one factor level had only seven observations and needed to be compared to a level with twenty-eight observations, so I also needed a 
test that was permuted and made few assumptions about central tendency and variance between distributions. Given all of these restrictions and the fact that there are only so many statistical 
tests with standard, accessible implentations, I settled on the Brunner-Munzel test for significance, with Cliff's delta as a measure of effect size. 

&emsp; &emsp; The permuted Brunner-Munzel test can quickly become computationally expensive for larger sample sizes, though, so I made sure to implement some conditional logic to only use the 
permuted variant of the test when necessary. Unfortunately, only having access to one, low-power laptop and no remote compute cluster, this still meant several hours of compute time each time. 
After several trial runs and tweaks to the program, I managed to get things down to about 1.5–2 hours of compute time. The base package for the permuted Brunner-Munzel test still remained a 
major limiting factor, though, and I couldn't find any alternatives already coded for Python, so writing one of my own with more array optimization is definitely on my to-do list.


#### Interactive Data-Visualization Dashboard

&emsp; &emsp; This dashboard is built using the HoloViz ecosystem, served through panel with a bokeh backend and largely implemented through param and holoviews. It leverages inputs from both pandas as well as
xarray, and outputs them to interactive overlays. Users can choose a dataset, filter by participant stratum and time point, and even scroll through a selected cross-section of the data in individual slices.
And, while data for each couple is shown in paired scatters of each participant, the plot also includes a dynamic violin overlay that allows the user to compare individual couples' data to the larger distribution
of participants within their stratum. The kernel density estimates are even split by parenting role, providing a fine-grained view of patterns within the dataset.


### LaTeX

&emsp; &emsp; Selections here are samples of scientific writing typeset in a LaTeX markup. For anyone who hasn't had the pleasure of using it, LaTeX is a word-processing language that allows
complex symbology, varying scripts, and fully customizable layouts to co-exist in a user-friendly system based on descriptive macros. It's open-source with lots of community packages , and you can edit
a .tex file in any text editor before rendering it into, say, a PDF. There are even online editors that let you edit and compile side-by-side in real time! I picked it up in the math department during undergrad,
and while it definitely carries a bit of a learning curve, I've yet to find another typesetting system with quite as much functionality and consistency.


#### Statistical Appendix

&emsp; &emsp; Written as a companion piece to the data analysis performed using the [hypothesis-testing program](https://github.com/galguibra/galguibra/blob/main/README.md#permuted-non-parametric-hypothesis-testing)
from the Python section above, this appendix walks through the motivation and methodology behind all the statistics. More than just making a case for my statistical tools of choice, I wanted to provide any interested parties
with all the information they'd need to actually understand how these tools work and how you can calculate them beyond just plugging numbers into a computer. I've spent a lot of time over the years chasing down
practical explanations for methods presented in research papers, and I feel like it's the least you can do for your audience if you're including anything unusual or obscure in your methodology. I broke everything
down into more digestible chunks, and I made sure to expand on and clarify any potentially confusing notation with unique variables and explicit description, referencing source material as-needed from the originators
of the methods in question.


### Excel

&emsp; &emsp; As for the Excel samples, I wrote them as part of a user-friendly data dashboard for people on the project team who might not be familiar with and/or comfortable using more formal 
database applications. I designed the system to auto-update itself based on basic data inputs like participant contact information, study visit dates, survey completion, engagement status, etc., 
with the back-end machinery in a separate workbook to simplify the front-facing toolkit. Complete with recruitment/retention trackers, statistical overviews, information on recent and upcoming 
follow-ups, and lots of dynamic array functionalities to keep things tidy, it really helped to streamline project data management.


#### Tracking Participants Awaiting Follow-Up Eligibility

&emsp; &emsp; .


#### Participant Record Query Tool

&emsp; &emsp; .
