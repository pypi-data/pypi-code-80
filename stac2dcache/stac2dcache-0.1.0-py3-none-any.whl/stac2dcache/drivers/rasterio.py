import rasterio
import rioxarray
import tempfile

from .base import Driver


class RasterioDriver(Driver):
    """ Driver to read raster data """
    def get(self, **kwargs):
        """
        Load the raster data in a rasterio-xarray DataArray object

        :param kwargs: (optional) arguments to be passed to open_rasterio
        :return :class:`~rioxarray.core.dataarray.DataArray`
        """
        gdal_config_options = {"GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR"}

        client_kwargs = getattr(self.filesystem, "client_kwargs", None)
        auth = None if not client_kwargs else client_kwargs.get("auth")
        if auth is not None:
            gdal_config_options['GDAL_HTTP_AUTH'] = 'BASIC'
            gdal_config_options['GDAL_HTTP_USERPWD'] = '{}:{}'.format(
                auth.login,
                auth.password
            )

        headers = None if not client_kwargs else client_kwargs.get("headers")
        if headers is not None:
            headers_text = '\n'.join([f'{key}: {value}'
                                      for key, value in headers.items()])
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(headers_text)
                gdal_config_options['GDAL_HTTP_HEADER_FILE'] = f.name

        with rasterio.Env(**gdal_config_options):
            data_array = rioxarray.open_rasterio(self.uri, **kwargs)
        return data_array
