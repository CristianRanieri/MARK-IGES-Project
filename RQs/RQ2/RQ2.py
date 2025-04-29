import pandas as pd
from itertools import combinations
from scipy import stats
from statsmodels.stats.multitest import multipletests

def analyze_groups(data, metrics, group_col, output_prefix="analysis_results", alpha=0.05):
    # Containers for results
    normality_results = []
    variance_results = []
    main_test_results = []
    posthoc_results = []

    for metric in metrics:
        print(f"\nAnalyzing Metric: {metric}\n" + "-" * 40)

        # Extract metric data
        metric_data = data[[group_col, metric]].dropna()
        groups = metric_data[group_col].unique()

        # Normality Test (Shapiro-Wilk)
        for group in groups:
            group_data = pd.to_numeric(
                metric_data[metric_data[group_col] == group][metric], errors="coerce"
            ).dropna()
            if group_data.empty:
                normality_results.append({
                    "Metric": metric, "Group": group, "W": None, "p-value": None, "Normal": None
                })
                continue
            stat, p = stats.shapiro(group_data)
            normality_results.append({
                "Metric": metric, "Group": group, "W": stat, "p-value": p,
                "Normal": p > alpha
            })

        # Variance Test (Levene's Test)
        group_data_list = [
            pd.to_numeric(metric_data[metric_data[group_col] == group][metric], errors="coerce").dropna()
            for group in groups
        ]
        group_data_list = [g for g in group_data_list if not g.empty]
        if len(group_data_list) >= 2:
            levene_stat, levene_p = stats.levene(*group_data_list)
            variance_results.append({
                "Metric": metric, "Levene Statistic": levene_stat, "p-value": levene_p,
                "Equal Variance": levene_p > alpha
            })

        # Determine Test Based on Assumptions
        normal = all(res["Normal"] for res in normality_results if res["Metric"] == metric)
        equal_variance = variance_results[-1]["Equal Variance"] if variance_results else False

        if normal and equal_variance:
            f_stat, f_p = stats.f_oneway(*group_data_list)
            test_name, test_stat, test_p = "ANOVA", f_stat, f_p
        elif not normal:
            h_stat, h_p = stats.kruskal(*group_data_list)
            test_name, test_stat, test_p = "Kruskal-Wallis", h_stat, h_p
        else:
            f_stat, f_p = stats.ttest_ind(*group_data_list, equal_var=False)
            test_name, test_stat, test_p = "Welch's ANOVA", f_stat, f_p

        main_test_results.append({
            "Metric": metric, "Test": test_name, "Test Statistic": test_stat,
            "p-value": test_p, "Significant": test_p < alpha
        })

        # Post-hoc Analysis (Mann-Whitney U) if Kruskal-Wallis is significant
        if test_name == "Kruskal-Wallis" and test_p < alpha:
            pairs = list(combinations(groups, 2))
            p_values = []
            pairwise_results = []

            for g1, g2 in pairs:
                group1_data = pd.to_numeric(
                    metric_data[metric_data[group_col] == g1][metric], errors="coerce"
                ).dropna()
                group2_data = pd.to_numeric(
                    metric_data[metric_data[group_col] == g2][metric], errors="coerce"
                ).dropna()
                if group1_data.empty or group2_data.empty:
                    continue
                u_stat, p_value = stats.mannwhitneyu(group1_data, group2_data, alternative="two-sided")
                p_values.append(p_value)
                pairwise_results.append({
                    "Metric": metric, "Group 1": g1, "Group 2": g2,
                    "U-Statistic": u_stat, "Raw p-value": p_value
                })

            # Holm-Bonferroni Correction
            if p_values:
                adjusted = multipletests(p_values, alpha=alpha, method="holm")
                adjusted_p_values = adjusted[1]
                rejections = adjusted[0]

                for i, result in enumerate(pairwise_results):
                    result["Adjusted p-value"] = adjusted_p_values[i]
                    result["Significant (Holm)"] = rejections[i]
                    posthoc_results.append(result)

    # Save Results to Separate CSV Files
    if normality_results:
        pd.DataFrame(normality_results).to_csv(f"{output_prefix}_normality.csv", index=False)
    if variance_results:
        pd.DataFrame(variance_results).to_csv(f"{output_prefix}_variance.csv", index=False)
    if main_test_results:
        pd.DataFrame(main_test_results).to_csv(f"{output_prefix}_main_test.csv", index=False)
    if posthoc_results:
        pd.DataFrame(posthoc_results).to_csv(f"{output_prefix}_posthoc.csv", index=False)




# Example Usage
if __name__ == "__main__":
    # Read data from CSV files
    producer_df = pd.read_csv('inputs/metrics_ml_producer_synth.csv')
    consumer_df = pd.read_csv('inputs/metrics_ml_consumer_synth.csv')
    toolkit_df = pd.read_csv('inputs/metrics_ml_Tool_synth.csv')
    both_df = pd.read_csv('inputs/metrics_ml_common_synth.csv')

    # Add Category column to each dataset
    producer_df["Category"] = "Producer"
    consumer_df["Category"] = "Consumer"
    toolkit_df["Category"] = "Toolkit"
    both_df["Category"] = "Both"

    # Merge datasets into a unified dataset
    ml_universe_dataset = pd.concat([producer_df, consumer_df, toolkit_df, both_df], ignore_index=True)

    ml_universe_dataset.to_csv("ml_universe_metrics.csv")
    # Metrics to analyze
    metrics = ['Stars', 'Size', 'Forks', 'Commit Count', 'ContributorNumber', 'Project Age', 'Activity Rate']
    group_col = "Category"

    # Analyze the unified dataset
    results = analyze_groups(ml_universe_dataset, metrics, group_col, output_prefix="RQ2_results/analysis_results")
