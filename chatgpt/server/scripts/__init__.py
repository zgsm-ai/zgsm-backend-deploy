# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def calculate_portfolio_metrics(returns, risk_free_rate=0.01):
    """
    Calculate common portfolio performance metrics.

    Args:
        returns (pd.Series or np.array): Portfolio returns.
        risk_free_rate (float): Risk-free rate of return.  Defaults to 0.01 (1%).

    Returns:
        pd.Series: A series containing the calculated metrics.
    """
    
    # Convert returns to a pandas Series if it's a numpy array
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)

    # Ensure returns is a pandas Series
    if not isinstance(returns, pd.Series):
        raise TypeError("Returns must be a pandas Series or a numpy array.")

    # Calculate total return
    total_return = (returns + 1).prod() - 1

    # Calculate annualized return
    annualized_return = (1 + total_return)**(252/len(returns)) - 1 # Assuming 252 trading days in a year

    # Calculate volatility (standard deviation of returns)
    volatility = returns.std()

    # Calculate annualized volatility
    annualized_volatility = volatility * np.sqrt(252) # Assuming 252 trading days in a year

    # Calculate Sharpe Ratio
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility

    # Calculate Sortino Ratio
    downside_returns = returns[returns < 0]
    downside_volatility = downside_returns.std()
    sortino_ratio = (annualized_return - risk_free_rate) / (downside_volatility * np.sqrt(252))

    # Calculate Maximum Drawdown
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    # Create a Pandas Series to store the results
    metrics = pd.Series({
        'Total Return': total_return,
        'Annualized Return': annualized_return,
        'Volatility': volatility,
        'Annualized Volatility': annualized_volatility,
        'Sharpe Ratio': sharpe_ratio,
        'Sortino Ratio': sortino_ratio,
        'Maximum Drawdown': max_drawdown
    })

    return metrics


if __name__ == '__main__':
    # Example usage:
    # Create a sample returns series
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0.001, 0.02, 252)) # Simulate daily returns for one year

    # Calculate portfolio metrics
    metrics = calculate_portfolio_metrics(returns, risk_free_rate=0.02)

    # Print the metrics
    print(metrics)
