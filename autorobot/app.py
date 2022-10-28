import sys
import time

from .bars import ExtendedBarServer
from .cases import ExtendedCaseServer
from .materials import ExtendedMaterialServer
from .nodes import ExtendedNodeServer
from .sections import ExtendedSectionServer
from .supports import ExtendedSupportServer
from .releases import ExtendedReleaseServer
from .resolve import ExtendedCalcEngine

from .constants import (
    RLicense,
    RLicenseStatus,
    RQuitOpt,
)

from .synonyms import synonyms

from .errors import (
    AutoRobotLicenseError,
    AutoRobotProjError,
    AutoRobotValueError,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    RobotApplication,
    IRDimServer,
    IRDimServerMode,
)

# Get a reference to the module instance
_this = sys.modules[__name__]

#: A reference to the current ``RobotApplication`` instance
app = None


class ExtendedRobotApp:
    """This class encapsulates and extends ``RobotApplication``.

    The attributes and methods of the underlying ``RobotApplication`` object
    can be accessed directly through an instance of this class

    :param bool visible:
       Whether the new ``RobotApplication`` is visible (default: ``True``)
    :param bool interactive:
       Whether the new ``RobotApplication`` is interactive (default: ``True``)
    :param float unit_length: The unit for length in meters (e.g. 1e3 is km)
    :param float unit_force: The unit for force in newtons (e.g. 1e3 is kN)
    :param float unit_mass: The unit for mass in kilograms (e.g. 1e3 is t)
    :param float unit_angle_in:
       The unit for angle input in radians (e.g. π / 180 is degrees)
    :param float unit_angle_out:
       The unit for angle output in radians (e.g. π / 180 is degrees)
    :param float unit_section:
       The unit for section dimensions in meters (e.g. 1e-3 is mm)
    """
    def __init__(self, visible=True, interactive=True, unit_length=1.,
        unit_force=1., unit_mass=1., unit_angle_in=1., unit_angle_out=1.,
        unit_section=1.):
        """Constructor method."""
        if unit_angle_out != 1.:
            raise AutoRobotValueError(
                'unit_angle_out is not implemented.'
            )
        self._app = RobotApplication()
        if not self.has_license:
            self.quit(save=False)
            raise AutoRobotLicenseError()
        if visible:
            self.show(interactive)
        else:
            self.hide()

        (
            self.unit_length,
            self.unit_force,
            self.unit_mass,
            self.unit_angle_in,
            self.unit_angle_out,
            self.unit_section
        ) = (
            unit_length, unit_force, unit_mass, unit_angle_in, unit_angle_out,
            unit_section
        )

    @property
    def bars(self):
        """
        Gets the current project's bar server as an instance of
        :py:class:`.ExtendedBarServer`.
        """
        return ExtendedBarServer(self.Project.Structure.Bars)

    @property
    def cases(self):
        """
        Gets the current project's case server as an instance of
        :py:class:`.ExtendedCaseServer`.
        """
        return ExtendedCaseServer(self.Project.Structure.Cases)

    @property
    def materials(self):
        """
        Gets the material label server as an instance of
        :py:class:`.ExtendedMaterialServer`.
        """
        return ExtendedMaterialServer(self.Project.Structure.Labels)

    @property
    def sections(self):
        """
        Gets the section label server as an instance of
        :py:class:`.ExtendedSectionServer`.
        """
        return ExtendedSectionServer(self.Project.Structure.Labels)

    @property
    def supports(self):
        """
        Gets the supports label server as an instance of
        :py:class:`.ExtendedSupportServer`.
        """
        return ExtendedSupportServer(self.Project.Structure.Labels)

    @property
    def releases(self):
        """
        Gets the releases label server as an instance of
        :py:class:`.ExtendedReleaseServer`.
        """
        return ExtendedReleaseServer(self.Project.Structure.Labels)

    @property
    def nodes(self):
        """
        Gets the current project's node server as an instance of
        :py:class:`.ExtendedNodeServer`.
        """
        return ExtendedNodeServer(self.Project.Structure.Nodes)

    @property
    def selections(self):
        """
        Gets the project's selection factory as an instance of
        ``IRobotSelectionFactory``.
        """
        return self.Project.Structure.Selections

    @property
    def structure(self):
        """
        Gets the current structure as an instance of ``IRobotStructure``.
        """
        return self.Project.Structure

    @property
    def calc_engine(self):
        """Gets the project's calculation engine as an instance of
        :py:class:`.ExtendedCalcEngine`.
        """
        return ExtendedCalcEngine(self.Project.CalcEngine)

    @property
    def steel_design(self):
        """Gets the steel member design server"""
        server = IRDimServer(self.Kernel.GetExtension('RDimServer'))
        server.Mode = IRDimServerMode.I_DSM_STEEL
        return server

    @property
    def has_license(self):
        """
        Returns *True* if the license was activated, *False* otherwise.
        """
        return any((self.LicenseCheckEntitlement(lic) == RLicenseStatus.OK
                    for lic in RLicense))

    def close(self):
        """Closes the project."""
        self.Project.Close()

    def new(self, proj_type):
        """Creates a new project.

        :param int proj_type:
          The type of project to be created.For more detail, see
          :py:class:`autorobot.RProjType`.

        .. tip:: This method supports :ref:`about_synonyms` for the
          **proj_type** arguments. For example: ::

                app.new('SHELL')
        """
        try:
            self.Project.New(synonyms[proj_type])
        except Exception:
            raise AutoRobotProjError(
                f"Couldn't create new project with '{proj_type}'."
            )

    def open(self, path):
        """Opens a file with given path (assuming rtd format)."""
        self.Project.Open(str(path))

    def quit(self, save=None):
        """Quits the RobotApplication.

        :param bool save: Whether to:

           * save the opened file (``True``)
           * discard changes (``False``)
           * prompt the user (``None``)
        """
        if save is None:
            self.Quit(RQuitOpt.PROMPT)
        elif save:
            self.Quit(RQuitOpt.SAVE)
        else:
            self.Quit(RQuitOpt.DISCARD)

        del self._app
        _this.app = None
        # Now wait a second to avoid file permission issues
        time.sleep(1)

    def save(self):
        """Saves the project if the file name is known.

        :return:
           ``True`` if the save command was executed, ``False`` otherwise
        """
        if self.Project.FileName:
            return self.Project.Save() or True
        return False

    def save_as(self, path):
        """Saves the project to path. The file format is rtd."""
        self.Project.SaveAs(str(path))

    def show(self, interactive=True):
        """Makes the ``RobotApplication`` visible.

        :param bool interactive:
           Whether the ``RobotApplication`` is interactive (default: ``True``)
        """
        self._app.Visible = True
        self._app.Interactive = interactive

    def hide(self):
        """Hides the ``RobotApplication``."""
        self._app.Visible = False
        self._app.Interactive = False

    def __getattr__(self, name):
        if name != '_app' and hasattr(self._app, name):
            return getattr(self._app, name)
        raise AttributeError(
            f"{self.__class__.__name__} has not attribute '{name}'.")


