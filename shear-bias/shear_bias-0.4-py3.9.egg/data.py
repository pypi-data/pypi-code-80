import os
import urllib.request
from shutil import move

def download_HST_images(dest_dir='data/HST'):
    """Download HST images from galsim repository
    
    Parameters
    ----------
    dest_dir: string, optional, default='data/HST'
        destination directory
    """

    url_1 = 'https://github.com/GalSim-developers/GalSim/raw/releases/2.0/examples/data'
    url_2 =  'https://github.com/GalSim-developers/GalSim/raw/releases/2.0/share'

    data_files = ['real_galaxy_catalog_23.5_example.fits',
                  'acs_I_unrot_sci_20_cf.fits',
                  'real_galaxy_images.fits',
                  'real_galaxy_PSF_images.fits']
    url = [url_1, url_2, url_1, url_1]


    if not os.path.exists(dest_dir):
        # TODO: Catch exception OSError if file exists, but is not dir
        os.makedirs(dest_dir)
        
    for u, d in zip(url, data_files):
        target = '{}/{}'.format(dest_dir, d)
        if os.path.isfile(target):
            print('Data file {} already exists, skipping...'.format(target))
        else:
            print('Downloading data file {}.'.format(target))
            urllib.request.urlretrieve('{}/{}'.format(u, d),
                                       '{}/{}'.format(dest_dir, d))
