import sys
import time

from .bars import ExtendedBarServer
from .cases import ExtendedCaseServer
from .materials import ExtendedMaterialServer
from .nodes import ExtendedNodeServer
from .sections import ExtendedSectionServer
from .selections import ExtendedSelectionFactory
from .supports import ExtendedSupportServer
from .releases import ExtendedReleaseServer

from .constants import (
    RLicense,
    RLicenseStatus,
    RQuitOpt,
)

from .synonyms import synonyms

from .errors import (
    AutoRobotLicenseError,
    AutoRobotProjError,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    RobotApplication,
)

from . import geometry

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
    """
    def __init__(self, visible=True, interactive=True):
        """Constructor method."""
        self.app = RobotApplication()
        if not self.has_license:
            self.quit(save=False)
            raise AutoRobotLicenseError()
        if visible:
            self.show(interactive)
        else:
            self.hide()

    @property
    def bars(self):
        """
        Gets the current project's bar server as an instance of
        :py:class:`.ExtendedBarServer`.
        """
        return ExtendedBarServer(self.app.Project.Structure.Bars, self)

    @property
    def cases(self):
        """
        Gets the current project's case server as an instance of
        :py:class:`.ExtendedCaseServer`.
        """
        return ExtendedCaseServer(self.app.Project.Structure.Cases, self)

    @property
    def geom(self):
        """
        Provides a handle to geometry functions defined in the ``geometry``
        sub-module.
        """
        return geometry

    @property
    def materials(self):
        """
        Gets the material label server as an instance of
        :py:class:`.ExtendedMaterialServer`.
        """
        return ExtendedMaterialServer(self.app.Project.Structure.Labels, self)

    @property
    def sections(self):
        """
        Gets the section label server as an instance of
        :py:class:`.ExtendedSectionServer`.
        """
        return ExtendedSectionServer(self.app.Project.Structure.Labels, self)

    @property
    def supports(self):
        """
        Gets the supports label server as an instance of
        :py:class:`.ExtendedSupportServer`.
        """
        return ExtendedSupportServer(self.app.Project.Structure.Labels, self)

    @property
    def releases(self):
        """
        Gets the releases label server as an instance of
        :py:class:`.ExtendedReleaseServer`.
        """
        return ExtendedReleaseServer(self.app.Project.Structure.Labels, self)

    @property
    def nodes(self):
        """
        Gets the current project's node server as an instance of
        :py:class:`.ExtendedNodeServer`.
        """
        return ExtendedNodeServer(self.app.Project.Structure.Nodes, self)

    @property
    def selections(self):
        """
        Gets the project's selection factory as an instance of
        :py:class:`.ExtendedSelectionFactory`.
        """
        return ExtendedSelectionFactory(self.app.Project.Structure.Selections)

    @property
    def structure(self):
        """
        Gets the current structure as an instance of ``IRobotStructure``.
        """
        return self.app.Project.Structure

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
            self.app.Project.New(synonyms[proj_type])
        except Exception:
            raise AutoRobotProjError(
                f"Couldn't create new project with '{proj_type}'."
            )

    def open(self, path):
        """Opens a file with given path (assuming rtd format)."""
        self.app.Project.Open(str(path))

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

        del self.app
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
        self.app.Visible = True
        self.app.Interactive = interactive

    def hide(self):
        """Hides the ``RobotApplication``."""
        self.app.Visible = False
        self.app.Interactive = False

    def __getattr__(self, name):
        if hasattr(self.app, name):
            return getattr(self.app, name)
        raise AttributeError(
            f"{self.__class__.__name__} has not attribute '{name}'.")


def initialize(visible=True, interactive=True):
    """Initialize a ``RobotApplication`` object.

    :param bool visible: Whether the application window is displayed
    :param bool interactive: Whether the application window is displayed

    .. note::

       A reference to the ``RobotApplication`` is stored in
       :py:data:`autorobot.app.app`.
    """
    _this.app = ExtendedRobotApp(visible, interactive)
    return _this.app
