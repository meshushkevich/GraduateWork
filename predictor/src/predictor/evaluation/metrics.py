from typing import Dict, List, Union

import numpy as np
import pandas as pd
from sklearn.metrics import (
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    roc_auc_score,
)


class TimeSeriesMetrics:
    def __init__(self):
        self.name = "time_series_metrics"

    @staticmethod
    def calculate_regression_metrics(
        y_true: np.ndarray, y_pred: np.ndarray
    ) -> Dict[str, float]:
        """Calculate regression metrics for time series predictions."""
        results = {
            "mae": mean_absolute_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "mse": mean_squared_error(y_true, y_pred),
        }

        # MAPE - avoid division by zero
        mask = y_true != 0
        if np.any(mask):
            results["mape"] = (
                np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
            )
        else:
            results["mape"] = np.inf

        # sMAPE - Symmetric Mean Absolute Percentage Error
        denominator = (np.abs(y_true) + np.abs(y_pred)) / 2
        mask = denominator != 0
        if np.any(mask):
            results["smape"] = (
                np.mean(np.abs(y_true[mask] - y_pred[mask]) / denominator[mask]) * 100
            )
        else:
            results["smape"] = 0.0

        # Directional accuracy - percentage of times the model predicts the correct direction
        if len(y_true) > 1:
            true_dir = np.diff(y_true) > 0
            pred_dir = np.diff(y_pred) > 0
            results["directional_accuracy"] = np.mean(true_dir == pred_dir) * 100
        else:
            results["directional_accuracy"] = 0.0

        return results

    @staticmethod
    def calculate_classification_metrics(
        y_true: np.ndarray, y_pred: np.ndarray, threshold: float = None
    ) -> Dict[str, float]:
        """Calculate classification metrics for anomaly detection."""
        if threshold is None:
            # Simple approach: classify as anomaly if prediction deviates significantly from true
            residuals = np.abs(y_true - y_pred)
            threshold = np.percentile(residuals, 95)  # Top 5% as anomalies

        # Create binary classification
        true_anomalies = np.abs(y_true - np.mean(y_true)) > threshold
        pred_anomalies = np.abs(y_pred - np.mean(y_pred)) > threshold

        results = {}
        if len(np.unique(true_anomalies)) > 1:
            results["precision"] = precision_score(
                true_anomalies, pred_anomalies, zero_division=0
            )
            results["recall"] = recall_score(
                true_anomalies, pred_anomalies, zero_division=0
            )
            results["f1_score"] = f1_score(
                true_anomalies, pred_anomalies, zero_division=0
            )

            try:
                results["auc_roc"] = roc_auc_score(true_anomalies, pred_anomalies)
            except ValueError:
                results["auc_roc"] = 0.5
        else:
            results["precision"] = 0.0
            results["recall"] = 0.0
            results["f1_score"] = 0.0
            results["auc_roc"] = 0.5

        return results


