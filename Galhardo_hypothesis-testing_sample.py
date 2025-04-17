"""Calculate non-parametric effect size and test for significance.

Summary:
--------
    Uses Cliff's delta as a measure of effect size and Brunner-Munzel for
    significance testing. A permuted test is used in pairwise comparisons
    involving the treatment group of [0, 1) sessions attended, owing to
    small sample size.

Hypotheses:
-----------
    H0:
    ---
        P(X < Y) <= P(Y < X) for X, Y random variables representing the
        distribution of median scores for a given measure and treatment groups
        X,Y such that participants in group X attended fewer total sessions
        than those in group Y.

    Ha:
    ---
        P(X < Y) > P(Y < X), with X, Y defined as in H0. For parental stress
        in particular, the direction of the hypothesis is reversed.

@author: Guilherme Galhardo
"""

import numpy as np
import pandas as pd
import scipy as sp
import permuted_brunnermunzel.brunnermunzel_test as pbm
import effect_size_analysis as esa
import functools as ft
import typing
import math  # noqa: API import
np.math = math  # Compatibility patch for pbm module

# Namespace containing datasets of parental behavior and self-assessment.
import behavior_Export_Formatting as bef


def get_measure_treatments(
    measure_series: pd.Series,
    group_labels: list[str],
) -> tuple[list[int], list[int], list[int]]:
    """Bin measure data into treatment groups.

    Parameters
    ----------
    measure_series : pd.Series
        Data for the given measure, indexed by treatment group.

    group_labels : list[str]
        List containing the labels of the treatment groups, used to take
        cross sections of measure_series.

    Returns
    -------
    measure_treatments : tuple[list[int], list[int], list[int]]
        List containing a sublist for each treatment group's subset
        of the data contained in measure_series.

    """
    measure_treatments = tuple(
        [
            measure_series.xs(group).to_numpy().tolist()
            for group in group_labels
        ]
    )

    return measure_treatments


def get_testing_groups(
    source_df: pd.DataFrame,
    group_labels: list[str],
    measure_labels: list[str],
) -> list[tuple[list[int], list[int], list[int]]]:
    """Generate nested array of each treatment group's data for each measure.

    Calls get_treatment_measures to generate sublists.

    Parameters
    ----------
    source_df : pd.DataFrame
        Pandas DataErame containing the original integer dataset. 

    group_labels : list[str]
        List containing the labels for each of the treatment groups.

    measure_labels : list[str]
        List containing the labels for each of the measures.

    Returns
    -------
    treatments_by_measure : list[tuple[list[int], list[int], list[int]]]
        Nested list containing a tuple for each measure, each of which
        contains a sublist for each treatment group. The sublists contain
        integer data cut from source_df.

    """
    measure_series = [source_df[label].dropna() for label in measure_labels]

    treatments_by_measure = [
        get_measure_treatments(series, group_labels)
        for series in measure_series
    ]

    return treatments_by_measure


def get_effect_size(
    treatment_x: list[int],
    treatment_y: list[int],
) -> tuple[float , tuple[np.float64, np.float64]]:
    """Calculate pairwise effect sizes using Cliff's delta.

    Parameters
    ----------
    treatment_x : list[int]
        List containing the data from treatment group X for the given measure.

    treatment_y : list[int]
        List containing the data from treatment group Y for the given measure.

    Returns
    -------
    effect : tuple(float, tuple[np.float64, np.float64]
        Test statistic and 95% CI for the pairwise test between
        treatment groups X and Y, given by X's stochastic dominance over Y.

    """
    effect = esa.cliff_delta(
        s1=treatment_x, s2=treatment_y, alpha=0.05, accurate_ci=True
    )

    return effect


