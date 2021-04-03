import turicreate as tc

def concat_sframes(list_of_sframes: tc.SFrame):
    sf_all = list_of_sframes[0]
    for sf in list_of_sframes[1:]:
        sf_all = sf_all.append(sf)
    return sf_all


__all__ = ['concat_sframes']
