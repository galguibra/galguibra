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


### Python

&emsp; &emsp; These samples were written to help process, analyze, and visualize ordinal, Likert-scale data from a series of REDCap surveys. The pre-existing data management system only made the 
data available in raw CSV files—each measure, timepoint, and participant record completely unlinked—so it needed a lot of processing before I could work with it effectively. Likewise, because of 
the non-Gaussian distribution of the data, differently shaped distributions across factor levels, and very small sample sizes *within* factor levels, most typical statistical tools like, e.g. 
ANOVA, wouldn't be valid. These scripts were all written with these issues in mind, and I made sure to include lots of tools to make the data and its complications as legible as possible.


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

&emsp; &emsp; .


### LaTeX

&emsp; &emsp; .


#### Statistical Appendix

&emsp; &emsp; .


### Excel

&emsp; &emsp; As for the Excel samples, I wrote them as part of a user-friendly data dashboard for people on the project team who might not be familiar with and/or comfortable using more formal 
database applications. I designed the system to auto-update itself based on basic data inputs like participant contact information, study visit dates, survey completion, engagement status, etc., 
with the back-end machinery in a separate workbook to simplify the front-facing toolkit. Complete with recruitment/retention trackers, statistical overviews, information on recent and upcoming 
follow-ups, and lots of dynamic array functionalities to keep things tidy, it really helped to streamline project data management.


#### Tracking Participants Awaiting Follow-Up Eligibility

&emsp; &emsp; .


#### Participant Record Query Tool

&emsp; &emsp; .
