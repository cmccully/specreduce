"""Template test class from which all [x]TestCase classes are derived.

NOTE: The below is keeping track of specific ideas, it should eventually go
into relevant docstrings in TestCase.

It outlines the form of a TestCase, which has the following structure:
    + TestCase.input_data = input data structure for the test case.
    + TestCase.output_data = output data structure for the test case.
    + TestCase.expected_output
    + TestCase.test_model = an abstract method that calls the relevant test callable.
"""
from abc import ABC, abstractmethod
from typing import Any, Callable, Union


class TestCase(ABC):
    """Abstract class for specreduce model/component testing suite."""
    # TODO: These are just placeholders, I'm not sure if these should be a
    # dataclass, named tuple (defined on a per-case basis, since different
    # tests require different i/o), or something else.
    input_data = None
    output_data = None
    test_result = None
    expected_output = None

    # @property
    # @abstractmethod
    # def input_data():
    #     raise NotImplementedError("Abstract attr/property")

    # @property
    # @abstractmethod
    # def test_result():
    #     raise NotImplementedError("Abstract attr/property")

    # @property
    # @abstractmethod
    # def expected_output():
    #     raise NotImplementedError("Abstract attr/property")

    # @property
    # @abstractmethod
    # def output_data():
    #     raise NotImplementedError("Abstract attr/property")

    def __call__(self, model, **kwargs):
        output = self.test_model(model, **kwargs)

    @abstractmethod
    def validate_output(self, output):
        """Validate the output against some stored expected output."""
        raise NotImplementedError("AbstractMethod")

    @abstractmethod
    def test_model(
        self,
        model: Callable,
        *,
        extras: Union[dict, None] = None,
    ):
        """Abstract method for the model testing functionality. It passes
        inputs to the model, and stores outputs (relevant to the derived
        TestCase object) in relevant places.

        Of the outputs, it is recommmended that TestCase.test_result be used in
        every derivative of this class.

        Arguments
        ---------
        model : Callable
            The model to be called. It should take the expected arguments
            (described in the derived class) as keyword arguments.

        extras : dict or None
            Extra arguments to be passed to the calibration function. This
            method accepts dicts or None, but the value passed to the model
            should *always* be a dict.

            E.g., if extras is None, [x]TestCase should convert it to an empty
            dictionary:
                >> if extras is None:
                >>     extras = {}
        """
        # TODO: Just filler code. This never gets run, but I usually raise
        # something just in case something truly remarkable happens.
        raise NotImplementedError("Abstract method")



class WaveCalTestCase(TestCase):
    """Tests a model meant to perform a wavelength calibration."""

    def __init__(self):
        """Initializes the WaveCalTestCase instance. This should collect
        relevant testing data (or the means with which to access it) into the
        class upon instantiation.

        Arguments
        ---------
        TODO: if needed
        """
        # TODO: These are just outlining the parameters we discussed yesterday.
        # Currently, a lot of this is in test_wavecal() below this class.
        mask = None
        flux = None
        uncertainties = None
        known_wavelengths = None

    def validate_output(self, output: Any):
        raise NotImplementedError

    def test_model(self, model: Callable, *, extras: Union[dict, None] = None):
        """This tests a wavelength calibration callable from the expected
        inputs, outputs, and test results.

        Arguments
        ---------
        model : Callable
            The model to be executed. It must take the following keyword arguments:
                TODO:
                + [...]

        extras : dict or None, keyword-only
            Extra arguments to pass to the models. This may be a dict or None.
            Ideally, the number of extras passed this way is minimized (to more
            closely follow how specreduce expects the algorithm to work).

        Raises
        ------
        TODO: Does this test raise anything itself?

        Returns
        -------
        TODO: What exactly does this test return?
        """
        if extras is None:
            extras = {}

        # TODO: This is where I am imagining the bulk of test_wavecal from
        # test_wavelenght_calibration.py would go.
        raise NotImplementedError


@pytest.fixture
def wavecal_test_class():
    """Instantiate a new TestCase class, with fresh data, for each model test
    case.

    To use this fixture, you call it passing the model and any extras (a
    keyword-only argument):
        wavecal_test_class(model, extras=extras)
    """
    return WaveCalTestCase()
