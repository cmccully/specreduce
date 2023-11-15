"""Tests for wavelength calibration using different wavelength calibration
models.
"""
from typing import Any, Callable, Union

from astropy.modeling import models, Model
from astropy.wcs import WCS
from specreduce.utils.synth_data import make_2d_arc_image
from specreduce.wavelength_calibration import WavelengthCalibrator
from specutils import SpectrumCollection, SpectrumList
import numpy as np
import pytest



# @pytest.mark.skip(reason="We don't test external algorithms by default")
@pytest.mark.external_algorithm
def test_wavecal():
    # Generate some fake data
    # input_tilt_model = models.Polynomial1D(degree=2, c0=0., c1=10., c2=30.)
    data, real_wcs = generate_arc()
    # Generate the extras the code needs
    # Run the WaveCal object
    calibrator = WavelengthCalibrator()
    # extras = {'input_model': models.Polynomial1D(degree=2, c0=0., c1=10., c2=30.)}
    extras = {'real_wcs': real_wcs}
    calibrated_spectrum: Union(SpectrumCollection, SpectrumList) = calibrator(data, extras)
    # Do some kind of QA on the output
    assert calibrator.success is True
    grid = np.meshgrid(*list(np.arange(length) for length in reversed(calibrated_spectrum.shape)),
                       indexing='xy')
    # expected_wavelengths = real_wcs(grid[0] + input_tilt_model(grid[1]))
    expected_wavelengths = real_wcs.pixel_to_world(*grid)
    np.testing.assert_allclose(calibrated_spectrum.wcs.pixel_to_world(*grid), expected_wavelengths)


def generate_arc():  # input_tilt_model: Model):

    real_wcs_header = {
        'CTYPE1': 'AWAV-GRA',  # Grating dispersion function with air wavelengths
        'CUNIT1': 'Angstrom',  # Dispersion units
        'CRPIX1': 719.8,       # Reference pixel [pix]
        'CRVAL1': 5500.0,      # Reference value [Angstrom]
        'CDELT1': 3.418,       # Linear dispersion [Angstrom/pix]
        'PV1_0': 5.0e5,        # Grating density [1/m]
        'PV1_1': 1,            # Diffraction order
        'PV1_2': 30.0,         # Incident angle [deg]
        'PV1_3': 1.765,        # Reference refraction
        'PV1_4': -1.077e6,     # Refraction derivative [1/m]
        'CTYPE2': 'PIXEL',     # Spatial detector coordinates
        'CUNIT2': 'pix',       # Spatial units
        'CRPIX2': 1,           # Reference pixel
        'CRVAL2': 0,           # Reference value
        'CDELT2': 1            # Spatial units per pixel
    }
    real_wcs = WCS(real_wcs_header)

    approx_wcs_header = {
        'CTYPE1': 'AWAV',
        'CUNIT1': 'Angstrom',
        'CRPIX1': 650.0,       # Reference pixel [pix]
        'CRVAL1': 5500.0,      # Reference value [Angstrom]
        'CDELT1': 3.07,        # Linear dispersion [Angstrom/pix]
        'CTYPE2': 'PIXEL',     # Spatial detector coordinates
        'CUNIT2': 'pix',       # Spatial units
        'CRPIX2': 1,           # Reference pixel
        'CRVAL2': 0,           # Reference value
        'CDELT2': 1            # Spatial units per pixel
    }
    approx_wcs = WCS(approx_wcs_header)

    ccd_im = make_2d_arc_image(
        1024, 512,
        wcs=real_wcs,
        line_fwhm=5.,
        linelists=['ArII',],
        # TODO: Currently the tilt_model doesn't work
        # tilt_func=input_tilt_model,
        add_noise=True
    )
    ccd_im.wcs = approx_wcs

    return ccd_im, real_wcs
