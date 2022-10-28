from .constants import (
    RCalcMode,
    RCalcStatus,
)

from .extensions import Capsule

from .robotom import RobotOM
from RobotOM import (
    IRobotCalcEngine,
)


class ExtendedCalcEngine(Capsule):

    _otype = IRobotCalcEngine

    def calculate(self, ignore_warnings=True, mode=RCalcMode.LOCAL):
        """Calculates the structure.

        :param bool ignore_warnings: Whether to ignore warning messages
        """
        prev_warnings = self._app.calc_engine.AnalysisParams.IgnoreWarnings
        self._app.calc_engine.AnalysisParams.IgnoreWarnings = ignore_warnings
        res = self.CalculateEx(mode)
        self._app.calc_engine.AnalysisParams.IgnoreWarnings = prev_warnings
