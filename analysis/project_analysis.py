import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ProjectAnalyzer:

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    # ------------------------------------
    # 1 Load Data
    # ------------------------------------

    def get_dataset_summary(self):

        summary = {
            "total_projects": len(self.df),
            "avg_margin": self.df["final_margin_pct"].mean(),
            "avg_delay_ratio": self.df["delay_ratio"].mean(),
            "avg_risk_mitigation": self.df["risk_mitigation_rate"].mean()
        }

        return summary


    # ------------------------------------
    # 2 Profitability by Line of Business
    # ------------------------------------

    def profitability_by_business(self):

        result = (
            self.df
            .groupby("line_of_business")["final_margin_pct"]
            .mean()
            .sort_values(ascending=False)
        )

        return result


    # ------------------------------------
    # 3 Profitability by Region
    # ------------------------------------

    def profitability_by_region(self):

        result = (
            self.df
            .groupby("region")["final_margin_pct"]
            .mean()
            .sort_values(ascending=False)
        )

        return result


    # ------------------------------------
    # 4 Tier vs Profitability
    # ------------------------------------

    def profitability_by_tier(self):

        result = (
            self.df
            .groupby("tier")["final_margin_pct"]
            .mean()
            .sort_values(ascending=False)
        )

        return result


    # ------------------------------------
    # 5 Forecast Accuracy
    # ------------------------------------

    def forecast_accuracy(self):

        self.df["forecast_error"] = (
            (self.df["final_cost"] - self.df["forecast_cost"]) /
            self.df["forecast_cost"]
        )

        return self.df["forecast_error"].mean()


    # ------------------------------------
    # 6 Change Order Impact
    # ------------------------------------

    def change_order_impact(self):

        result = (
            self.df
            .groupby("line_of_business")["change_order_profit"]
            .mean()
        )

        return result


    # ------------------------------------
    # 7 Delays by Business
    # ------------------------------------

    def delay_by_business(self):

        result = (
            self.df
            .groupby("line_of_business")["delay_ratio"]
            .mean()
        )

        return result


    # ------------------------------------
    # 8 Delays vs Profitability
    # ------------------------------------

    def delays_vs_profit(self):

        correlation = self.df["delay_ratio"].corr(
            self.df["final_margin_pct"]
        )

        return correlation


    # ------------------------------------
    # 9 Risk Exposure
    # ------------------------------------

    def risk_exposure(self):

        return self.df["risks_registered"].mean()


    # ------------------------------------
    # 10 Risk Mitigation
    # ------------------------------------

    def risk_mitigation_by_region(self):

        result = (
            self.df
            .groupby("region")["risk_mitigation_rate"]
            .mean()
        )

        return result


    # ------------------------------------
    # 11 Risks vs Delays
    # ------------------------------------

    def risks_vs_delays(self):

        correlation = self.df["risks_registered"].corr(
            self.df["delay_ratio"]
        )

        return correlation


    # ------------------------------------
    # 12 Risk Management Issues
    # ------------------------------------

    def risk_management_issues(self):

        return self.df["risk_management_issue"].mean()


    # ------------------------------------
    # 13 Portfolio Distribution
    # ------------------------------------

    def portfolio_distribution(self):

        result = (
            self.df
            .groupby("region")
            .size()
        )

        return result


    # ------------------------------------
    # 14 Duration vs Cost
    # ------------------------------------

    def duration_vs_cost_corr(self):

        return self.df["estimated_duration_days"].corr(
            self.df["forecast_cost"]
        )


    # ------------------------------------
    # 15 Problematic Projects
    # ------------------------------------

    def problematic_projects(self):

        problematic = self.df[
            (self.df["high_delay_flag"] == 1) |
            (self.df["low_margin_flag"] == 1) |
            (self.df["risk_management_issue"] == 1)
        ]

        return len(problematic)