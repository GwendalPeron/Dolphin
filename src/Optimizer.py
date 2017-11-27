# The MIT License (MIT)
#
# Copyright (c) 2015 Christian Zielinski
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Original implementation : Christian Zielinski @ https://github.com/czielinski/portfolioopt

import numpy as np
import pandas as pd
import cvxopt as opt
import cvxopt.solvers as optsolvers
import warnings



'''
    tangency_portfolio(cov_mat, exp_rets, allow_short=False, min_weight=None, max_weight=None)
    Computes a tangency portfolio, i.e. a maximum Sharpe ratio portfolio.

    Note: As the Sharpe ratio is not invariant with respect
    to leverage, it is not possible to construct non-trivial
    market neutral tangency portfolios. This is because for
    a positive initial Sharpe ratio the sharpe grows unbound
    with increasing leverage.

    Parameters
    ----------
    cov_mat: pandas.DataFrame
        Covariance matrix of asset returns.
    exp_rets: pandas.Series
        Expected asset returns (often historical returns).
    allow_short: bool, optional
        If 'False' construct a long-only portfolio.
        If 'True' allow shorting, i.e. negative weights.

    Returns
    -------
    weights: pandas.Series
        Optimal asset weights.
'''
class Optimizer:
    def tangency_portfolio(cov_mat, exp_rets, allow_short=False, min_weight=None, max_weight=None):
        if not isinstance(cov_mat, pd.DataFrame):
            raise ValueError("Covariance matrix is not a DataFrame")

        if not isinstance(exp_rets, pd.Series):
            raise ValueError("Expected returns is not a Series")

        if not cov_mat.index.equals(exp_rets.index):
            raise ValueError("Indices do not match")

        n = len(cov_mat)

        if min_weight is None:
            min_weight = np.zeros((n, 1))
        if max_weight is None:
            max_weight = np.ones((n, 1))

        min_weight = np.array(min_weight).reshape((n, 1))
        max_weight = np.array(max_weight).reshape((n, 1))

        P = opt.matrix(cov_mat.values)
        q = opt.matrix(0.0, (n, 1))

        # Constraints Gx <= h
        if not allow_short:
            # exp_rets*x >= 1 and x >= 0
            # TODO make this exp_rets*x >=1 and 0.01 >= x >= 0.1
            G = opt.matrix(np.vstack((-exp_rets.values,
                                      -np.identity(n))))
            h = opt.matrix(np.vstack((-1.0,
                                      np.zeros((n, 1)))))
        else:
            # exp_rets*x >= 1
            G = opt.matrix(-exp_rets.values).T
            h = opt.matrix(-1.0)

        # Solve
        optsolvers.options['show_progress'] = False
        sol = optsolvers.qp(P, q, G, h)

        if sol['status'] != 'optimal':
            warnings.warn("Convergence problem")

        # Put weights into a labeled series
        weights = pd.Series(sol['x'], index=cov_mat.index)

        # Rescale weights, so that sum(weights) = 1
        weights /= weights.sum()
        return weights