class BacktestMetrics:
    def __init__(self):
        self.name = "backtest_metrics"

    @staticmethod
    def walk_forward_validation(
        model,
        df: pd.DataFrame,
        feature_columns: List[str],
        target_column: str,
        initial_train_size: int,
        step_size: int = 1,
        forecast_horizon: int = 1,
    ) -> Dict[str, Union[List, np.ndarray]]:
        """Perform walk-forward validation for time series models."""
        predictions = []
        actuals = []
        train_indices = []
        test_indices = []

        df = df.copy()
        df = df.reset_index(drop=True)

        for i in range(initial_train_size, len(df) - forecast_horizon + 1, step_size):
            # Split data
            train_data = df.iloc[:i]
            test_data = df.iloc[i : i + forecast_horizon]

            # Extract features and targets
            X_train = train_data[feature_columns]
            y_train = train_data[target_column]
            X_test = test_data[feature_columns]

            # Fit model on training data
            model.fit(X_train, y_train)

            # Make predictions
            if hasattr(model, "predict"):
                preds = model.predict(X_test)
                if isinstance(preds, np.ndarray):
                    if len(preds.shape) > 1 and preds.shape[1] == 1:
                        preds = preds.flatten()
                predictions.append(preds[-1])
                actuals.append(test_data[target_column].values[-1])

                train_indices.append(i)
                test_indices.append(i + forecast_horizon - 1)

        return {
            "predictions": predictions,
            "actuals": actuals,
            "train_indices": train_indices,
            "test_indices": test_indices,
        }

    @staticmethod
    def rolling_window_validation(
        model,
        df: pd.DataFrame,
        feature_columns: List[str],
        target_column: str,
        window_size: int,
        step_size: int = 1,
        forecast_horizon: int = 1,
    ) -> Dict[str, Union[List, np.ndarray]]:
        """Perform rolling window validation for time series models."""
        predictions = []
        actuals = []
        window_start_indices = []
        window_end_indices = []

        df = df.copy()
        df = df.reset_index(drop=True)

        for i in range(0, len(df) - window_size - forecast_horizon + 1, step_size):
            # Define window
            start_idx = i
            end_idx = i + window_size

            # Split data
            window_data = df.iloc[start_idx:end_idx]
            test_data = df.iloc[end_idx : end_idx + forecast_horizon]

            # Extract features and targets
            X_window = window_data[feature_columns]
            y_window = window_data[target_column]
            X_test = test_data[feature_columns]

            # Fit model on window data
            model.fit(X_window, y_window)

            # Make predictions
            if hasattr(model, "predict"):
                preds = model.predict(X_test)
                if isinstance(preds, np.ndarray):
                    if len(preds.shape) > 1 and preds.shape[1] == 1:
                        preds = preds.flatten()
                predictions.append(preds[-1])
                actuals.append(test_data[target_column].values[-1])

                window_start_indices.append(start_idx)
                window_end_indices.append(end_idx + forecast_horizon - 1)

        return {
            "predictions": predictions,
            "actuals": actuals,
            "window_start_indices": window_start_indices,
            "window_end_indices": window_end_indices,
        }

    @staticmethod
    def evaluate_backtest(
        predictions: np.ndarray, actuals: np.ndarray
    ) -> Dict[str, float]:
        """Evaluate backtest predictions using various metrics."""
        if len(predictions) != len(actuals):
            raise ValueError(
                f"Predictions length ({len(predictions)}) does not match actuals length ({len(actuals)})"
            )

        regression_metrics = TimeSeriesMetrics.calculate_regression_metrics(
            actuals, predictions
        )

        # Add time series specific metrics
        # Cumulative error
        cumulative_error = np.sum(predictions - actuals)
        regression_metrics["cumulative_error"] = cumulative_error

        # Max error
        regression_metrics["max_error"] = np.max(np.abs(predictions - actuals))

        # Correlation
        correlation = np.corrcoef(predictions, actuals)[0, 1]
        if np.isnan(correlation):
            correlation = 0.0
        regression_metrics["correlation"] = correlation

        return regression_metrics


class SurvivalMetrics:
    def __init__(self):
        self.name = "survival_metrics"

    @staticmethod
    def concordance_index(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate concordance index (C-index) for survival models."""
        if len(y_true) != len(y_pred):
            raise ValueError("True values and predictions must have the same length")

        n = len(y_true)
        concordant_pairs = 0
        permissible_pairs = 0

        for i in range(n):
            for j in range(i + 1, n):
                if y_true[i] != y_true[j]:
                    permissible_pairs += 1
                    if (y_true[i] < y_true[j] and y_pred[i] < y_pred[j]) or (
                        y_true[i] > y_true[j] and y_pred[i] > y_pred[j]
                    ):
                        concordant_pairs += 1

        if permissible_pairs == 0:
            return 0.5

        return concordant_pairs / permissible_pairs

    @staticmethod
    def brier_score(y_true: np.ndarray, y_pred: np.ndarray, times: np.ndarray) -> float:
        """Calculate Brier score at specific time points for survival models."""
        if len(y_true) != len(y_pred) or len(y_true) != len(times):
            raise ValueError("All inputs must have the same length")

        # Simplified Brier score - square of difference
        return np.mean((y_true - y_pred) ** 2)