def initialize(visible=True, interactive=True, unit_length=1., unit_force=1.,
    unit_mass=1., unit_angle_in=1., unit_angle_out=1., unit_section=1.):
    """Initialize a ``RobotApplication`` object.

    :param bool visible: Whether the application window is displayed
    :param bool interactive: Whether the application window is displayed
    :param float unit_length: The unit for length in meters (e.g. 1e3 is km)
    :param float unit_force: The unit for force in newtons (e.g. 1e3 is kN)
    :param float unit_mass: The unit for mass in kilograms (e.g. 1e3 is t)
    :param float unit_angle_in:
       The unit for angle input in radians (e.g. π / 180 is degrees)
    :param float unit_angle_out:
       The unit for angle output in radians (e.g. π / 180 is degrees)
    :param float unit_section:
       The unit for section dimensions in meters (e.g. 1e-3 is mm)

    .. note::

       A reference to the ``RobotApplication`` is stored in
       :py:data:`autorobot.app.app`.
    """
    units = (
        unit_length, unit_force, unit_mass, unit_angle_in, unit_angle_out,
        unit_section
    )
    _this.app = ExtendedRobotApp(visible, interactive, *units)
    return _this.app


def get_app():
    """Returns the current *ExtendedRobotApp* instance.
    """
    return _this.app
