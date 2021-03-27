import numpy as np


def perturb(data, pmean, pstd, prem):
    """Perturb the data"""
    # Perturb data
    data *= np.random.normal(pmean, pstd, data.shape)

    # Choose certain ratio of the data by random to illustrate loss of data
    data *= np.random.choice([np.nan, 1], size=(data.shape), p=[prem, 1 - prem])

    return data


def splitData(data, fraction_train=2 / 3, type_split="time"):
    """Split data into seen (training set) and unseen (test set) data"""
    # Get a list of data indices
    nonnans = np.argwhere(~np.isnan(data))
    index = np.arange(len(nonnans))

    # Copy original data structure to not mutate it
    train = data.copy()
    test = data.copy()

    # Specify which type of split we want
    # Split randomly over all datapoints
    if type_split == "random":
        # Shuffle the data in a random order
        np.random.shuffle(index)

        # Make division of data
        div = int(np.floor(len(index) * fraction_train))
        test_nan = index[:div]
        train_nan = index[div:]

        # Rebuild data into the two sets
        for i in train_nan:
            ti = nonnans[i]
            train[ti[0]][ti[1]] = np.nan
        for i in test_nan:
            ti = nonnans[i]
            test[ti[0]][ti[1]] = np.nan

    # Split over a section in time
    elif type_split == "time":
        # Make division of data
        div = int(np.floor(len(index) * fraction_train))
        test_nan = index[:div]
        train_nan = index[div:]

        # Rebuild data into the two sets
        for i in train_nan:
            ti = nonnans[i]
            train[ti[0]][ti[1]] = np.nan
        for i in test_nan:
            ti = nonnans[i]
            test[ti[0]][ti[1]] = np.nan

    return train, test


def hpd_grid(sample, alpha=0.05, roundto=2):
    """Calculate highest posterior density (HPD) of array for given alpha.
    The HPD is the minimum width Bayesian credible interval (BCI).
    The function works for multimodal distributions, returning more than one mode

    Parameters
    ----------

    sample : Numpy array or python list
        An array containing MCMC samples
    alpha : float
        Desired probability of type I error (defaults to 0.05)
    roundto: integer
        Number of digits after the decimal point for the results

    Returns
    ----------
    hpd: array with the lower

    """
    sample = np.asarray(sample)
    sample = sample[~np.isnan(sample)]
    # get upper and lower bounds
    l = np.min(sample)
    u = np.max(sample)
    density = kde.gaussian_kde(sample)
    x = np.linspace(l, u, 2000)
    y = density.evaluate(x)
    # y = density.evaluate(x, l, u) waitting for PR to be accepted
    xy_zipped = zip(x, y / np.sum(y))
    xy = sorted(xy_zipped, key=lambda x: x[1], reverse=True)
    xy_cum_sum = 0
    hdv = []
    for val in xy:
        xy_cum_sum += val[1]
        hdv.append(val[0])
        if xy_cum_sum >= (1 - alpha):
            break
    hdv.sort()
    diff = (u - l) / 20  # differences of 5%
    hpd = []
    hpd.append(round(min(hdv), roundto))
    for i in range(1, len(hdv)):
        if hdv[i] - hdv[i - 1] >= diff:
            hpd.append(round(hdv[i - 1], roundto))
            hpd.append(round(hdv[i], roundto))
    hpd.append(round(max(hdv), roundto))
    ite = iter(hpd)
    hpd = list(zip(ite, ite))
    modes = []
    for value in hpd:
        x_hpd = x[(x > value[0]) & (x < value[1])]
        y_hpd = y[(x > value[0]) & (x < value[1])]
        modes.append(round(x_hpd[np.argmax(y_hpd)], roundto))
    return hpd, x, y, modes
