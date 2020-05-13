# autoRobot
Convenience functions to use Robot Structural Analysis API in CPython

**autoRobot** consists of a collection of functions to simplify the use of Robot SA API. The API is written for a .NET environment and can be accessed through the [pythonnet](https://github.com/pythonnet/pythonnet) module. As opposed to IronPyhton, pythonnet is based on pure CPython and allows access to scientific librairies like [numpy](https://github.com/numpy/numpy) and [scipy](https://github.com/scipy/scipy).

Scripts written to automate Robot can look austere when written directly with the API and the information they contain can be lost in a flurry of all-capital-twenty-letter words. **autorobot** provides convenience functions to shorten the syntax and adds functionalities to the software's internal servers. Taking advantage of CPython means that the code can be written in the form of [jupyter notebooks](https://github.com/jupyter/notebook) that offer a convenient interface for short code cells, diagrams and formatted text.

**autorobot** can be used for pre- and post-processing.