def get_significance(
    treatment_x: list[int],
    treatment_y: list[int],
    measure_name: str,
) -> tuple[np.float64, float | np.float64]:
    """Perform Brunner-Munzel test, using permutation if necessary.

    Parameters
    ----------
    treatment_x : list[int]
        List containing the data from treatment group X for the given measure.

    treatment_y : list[int]
        List containing the data from treatment group Y for the given measure.
        
    measure_name : str
        Label for given measure.

    Returns
    -------
    significance : tuple[np.float64, float | np.float64]
        Test statistic and p-value for the pairwise test between
        treatment groups X and Y, performed with the alternative hypothesis
        that P(X < Y) > P(Y < X). For parental stress in particular, the
        direction of the hypothesis is reversed. p-value will be a float when
        performing the permuted test, and np.float64 when performing the
        standard test.

    """
    permute_check = min(map(len, [treatment_x, treatment_y])) < 10

    test_function = (
        pbm.permuted_brunnermunzel if permute_check else sp.stats.brunnermunzel
    )

    alternative = "less" if measure_name != "Parental Stress" else "greater"

    test_call = ft.partial(
        test_function, alternative=alternative, nan_policy="omit"
    )

    significance = test_call(treatment_x, treatment_y)

    return significance


def test_measure(
    measure_treatments: list[list[int]],
    group_labels: list[str],
    measure_name: str
) -> pd.Series:
    """Calculate effect-size and significance for the given measure.

    Calls get_effect_size and get_significance.

    Parameters
    ----------
    measure_treatments : list[list[int]]
        List containing a sublist for each treatment group's subset
        of the data for the given measure.

    group_labels : list[str]
        List containing the labels for each of the treatment groups.

    measure_name : str
        Label for given measure.

    Returns
    -------
    pairwise_stats : pd.Series
        Pandas series of lists, each containing two tuples. The first contains
        the effect size given by Cliff's delta, along with an interpretation.
        The second tuple contains the Brunner-Munzel W-statistic, as well as
        its associated p-value.

    """
    treatment_0, treatment_1, treatment_2 = measure_treatments

    testing_pairs = [
        (treatment_0, treatment_1),
        (treatment_1, treatment_2),
        (treatment_0, treatment_2),
    ]

    pair_labels = [
        f"{group_labels[x]} v.s. {group_labels[y]}"
        for x, y in [(0, 1), (1, 2), (0, 2)]
    ]

    pairwise_stats = pd.Series(
        [
            [get_effect_size(*pair), get_significance(*pair, measure_name)]
            for pair in testing_pairs
        ],
        index=pair_labels,
        name=measure_name,
    )

    return pairwise_stats


def analyze_data(source_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate effect size and significance statistics for all measures.

    For each measure in the overall dataset, analyze_data will bin the data
    by treatment group and then perform pairwise calculations for Cliff's delta
    and the Brunner-Munzel test, possibly permuted if appropriate.

    Calls get_testing_groups and test_measure

    Parameters
    ----------
    source_df : pd.DataFrame
        Pandas dataframe containing the original dataset.

    Returns
    -------
    measure_stats : pd.DataFrame
        Pandas dataframe containing calculated, pairwise statistics by measure.
        Each product of measure and pairwise test, yielding twelve total
        results, is of the following form:
        
        list[tuple(float, tuple(float, float)), tuple(float, float)]
        
        The first of the outermost two tuples is for effect size, and the
        second for significance. In the effect size tuple, we have the point
        estimate and the tuple representing the 95% CI. In the significance
        tuple, we have the W-statistic and the p-value.

    """
    group_labels = source_df.index.unique().to_numpy().tolist()
    measure_labels = source_df.columns.to_numpy().tolist()

    testing_groups = get_testing_groups(
        source_df,
        group_labels,
        measure_labels,
    )

    measure_stats = pd.DataFrame(
        [
            test_measure(measure_treatments, group_labels, measure_name)
            for measure_treatments, measure_name in zip(
                testing_groups, measure_labels
            )
        ]
    )

    return measure_stats


bm_df = bef.bm_df.xs(1, level="Timepoint").droplevel("Participant")
measure_stats_df = analyze_data(bm_df)
