import numpy as np
import random

import networkx as nx

def sbm_graph(n, k, a, b):
    if n % k != 0:
        raise ValueError('n %k != 0')
    elif a <= b:
        raise ValueError('a <= b')
    sizes = [int(n/k) for _ in range(k)]
    _p = np.log(n) * a / n
    _q = np.log(n) * b / n
    if _p > 1 or _q > 1:
        raise ValueError('%f (probability) larger than 1' % _p)
    p = np.diag(np.ones(k) * (_p - _q)) + _q * np.ones([k, k])
    return nx.generators.community.stochastic_block_model(sizes, p)

class SIBM2:
    '''SIBM with two community'''
    def __init__(self, graph, _beta, _gamma):
        self.G = graph
        self._beta = _beta
        self._gamma = _gamma
        self.n = len(self.G.nodes)
        # randomly initiate a configuration
        self.sigma = [1 for i in range(self.n)]
        nodes = list(self.G)
        random.Random().shuffle(nodes)
        k = 2
        self.k = k
        for node_state in range(k):
            for i in range(self.n // k):
                self.sigma[nodes[i * k + node_state]] = 2 * node_state - 1
        # node state is +1 or -1
        self.m = self.n / 2 # number of +1
        self.mixed_param = self._gamma * np.log(self.n)
        self.mixed_param /= self.n
    def get_dH(self, trial_location):
        _sum = 0
        w_s = self.sigma[trial_location]
        for i in self.G[trial_location]:
                _sum += self.sigma[i]
        _sum *= w_s * (1 + self.mixed_param)
        _sum -= self.mixed_param * (w_s * (2 * self.m - self.n) - 1)
        return _sum
    def _metropolis_single(self):
        # randomly select one position to inspect
        r = random.randint(0, self.n - 1)
        delta_H = self.get_dH(r)
        if delta_H < 0:  # lower energy: flip for sure
            self.sigma[r] *= -1
            self.m += self.sigma[r]
        else:  # Higher energy: flip sometimes
            probability = np.exp(-1.0 * self._beta * delta_H)
            if np.random.rand() < probability:
                self.sigma[r] *= -1
                self.m += self.sigma[r]
    def metropolis(self, N=40):
        # iterate given rounds
        for _ in range(N):
            for _ in range(self.n):
                self._metropolis_single()
        return self.sigma

class SIBMk:
    '''SIBM with multiple community'''
    def __init__(self, graph, _beta, _gamma, k=2):
        self.G = graph
        self._beta = _beta
        self._gamma = _gamma
        self.n = len(self.G.nodes)
        # randomly initiate a configuration
        self.sigma = [1 for i in range(self.n)]
        nodes = list(self.G)
        random.Random().shuffle(nodes)
        self.k = k
        for node_state in range(k):
            for i in range(self.n // k):
                self.sigma[nodes[i * k + node_state]] = node_state
        # node state is 0, 1, \dots, k-1
        self.m = [self.n / k for i in range(k)] # each number of w^s
        self.mixed_param = _gamma * np.log(self.n)
        self.mixed_param /= self.n
    def get_dH(self, trial_location, w_s):
        _sum = 0
        sigma_r = self.sigma[trial_location]
        w_s_sigma_r = (w_s + sigma_r) % self.k
        for i in self.G[trial_location]:
            if sigma_r == self.sigma[i]:
                _sum += 1
            elif w_s_sigma_r == self.sigma[i]:
                _sum -= 1
        _sum *= (1 + self.mixed_param)
        _sum += self.mixed_param * (self.m[w_s_sigma_r] - self.m[sigma_r] + 1)
        return _sum
    def _metropolis_single(self):
        # randomly select one position to inspect
        r = random.randint(0, self.n - 1)
         # randomly select one new flipping state to inspect
        w_s = random.randint(1, self.k - 1)
        delta_H = self.get_dH(r, w_s)
        if delta_H < 0:  # lower energy: flip for sure
            self.m[self.sigma[r]] -= 1
            self.sigma[r] = (w_s + self.sigma[r]) % self.k
            self.m[self.sigma[r]] += 1
        else:  # Higher energy: flip sometimes
            probability = np.exp(-1.0 * self._beta * delta_H)
            if np.random.rand() < probability:
                self.m[self.sigma[r]] -= 1
                self.sigma[r] = (w_s + self.sigma[r]) % self.k
                self.m[self.sigma[r]] += 1
    def metropolis(self, N=40):
        # iterate given rounds
        for _ in range(N):
            for _ in range(self.n):
                self._metropolis_single()
        return self.sigma


def _estimate_a_b(graph, k=2):
    '''for multiple communities
    '''
    n = len(graph.nodes)
    e = len(graph.edges)
    t = 0
    for _, v in nx.algorithms.cluster.triangles(graph).items():
        t += v
    t /= 3
    eq_1 = e / (n * np.log(n))
    eq_2 = t / (np.log(n) ** 3)
    # solve b first
    coeff_3 = -1 * (k - 1)
    coeff_2 = 6 * (k - 1) * eq_1
    coeff_1 = -12 * (k - 1) * (eq_1 ** 2)
    coeff_0 = 8 * k * (eq_1 ** 3) - 6 * eq_2
    coeff = [coeff_3, coeff_2, coeff_1, coeff_0]
    b = -1
    for r in np.roots(coeff):
        if abs(np.imag(r)) < 1e-10:
            b = np.real(r)
            break
    a = 2 * k * eq_1 - (k - 1) * b
    if b < 0 or b > a:
        raise ValueError('')
    return (a, b)

def SIBM(graph, k=2, max_iter=40, gamma=None, beta=None):
    if beta is None:
        try:
            a, b = _estimate_a_b(graph, k)
        except ValueError:
            a, b = k, k
        square_term = (a + b - k) ** 2 - 4 * a * b
        if square_term > 0:
            _beta_star = np.log((a + b - k - np.sqrt(square_term))/ (2 * b))
            beta = 1.2 * _beta_star
        else:
            beta = 1.2
    if gamma is None:
        gamma = 6 * b

    if k == 2:
        sibm = SIBM2(graph, beta, gamma)
    else:
        sibm = SIBMk(graph, beta, gamma, k)
    return sibm.metropolis(N=max_iter)
