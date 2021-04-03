def miax(minv, maxv, numv):
    try:
        if numv >= minv and numv <= maxv:
            return numv
        else:
            if minv > numv:
                return minv
            else:
                return maxv
    except Exception as err:
        return 0

