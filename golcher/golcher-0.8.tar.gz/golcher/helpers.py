import numpy as np
import scipy.special as misc
from collections import Counter
from itertools import permutations


def get_condition_map(full_A, branching_factor, shuffle):
    """
    Create a Conditional Map.
    Given the predecessor letter as a key, the map will return allowed next letters.
    It could be used for generating text with short range dependencies
    as well as independent random texts(when branching_factor = len(full_A))

    :param full_A: An Alphabet
    :param branching_factor: Number of letters allowed after given letter
    :param shuffle: Should we shuffle the alphabet before giving the first N=branching_factor letters as allowed successors
    :return: the Condition Map dictionary
    """
    condition_map = {}
    full_A_copy = full_A[:]
    for a in full_A:
        if shuffle:
            np.random.shuffle(full_A_copy)
        A = full_A_copy[:branching_factor]
        condition_map[a] = A
    return condition_map


def get_uniform_distribution(size):
    """
    :param size: size == |Alphabet|
    :return: uniform distributed probabilities of letters in an Alphabet
    """
    probs = np.ones(size)
    return probs / sum(probs)


def get_power_distribution(size, pow=3):
    """
    :param size: size == |Alphabet|
    :pow pow: the power of X
    :return: power distributed probabilities of letters in an Alphabet. A normalized [1,2,...,size]^pow
    """
    probs = np.arange(1, size + 1) ** pow
    return probs / sum(probs)


def get_expon_distribution(size):
    """
    :param size: size == |Alphabet|
    :return: exponential distributed probabilities of letters in an Alphabet. A normalized e^[1,2,...,size]
    """
    probs = np.exp(-np.arange(1, size + 1))
    return probs / sum(probs)


def distrib_info(p):
    """
    Get base information about given distribution p
    :param p: probabilities
    :return: a dictionary with following keys: 'geo_mean', 'mean', 'min', 'max', 'entropy'
    """
    return {
        'geo_mean': np.exp(np.mean(np.log(p))),
        'mean': np.mean(p),
        'min': np.min(p),
        'max': np.max(p),
        'entropy': -np.sum(p * np.log(p))
    }


def generate_conditional_text(condition_map, probs, N, start="a"):
    """
    Generate a text given the condition_map, probabilities of next letters, size=N and the starting letter.
    Note
    If the condition_map was generated with `shuffle=True' the same probs will be assigned to different letters depending
    the predecessor.
    This trick help creates texts that has large alphabet size but behave like texts with
    `smaller Alphabet size == branching_factor`
    :param condition_map: condition_map obtained from `~helpers.get_condition_map()`
    :param probs: list of probabilities for the next letters returned by condition_map
    :param N: size of the text
    :param start: start letters
    :return: generated text
    """
    res = []
    for i in range(N):
        A = condition_map[start]
        res.append(np.random.choice(A, p=probs))
        start = res[-1]
    conditional_text = "".join(res)
    return conditional_text


def all_probs_count(len_A, n):
    """
    Count how many different n-grams (for n=n) possible given Alphabet size = len_A
    """
    return len_A ** n


def count_uniq_positions(len_A, n):
    """
    Count how many unique pos n-grams occupy, given Alphabet size = len_A
    """
    r = len_A - 1
    return misc.comb(r + n, r)


def ngram_to_points(ngram, A, log=False):
    """
      Convert ngram like aab to steps. For example
      A = {a:0.2, b:0.3, c:0.5}
      steps = [0.2, 0.2*0.3, 0.2*0.3+0.5]
      Or if log=True
      steps = [log(0.2), log(0.2)+log(0.3), log(0.2)+log(0.3)+log(0.5)]

    :param ngram: n-gram
    :param A: a dictionary like {letter: probability}
    :param log: should returns probabilities in log scale
    :return: steps
    """
    if log:
        return np.cumsum([0] + [np.log(A[a]) for a in ngram])
    else:
        return np.cumprod([1] + [A[a] for a in ngram])


