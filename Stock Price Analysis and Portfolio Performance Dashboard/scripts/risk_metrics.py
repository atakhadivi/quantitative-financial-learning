import numpy as np
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression

def annualized_return(returns, periods=252):
    return np.mean(returns) * periods

def annualized_volatility(returns, periods=252):
    return np.std(returns) * np.sqrt(periods)

class RiskMetrics:
    @staticmethod
    def sharpe_ratio(returns, risk_free_rate=0.01, periods=252):
        return (annualized_return(returns, periods) - risk_free_rate) / annualized_volatility(returns, periods)
    
    @staticmethod
    def sortino_ratio(returns, risk_free_rate=0.01, target=0, periods=252):
        mean_return = np.mean(returns)
        downside = returns[returns < target]
        if downside.size == 0:
            return np.nan
        downside_std = np.std(downside) * np.sqrt(periods)
        return (mean_return * periods - risk_free_rate) / downside_std
    
    @staticmethod
    def max_drawdown(returns):
        cum_returns = (1 + returns).cumprod()
        peak = cum_returns.expanding(min_periods=1).max()
        drawdown = (cum_returns / peak) - 1
        return drawdown.min()

class PortfolioAnalytics:
    @staticmethod
    def calculate_portfolio_returns(weights, cov_matrix):
        return weights.T @ cov_matrix @ weights
    
    @staticmethod
    def optimize_weights(mean_returns, cov_matrix):
        num_assets = len(mean_returns)
        def objective(w):
            return w.T @ cov_matrix @ w
        
        def constraint_eq(w):
            return w.sum() - 1.0
        
        cons = ({'type': 'eq', 'fun': constraint_eq})
        bounds = tuple((0, 1) for _ in range(num_assets))
        opt = minimize(
            objective,
            num_assets * [1./num_assets],
            method='SLSQP',
            bounds=bounds,
            constraints=cons
        )
        return opt.x