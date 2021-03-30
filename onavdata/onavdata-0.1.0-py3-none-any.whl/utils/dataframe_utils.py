import numpy as np
mm_to_m = 1e-3


def get_columns(df, startswith_str):
    """
    Returns list of columns in data-frame `df` which begin with the
    `startswith_str` string.  The list is sorted prior to return.  This ensures
    the return order will be X->Y->Z for 3-axis sensors.
    """
    cols = [col for col in df if col.startswith(startswith_str)]
    cols.sort()
    return cols


def get_accel_cols(df, startswith_str='Accel', verbose=False):
    cols = get_columns(df, startswith_str)
    if verbose:
        print('Accel Columns Found:\n\t'+'\t'.join(['%s' % c for c in cols]))
    return cols


def get_gyro_cols(df, startswith_str='AngleRate', verbose=False):
    cols = get_columns(df, startswith_str)
    if verbose:
        print('Gyro Columns Found:\n\t'+'\t'.join(['%s' % c for c in cols]))
    return cols


def get_mag_cols(df, startswith_str='MagField', verbose=False):
    cols = get_columns(df, startswith_str)
    if verbose:
        print('Mag Columns Found:\n\t'+'\t'.join(['%s' % c for c in cols]))
    return cols


def convert_deg2rad(df, inplace=False):
    """ Convert any column units from (deg*) to (rad*)
    (e.g. Euler angles and/or gyro measurements)
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    for col in df_out.columns:
        if '(deg' in col:
            print("Converting '%s' readings from (deg*) to (rad*)." % col)
            df_out[col] = np.deg2rad(df_out[col])
            df_out.rename(columns={col: col.replace('(deg', '(rad')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def convert_mm2m(df, inplace=False):
    """ Convert any column units from (mm*) to (m*)
    (e.g. Height in (mm) and/or speed (mm/s) measurements)
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    for col in df_out.columns:
        if '(mm' in col:
            print("Converting '%s' readings from (mm*) to (m*)." % col)
            df_out[col] = df_out[col] * mm_to_m
            df_out.rename(columns={col: col.replace('(mm', '(m')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def convert_mG2mps2(df, mG2mps2=9.80665e-3, inplace=False):
    """ Convert any accel columns from (mG) to (m/s^2).
    The accelerometer columns are retrieved using the `get_accel_cols`
    method.
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    cols_accel = get_accel_cols(df_out)
    for col in cols_accel:
        if '(mG)' in col:
            print("Converting '%s' readings from (mG) to (m/s^2)." % col)
            df_out[col] = mG2mps2*df_out[col]
            df_out.rename(columns={col: col.replace('(mG)', '(m/s^2)')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out