def get_all_points_new(ngram, A, log=False):
    """
    List all possible path of ngram permutations
    :param ngram: ngram
    :param A: dict {letter: probability}
    :param log: steps in logarithmic scale
    :return: numpy array of all possible steps of single ngram
    """
    return np.asarray([ngram_to_points(ngram, A, log=log) for ngram in permutations(ngram)])


def count_ngrams(text, n):
    """
    :param text: text
    :param n: n of n-gram
    :return: Counter objects for n-grams in the text
    """
    ngrams = [text[i:i + n] for i in range(len(text) - n)]
    return Counter(ngrams)


def analyze_V_grows(text, to_n=10):
    """
    Analyse how a dictionary of unique n-grams grows with n grows
    :param text:
    :param to_n: max n
    :return: generator of len(Vocabulary of n-grams)
    """
    for n in range(to_n):
        yield len(count_ngrams(text, n))


def range_ngram_distrib(text, n, top_most=-1):
    """
    List n-grams with theis probabilities from the most popular to the smaller ones
    :param text: text
    :param n: n of n-gram
    :param top_most: count of most popular n-grams to be returned, or -1 to return all
    :return: list of ngrams, list of probs
    """
    ngram_counts = count_ngrams(text, n)
    if top_most >= 0:
        ngrams = np.asarray(ngram_counts.most_common(top_most))[:, 0]
        counts = np.asarray(np.asarray(ngram_counts.most_common(top_most))[:, 1], dtype=int)
    else:
        ngrams = np.asarray(ngram_counts.most_common())[:, 0]
        counts = np.asarray(np.asarray(ngram_counts.most_common())[:, 1], dtype=int)
    return ngrams, counts


def get_ngram_probs(text, n):
    """
    :param text: text
    :param n: n of n-gram
    :return: n-grams, n-gram relative frequencies
    """
    ngrams, counts = range_ngram_distrib(text, n=n)
    total = sum(counts)
    probs = counts / total
    return ngrams, probs


def show_ocupation(text, n, ax):
    """
    Show n-gram probabilities as points
    :param text: text
    :param n: n of n-gram
    :param ax: axes of matplotlib
    :return:
    """
    _, probs = get_ngram_probs(text, n)
    ax.scatter(probs, np.zeros_like(probs))


def get_points(p, n_max):
    """
    Returns ranked probabilities of ngram for n up to n_max given distribution p
    """
    xs = []
    xs.extend(p)
    x = p
    for n in range(1, n_max):
        x = x[None].T @ p[None]
        xs.extend(x.flatten())

    xs = sorted(xs, reverse=True)
    return xs


def get_probability_map(text, n):
    """
    Create n-gram probability dictionary based on the text
    :param text: target text
    :param n: n of n-gram
    :return: dictionary {n-gram: probability}
    """
    counter = count_ngrams(text, n)
    total = np.sum(list(counter.values()))
    return {gram: c / total for gram, c in list(dict(counter).items())}

#http://normal-extensions.com/2013/08/04/entropy-for-n-grams/
#https://drive.google.com/file/d/1v8GEMzLlwAiFxXczlstYzKt4r7NxmKyq/view?usp=sharing
def entropy(text, n=1):
    """
    Get probability distribution of n-grams and count it's Shanon entropy
    :param text: text
    :param n: n of n-grams
    :return: entropy of the text
    """
    prob_map = get_probability_map(text, n)
    probs = np.asarray(list(prob_map.values()))
    return -np.sum(probs * np.log(probs))


def cond_entropy(text, n):
    """
    Compute conditional entropy.
    Given an predecessor (n-1)-gram get conditional probability of the successor letter and compute it's entropy
    :param text: text
    :param n: n of n-gram
    :return: conditional entropy value
    """
    long_map = get_probability_map(text, n)
    short_map = get_probability_map(text, n - 1)
    return -np.sum([long_map[gram] * np.log(long_map[gram] / short_map[gram[:-1]]) for gram in long_map])
