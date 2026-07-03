"""GNS Animator4 Python batch-scripting API.

``gnspy`` is the compiled Python extension shipped with GNS Animator4. It exposes
the post-processor's model, results, presentation and view objects to Python so
that sessions can be driven programmatically, both interactively and in batch
(command-line) mode.

Notes
-----
Every script starts from a single global handle of type :class:`GNS`, reachable
as ``gnspy.gns`` (the name ``gnspy.a4`` refers to the same handle). From it you
obtain slot, presentation, view, image, video and variable handles, execute
Animator command-line commands via :meth:`GNS.executeCommand`, and run model or
curve scans. Handle objects are never constructed directly; they are returned by
the factory methods on :class:`GNS` and its relatives.

Entity, element, property and view selections are expressed with the bit-flag
enumerations defined in this module (for example :class:`Element`,
:class:`Property`, :class:`Item` and :class:`View`). Flags that the manual marks
as combinable may be OR-ed together with ``|``. Convenience module-level aliases
in ``UPPER_CASE`` (such as :data:`BAR` or :data:`PID_SHELL`) point at the
matching enum members.
"""

import enum
import typing

class Analysis(enum.IntEnum):
    """Analysis type reported for a result slot.

    Notes
    -----
    These values are mutually exclusive; they are never combined.
    """

    #: Analysis type is unknown or not set.
    Undefined = 0
    #: Transient (time-history) analysis.
    Transient = 1
    #: Static analysis.
    Static = 2
    #: Modal (eigenvalue) analysis.
    Modal = 3
    #: Frequency-response analysis.
    FrequencyResponse = 4

class ArrowPosition(enum.IntEnum):
    """Arrow-head placement along a presentation line.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Arrow head at the starting position.
    Start = 1
    #: Arrow head at the ending position.
    End = 2
    #: Arrow heads at both the starting and ending positions.
    StartAndEnd = 3

class BorderMode(enum.IntEnum):
    """Border-drawing mode for a presentation region.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Arc-shaped border.
    Arc = 0
    #: Straight segment border.
    Seg = 1

class Element(enum.IntFlag):
    """Element-type selection flags for model queries.

    Flags select which finite-element types a query returns. ``Shell`` and
    ``Solid`` are convenience combinations covering every shell or solid type,
    and ``All`` selects every element type.

    Notes
    -----
    Flags are bitwise-combinable with ``|``; refer to the individual method for
    the combinations it accepts.
    """

    #: SPH elements only.
    Sph = 1
    #: Bar elements only.
    Bar = 2
    #: Beam elements only.
    Beam = 4
    #: Spring elements only.
    Spring = 8
    #: Damper elements only.
    Damper = 16
    #: Joint elements only.
    Joint = 32
    #: Mass elements only.
    Mass = 64
    #: Nel (non-structural) elements only.
    Nel = 128
    #: Quad shell elements only.
    Quad = 256
    #: Tria shell elements only.
    Tria = 512
    #: All shell elements (Quad and Tria).
    Shell = 768
    #: Hexa solid elements only.
    Hexa = 1024
    #: Penta solid elements only.
    Penta = 2048
    #: Tetra solid elements only.
    Tetra = 4096
    #: Pyra solid elements only.
    Pyra = 8192
    #: All solid elements (Hexa, Penta, Tetra and Pyra).
    Solid = 15360
    #: Rigid (RBE) elements only.
    Rbe = 16384
    #: RBE2 elements only.
    Rbe2 = 32768
    #: RBE3 elements only.
    Rbe3 = 65536
    #: Connection elements only.
    Conn = 131072
    #: All element types (bitwise OR of every flag).
    All = 262143

class Event(enum.IntFlag):
    """Program event types used for event subscription and polling.

    Notes
    -----
    Event flags are bitwise-combinable with ``|``. ``Event.All`` selects every
    available event. The integer values are assigned by convention and are not
    published in the API reference; reference members by name rather than by
    numeric value.
    """

    #: A new slot was added.
    SlotAdded = 1
    #: A slot was deleted.
    SlotRemoved = 2
    #: The slots were reorganised.
    SlotsReorganized = 4
    #: A slot's geometry, displacement or function input file changed.
    SlotInputFilesChanged = 8
    #: Geometry was loaded into any slot.
    GeometryLoaded = 16
    #: A slot's properties changed.
    PropertiesChanged = 32
    #: The program is exiting.
    ProgramExit = 64
    #: The program is exiting via a script.
    ScriptExit = 128
    #: All available events (bitwise OR of every flag).
    All = 255

class FontStyle(enum.IntEnum):
    """Font styling applied to presentation text.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Regular (unstyled) text.
    Normal = 0
    #: Bold text.
    Bold = 1

class FrameSide(enum.IntEnum):
    """Side selection for a presentation frame border.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Left side of the frame.
    Left = 1
    #: Top side of the frame.
    Top = 2
    #: Right side of the frame.
    Right = 4
    #: Bottom side of the frame.
    Bottom = 8
    #: All four sides of the frame.
    All = 15

class Function(enum.IntEnum):
    """Result-function kind (scalar, vector or tensor).

    Notes
    -----
    These values are mutually exclusive; they are never combined.
    """

    #: Scalar function.
    Function = 0
    #: Vector function.
    Vector = 1
    #: Tensor function.
    Tensor = 2

class FunctionItem(enum.IntEnum):
    """Entity kind that a result function is evaluated on.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Nodal function item.
    Node = 0
    #: Element function item.
    Element = 1
    #: Property (part) function item.
    Property = 2
    #: Node-element function item.
    NodeElement = 3

class Item(enum.IntFlag):
    """Entity-type selection flags for model queries.

    Selects non-element entities such as constraints, loads, coordinate systems
    and organisational items. ``Auxiliaries`` is a convenience combination of the
    auxiliary entity flags (Spc, Mpc, Force, Moment and Coord).

    Notes
    -----
    Flags are bitwise-combinable with ``|``; refer to the individual method for
    the combinations it accepts.
    """

    #: Single-point constraints.
    Spc = 1
    #: Multi-point constraints.
    Mpc = 2
    #: Forces.
    Force = 4
    #: Moments.
    Moment = 8
    #: Coordinate systems.
    Coord = 16
    #: All auxiliaries (Spc, Mpc, Force, Moment and Coord).
    Auxiliaries = 31
    #: Impact points.
    ImpactPoint = 32
    #: Cross sections.
    CSection = 64
    #: Nodes.
    Node = 128
    #: Layers.
    Layer = 256
    #: Groups.
    Group = 512
    #: Currently selected items.
    Selected = 1024

class LabelPosition(enum.IntEnum):
    """Label placement for a presentation object.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Label at horizontal right.
    HorizontalRight = 0
    #: Label at horizontal left.
    HorizontalLeft = 1
    #: Label at horizontal center.
    HorizontalCenter = 2
    #: Label at vertical top.
    VerticalTop = 3
    #: Label at vertical bottom.
    VerticalBottom = 4
    #: Label at vertical center.
    VerticalCenter = 5

class LegendPosition(enum.IntEnum):
    """Legend placement relative to a plot.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: User-defined legend position.
    User = 0
    #: Left of the plot.
    Left = 1
    #: Below the plot.
    Below = 2
    #: Bottom left of the plot.
    BottomLeft = 3
    #: Bottom right of the plot.
    BottomRight = 4
    #: Right of the plot.
    Right = 5
    #: Top left of the plot.
    TopLeft = 6
    #: Top right of the plot.
    TopRight = 7
    #: Bottom center of the plot.
    BottomCenter = 8
    #: Top center of the plot.
    TopCenter = 9
    #: Left center of the plot.
    LeftCenter = 10
    #: Right center of the plot.
    RightCenter = 11

class LineStyle(enum.IntEnum):
    """Line-drawing style for curves and presentation lines.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Continuous (solid) line.
    Continuous = 0
    #: Dashed line.
    Dashed = 1
    #: Dash-and-dot line.
    DashAndDot = 2
    #: Dotted line.
    Dotted = 3
    #: Small-dashed line.
    SmallDashed = 4
    #: Invisible (hidden) line.
    Invisible = 5

class MarkerStyle(enum.IntEnum):
    """Marker style for function-curve data points.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Filled quad marker.
    FilledQuad = 0
    #: Open quad marker.
    Quad = 1
    #: Filled triangle marker.
    FilledTria = 2
    #: Open triangle marker.
    Tria = 3
    #: Filled circle marker.
    FilledCircle = 4
    #: Open circle marker.
    Circle = 5
    #: Filled diamond marker.
    FilledDiamond = 6
    #: Open diamond marker.
    Diamond = 7
    #: Cross marker.
    Cross = 8
    #: Star marker.
    Star = 9

class PageOrientation(enum.IntEnum):
    """Page orientation of a presentation page.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Landscape orientation.
    Landscape = 0
    #: Portrait orientation.
    Portrait = 1

class PolygonType(enum.IntEnum):
    """Shape of a presentation polygon object.

    Notes
    -----
    These values are mutually exclusive; they are never combined. The integer
    values are assigned by convention and are not published in the API
    reference; reference members by name rather than by numeric value.
    """

    #: Triangle.
    Triangle = 0
    #: Rectangle.
    Rectangle = 1
    #: General polygon.
    Polygon = 2

class Presentation(enum.IntFlag):
    """Presentation-object type selection flags.

    Selects presentation objects by kind. ``Curve`` is a common flag for every
    curve, ``Plot`` a common flag for every plot type, and ``All`` selects every
    presentation object.

    Notes
    -----
    Flags are bitwise-combinable with ``|``; refer to the individual method for
    the combinations it accepts. The integer values are assigned by convention
    and are not published in the API reference; reference members by name rather
    than by numeric value.
    """

    #: Axis object of any plot.
    Axis = 1
    #: Bar-chart object.
    BarChart = 2
    #: BarSet object of a bar chart.
    BarSet = 4
    #: ColorMap object of a color plot.
    ColorMap = 8
    #: Color-plot object.
    ColorPlot = 16
    #: Common flag for all curves.
    Curve = 32
    #: Embedded-view object.
    EmbedView = 64
    #: Group object.
    Group = 128
    #: Image object.
    Image = 256
    #: Legend object of any plot.
    Legend = 512
    #: Line object.
    Line = 1024
    #: Common flag for all plots.
    Plot = 2048
    #: Polar-plot object.
    PolarPlot = 4096
    #: Set object of an XY plot.
    Set = 8192
    #: Set3D object of a 3D plot.
    Set3D = 16384
    #: Table object.
    Table = 32768
    #: TableField object of a table.
    TableField = 65536
    #: Text object.
    Text = 131072
    #: 3D-plot object.
    ThreeDPlot = 262144
    #: Vector object of a polar plot.
    Vector = 524288
    #: XY-plot object.
    XYPlot = 1048576
    #: Common flag for all presentation objects.
    All = 2097151

class Property(enum.IntFlag):
    """Property-type (part-type) selection flags for model queries.

    Selects parts by their element type. ``Shell`` and ``Solid`` are convenience
    combinations covering every shell or solid part, and ``All`` selects every
    part.

    Notes
    -----
    Flags are bitwise-combinable with ``|``; refer to the individual method for
    the combinations it accepts.
    """

    #: SPH parts only.
    Sph = 1
    #: Bar parts only.
    Bar = 2
    #: Beam parts only.
    Beam = 4
    #: Discrete parts only.
    Discrete = 8
    #: Joint parts only.
    Joint = 16
    #: Mass parts only.
    Mass = 32
    #: Nel (non-structural) parts only.
    Nel = 64
    #: Quad shell parts only.
    Quad = 128
    #: Tria shell parts only.
    Tria = 256
    #: All shell parts (Quad and Tria).
    Shell = 384
    #: Hexa solid parts only.
    Hexa = 512
    #: Penta solid parts only.
    Penta = 1024
    #: Tetra solid parts only.
    Tetra = 2048
    #: Pyra solid parts only.
    Pyra = 4096
    #: All solid parts (Hexa, Penta, Tetra and Pyra).
    Solid = 7680
    #: Rigid (RBE) parts only.
    Rbe = 8192
    #: Single-point-constraint parts only.
    Spc = 16384
    #: Multi-point-constraint parts only.
    Mpc = 32768
    #: Force parts only.
    Force = 65536
    #: Moment parts only.
    Moment = 131072
    #: Coordinate-system parts only.
    Coord = 262144
    #: Connection parts only.
    Conn = 524288
    #: All part types (bitwise OR of every flag).
    All = 1048575

class View(enum.IntFlag):
    """View-type selection flags.

    Notes
    -----
    Each value corresponds to a single view type. ``View.Active`` denotes the
    currently active view and ``View.All`` selects every view.
    """

    #: Model view.
    Model = 1
    #: Curve view.
    Curve = 2
    #: FLC (forming-limit-curve) view.
    FLC = 4
    #: Video view.
    Video = 8
    #: Presentation view.
    Presentation = 16
    #: The currently active view.
    Active = 32
    #: All views (bitwise OR of every flag).
    All = 63

# Module-level flag aliases (see the corresponding enum).
AUXILIARY = Item.Auxiliaries
ActiveView = View.Active
BAR = Element.Bar
BEAM = Element.Beam
CONN = Element.Conn
COORD = Item.Coord
CSECTION = Item.CSection
CurveView = View.Curve
DAMPER = Element.Damper
ELEMENT = Element.All
FLCView = View.FLC
FORCE = Item.Force
FREQUENCYRESPONSE = Analysis.FrequencyResponse
FUNCTIONS = Function.Function
GROUP = Item.Group
HEXA = Element.Hexa
IMPACTPOINT = Item.ImpactPoint
JOINT = Element.Joint
LAYER = Item.Layer
MASS = Element.Mass
MODAL = Analysis.Modal
MOMENT = Item.Moment
MPC = Item.Mpc
ModelView = View.Model
NEL = Element.Nel
NODE = Item.Node
PENTA = Element.Penta
PID = Property.All
PID_BAR = Property.Bar
PID_BEAM = Property.Beam
PID_CONN = Property.Conn
PID_COORD = Property.Coord
PID_DISCRETE = Property.Discrete
PID_FORCE = Property.Force
PID_HEXA = Property.Hexa
PID_JOINT = Property.Joint
PID_MASS = Property.Mass
PID_MOMENT = Property.Moment
PID_MPC = Property.Mpc
PID_NEL = Property.Nel
PID_PENTA = Property.Penta
PID_PYRA = Property.Pyra
PID_QUAD = Property.Quad
PID_RBE = Property.Rbe
PID_SHELL = Property.Shell
PID_SOLID = Property.Solid
PID_SPC = Property.Spc
PID_SPH = Property.Sph
PID_TETRA = Property.Tetra
PID_TRIA = Property.Tria
PYRA = Element.Pyra
PresentationView = View.Presentation
QUAD = Element.Quad
RBE = Element.Rbe
RBE2 = Element.Rbe2
RBE3 = Element.Rbe3
SELECTED = Item.Selected
SHELL = Element.Shell
SOLID = Element.Solid
SPC = Item.Spc
SPH = Element.Sph
SPRING = Element.Spring
STATIC = Analysis.Static
TENSORS = Function.Tensor
TETRA = Element.Tetra
TRANSIENT = Analysis.Transient
TRIA = Element.Tria
UNDEFINED = Analysis.Undefined
VECTORS = Function.Vector
VideoView = View.Video

#: The global GNS handle; the entry point for every script.
gns: GNS
#: Alternative name for the global GNS handle (identical to :data:`gns`).
a4: GNS

def getGlobalDirectory() -> str:
    r"""Return the program's global directory.

    Returns
    -------
    str
        The global directory, usually the Animator4 installation directory.

    Examples
    --------
    >>> import gnspy
    >>> print(gnspy.getGlobalDirectory())
    C:\\Program Files\\GNS mbH\\Animator4
    """

def getProgramName() -> str:
    """Return the program name.

    Returns
    -------
    str
        The program name, for example ``"Animator4"``.

    Examples
    --------
    >>> import gnspy
    >>> print(gnspy.getProgramName())
    Animator4
    """

def getUserDirectory() -> str:
    """Return the program's local user directory.

    Returns
    -------
    str
        The per-user directory, for example ``"~/.a4dir"``.

    Examples
    --------
    >>> import gnspy
    >>> print(gnspy.getUserDirectory())
    ~/.a4dir
    """

def hasLicenseOption(option: str) -> bool:
    """Report whether a license option is available.

    Parameters
    ----------
    option : str
        The license-option code to check, for example ``"PED"``.

    Returns
    -------
    bool
        ``True`` if the option is available with the current license,
        ``False`` otherwise.

    Examples
    --------
    >>> import gnspy
    >>> if gnspy.hasLicenseOption('PED'):
    ...     print('PED available')
    """

class GNS:
    """Global GNS handle object.

    The global handle is the entry point for any GNS Python script. It is used
    to obtain slot, presentation and view handles, execute commands, access
    slot-independent images, videos and variables, perform calculations and run
    model or curve scans.

    Notes
    -----
    The handle is a singleton and is never constructed directly. There is always
    exactly one global handle, obtained as ``gnspy.gns``::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> allslots = gns.getSlotList()
        >>> slot = allslots[0]
        >>> allviews = gns.getViewList()
        >>> view = allviews[0]
        >>> interface = gns.getUserVariable("INPUTIFACE").getValue()
        >>> filename = gns.getUserVariable("FILENAME").getValue()
        >>> gns.executeCommand(
        ...     "rea fil {} {} GEO=0:pid:all ADD=no".format(interface, filename), slot
        ... )
        >>> gns.executeCommand("era qua all", slot, view=view)
    """

    def beginEditing(self, commandDescription: str) -> None:
        """Begin an editing block that will be undoable as a single step.

        Any edits made between this call and the matching :meth:`endEditing`
        call are grouped into a single Undo step.

        Parameters
        ----------
        commandDescription : str
            The text used as the Undo description for the grouped edits.

        Returns
        -------
        None

        Warnings
        --------
        Be careful using this in a non-blocking script.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.beginEditing("Set some values")
        >>> # set some values
        >>> gns.endEditing(True)
        """

    def endEditing(self, success: bool) -> None:
        """End an editing block started with :meth:`beginEditing`.

        Parameters
        ----------
        success : bool
            If ``False``, all changes made between :meth:`beginEditing` and this
            call are undone; if ``True`` they are kept as a single Undo step.

        Returns
        -------
        None

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.beginEditing("Set some values")
        >>> # set some values
        >>> gns.endEditing(True)
        """

    def executeCommand(
        self,
        command: str,
        slot: GNSSlot | None = None,
        module: GNSModule | None = None,
        view: GNSView | None = None,
        pres: GNSPresentation | None = None,
    ) -> tuple[int, str, list[GNSResultVariable]]:
        """Execute an Animator command, optionally on specified targets.

        Parameters
        ----------
        command : str
            The Animator command string to execute.
        slot : GNSSlot or None, optional
            The slot to target; ``None`` (default) uses no explicit slot target.
        module : GNSModule or None, optional
            The module to target; ``None`` (default) uses no explicit module
            target.
        view : GNSView or None, optional
            The view to target; ``None`` (default) uses no explicit view target.
        pres : GNSPresentation or None, optional
            The presentation to target; ``None`` (default) uses no explicit
            presentation target.

        Returns
        -------
        tuple of (int, str, list of GNSResultVariable)
            The command success status (``1`` on success, ``0`` on failure), any
            error or warning message text, and the result variables produced by
            the command.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> status, msg, resvars = gns.executeCommand("xcm vie new mod")
        """

    def getSlotList(self, filter: str | None = None) -> list[GNSSlot]:
        """Return all slots, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSlot
            The matching slot handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getSlotList()
        """

    def getActiveSlotList(self, filter: str | None = None) -> list[GNSSlot]:
        """Return all active slots, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSlot
            The matching active slot handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getActiveSlotList()
        """

    def getSlotById(self, id: int) -> GNSSlot | None:
        """Return the slot with the given id.

        Parameters
        ----------
        id : int
            The slot id to look up.

        Returns
        -------
        GNSSlot or None
            The matching slot, or ``None`` if no slot with the given id exists.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getSlotById(0)
        """

    def getSlotByName(self, name: str) -> GNSSlot | None:
        """Return the slot with the given name.

        Parameters
        ----------
        name : str
            The slot name to look up.

        Returns
        -------
        GNSSlot or None
            The matching slot, or ``None`` if no slot with the given name exists.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getSlotByName("Can")
        """

    def getCommandTargetSlots(self) -> list[GNSSlot]:
        """Return the current command target slots.

        Returns
        -------
        list of GNSSlot
            The slots currently targeted by commands.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getCommandTargetSlots()
        """

    def getCommandTargetModules(self, slotid: int) -> list[GNSModule]:
        """Return the command target modules for the given slot.

        Parameters
        ----------
        slotid : int
            The id of the slot whose command target modules are required.

        Returns
        -------
        list of GNSModule
            The modules currently targeted by commands for the given slot.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getCommandTargetModules(0)
        """

    def getViewList(self, type: View = ..., filter: str | None = None) -> list[GNSView]:
        """Return all views, optionally filtered by type.

        Parameters
        ----------
        type : View, optional
            View-type flag selecting which views to return. Combine flags with
            ``|``. Default is ``View.All`` (every view type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSView
            The matching view handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getViewList()
        """

    def getViewById(self, id: int) -> GNSView | None:
        """Return the view with the given id.

        Parameters
        ----------
        id : int
            The view id to look up.

        Returns
        -------
        GNSView or None
            The matching view, or ``None`` if no view with the given id exists.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getViewById(1)
        """

    def getViewByName(self, name: str) -> GNSView | None:
        """Return the view with the given name.

        Parameters
        ----------
        name : str
            The view name to look up.

        Returns
        -------
        GNSView or None
            The matching view, or ``None`` if no view with the given name exists.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getViewByName("Model")
        """

    def getCommandTargetViews(self) -> list[GNSView]:
        """Return the current command target views.

        Returns
        -------
        list of GNSView
            The views currently targeted by commands.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getCommandTargetViews()
        """

    def getPresentationList(self, filter: str | None = None) -> list[GNSPresentation]:
        """Return all presentations, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSPresentation
            The matching presentation handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getPresentationList()
        """

    def getCommandTargetPresentations(self) -> list[GNSPresentation]:
        """Return the current command target presentations.

        Returns
        -------
        list of GNSPresentation
            The presentations currently targeted by commands.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getCommandTargetPresentations()
        """

    def getPresentationById(self, id: int) -> GNSPresentation | None:
        """Return the presentation with the given id.

        Parameters
        ----------
        id : int
            The presentation id to look up.

        Returns
        -------
        GNSPresentation or None
            The matching presentation, or ``None`` if none has the given id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getPresentationById(1)
        """

    def getPresentationByName(self, name: str) -> GNSPresentation | None:
        """Return the presentation with the given name.

        Parameters
        ----------
        name : str
            The presentation name to look up.

        Returns
        -------
        GNSPresentation or None
            The matching presentation, or ``None`` if none has the given name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getPresentationByName("Presentation")
        """

    def getImageById(self, id: int) -> GNSImage | None:
        """Return the global image with the given id.

        Parameters
        ----------
        id : int
            The image id to look up.

        Returns
        -------
        GNSImage or None
            The matching global image, or ``None`` if none has the given id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getImageById(1)
        """

    def getImageByName(self, name: str) -> GNSImage | None:
        """Return the global image with the given name.

        Parameters
        ----------
        name : str
            The image name to look up.

        Returns
        -------
        GNSImage or None
            The matching global image, or ``None`` if none has the given name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getImageByName("myimage")
        """

    def getImageList(self, filter: str | None = None) -> list[GNSImage]:
        """Return all global images, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSImage
            The matching global image handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getImageList()
        """

    def getVideoById(self, id: int) -> GNSVideo | None:
        """Return the global video with the given id.

        Parameters
        ----------
        id : int
            The video id to look up.

        Returns
        -------
        GNSVideo or None
            The matching global video, or ``None`` if none has the given id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getVideoById(1)
        """

    def getVideoByName(self, id: str) -> GNSVideo | None:
        """Return the global video with the given name.

        Parameters
        ----------
        id : str
            The video name to look up. The parameter is named ``id`` in the
            compiled API even though it selects the video by name.

        Returns
        -------
        GNSVideo or None
            The matching global video, or ``None`` if none has the given name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getVideoByName("myvideo")
        """

    def getVideoList(self, filter: str | None = None) -> list[GNSVideo]:
        """Return all global videos, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSVideo
            The matching global video handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getVideoList()
        """

    def getReferencedPattern(self, name: str) -> GNSPattern | None:
        """Return the referenced pattern with the given name.

        Parameters
        ----------
        name : str
            The referenced pattern name to look up.

        Returns
        -------
        GNSPattern or None
            The matching referenced pattern, or ``None`` if none has the given
            name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getReferencedPattern("My_Pattern")
        """

    def getReferencedPatternList(self, filter: str | None = None) -> list[GNSPattern]:
        """Return all referenced patterns, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSPattern
            The matching referenced pattern handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> rpatlist = gns.getReferencedPatternList()
        """

    def getUserVariable(self, name: str) -> GNSUserVariable | None:
        """Return the user variable with the given name.

        Parameters
        ----------
        name : str
            The user variable name to look up.

        Returns
        -------
        GNSUserVariable or None
            The matching user variable, or ``None`` if none has the given name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> var = gns.getUserVariable(name)
        """

    def getUserVariableList(self, filter: str | None = None) -> list[GNSUserVariable]:
        """Return all user variables, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSUserVariable
            The matching user variable handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> varlist = gns.getUserVariableList()
        """

    def getSystemVariable(self, name: str) -> GNSSystemVariable | None:
        """Return the system variable with the given name.

        Parameters
        ----------
        name : str
            The system variable name to look up.

        Returns
        -------
        GNSSystemVariable or None
            The matching system variable, or ``None`` if none has the given name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> var = gns.getSystemVariable(name)
        """

    def getSystemVariableList(self, filter: str | None = None) -> list[GNSSystemVariable]:
        """Return all system variables, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSystemVariable
            The matching system variable handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> varlist = gns.getSystemVariableList()
        """

    def getCurveScanObject(self, Interface: str, inputfile: str) -> GNSCurveScan | None:
        """Scan an input file for curves and return a curve-scan handle.

        Parameters
        ----------
        Interface : str
            The solver interface name to scan with, e.g. ``"Pamcrash"``.
        inputfile : str
            The path of the input file to scan.

        Returns
        -------
        GNSCurveScan or None
            The curve-scan handle, or ``None`` if the file could not be scanned.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getCurveScanObject("Pamcrash", "Can.THP")
        """

    def getModelScanObject(self, Interface: str, inputfile: str) -> GNSModelScan | None:
        """Scan an input file for a model and return a model-scan handle.

        Parameters
        ----------
        Interface : str
            The solver interface name to scan with, e.g. ``"Pamcrash"``.
        inputfile : str
            The path of the input file to scan.

        Returns
        -------
        GNSModelScan or None
            The model-scan handle, or ``None`` if the file could not be scanned.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        """

    def isAboutToQuit(self) -> bool:
        """Return whether the program is about to quit.

        This provides a notification before the program quits and cancels
        running scripts.

        Returns
        -------
        bool
            ``True`` if the program is about to quit, otherwise ``False``.

        See Also
        --------
        GNS.waitForEvent : Event-driven alternative that is more efficient than
            polling.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> while True:
        ...     if gns.isAboutToQuit() == 1:
        ...         pass  # DoWhatYouWantAndQuit()
        ...     # some other tasks
        """

    def waitForEvent(self, events: Event) -> Event:
        """Wait for one of the requested events and return the event that occurred.

        Blocks the script until one of the requested events occurs. Note that
        ``Event.ProgramExit`` and ``Event.ScriptExit`` are always returned if
        they occur. Use ``Event.All`` to wait for any event.

        Parameters
        ----------
        events : Event
            The event flags to wait for. Combine flags with ``|``.

        Returns
        -------
        Event
            The event that occurred.

        Examples
        --------
        >>> import gnspy
        >>> import sys
        >>> gns = gnspy.gns
        >>> while True:
        ...     event = gns.waitForEvent(gnspy.Event.GeometryLoaded)
        ...     if event == gnspy.Event.ProgramExit or event == gnspy.Event.ScriptExit:
        ...         sys.exit()
        ...     handleEvent(event)
        """

    def getTextFont(self) -> GNSFont:
        """Return the global option text font.

        Returns
        -------
        GNSFont
            The global option text font.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> textFont = gns.getTextFont()
        >>> textFont.getName()
        """

    def getLabelFont(self) -> GNSFont:
        """Return the global option label font.

        Returns
        -------
        GNSFont
            The global option label font.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> labelFont = gns.getLabelFont()
        >>> labelFont.getName()
        """

    def createKeyword(self, *args: object, **kwargs: object) -> GNSKeyword:
        """Construct a solver keyword (deprecated).

        .. deprecated::
            Use :meth:`GNSSlot.createKeyword` instead.

        Returns
        -------
        GNSKeyword
            The newly constructed keyword.

        Notes
        -----
        This method is deprecated and retained only for backward compatibility;
        its signature is not published in the API reference. Call
        :meth:`GNSSlot.createKeyword` on the target slot instead.
        """

    def getKeywordById(self, *args: object, **kwargs: object) -> GNSKeyword | None:
        """Return a keyword by id (deprecated).

        .. deprecated::
            Use :meth:`GNSSlot.getKeywordById` instead.

        Returns
        -------
        GNSKeyword or None
            The matching keyword, or ``None`` if none matches.

        Notes
        -----
        This method is deprecated and retained only for backward compatibility;
        its signature is not published in the API reference. Call
        :meth:`GNSSlot.getKeywordById` on the target slot instead.
        """

    def getKeywordByIndex(self, *args: object, **kwargs: object) -> GNSKeyword | None:
        """Return a keyword by index (deprecated).

        .. deprecated::
            Use :meth:`GNSSlot.getKeywordByIndex` instead.

        Returns
        -------
        GNSKeyword or None
            The matching keyword, or ``None`` if the index is out of range.

        Notes
        -----
        This method is deprecated and retained only for backward compatibility;
        its signature is not published in the API reference. Call
        :meth:`GNSSlot.getKeywordByIndex` on the target slot instead.
        """

    def getKeywordByName(self, *args: object, **kwargs: object) -> GNSKeyword | None:
        """Return a keyword by name (deprecated).

        .. deprecated::
            Use :meth:`GNSSlot.getKeywordByName` instead.

        Returns
        -------
        GNSKeyword or None
            The matching keyword, or ``None`` if none matches.

        Notes
        -----
        This method is deprecated and retained only for backward compatibility;
        its signature is not published in the API reference. Call
        :meth:`GNSSlot.getKeywordByName` on the target slot instead.
        """

    def getKeywordList(self, *args: object, **kwargs: object) -> list[GNSKeyword]:
        """Return the keyword list (deprecated).

        .. deprecated::
            Use :meth:`GNSSlot.getKeywordList` instead.

        Returns
        -------
        list of GNSKeyword
            The matching keywords, empty if none match.

        Notes
        -----
        This method is deprecated and retained only for backward compatibility;
        its signature is not published in the API reference. Call
        :meth:`GNSSlot.getKeywordList` on the target slot instead.
        """

    def getSolver(self, *args: object, **kwargs: object) -> str:
        """Return the solver name (deprecated).

        .. deprecated::
            Use :meth:`GNSSlot.getSolver` instead.

        Returns
        -------
        str
            The solver name.

        Notes
        -----
        This method is deprecated and retained only for backward compatibility;
        its signature is not published in the API reference. Call
        :meth:`GNSSlot.getSolver` on the target slot instead.
        """

    def setSolver(self, *args: object, **kwargs: object) -> None:
        """Set the solver (deprecated).

        .. deprecated::
            Use :meth:`GNSSlot.setSolver` instead.

        Returns
        -------
        None

        Notes
        -----
        This method is deprecated and retained only for backward compatibility;
        its signature is not published in the API reference. Call
        :meth:`GNSSlot.setSolver` on the target slot instead.
        """

class GNSSlot:
    """GNS Slot handle object.

    A slot handle exposes the entities, variables, modules, images, videos and
    solver keywords loaded into a single Animator slot. It is also the target
    for entity picking, slot-based selected items and command execution.

    Notes
    -----
    Slot handles are not constructed directly. Obtain one from the global GNS
    object with :meth:`getSlotList`::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> nodes = slot.getNodeList()
        >>> slot.executeCommand("era bar all")
    """

    def getName(self) -> str:
        """Return the slot name.

        Returns
        -------
        str
            The slot's name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slo_name = slot.getName()
        """

    def getId(self) -> int:
        """Return the slot id.

        Returns
        -------
        int
            The slot's numeric id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slo_id = slot.getId()
        """

    def isActive(self) -> bool:
        """Return whether this is the active slot.

        Returns
        -------
        bool
            ``True`` if this slot is currently active, otherwise ``False``.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> is_active = slot.isActive()
        """

    def getColor(self) -> GNSColor:
        """Return the slot color.

        Returns
        -------
        GNSColor
            The slot's color.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> color = slot.getColor()
        """

    def hasPropertyThickness(self) -> bool:
        """Return whether any property in the slot carries a thickness.

        Returns
        -------
        bool
            ``True`` if property thickness exists for this slot's properties.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slot.hasPropertyThickness()
        """

    def getModelSize(self) -> tuple[float, float, float, float, float, float]:
        """Return the model-coordinate bounding box of the geometry.

        The bounding box is computed on the undeformed geometry without taking
        pid explodes into account. If the slot has no geometry, all six values
        are ``0.0``.

        Returns
        -------
        tuple of float
            Six values ``(min_x, min_y, min_z, max_x, max_y, max_z)`` giving the
            minimum and maximum corners of the bounding box.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> min_x, min_y, min_z, max_x, max_y, max_z = slot.getModelSize()

        See Also
        --------
        GNSModelView.getModelSize : Bounding box of only the visible items.
        """

    def executeCommand(self, command: str) -> tuple[int, str, list[GNSResultVariable]]:
        """Execute an Animator command with this slot as the target.

        Parameters
        ----------
        command : str
            The Animator command string to execute.

        Returns
        -------
        tuple of (int, str, list of GNSResultVariable)
            The command success status (``1`` on success, ``0`` on failure), any
            error or warning message text, and the result variables produced by
            the command.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> status, msg, resvars = slot.executeCommand("slo swi off")
        """

    def getUDefCoordinates(self, nodes: list[GNSNode]) -> list[tuple[float, float, float]]:
        """Return the undeformed coordinates of the given nodes.

        Parameters
        ----------
        nodes : list of GNSNode
            The nodes whose undeformed coordinates are required.

        Returns
        -------
        list of tuple of float
            One ``(x, y, z)`` tuple per node, in the same order as ``nodes``.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> nodes = slot.getNodeList()
        >>> slot.getUDefCoordinates(nodes)
        """

    def getSolver(self) -> str:
        """Return the current solver.

        Returns
        -------
        str
            The name of the current solver, e.g. ``'PAM-CRASH'``.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slot.getSolver()
        'PAM-CRASH'
        """

    def setSolver(self, solver: str) -> None:
        """Set the current solver.

        Parameters
        ----------
        solver : str
            The name of the solver to make current, e.g. ``'PAM-CRASH'``.

        Returns
        -------
        None

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slot.setSolver('PAM-CRASH')
        """

    # -- Nodes ---------------------------------------------------------------

    def getNodeById(self, id: int) -> GNSNode | None:
        """Return the node with the given id.

        Parameters
        ----------
        id : int
            The node id to look up.

        Returns
        -------
        GNSNode or None
            The matching node, or ``None`` if no node has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> node = slot.getNodeById(100)
        """

    def getNodeList(self, filter: str | None = None) -> list[GNSNode]:
        """Return the slot's nodes, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSNode
            The matching nodes, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> nodes = slot.getNodeList()
        """

    def getNode(self, id: int) -> GNSNode | None:
        """Return the node with the given id (deprecated).

        Parameters
        ----------
        id : int
            The node id to look up.

        Returns
        -------
        GNSNode or None
            The matching node, or ``None`` if no node has the given id.

        Notes
        -----
        Deprecated. Use :meth:`getNodeById` instead.
        """

    # -- Modules -------------------------------------------------------------

    def getRootModule(self) -> GNSModule | None:
        """Return the root module of the slot.

        Returns
        -------
        GNSModule or None
            The root module, or ``None`` if the slot has no modules.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> module = slot.getRootModule()
        """

    def getDefaultModule(self, filter: str | None = None) -> GNSModule | None:
        """Return the slot's default module.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        GNSModule or None
            The default module, or ``None`` if there is none.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> module = slot.getDefaultModule()
        """

    def getModuleList(self, filter: str | None = None) -> list[GNSModule]:
        """Return the slot's modules, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSModule
            The matching modules, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> modules = slot.getModuleList()
        """

    def getModulesByName(self, parent: GNSModule | None, name: str) -> list[GNSModule]:
        """Return all modules with the given name under an optional parent.

        Parameters
        ----------
        parent : GNSModule or None
            The parent module to search under; pass ``None`` to search from the
            root module.
        name : str
            The module name to match.

        Returns
        -------
        list of GNSModule
            The matching modules, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> parent = slot.getRootModule()
        >>> modules = slot.getModulesByName(parent, "wheel")
        """

    def getModulesById(self, parent: GNSModule | None, id: int) -> list[GNSModule]:
        """Return all modules with the given user id under an optional parent.

        Parameters
        ----------
        parent : GNSModule or None
            The parent module to search under; pass ``None`` to search from the
            root module.
        id : int
            The module user id to match.

        Returns
        -------
        list of GNSModule
            The matching modules, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> parent = slot.getRootModule()
        >>> modules = slot.getModulesById(parent, 100)
        """

    # -- State sets ----------------------------------------------------------

    def getStateSetList(self) -> list[GNSStateSet]:
        """Return all state sets in the slot.

        Returns
        -------
        list of GNSStateSet
            The slot's state sets, empty if there are none.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> plist = slot.getStateSetList()
        """

    def getStateSetById(self, id: int) -> GNSStateSet | None:
        """Return the state set with the given id.

        Parameters
        ----------
        id : int
            The state set id to look up.

        Returns
        -------
        GNSStateSet or None
            The matching state set, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = slot.getStateSetById(0)
        """

    def getStateSetByName(self, name: str) -> GNSStateSet | None:
        """Return the state set with the given name.

        Parameters
        ----------
        name : str
            The state set name to look up.

        Returns
        -------
        GNSStateSet or None
            The matching state set, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = slot.getStateSetByName("set 1")
        """

    # -- Elements ------------------------------------------------------------

    def getElementById(self, id: int, type: Element = ...) -> GNSElement | None:
        """Return the element with the given id and optional type.

        Parameters
        ----------
        id : int
            The element id to look up.
        type : Element, optional
            Element-type flag constraining the lookup. Combine flags with ``|``.
            Default is ``Element.All`` (any element type).

        Returns
        -------
        GNSElement or None
            The matching element, or ``None`` if no element has the given id
            and type.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> elem = slot.getElementById(100, type=gnspy.Element.Hexa)
        """

    def getElementList(self, type: Element = ..., filter: str | None = None) -> list[GNSElement]:
        """Return the slot's elements, optionally typed and filtered.

        Parameters
        ----------
        type : Element, optional
            Element-type flag selecting which elements to return. Combine flags
            with ``|``. Default is ``Element.All`` (every element).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSElement
            The matching elements, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> elist = slot.getElementList(type=gnspy.Element.Hexa)
        """

    def getElement(self, id: int, type: Element = ...) -> GNSElement | None:
        """Return the element with the given id and optional type (deprecated).

        Parameters
        ----------
        id : int
            The element id to look up.
        type : Element, optional
            Element-type flag constraining the lookup. Combine flags with ``|``.
            Default is ``Element.All`` (any element type).

        Returns
        -------
        GNSElement or None
            The matching element, or ``None`` if no element has the given id
            and type.

        Notes
        -----
        Deprecated. Use :meth:`getElementById` instead.
        """

    # -- Properties ----------------------------------------------------------

    def getPropertyById(self, id: int) -> GNSProperty | None:
        """Return the property with the given id.

        Parameters
        ----------
        id : int
            The property id to look up.

        Returns
        -------
        GNSProperty or None
            The matching property, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> prop1 = slot.getPropertyById(100)
        """

    def getPropertyByName(self, name: str) -> GNSProperty | None:
        """Return the property with the given name.

        Parameters
        ----------
        name : str
            The property name to look up.

        Returns
        -------
        GNSProperty or None
            The matching property, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> prop2 = slot.getPropertyByName("Shell_Prop")
        """

    def getPropertyList(self, type: Property = ..., filter: str | None = None) -> list[GNSProperty]:
        """Return the slot's properties, optionally typed and filtered.

        Parameters
        ----------
        type : Property, optional
            Property-type flag selecting which properties to return. Combine
            flags with ``|``. Default is ``Property.All`` (every property).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSProperty
            The matching properties, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> plist = slot.getPropertyList()
        """

    # -- Materials -----------------------------------------------------------

    def getMaterialById(self, id: int) -> GNSMaterial | None:
        """Return the material with the given id.

        Parameters
        ----------
        id : int
            The material id to look up.

        Returns
        -------
        GNSMaterial or None
            The matching material, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> mat = slot.getMaterialById(100)
        """

    def getMaterialByName(self, name: str) -> GNSMaterial | None:
        """Return the material with the given name.

        Parameters
        ----------
        name : str
            The material name to look up.

        Returns
        -------
        GNSMaterial or None
            The matching material, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> mat = slot.getMaterialByName("Shell_Material")
        """

    def getMaterialList(self, filter: str | None = None) -> list[GNSMaterial]:
        """Return the slot's materials, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMaterial
            The matching materials, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> matlist = slot.getMaterialList()
        """

    # -- Groups --------------------------------------------------------------

    def getGroupByName(self, name: str) -> GNSGroup | None:
        """Return the group with the given name.

        Parameters
        ----------
        name : str
            The group name to look up.

        Returns
        -------
        GNSGroup or None
            The matching group, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> group = slot.getGroupByName("Shell_Group")
        """

    def getGroupById(self, id: int) -> GNSGroup | None:
        """Return the group with the given id.

        Parameters
        ----------
        id : int
            The group id to look up.

        Returns
        -------
        GNSGroup or None
            The matching group, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> group = slot.getGroupById(100)
        """

    def getGroupList(self, filter: str | None = None) -> list[GNSGroup]:
        """Return the slot's groups, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching groups, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> grouplist = slot.getGroupList()
        """

    def getGroupListByProperty(
        self, prop: GNSProperty, filter: str | None = None
    ) -> list[GNSGroup]:
        """Return groups that contain the given property.

        Parameters
        ----------
        prop : GNSProperty
            The property whose containing groups are required.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching groups, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> prop = slot.getPropertyList()[0]
        >>> grouplist = slot.getGroupListByProperty(prop)
        """

    def getGroupListByNode(
        self, node: GNSNode, indirect: bool = True, filter: str | None = None
    ) -> list[GNSGroup]:
        """Return groups that contain the given node.

        Parameters
        ----------
        node : GNSNode
            The node whose containing groups are required.
        indirect : bool, optional
            If ``True`` (default), also match groups that contain the node
            indirectly via a property or element; if ``False``, only match
            groups that contain the node directly.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching groups, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> node = slot.getNodeList()[0]
        >>> grouplist = slot.getGroupListByNode(node)
        """

    def getGroupListByElement(
        self, element: GNSElement, indirect: bool = True, filter: str | None = None
    ) -> list[GNSGroup]:
        """Return groups that contain the given element.

        Parameters
        ----------
        element : GNSElement
            The element whose containing groups are required.
        indirect : bool, optional
            If ``True`` (default), also match groups that contain the element
            indirectly via a property; if ``False``, only match groups that
            contain the element directly.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching groups, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> elem = slot.getElementList()[0]
        >>> grouplist = slot.getGroupListByElement(elem)
        """

    # ``getGroup`` is deprecated; use ``getGroupById`` or ``getGroupByName``.
    # Overloaded stubs carry no docstring (ruff D418 forbids it on ``@overload``).
    @typing.overload
    def getGroup(self, id: int) -> GNSGroup | None: ...
    @typing.overload
    def getGroup(self, name: str) -> GNSGroup | None: ...

    # -- Layers --------------------------------------------------------------

    def getLayerByName(self, name: str) -> GNSLayer | None:
        """Return the layer with the given name.

        Parameters
        ----------
        name : str
            The layer name to look up.

        Returns
        -------
        GNSLayer or None
            The matching layer, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> layer = slot.getLayerByName("Shell_Layer")
        """

    def getLayerByProperty(self, prop: GNSProperty) -> GNSLayer | None:
        """Return the layer that owns the given property.

        Parameters
        ----------
        prop : GNSProperty
            The property whose layer is required.

        Returns
        -------
        GNSLayer or None
            The matching layer, or ``None`` if no layer has the property.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> prop = gnspy.gns.getPropertyByName("Shell")
        >>> layer = slot.getLayerByProperty(prop)
        """

    def getLayerList(self, filter: str | None = None) -> list[GNSLayer]:
        """Return the slot's layers, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSLayer
            The matching layers, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> layerlist = slot.getLayerList()
        """

    # ``getLayer`` is deprecated; use ``getLayerByName`` or ``getLayerByProperty``.
    # Overloaded stubs carry no docstring (ruff D418 forbids it on ``@overload``).
    @typing.overload
    def getLayer(self, name: str) -> GNSLayer | None: ...
    @typing.overload
    def getLayer(self, prop: GNSProperty) -> GNSLayer | None: ...

    # -- Impact points -------------------------------------------------------

    def getImpactPointById(self, id: int) -> GNSImpactPoint | None:
        """Return the impact point with the given id.

        Parameters
        ----------
        id : int
            The impact point id to look up.

        Returns
        -------
        GNSImpactPoint or None
            The matching impact point, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> ip = slot.getImpactPointById(1)
        """

    def getImpactPointByName(self, name: str) -> GNSImpactPoint | None:
        """Return the impact point with the given name.

        Parameters
        ----------
        name : str
            The impact point name to look up.

        Returns
        -------
        GNSImpactPoint or None
            The matching impact point, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> ip = slot.getImpactPointByName("Shell_ImpactPoint")
        """

    def getImpactPointList(self, filter: str | None = None) -> list[GNSImpactPoint]:
        """Return the slot's impact points, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSImpactPoint
            The matching impact points, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> iplist = slot.getImpactPointList()
        """

    # -- SPCs ----------------------------------------------------------------

    def getSpcById(self, id: int) -> GNSSpc | None:
        """Return the SPC with the given id.

        Parameters
        ----------
        id : int
            The SPC id to look up.

        Returns
        -------
        GNSSpc or None
            The matching SPC, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> spc = slot.getSpcById(100)
        """

    def getSpcList(self, filter: str | None = None) -> list[GNSSpc]:
        """Return the slot's SPCs, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSpc
            The matching SPCs, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> spclist = slot.getSpcList()
        """

    def getSpc(self, id: int) -> GNSSpc | None:
        """Return the SPC with the given id (deprecated).

        Parameters
        ----------
        id : int
            The SPC id to look up.

        Returns
        -------
        GNSSpc or None
            The matching SPC, or ``None`` if none has the given id.

        Notes
        -----
        Deprecated. Use :meth:`getSpcById` instead.
        """

    # -- MPCs ----------------------------------------------------------------

    def getMpcById(self, id: int) -> GNSMpc | None:
        """Return the MPC with the given id.

        Parameters
        ----------
        id : int
            The MPC id to look up.

        Returns
        -------
        GNSMpc or None
            The matching MPC, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> mpc = slot.getMpcById(100)
        """

    def getMpcList(self, filter: str | None = None) -> list[GNSMpc]:
        """Return the slot's MPCs, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMpc
            The matching MPCs, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> mpclist = slot.getMpcList()
        """

    def getMpc(self, id: int) -> GNSMpc | None:
        """Return the MPC with the given id (deprecated).

        Parameters
        ----------
        id : int
            The MPC id to look up.

        Returns
        -------
        GNSMpc or None
            The matching MPC, or ``None`` if none has the given id.

        Notes
        -----
        Deprecated. Use :meth:`getMpcById` instead.
        """

    # -- Sections ------------------------------------------------------------

    def getSectionById(self, id: int) -> GNSSection | None:
        """Return the section with the given id.

        Parameters
        ----------
        id : int
            The section id to look up.

        Returns
        -------
        GNSSection or None
            The matching section, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> section = slot.getSectionById(100)
        """

    def getSectionList(self, filter: str | None = None) -> list[GNSSection]:
        """Return the slot's sections, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSection
            The matching sections, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> sectionlist = slot.getSectionList()
        """

    def getSection(self, id: int) -> GNSSection | None:
        """Return the section with the given id (deprecated).

        Parameters
        ----------
        id : int
            The section id to look up.

        Returns
        -------
        GNSSection or None
            The matching section, or ``None`` if none has the given id.

        Notes
        -----
        Deprecated. Use :meth:`getSectionById` instead.
        """

    # -- Forces --------------------------------------------------------------

    def getForceById(self, id: int) -> GNSForce | None:
        """Return the force with the given id.

        Parameters
        ----------
        id : int
            The force id to look up.

        Returns
        -------
        GNSForce or None
            The matching force, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> force = slot.getForceById(100)
        """

    def getForceList(self, filter: str | None = None) -> list[GNSForce]:
        """Return the slot's forces, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSForce
            The matching forces, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> forcelist = slot.getForceList()
        """

    def getForce(self, id: int) -> GNSForce | None:
        """Return the force with the given id (deprecated).

        Parameters
        ----------
        id : int
            The force id to look up.

        Returns
        -------
        GNSForce or None
            The matching force, or ``None`` if none has the given id.

        Notes
        -----
        Deprecated. Use :meth:`getForceById` instead.
        """

    # -- Moments -------------------------------------------------------------

    def getMomentById(self, id: int) -> GNSMoment | None:
        """Return the moment with the given id.

        Parameters
        ----------
        id : int
            The moment id to look up.

        Returns
        -------
        GNSMoment or None
            The matching moment, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> moment = slot.getMomentById(100)
        """

    def getMomentList(self, filter: str | None = None) -> list[GNSMoment]:
        """Return the slot's moments, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMoment
            The matching moments, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> momentlist = slot.getMomentList()
        """

    def getMoment(self, id: int) -> GNSMoment | None:
        """Return the moment with the given id (deprecated).

        Parameters
        ----------
        id : int
            The moment id to look up.

        Returns
        -------
        GNSMoment or None
            The matching moment, or ``None`` if none has the given id.

        Notes
        -----
        Deprecated. Use :meth:`getMomentById` instead.
        """

    # -- Coordinate systems --------------------------------------------------

    def getCoordById(self, id: int) -> GNSCoord | None:
        """Return the coordinate system with the given id.

        Parameters
        ----------
        id : int
            The coordinate system id to look up.

        Returns
        -------
        GNSCoord or None
            The matching coordinate system, or ``None`` if none has the given
            id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> coord = slot.getCoordById(100)
        """

    def getCoordList(self, filter: str | None = None) -> list[GNSCoord]:
        """Return the slot's coordinate systems, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSCoord
            The matching coordinate systems, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> coordlist = slot.getCoordList()
        """

    def getCoord(self, id: int) -> GNSCoord | None:
        """Return the coordinate system with the given id (deprecated).

        Parameters
        ----------
        id : int
            The coordinate system id to look up.

        Returns
        -------
        GNSCoord or None
            The matching coordinate system, or ``None`` if none has the given
            id.

        Notes
        -----
        Deprecated. Use :meth:`getCoordById` instead.
        """

    # -- Curves --------------------------------------------------------------

    def getCurveById(self, id: int) -> GNSCurve | None:
        """Return the curve with the given id.

        Parameters
        ----------
        id : int
            The curve id to look up.

        Returns
        -------
        GNSCurve or None
            The matching curve, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> curve = slot.getCurveById(100)
        """

    def getCurveByName(self, name: str) -> GNSCurve | None:
        """Return the curve with the given name.

        Parameters
        ----------
        name : str
            The curve name to look up.

        Returns
        -------
        GNSCurve or None
            The matching curve, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> curve = slot.getCurveByName("Shell_Curve")
        """

    def getCurveList(self, filter: str | None = None) -> list[GNSCurve]:
        """Return the slot's curves, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSCurve
            The matching curves, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> curvelist = slot.getCurveList()
        """

    # -- Images --------------------------------------------------------------

    def getImageById(self, id: int) -> GNSImage | None:
        """Return the image with the given id.

        Parameters
        ----------
        id : int
            The image id to look up.

        Returns
        -------
        GNSImage or None
            The matching image, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> img = slot.getImageById(100)
        """

    def getImageByName(self, name: str) -> GNSImage | None:
        """Return the image with the given name.

        Parameters
        ----------
        name : str
            The image name to look up.

        Returns
        -------
        GNSImage or None
            The matching image, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> img = slot.getImageByName("myimage")
        """

    def getImageList(self, filter: str | None = None) -> list[GNSImage]:
        """Return the slot's images, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSImage
            The matching images, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> imglist = slot.getImageList()
        """

    # -- Videos --------------------------------------------------------------

    def getVideoById(self, id: int) -> GNSVideo | None:
        """Return the video with the given id.

        Parameters
        ----------
        id : int
            The video id to look up.

        Returns
        -------
        GNSVideo or None
            The matching video, or ``None`` if none has the given id.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> vid = slot.getVideoById(100)
        """

    def getVideoByName(self, name: str) -> GNSVideo | None:
        """Return the video with the given name.

        Parameters
        ----------
        name : str
            The video name to look up.

        Returns
        -------
        GNSVideo or None
            The matching video, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> vid = slot.getVideoByName("Shell_Video")
        """

    def getVideoList(self, filter: str | None = None) -> list[GNSVideo]:
        """Return the slot's videos, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSVideo
            The matching videos, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> vidlist = slot.getVideoList()
        """

    # -- Variables -----------------------------------------------------------

    def getUserVariableList(self, filter: str | None = None) -> list[GNSUserVariable]:
        """Return the slot's user variables, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSUserVariable
            The matching user variables, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> varlist = slot.getUserVariableList()
        """

    def getSystemVariableList(self, filter: str | None = None) -> list[GNSSystemVariable]:
        """Return the slot's system variables, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSystemVariable
            The matching system variables, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> varlist = slot.getSystemVariableList()
        """

    def getUserVariable(self, name: str) -> GNSUserVariable | None:
        """Return the user variable with the given name.

        Parameters
        ----------
        name : str
            The user variable name to look up.

        Returns
        -------
        GNSUserVariable or None
            The matching user variable, or ``None`` if none has the given name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> var = slot.getUserVariable("varname")
        """

    def getSystemVariable(self, name: str) -> GNSSystemVariable | None:
        """Return the system variable with the given name.

        Parameters
        ----------
        name : str
            The system variable name to look up.

        Returns
        -------
        GNSSystemVariable or None
            The matching system variable, or ``None`` if none has the given
            name.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> var = slot.getSystemVariable("varname")
        """

    # -- Includes ------------------------------------------------------------

    def getTopLevelIncludeList(self) -> list[GNSInclude]:
        """Return the top-level include files of the slot.

        Returns
        -------
        list of GNSInclude
            The top-level files as include handles.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> files = slot.getTopLevelIncludeList()
        """

    # -- Solver keywords -----------------------------------------------------

    def createKeyword(
        self,
        type: str,
        file: GNSInclude | None = None,
        solver: str | None = None,
        id: int | None = None,
        name: str | None = None,
    ) -> GNSKeyword:
        """Construct a solver keyword of the given type.

        Parameters
        ----------
        type : str
            The keyword type to construct, e.g. ``"PART"``.
        file : GNSInclude or None, optional
            The include file to add the keyword to; ``None`` (default) uses the
            current file.
        solver : str or None, optional
            The solver to construct the keyword for; ``None`` (default) uses the
            current solver.
        id : int or None, optional
            The keyword id, if the keyword type has one.
        name : str or None, optional
            The keyword name, if the keyword type has one.

        Returns
        -------
        GNSKeyword
            The newly constructed keyword.

        Raises
        ------
        Exception
            If the given keyword type does not support an id and/or name, or if
            an option is required before the id can exist (e.g. ``'TITLE'`` for
            LS-Dyna).

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> keyword = slot.createKeyword("PART", solver="PAM-CRASH", id=600)
        >>> keyword.setValue("ATYPE", "SHELL")
        """

    def getKeywordById(self, type: str, id: int, solver: str | None = None) -> GNSKeyword | None:
        """Return the keyword of the given type with the given id.

        Parameters
        ----------
        type : str
            The keyword type to look up, e.g. ``"MATER"``.
        id : int
            The keyword id to look up.
        solver : str or None, optional
            The solver to query; ``None`` (default) uses the current solver.

        Returns
        -------
        GNSKeyword or None
            The matching keyword, or ``None`` if none matches.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slot.getKeywordById("MATER", 10)
        """

    def getKeywordByIndex(
        self, type: str, index: int, solver: str | None = None
    ) -> GNSKeyword | None:
        """Return the keyword of the given type at the given index.

        Parameters
        ----------
        type : str
            The keyword type to look up, e.g. ``"DIS3D"``.
        index : int
            The zero-based index of the keyword.
        solver : str or None, optional
            The solver to query; ``None`` (default) uses the current solver.

        Returns
        -------
        GNSKeyword or None
            The matching keyword, or ``None`` if the index is out of range.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slot.getKeywordByIndex("DIS3D", 12)
        """

    def getKeywordByName(
        self, type: str, name: str, solver: str | None = None
    ) -> GNSKeyword | None:
        """Return the keyword of the given type with the given name.

        Parameters
        ----------
        type : str
            The keyword type to look up, e.g. ``"GROUP"``.
        name : str
            The keyword name to look up.
        solver : str or None, optional
            The solver to query; ``None`` (default) uses the current solver.

        Returns
        -------
        GNSKeyword or None
            The matching keyword, or ``None`` if none matches.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slot.getKeywordByName("GROUP", "BIW Contact")
        """

    def getKeywordList(
        self,
        type: str | None = None,
        file: GNSInclude | None = None,
        solver: str | None = None,
        filter: str | None = None,
    ) -> list[GNSKeyword]:
        """Return the slot's keywords, optionally typed and filtered.

        Parameters
        ----------
        type : str or None, optional
            The keyword type to return, e.g. ``"MATER"``; ``None`` (default)
            returns all types.
        file : GNSInclude or None, optional
            Restrict the result to keywords in this include file; ``None``
            (default) does not restrict by file.
        solver : str or None, optional
            The solver to query; ``None`` (default) uses the current solver.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSKeyword
            The matching keywords, empty if none match.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slot.getKeywordList("MATER")
        """

class GNSNode:
    """Handle to a single node of a loaded model.

    A node exposes its identity, owning module and slot, its coordinates and
    displacements for a given state, result-function values, and its connectivity
    to elements.

    Notes
    -----
    Node handles are not constructed directly. Obtain one from a ``GNSSlot`` (for
    example ``slot.getNodeById(100)`` or ``slot.getNodeList()``) or from a
    ``GNSModule`` (``module.getNodeById(100)``).

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> node = slot.getNodeById(100)
    >>> node_id = node.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this node.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = node.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this node.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = node.getSlot()
        """

    def getId(self) -> int:
        """Return the node's user id.

        Returns
        -------
        int
            The user-visible node id.

        Examples
        --------
        >>> node.getId()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module this node belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the node has no module.

        Examples
        --------
        >>> node.getModule()
        """

    def getUDefCoordinates(self) -> tuple[float, float, float]:
        """Return the node's undeformed coordinates.

        Returns
        -------
        tuple of float
            The undeformed position as ``(x, y, z)``.

        Examples
        --------
        >>> node.getUDefCoordinates()
        """

    def getCoordinates(
        self, stateset: GNSStateSet, state: GNSState | None = None
    ) -> tuple[float, float, float]:
        """Return the node's coordinates for a given state set and state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set the coordinates are evaluated in.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        tuple of float
            The position as ``(x, y, z)``.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> node.getCoordinates(stateset, state)
        """

    def getDisplacement(
        self, stateset: GNSStateSet, state: GNSState | None = None
    ) -> tuple[float, float, float]:
        """Return the node's displacement for the active view, state set and state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set the displacement is evaluated in.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        tuple of float
            The displacement components ``(x, y, z)``, with the magnitude ``r``
            also reported.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> node.getDisplacement(stateset, state)
        """

    def getComplexDisplacement(
        self, stateset: GNSStateSet, state: GNSState | None = None
    ) -> tuple[float, float, float, float, float, float]:
        """Return the node's complex displacement for a given state set and state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set the displacement is evaluated in.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        tuple of float
            The real and imaginary displacement components, reported in the order
            ``(xr, yr, zr, rr, xi, yi, zi, ir)`` where the ``*r`` values are the
            real parts (and magnitude) and the ``*i`` values the imaginary parts.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> node.getComplexDisplacement(stateset, state)
        """

    def getConnectedList(
        self, level: int = 1, type: Element = ...
    ) -> list[GNSElement | GNSRbeElement]:
        """Return items connected to this node up to a connectivity level.

        Parameters
        ----------
        level : int, optional
            Connectivity depth ``>= 0`` up to and including which neighbours are
            collected. A ``level`` of ``0`` returns all connected neighbours.
            Default is ``1``.
        type : Element, optional
            Element-type and entity-type flags selecting which neighbours to
            return; combine flags with ``|``. Default is ``Element`` (all types).

        Returns
        -------
        list of GNSElement or GNSRbeElement
            The connected item handles. The concrete type of each item depends on
            the requested ``type``.

        Examples
        --------
        >>> node.getConnectedList()
        """

    def getFunctionValues(
        self,
        stateset: GNSStateSet,
        function: GNSFunction,
        state: GNSState | None = None,
    ) -> list[float]:
        """Return result-function values at this node for the active view.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate in.
        function : GNSFunction
            The result function to evaluate.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        list of float
            The function values. The shape depends on the function type: a scalar
            function yields a single value; a vector function yields the
            components followed by the magnitude ``(Vx, Vy, Vz, Vmag)``; a tensor
            function yields 12 values, the first 9 being three eigenvectors and
            the last 3 the corresponding eigenvalues.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> node.getFunctionValues(stateset, func, state)
        """

    def getComplexFunctionValues(
        self,
        stateset: GNSStateSet,
        function: GNSFunction,
        state: GNSState | None = None,
    ) -> list[tuple[float, float]]:
        """Return complex result-function values at this node for the active view.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate in.
        function : GNSFunction
            The result function to evaluate.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        list of tuple of float
            One ``(real, imaginary)`` pair per component. A scalar function yields
            one pair; a vector function yields pairs in ``(x, y, z)`` order; a
            tensor function yields pairs in ``(xx, yy, zz, xy, xz, yz)`` order.

        Notes
        -----
        For function values with swing states, values for state 1 are returned.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> node.getComplexFunctionValues(stateset, func, state)
        """

    def getElementList(self, filter: str | None = None) -> list[GNSElement]:
        """Return the elements connected to this node.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSElement
            The connected element handles.

        Examples
        --------
        >>> elist = node.getElementList()
        """

    def getNormalDirection(self, modelview: GNSModelView) -> tuple[float, float, float]:
        """Return the node normal direction in a model view.

        The normal is computed with the "Mean Weighted by Sine and Edge Length
        Reciprocal" (MWSELR) algorithm.

        Parameters
        ----------
        modelview : GNSModelView
            The model view to evaluate the normal in.

        Returns
        -------
        tuple of float
            The normal direction ``(x, y, z)``.

        Examples
        --------
        >>> view = gns.getViewList(type=gnspy.View.Model)[0]
        >>> normal = node.getNormalDirection(view)
        """

class GNSElement:
    """Handle to a single finite element of a loaded model.

    An element exposes its identity, type, owning module and slot, its property
    and nodes, its connectivity, visibility, failure state, and result-function
    values (including top/bottom shell values).

    Notes
    -----
    Element handles are not constructed directly. Obtain one from a ``GNSSlot``
    (for example ``slot.getElementById(100)`` or ``slot.getElementList()``) or
    from a ``GNSModule`` (``module.getElementById(100)``).

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> element = slot.getElementById(100)
    >>> element_id = element.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this element.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = element.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this element.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = element.getSlot()
        """

    def getId(self) -> int:
        """Return the element's user id.

        Returns
        -------
        int
            The user-visible element id.

        Examples
        --------
        >>> element.getId()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module this element belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the element has no module.

        Examples
        --------
        >>> element.getModule()
        """

    def getType(self) -> Element | None:
        """Return the element's type flag.

        Returns
        -------
        Element or None
            The element-type flag, or ``None`` if the element type is unknown.

        Examples
        --------
        >>> element.getType()
        """

    def getProperty(self) -> GNSProperty | None:
        """Return the property assigned to this element.

        Returns
        -------
        GNSProperty or None
            The element's property, or ``None`` if it has none.

        Examples
        --------
        >>> element.getProperty()
        """

    def getPart(self) -> GNSProperty | None:
        """Return the element's property (deprecated).

        .. deprecated::
            Use :meth:`getProperty` instead.

        Returns
        -------
        GNSProperty or None
            The element's property, or ``None`` if it has none.
        """

    def getNodes(self) -> list[GNSNode]:
        """Return the element's nodes.

        Returns
        -------
        list of GNSNode
            The node handles making up this element.

        Examples
        --------
        >>> element.getNodes()
        """

    def getCommandToken(self) -> str:
        """Return the element type's command token.

        Returns
        -------
        str
            The command token identifying the element type.

        Examples
        --------
        >>> element.getCommandToken()
        """

    def getConnectedList(
        self, level: int = 1, type: Element = ...
    ) -> list[GNSElement | GNSRbeElement]:
        """Return items connected to this element up to a connectivity level.

        Parameters
        ----------
        level : int, optional
            Connectivity depth ``>= 0`` up to and including which neighbours are
            collected. A ``level`` of ``0`` returns all connected neighbours.
            Default is ``1``.
        type : Element, optional
            Element-type and entity-type flags selecting which neighbours to
            return; combine flags with ``|``. Default is ``Element`` (all types).

        Returns
        -------
        list of GNSElement or GNSRbeElement
            The connected item handles. The concrete type of each item depends on
            the requested ``type``.

        Examples
        --------
        >>> element.getConnectedList()
        """

    def getConnectedVisibleList(
        self, view: GNSModelView, level: int = 1, type: Element = ...
    ) -> list[GNSElement | GNSRbeElement]:
        """Return visible items connected to this element in a view.

        Parameters
        ----------
        view : GNSModelView
            The model view in which visibility is evaluated.
        level : int, optional
            Connectivity depth ``>= 0`` up to and including which neighbours are
            collected. A ``level`` of ``0`` returns all visible connected
            neighbours. Default is ``1``.
        type : Element, optional
            Element-type and entity-type flags selecting which neighbours to
            return; combine flags with ``|``. Default is ``Element`` (all types).

        Returns
        -------
        list of GNSElement or GNSRbeElement
            The visible connected item handles. The concrete type of each item
            depends on the requested ``type``.

        Examples
        --------
        >>> element.getConnectedVisibleList(view)
        """

    def getFunctionValues(
        self,
        stateset: GNSStateSet,
        function: GNSFunction,
        state: GNSState | None = None,
    ) -> list[float]:
        """Return result-function values on this element for the active view.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate in.
        function : GNSFunction
            The result function to evaluate.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        list of float
            The function values. The shape depends on the function type: a scalar
            function yields a single value; a vector function yields the
            components followed by the magnitude ``(Vx, Vy, Vz, Vmag)``; a tensor
            function yields 12 values, the first 9 being three eigenvectors and
            the last 3 the corresponding eigenvalues.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> element.getFunctionValues(stateset, func, state)
        """

    def getComplexFunctionValues(
        self,
        stateset: GNSStateSet,
        function: GNSFunction,
        state: GNSState | None = None,
    ) -> list[tuple[float, float]]:
        """Return complex result-function values on this element.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate in.
        function : GNSFunction
            The result function to evaluate.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        list of tuple of float
            One ``(real, imaginary)`` pair per component. A scalar function yields
            one pair; a vector function yields pairs in ``(x, y, z)`` order; a
            tensor function yields pairs in ``(xx, yy, zz, xy, xz, yz)`` order.

        Notes
        -----
        For function values with swing states, values for state 1 are returned.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> element.getComplexFunctionValues(stateset, func, state)
        """

    def getTopFunctionValues(
        self, stateset: GNSStateSet, state: GNSState | None = None
    ) -> list[float]:
        """Return top-surface result-function values on this element.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate in.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        list of float
            The top-surface function values. The shape depends on the function
            type: scalar yields a single value; vector yields
            ``(Vx, Vy, Vz, Vmag)``; tensor yields 12 values (three eigenvectors
            followed by three eigenvalues).

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> element.getTopFunctionValues(stateset, state)
        """

    def getBottomFunctionValues(
        self, stateset: GNSStateSet, state: GNSState | None = None
    ) -> list[float]:
        """Return bottom-surface result-function values on this element.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate in.
        state : GNSState or None, optional
            The state to evaluate. If ``None`` (default) or omitted, values are
            returned for the ZERO state.

        Returns
        -------
        list of float
            The bottom-surface function values. The shape depends on the function
            type: scalar yields a single value; vector yields
            ``(Vx, Vy, Vz, Vmag)``; tensor yields 12 values (three eigenvectors
            followed by three eigenvalues).

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> element.getBottomFunctionValues(stateset, state)
        """

    def getFailureState(self, stateset: GNSStateSet) -> GNSState | None:
        """Return the state at which this element failed.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to search for failure.

        Returns
        -------
        GNSState or None
            The state at which the element failed, or ``None`` if it did not fail.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> element.getFailureState(stateset)
        """

    def isVisible(self, modelview: GNSModelView) -> bool | None:
        """Report whether this element is visible in a model view.

        Parameters
        ----------
        modelview : GNSModelView
            The model view to test visibility in.

        Returns
        -------
        bool or None
            ``True`` if the element is visible in the given view, ``False`` if
            not, or ``None`` if visibility cannot be determined.

        Examples
        --------
        >>> element.isVisible(view)
        """

class GNSRbeElement(GNSElement):
    """Handle to a rigid-body (RBE) element of a loaded model.

    Extends :class:`GNSElement` with access to the RBE master node and its
    components, and to the slave nodes with their components and weighting
    factors.

    Notes
    -----
    RBE element handles are not constructed directly. Obtain one from a
    ``GNSSlot`` or ``GNSModule`` by requesting the RBE element type, for example
    ``slot.getElementById(100, type=gnspy.Element.Rbe)``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> rbe = slot.getElementById(100, type=gnspy.Element.Rbe)
    >>> master_node = rbe.getMasterNode()
    """

    def getMasterNode(self) -> GNSNode | None:
        """Return the RBE element's master node.

        Returns
        -------
        GNSNode or None
            The master node, or ``None`` if there is none.

        Examples
        --------
        >>> rbe.getMasterNode()
        """

    def getMasterNodeComponents(self) -> int:
        """Return the number of master-node components.

        Returns
        -------
        int
            The number of constrained components on the master node.

        Examples
        --------
        >>> rbe.getMasterNodeComponents()
        """

    def getNumSlaveNodes(self) -> int:
        """Return the number of slave nodes.

        Returns
        -------
        int
            The count of slave nodes.

        Examples
        --------
        >>> rbe.getNumSlaveNodes()
        """

    def getSlaveNodes(self) -> list[GNSNode]:
        """Return the RBE element's slave nodes.

        Returns
        -------
        list of GNSNode
            The slave node handles.

        Examples
        --------
        >>> rbe.getSlaveNodes()
        """

    def getSlaveComponents(self) -> list[int]:
        """Return the components of each slave node.

        Returns
        -------
        list of int
            The constrained components, one entry per slave node.

        Examples
        --------
        >>> rbe.getSlaveComponents()
        """

    def getSlaveWeights(self) -> list[float]:
        """Return the weighting factor of each slave node.

        Returns
        -------
        list of float
            The weighting factors, one entry per slave node.

        Examples
        --------
        >>> rbe.getSlaveWeights()
        """

class GNSModule:
    """Handle to a model module (assembly sub-tree) of a loaded model.

    A module groups model entities and can act as a command target. It provides
    lookup of child modules, nodes, elements, properties, materials, boundary
    conditions (SPC/MPC), loads (force/moment), coordinate systems, layers,
    groups, curves and impact points that belong to it.

    Notes
    -----
    Module handles are not constructed directly. Obtain one from a ``GNSSlot``,
    for example ``slot.getModulesByName("Wheel")[0]`` or
    ``slot.getDefaultModule()``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> module = slot.getModulesByName("Wheel")[0]
    >>> mpids = module.getPropertyList()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this module.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = module.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this module.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = module.getSlot()
        """

    def getParent(self) -> GNSModule | None:
        """Return this module's parent module.

        Returns
        -------
        GNSModule or None
            The parent module, or ``None`` for the root module.

        Examples
        --------
        >>> parent_module = module.getParent()
        """

    def getName(self) -> str:
        """Return the module name.

        Returns
        -------
        str
            The module name. For the root module the real module name is
            returned even though dialogs display the symbolic name ``'/'``; both
            names may be used in commands.

        Examples
        --------
        >>> name = module.getName()
        """

    def getId(self) -> int:
        """Return the module id.

        Returns
        -------
        int
            The module id.

        Examples
        --------
        >>> module.getId()
        """

    def getNodeById(self, id: int) -> GNSNode | None:
        """Return the node with the given user id.

        Parameters
        ----------
        id : int
            The user id of the node.

        Returns
        -------
        GNSNode or None
            The node handle, or ``None`` if no node has that id.

        Examples
        --------
        >>> node = module.getNodeById(100)
        """

    # Deprecated: use getNodeById. Signature mirrors that typed sibling.
    def getNode(self, id: int) -> GNSNode | None:
        """Return the node with the given user id (deprecated).

        .. deprecated::
            Use :meth:`getNodeById` instead.

        Parameters
        ----------
        id : int
            The user id of the node.

        Returns
        -------
        GNSNode or None
            The node handle, or ``None`` if no node has that id.
        """

    def getNodeList(self, filter: str | None = None) -> list[GNSNode]:
        """Return the module's nodes.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSNode
            The matching node handles.

        Examples
        --------
        >>> nodes = module.getNodeList()
        """

    def getChildModules(self) -> list[GNSModule]:
        """Return all child modules.

        Returns
        -------
        list of GNSModule
            The child module handles.

        Examples
        --------
        >>> module.getChildModules()
        """

    def getChildModuleByName(self, name: str) -> GNSModule | None:
        """Return the child module with the given name.

        Parameters
        ----------
        name : str
            The child module name.

        Returns
        -------
        GNSModule or None
            The child module, or ``None`` if none has that name.

        Examples
        --------
        >>> chmodule = module.getChildModuleByName("Tyre")
        """

    def getChildModuleById(self, id: int) -> GNSModule | None:
        """Return the child module with the given user id.

        Parameters
        ----------
        id : int
            The child module user id.

        Returns
        -------
        GNSModule or None
            The child module, or ``None`` if none has that id.

        Examples
        --------
        >>> module.getChildModuleById(2)
        """

    # Deprecated: use getElementById. Signature mirrors that typed sibling.
    def getElement(self, id: int, type: Element = ...) -> GNSElement | None:
        """Return the element with the given id and (optionally) type (deprecated).

        .. deprecated::
            Use :meth:`getElementById` instead.

        Parameters
        ----------
        id : int
            The user id of the element.
        type : Element, optional
            Element-type flag the element must match. Default is ``Element.All``
            (any type).

        Returns
        -------
        GNSElement or None
            The element handle, or ``None`` if no element matches the id and type.
        """

    def getElementById(self, id: int, type: Element = ...) -> GNSElement | None:
        """Return the element with the given id and (optionally) type.

        Parameters
        ----------
        id : int
            The user id of the element.
        type : Element, optional
            Element-type flag the element must match. Default is ``Element.All``
            (any type).

        Returns
        -------
        GNSElement or None
            The element handle, or ``None`` if no element matches the id and type.

        Examples
        --------
        >>> elem = module.getElementById(100, type=gnspy.Element.Hexa)
        """

    def getElementList(self, type: Element = ..., filter: str | None = None) -> list[GNSElement]:
        """Return the module's elements, optionally filtered by type.

        Parameters
        ----------
        type : Element, optional
            Element-type flags selecting which elements to return; combine flags
            with ``|``. Default is ``Element.All`` (every type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSElement
            The matching element handles.

        Examples
        --------
        >>> elist = module.getElementList(type=gnspy.Element.Hexa | gnspy.Element.Rbe)
        """

    def getPropertyById(self, id: int) -> GNSProperty | None:
        """Return the property with the given id.

        Parameters
        ----------
        id : int
            The property user id.

        Returns
        -------
        GNSProperty or None
            The property handle, or ``None`` if none has that id.

        Examples
        --------
        >>> prop1 = module.getPropertyById(100)
        """

    def getPropertyByName(self, name: str) -> GNSProperty | None:
        """Return the property with the given name.

        Parameters
        ----------
        name : str
            The property name.

        Returns
        -------
        GNSProperty or None
            The property handle, or ``None`` if none has that name.

        Examples
        --------
        >>> prop2 = module.getPropertyByName("Shell_Prop")
        """

    def getPropertyList(self, type: Property = ..., filter: str | None = None) -> list[GNSProperty]:
        """Return the module's properties, optionally filtered by type.

        Parameters
        ----------
        type : Property, optional
            Property-type flags selecting which properties to return; combine
            flags with ``|``. Default is ``Property.All`` (every type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSProperty
            The matching property handles.

        Examples
        --------
        >>> plist = module.getPropertyList(type=gnspy.Element.Quad | gnspy.Element.Bar)
        """

    def getMaterialById(self, id: int) -> GNSMaterial | None:
        """Return the material with the given id.

        Parameters
        ----------
        id : int
            The material user id.

        Returns
        -------
        GNSMaterial or None
            The material handle, or ``None`` if none has that id.

        Examples
        --------
        >>> mat = module.getMaterialById(100)
        """

    def getMaterialByName(self, name: str) -> GNSMaterial | None:
        """Return the material with the given name.

        Parameters
        ----------
        name : str
            The material name.

        Returns
        -------
        GNSMaterial or None
            The material handle, or ``None`` if none has that name.

        Examples
        --------
        >>> mat = module.getMaterialByName("Shell_Material")
        """

    def getMaterialList(self, filter: str | None = None) -> list[GNSMaterial]:
        """Return the module's materials.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMaterial
            The matching material handles.

        Examples
        --------
        >>> matlist = module.getMaterialList()
        """

    # Deprecated: use getSpcById. Signature mirrors that typed sibling.
    def getSpc(self, id: int) -> GNSSpc | None:
        """Return the single-point constraint with the given id (deprecated).

        .. deprecated::
            Use :meth:`getSpcById` instead.

        Parameters
        ----------
        id : int
            The SPC user id.

        Returns
        -------
        GNSSpc or None
            The SPC handle, or ``None`` if none has that id.
        """

    def getSpcById(self, id: int) -> GNSSpc | None:
        """Return the single-point constraint with the given id.

        Parameters
        ----------
        id : int
            The SPC user id.

        Returns
        -------
        GNSSpc or None
            The SPC handle, or ``None`` if none has that id.

        Examples
        --------
        >>> spc = module.getSpcById(100)
        """

    def getSpcList(self, filter: str | None = None) -> list[GNSSpc]:
        """Return the module's single-point constraints.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSpc
            The matching SPC handles.

        Examples
        --------
        >>> spclist = module.getSpcList()
        """

    # Deprecated: use getMpcById. Signature mirrors that typed sibling.
    def getMpc(self, id: int) -> GNSMpc | None:
        """Return the multi-point constraint with the given id (deprecated).

        .. deprecated::
            Use :meth:`getMpcById` instead.

        Parameters
        ----------
        id : int
            The MPC user id.

        Returns
        -------
        GNSMpc or None
            The MPC handle, or ``None`` if none has that id.
        """

    def getMpcById(self, id: int) -> GNSMpc | None:
        """Return the multi-point constraint with the given id.

        Parameters
        ----------
        id : int
            The MPC user id.

        Returns
        -------
        GNSMpc or None
            The MPC handle, or ``None`` if none has that id.

        Examples
        --------
        >>> mpc = module.getMpcById(100)
        """

    def getMpcList(self, filter: str | None = None) -> list[GNSMpc]:
        """Return the module's multi-point constraints.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMpc
            The matching MPC handles.

        Examples
        --------
        >>> mpclist = module.getMpcList()
        """

    # Deprecated: use getForceById. Signature mirrors that typed sibling.
    def getForce(self, id: int) -> GNSForce | None:
        """Return the force with the given id (deprecated).

        .. deprecated::
            Use :meth:`getForceById` instead.

        Parameters
        ----------
        id : int
            The force user id.

        Returns
        -------
        GNSForce or None
            The force handle, or ``None`` if none has that id.
        """

    def getForceById(self, id: int) -> GNSForce | None:
        """Return the force with the given id.

        Parameters
        ----------
        id : int
            The force user id.

        Returns
        -------
        GNSForce or None
            The force handle, or ``None`` if none has that id.

        Examples
        --------
        >>> force = module.getForceById(100)
        """

    def getForceList(self, filter: str | None = None) -> list[GNSForce]:
        """Return the module's forces.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSForce
            The matching force handles.

        Examples
        --------
        >>> forcelist = module.getForceList()
        """

    # Deprecated: use getMomentById. Signature mirrors that typed sibling.
    def getMoment(self, id: int) -> GNSMoment | None:
        """Return the moment with the given id (deprecated).

        .. deprecated::
            Use :meth:`getMomentById` instead.

        Parameters
        ----------
        id : int
            The moment user id.

        Returns
        -------
        GNSMoment or None
            The moment handle, or ``None`` if none has that id.
        """

    def getMomentById(self, id: int) -> GNSMoment | None:
        """Return the moment with the given id.

        Parameters
        ----------
        id : int
            The moment user id.

        Returns
        -------
        GNSMoment or None
            The moment handle, or ``None`` if none has that id.

        Examples
        --------
        >>> moment = module.getMomentById(100)
        """

    def getMomentList(self, filter: str | None = None) -> list[GNSMoment]:
        """Return the module's moments.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMoment
            The matching moment handles.

        Examples
        --------
        >>> momentlist = module.getMomentList()
        """

    # Deprecated: use getCoordById. Signature mirrors that typed sibling.
    def getCoord(self, id: int) -> GNSCoord | None:
        """Return the coordinate system with the given id (deprecated).

        .. deprecated::
            Use :meth:`getCoordById` instead.

        Parameters
        ----------
        id : int
            The coordinate-system user id.

        Returns
        -------
        GNSCoord or None
            The coordinate-system handle, or ``None`` if none has that id.
        """

    def getCoordById(self, id: int) -> GNSCoord | None:
        """Return the coordinate system with the given id.

        Parameters
        ----------
        id : int
            The coordinate-system user id.

        Returns
        -------
        GNSCoord or None
            The coordinate-system handle, or ``None`` if none has that id.

        Examples
        --------
        >>> coord = module.getCoordById(100)
        """

    def getCoordList(self, filter: str | None = None) -> list[GNSCoord]:
        """Return the module's coordinate systems.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSCoord
            The matching coordinate-system handles.

        Examples
        --------
        >>> coordlist = module.getCoordList()
        """

    # Deprecated: use getLayerByName or getLayerByProperty. The overloads mirror
    # those two typed sibling factories (lookup by name or by property).
    @typing.overload
    def getLayer(self, name: str) -> GNSLayer | None: ...
    @typing.overload
    def getLayer(self, prop: GNSProperty) -> GNSLayer | None: ...
    def getLayerByName(self, name: str) -> GNSLayer | None:
        """Return the layer with the given name.

        Parameters
        ----------
        name : str
            The layer name.

        Returns
        -------
        GNSLayer or None
            The layer handle, or ``None`` if none has that name.

        Examples
        --------
        >>> layer = module.getLayerByName("Shell_Layer")
        """

    def getLayerByProperty(self, prop: GNSProperty) -> GNSLayer | None:
        """Return the layer that contains the given property.

        Parameters
        ----------
        prop : GNSProperty
            The property whose layer is sought.

        Returns
        -------
        GNSLayer or None
            The layer handle, or ``None`` if no layer has that property.

        Examples
        --------
        >>> prop = module.getPropertyByName("Shell")
        >>> layer = module.getLayerByProperty(prop)
        """

    def getLayerList(self, filter: str | None = None) -> list[GNSLayer]:
        """Return the module's layers.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSLayer
            The matching layer handles.

        Examples
        --------
        >>> layerlist = module.getLayerList()
        """

    # Deprecated: use getGroupByName. Signature mirrors that typed sibling.
    def getGroup(self, name: str) -> GNSGroup | None:
        """Return the group with the given name (deprecated).

        .. deprecated::
            Use :meth:`getGroupByName` instead.

        Parameters
        ----------
        name : str
            The group name.

        Returns
        -------
        GNSGroup or None
            The group handle, or ``None`` if none has that name.
        """

    def getGroupByName(self, name: str) -> GNSGroup | None:
        """Return the group with the given name.

        Parameters
        ----------
        name : str
            The group name.

        Returns
        -------
        GNSGroup or None
            The group handle, or ``None`` if none has that name.

        Examples
        --------
        >>> group = module.getGroupByName("Shell_Group")
        """

    def getGroupList(self, filter: str | None = None) -> list[GNSGroup]:
        """Return the module's groups.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching group handles.

        Examples
        --------
        >>> grouplist = module.getGroupList()
        """

    def getGroupListByProperty(
        self, prop: GNSProperty, filter: str | None = None
    ) -> list[GNSGroup]:
        """Return the groups that contain a given property.

        Parameters
        ----------
        prop : GNSProperty
            The property whose containing groups are sought.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching group handles.

        Examples
        --------
        >>> prop = slot.getPropertyList()[0]
        >>> grouplist = module.getGroupListByProperty(prop)
        """

    def getGroupListByNode(
        self, node: GNSNode, indirect: bool = True, filter: str | None = None
    ) -> list[GNSGroup]:
        """Return the groups that contain a given node.

        Parameters
        ----------
        node : GNSNode
            The node whose containing groups are sought.
        indirect : bool, optional
            If ``True`` (default), also match groups that contain the node
            indirectly through a property or element.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching group handles.

        Examples
        --------
        >>> node = module.getNodeList()[0]
        >>> grouplist = module.getGroupListByNode(node)
        """

    def getGroupListByElement(
        self, element: GNSElement, indirect: bool = True, filter: str | None = None
    ) -> list[GNSGroup]:
        """Return the groups that contain a given element.

        Parameters
        ----------
        element : GNSElement
            The element whose containing groups are sought.
        indirect : bool, optional
            If ``True`` (default), also match groups that contain the element
            indirectly through a property.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching group handles.

        Examples
        --------
        >>> elem = slot.getElementList()[0]
        >>> grouplist = module.getGroupListByElement(elem)
        """

    def getCurveById(self, id: int) -> GNSCurve | None:
        """Return the curve with the given id.

        Parameters
        ----------
        id : int
            The curve user id.

        Returns
        -------
        GNSCurve or None
            The curve handle, or ``None`` if none has that id.

        Examples
        --------
        >>> curve = module.getCurveById(100)
        """

    def getCurveByName(self, name: str) -> GNSCurve | None:
        """Return the curve with the given name.

        Parameters
        ----------
        name : str
            The curve name.

        Returns
        -------
        GNSCurve or None
            The curve handle, or ``None`` if none has that name.

        Examples
        --------
        >>> curve = module.getCurveByName("Shell_Curve")
        """

    def getColor(self, modelview: GNSModelView) -> GNSColor:
        """Return the module's color in a model view.

        Parameters
        ----------
        modelview : GNSModelView
            The model view to read the color from.

        Returns
        -------
        GNSColor
            The module color.

        Examples
        --------
        >>> view = gns.getViewByName("Model")
        >>> color = module.getColor(view)
        """

    def getImpactPointById(self, id: int) -> GNSImpactPoint | None:
        """Return the impact point with the given id.

        Parameters
        ----------
        id : int
            The impact-point user id.

        Returns
        -------
        GNSImpactPoint or None
            The impact-point handle, or ``None`` if none has that id.

        Examples
        --------
        >>> impactpoint = module.getImpactPointById(1)
        """

    def getImpactPointByName(self, name: str) -> GNSImpactPoint | None:
        """Return the impact point with the given name.

        Parameters
        ----------
        name : str
            The impact-point name.

        Returns
        -------
        GNSImpactPoint or None
            The impact-point handle, or ``None`` if none has that name.

        Examples
        --------
        >>> impactpoint = module.getImpactPointByName("Impact_Point1")
        """

    def getImpactPointList(self, filter: str | None = None) -> list[GNSImpactPoint]:
        """Return the module's impact points.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSImpactPoint
            The matching impact-point handles.

        Examples
        --------
        >>> impactpoints = module.getImpactPointList()
        """

class GNSGroup:
    """Handle to a named group of a loaded model.

    A group collects properties, elements and nodes (directly or by reference)
    and may form a parent/child hierarchy.

    Notes
    -----
    Group handles are not constructed directly. Obtain one from a ``GNSSlot``
    (for example ``slot.getGroupByName("shell_group")``) or from a ``GNSModule``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> group = slot.getGroupByName("shell_group")
    >>> elems = group.getElementList()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this group.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = group.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this group.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = group.getSlot()
        """

    def getId(self) -> int:
        """Return the group id.

        Returns
        -------
        int
            The group id.

        Examples
        --------
        >>> group.getId()
        """

    def getName(self) -> str:
        """Return the group name.

        Returns
        -------
        str
            The group name.

        Examples
        --------
        >>> group.getName()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module this group belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the group has no module.

        Examples
        --------
        >>> group.getModule()
        """

    def getPropertyList(self, type: Property = ..., filter: str | None = None) -> list[GNSProperty]:
        """Return the group's properties, optionally filtered by type.

        Parameters
        ----------
        type : Property, optional
            Property-type flags selecting which properties to return; combine
            flags with ``|``. Default is ``Property.All`` (every type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSProperty
            The matching property handles.

        Examples
        --------
        >>> group.getPropertyList()
        """

    def getElementList(self, type: Element = ..., filter: str | None = None) -> list[GNSElement]:
        """Return the group's elements, optionally filtered by type.

        Parameters
        ----------
        type : Element, optional
            Element-type flags selecting which elements to return; combine flags
            with ``|``. Default is ``Element.All`` (every type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSElement
            The matching element handles.

        Examples
        --------
        >>> group.getElementList()
        """

    def getReferencedElementList(
        self, type: Element = ..., filter: str | None = None
    ) -> list[GNSElement]:
        """Return the group's elements including those referenced via properties.

        Like :meth:`getElementList`, but properties held by the group are also
        expanded to their elements.

        Parameters
        ----------
        type : Element, optional
            Element-type flags selecting which elements to return; combine flags
            with ``|``. Default is ``Element.All`` (every type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSElement
            The matching element handles, including referenced elements.

        Examples
        --------
        >>> group.getReferencedElementList()
        """

    def getNodeList(self, filter: str | None = None) -> list[GNSNode]:
        """Return the group's nodes.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSNode
            The matching node handles.

        Examples
        --------
        >>> group.getNodeList()
        """

    def getReferencedNodeList(self, filter: str | None = None) -> list[GNSNode]:
        """Return the group's nodes including those referenced via elements.

        Like :meth:`getNodeList`, but elements and properties held by the group
        are also expanded to their nodes.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSNode
            The matching node handles, including referenced nodes.

        Examples
        --------
        >>> group.getReferencedNodeList()
        """

    def getParent(self) -> GNSGroup | None:
        """Return this group's parent group.

        Returns
        -------
        GNSGroup or None
            The parent group, or ``None`` if the group has no parent.

        Examples
        --------
        >>> group.getParent()
        """

    def getChildren(self, filter: str | None = None) -> list[GNSGroup]:
        """Return this group's child groups.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSGroup
            The matching child group handles.

        Examples
        --------
        >>> group.getChildren()
        """

class GNSLayer:
    """Handle to a layer of a loaded model.

    A layer collects properties and may form a parent/child hierarchy. It also
    exposes layer- and pid-level attributes and its display color.

    Notes
    -----
    Layer handles are not constructed directly. Obtain one from a ``GNSSlot``
    (for example ``slot.getLayerByName("hood")``) or from a ``GNSModule``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> layer = slot.getLayerByName("hood")
    >>> pids = layer.getPropertyList()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this layer.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = layer.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this layer.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = layer.getSlot()
        """

    def getName(self) -> str:
        """Return the layer name.

        Returns
        -------
        str
            The layer name.

        Examples
        --------
        >>> layer.getName()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module this layer belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the layer has no module.

        Examples
        --------
        >>> layer.getModule()
        """

    def getPropertyList(self, type: Property = ..., filter: str | None = None) -> list[GNSProperty]:
        """Return the layer's properties, optionally filtered by type.

        Parameters
        ----------
        type : Property, optional
            Property-type flags selecting which properties to return; combine
            flags with ``|``. Default is ``Property.All`` (every type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSProperty
            The matching property handles.

        Examples
        --------
        >>> layer.getPropertyList()
        """

    def getParent(self) -> GNSLayer | None:
        """Return this layer's parent layer.

        Returns
        -------
        GNSLayer or None
            The parent layer, or ``None`` if the layer has no parent.

        Examples
        --------
        >>> layer.getParent()
        """

    def getChildren(self, filter: str | None = None) -> list[GNSLayer]:
        """Return this layer's child layers.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSLayer
            The matching child layer handles.

        Examples
        --------
        >>> layer.getChildren()
        """

    def getLayerAttributes(self) -> dict[str, str]:
        """Return the layer's attributes.

        Returns
        -------
        dict of str to str
            The layer attributes keyed by attribute name.

        Examples
        --------
        >>> layer.getLayerAttributes()
        """

    def getPidAttributes(self) -> dict[int, str]:
        """Return the layer's per-pid attributes.

        Returns
        -------
        dict of int to str
            The pid attributes keyed by pid.

        Examples
        --------
        >>> layer.getPidAttributes()
        """

    def getColor(self, modelview: GNSModelView) -> GNSColor:
        """Return the layer's color in a model view.

        Parameters
        ----------
        modelview : GNSModelView
            The model view to read the color from.

        Returns
        -------
        GNSColor
            The layer color.

        Examples
        --------
        >>> view = gns.getViewByName("Model")
        >>> color = layer.getColor(view)
        """

class GNSSection:
    """Handle to a section (cut plane) definition of a loaded model.

    A section describes a circular or rectangular cutting plane and reports its
    geometry (base point, normal, dimensions) and its reaction force for a state.

    Notes
    -----
    Section handles are not constructed directly. Obtain one from a ``GNSSlot``,
    for example ``slot.getSectionById(100)``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> sec = slot.getSectionById(100)
    >>> section_id = sec.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this section.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = section.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this section.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = section.getSlot()
        """

    def getId(self) -> int:
        """Return the section id.

        Returns
        -------
        int
            The section id.

        Examples
        --------
        >>> section.getId()
        """

    def getName(self) -> str:
        """Return the section name.

        Returns
        -------
        str
            The section name.

        Examples
        --------
        >>> section.getName()
        """

    def getBasePoint(self) -> tuple[float, float, float]:
        """Return the section's base point on the cut plane.

        Returns
        -------
        tuple of float
            The base point ``(x, y, z)``.

        Examples
        --------
        >>> section.getBasePoint()
        """

    def getNormalDirection(self) -> tuple[float, float, float]:
        """Return the section's normal direction.

        Returns
        -------
        tuple of float
            The normal direction ``(x, y, z)``.

        Examples
        --------
        >>> section.getNormalDirection()
        """

    def getNormalHead(self) -> tuple[float, float, float]:
        """Return the head position of the section normal.

        Returns
        -------
        tuple of float
            The normal head position ``(x, y, z)``.

        Examples
        --------
        >>> section.getNormalHead()
        """

    def getGroupName(self) -> str:
        """Return the name of the group related to this section.

        Returns
        -------
        str
            The related group name.

        Examples
        --------
        >>> section.getGroupName()
        """

    def getSectionType(self) -> str:
        """Return the section shape type.

        Returns
        -------
        str
            The section type, either ``"circular"`` or ``"rectangular"``.

        Examples
        --------
        >>> section.getSectionType()
        """

    def getForce(self, stateset: GNSStateSet, state: GNSState) -> tuple[float, float, float, float]:
        """Return the section reaction-force vector for a state set and state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate in.
        state : GNSState
            The state to evaluate.

        Returns
        -------
        tuple of float
            The force vector ``(i, j, k, m)`` where ``i, j, k`` are the direction
            components and ``m`` is the magnitude.

        Examples
        --------
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> section.getForce(stateset, state)
        """

    def getRadius(self) -> float:
        """Return the radius of a circular cut plane.

        Returns
        -------
        float
            The radius of the circular cut plane; ``0`` denotes an infinite
            (unbounded) plane.

        Examples
        --------
        >>> section.getRadius()
        """

    def getRectHeadPosition(self) -> tuple[float, float, float]:
        """Return the head position of a rectangular section's edge vector.

        Returns
        -------
        tuple of float
            The edge-vector head position ``(x, y, z)``.

        Examples
        --------
        >>> section.getRectHeadPosition()
        """

    def getRectDimensions(self) -> tuple[float, float] | None:
        """Return the edge lengths of a rectangular section.

        Returns
        -------
        tuple of float or None
            The edge lengths ``(a, b)``, or ``None`` if the section is not
            rectangular.

        Examples
        --------
        >>> section.getRectDimensions()
        """

class GNSCrossSection:
    """Handle to a cross-section display object of a model view.

    A cross section exposes its activation and display state (cutting line, pid
    color mode, solid drawing, force display), its geometry vectors (position and
    normal), and its reaction force vector.

    Notes
    -----
    Cross-section handles are not constructed directly. Obtain one from a
    ``GNSModelView``, for example ``view.getCrossSection(slot, 1)``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> view = gns.getViewList()[0]
    >>> cs = view.getCrossSection(slot, 1)
    >>> cs_tail = cs.getTailPositionVector()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this cross section.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = cs.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this cross section.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = cs.getSlot()
        """

    def getId(self) -> int:
        """Return the cross-section id.

        Returns
        -------
        int
            The cross-section id.

        Examples
        --------
        >>> cs.getId()
        """

    def getActivationState(self) -> str:
        """Return the cross-section activation state.

        Returns
        -------
        str
            Either ``"on"`` or ``"off"``.

        Examples
        --------
        >>> cs.getActivationState()
        """

    def getType(self) -> str:
        """Return the cross-section type.

        Returns
        -------
        str
            Either ``"Lagrange"`` or ``"Euler"``.

        Examples
        --------
        >>> cs.getType()
        """

    def getGeomDisplayType(self) -> str:
        """Return the model-geometry display type of the cross section.

        Returns
        -------
        str
            One of ``"hide"``, ``"cut"`` or ``"show"``.

        Examples
        --------
        >>> cs.getGeomDisplayType()
        """

    def getCuttingLineStatus(self) -> str:
        """Return whether the cutting line is displayed.

        Returns
        -------
        str
            Either ``"on"`` or ``"off"``.

        Examples
        --------
        >>> cs.getCuttingLineStatus()
        """

    def getCuttingLineWidth(self) -> float:
        """Return the cutting-line width.

        Returns
        -------
        float
            The cutting-line width.

        Examples
        --------
        >>> cs.getCuttingLineWidth()
        """

    def getCuttingLineStyle(self) -> str:
        """Return the cutting-line stippling style.

        Returns
        -------
        str
            The cutting-line stippling (style) name.

        Examples
        --------
        >>> cs.getCuttingLineStyle()
        """

    def getCuttingLineColor(self) -> list[float]:
        """Return the cutting-line color.

        Returns
        -------
        list of float
            The RGBA components of the cutting-line color.

        Examples
        --------
        >>> cs.getCuttingLineColor()
        """

    def getPidColorModeStatus(self) -> str:
        """Return whether pid color mode is active.

        Returns
        -------
        str
            Either ``"on"`` or ``"off"``.

        Examples
        --------
        >>> cs.getPidColorModeStatus()
        """

    def getSolidDrawingModeStatus(self) -> str:
        """Return whether solid drawing mode is active.

        Returns
        -------
        str
            Either ``"on"`` or ``"off"``.

        Examples
        --------
        >>> cs.getSolidDrawingModeStatus()
        """

    def getTailPositionVector(self) -> tuple[float, float, float]:
        """Return the position vector of the cross-section plane.

        Returns
        -------
        tuple of float
            The plane's position (tail) vector ``(x, y, z)``.

        Examples
        --------
        >>> cs.getTailPositionVector()
        """

    def getNormalVector(self) -> tuple[float, float, float]:
        """Return the normal vector of the cross-section plane.

        Returns
        -------
        tuple of float
            The plane's normal vector ``(x, y, z)``.

        Examples
        --------
        >>> cs.getNormalVector()
        """

    def getForceVector(self) -> tuple[float, float, float]:
        """Return the cross-section reaction-force vector.

        Returns
        -------
        tuple of float
            The reaction force expressed as magnitude and direction.

        Examples
        --------
        >>> cs.getForceVector()
        """

    def getForceDrawStyle(self) -> str:
        """Return the force-vector display style.

        Returns
        -------
        str
            The force-vector display style name.

        Examples
        --------
        >>> cs.getForceDrawStyle()
        """

class GNSCoord:
    """Handle to a coordinate system of a loaded model.

    A coordinate system exposes its identity, owning slot, transformation matrix,
    type, associated property, attached node and defining nodes.

    Notes
    -----
    Coordinate-system handles are not constructed directly. Obtain one from a
    ``GNSSlot`` (for example ``slot.getCoordById(100)``) or from a ``GNSModule``
    (``module.getCoordById(100)``).

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> coord = slot.getCoordById(100)
    >>> coord_mat = coord.getMatrix()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this coordinate system.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = coord.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this coordinate system.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = coord.getSlot()
        """

    def getId(self) -> int:
        """Return the coordinate system's user id.

        Returns
        -------
        int
            The user-visible coordinate-system id.

        Examples
        --------
        >>> coord.getId()
        """

    def getProperty(self) -> GNSProperty | None:
        """Return the property associated with this coordinate system.

        Returns
        -------
        GNSProperty or None
            The associated property, or ``None`` if it has none.

        Examples
        --------
        >>> coord.getProperty()
        """

    def getPart(self) -> GNSProperty | None:
        """Return the coordinate system's property (deprecated).

        .. deprecated::
            Use :meth:`getProperty` instead.

        Returns
        -------
        GNSProperty or None
            The associated property, or ``None`` if it has none.
        """

    def getAttachedNode(self) -> GNSNode | None:
        """Return the node this coordinate system is attached to.

        Returns
        -------
        GNSNode or None
            The attached node, or ``None`` if none is attached.

        Examples
        --------
        >>> coord.getAttachedNode()
        """

    def getMatrix(self) -> list[float]:
        """Return the coordinate system's transformation matrix.

        Returns
        -------
        list of float
            The matrix entries for this coordinate system.

        Examples
        --------
        >>> coord.getMatrix()
        """

    def getType(self) -> str:
        """Return the coordinate system's type.

        Returns
        -------
        str
            The coordinate-system type.

        Examples
        --------
        >>> coord.getType()
        """

    def getNodes(self) -> list[GNSNode]:
        """Return the nodes that define this coordinate system.

        Returns
        -------
        list of GNSNode
            The defining node handles.

        Examples
        --------
        >>> coord.getNodes()
        """

class GNSProperty:
    """Handle to a model property (base class for all property types).

    A property groups elements that share the same physical definition
    (thickness, material, section, and so on). This base class exposes the
    attributes common to every property type; specialised subclasses such as
    ``GNSBarProperty``, ``GNSShellProperty``, ``GNSSolidProperty``,
    ``GNSMassProperty`` and ``GNSCompositeProperty`` add type-specific queries.

    Notes
    -----
    Property handles are not constructed directly. Obtain them from a
    ``GNSSlot`` (for example ``GNSSlot.getPropertyById`` or
    ``GNSSlot.getPropertyList``) or from a ``GNSModule``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    >>> id = prop.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this property.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = property.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this property.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = property.getSlot()
        """

    def getId(self) -> int:
        """Return the property's user id.

        Returns
        -------
        int
            The user-defined property id.

        Examples
        --------
        >>> prop.getId()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module the property belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the property is not assigned to
            a module.

        Examples
        --------
        >>> prop.getModule()
        """

    def getName(self) -> str:
        """Return the property name.

        Returns
        -------
        str
            The property name.

        Examples
        --------
        >>> prop.getName()
        """

    def getColor(self, modelview: GNSModelView) -> GNSColor:
        """Return the property colour in the given model view.

        Parameters
        ----------
        modelview : GNSModelView
            The model view whose colouring is queried.

        Returns
        -------
        GNSColor
            The property colour.

        Examples
        --------
        >>> view = gns.getViewByName("Model")
        >>> color = prop.getColor(view)
        """

    def getElementList(self, filter: str | None = None) -> list[GNSElement]:
        """Return the property's elements, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            element of the property.

        Returns
        -------
        list of GNSElement
            The matching element handles.

        Examples
        --------
        >>> prop.getElementList()
        """

    def getElementType(self) -> str:
        """Return the element type of the property as a string.

        Returns
        -------
        str
            The element-type mnemonic (for example ``"hex"`` for solid
            elements).

        Examples
        --------
        >>> prop.getElementType()
        """

    def getType(self) -> Element | None:
        """Return the element-type flag of the property.

        Returns
        -------
        Element or None
            The ``Element`` flag describing the property's element type, or
            ``None`` if the element type is unknown.

        Examples
        --------
        >>> prop.getType()
        """

    def getMaterial(self) -> GNSMaterial | None:
        """Return the material assigned to the property.

        Returns
        -------
        GNSMaterial or None
            The assigned material (only for shell, solid, beam and bar
            properties), or ``None`` if no material applies.

        Examples
        --------
        >>> prop.getMaterial()
        """

    def getFunctionValues(
        self,
        stateset: GNSStateSet,
        function: GNSFunction,
        state: GNSState | None = None,
    ) -> list[float]:
        """Return real function values of the property for a result state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate.
        function : GNSFunction
            The result function to evaluate.
        state : GNSState or None, optional
            The state to evaluate; ``None`` (default) evaluates the ZERO
            state.

        Returns
        -------
        list of float
            The function values for the active view, state set, function and
            state.

        Notes
        -----
        The shape of the result depends on the function type:

        * Scalar: a single value, e.g. ``6.3``.
        * Vector: components and magnitude, e.g. ``(Vx, Vy, Vz, Vmag)``.
        * Tensor: 12 values, the first 9 being three eigenvectors and the last
          3 the corresponding eigenvalues.

        Examples
        --------
        >>> view = gns.getViewList()[0]
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> prop.getFunctionValues(stateset, func, state)
        """

    def getComplexFunctionValues(
        self,
        stateset: GNSStateSet,
        function: GNSFunction,
        state: GNSState | None = None,
    ) -> list[tuple[float, float]]:
        """Return complex function values of the property for a result state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate.
        function : GNSFunction
            The result function to evaluate.
        state : GNSState or None, optional
            The state to evaluate; ``None`` (default) evaluates the ZERO
            state.

        Returns
        -------
        list of tuple of float
            Real/imaginary component pairs for the active view, state set,
            function and state.

        Notes
        -----
        The shape of the result depends on the function type:

        * Scalar: a real/imaginary pair, e.g. ``((6.3, 2.8),)``.
        * Vector: real/imaginary pairs in ``(x, y, z)`` order.
        * Tensor: real/imaginary pairs in ``(xx, yy, zz, xy, xz, yz)`` order.

        For function values with swing states, values for state 1 are returned.

        Examples
        --------
        >>> view = gns.getViewList()[0]
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> prop.getComplexFunctionValues(stateset, func, state)
        """

    def getStyle(self, modelview: GNSModelView) -> str:
        """Return the display style of the property in the given model view.

        Parameters
        ----------
        modelview : GNSModelView
            The model view whose style is queried.

        Returns
        -------
        str
            The style mnemonic (for example ``"she"`` for Shaded with Edge).

        Examples
        --------
        >>> view = gns.getViewByName("Model")
        >>> prop.getStyle(view)
        """

class GNSBarProperty(GNSProperty):
    """Handle to a bar (1D) property.

    Represents beam, bar, spring, damper and similar one-dimensional element
    properties. In addition to the inherited ``GNSProperty`` members it exposes
    the bar section area and a textual description of the bar type.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getPropertyById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    >>> sa = prop.getBarSectionArea()
    """

    def getBarSectionArea(self) -> float:
        """Return the sectional area of the bar property.

        Returns
        -------
        float
            The cross-sectional area (only for beam and bar properties).

        Examples
        --------
        >>> prop.getBarSectionArea()
        """

    def getBarDesc(self) -> str:
        """Return a textual description of the bar type.

        Returns
        -------
        str
            The bar type, e.g. ``"Bar"``, ``"Plotel"``, ``"Beam"``,
            ``"Spring"``, ``"Damper"``, ``"Joint"``, ``"Spotweld"`` or
            ``"Connector"``.

        Examples
        --------
        >>> prop.getBarDesc()
        """

class GNSShellProperty(GNSProperty):
    """Handle to a shell (2D) property.

    Represents shell element properties. In addition to the inherited
    ``GNSProperty`` members it exposes the shell thickness and total area.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getPropertyById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    """

    def getThickness(self) -> float:
        """Return the thickness of the shell elements of the property.

        Returns
        -------
        float
            The shell thickness.

        Examples
        --------
        >>> prop.getThickness()
        """

    def getArea(self) -> float:
        """Return the total area of the shell elements of the property.

        Returns
        -------
        float
            The total shell area.

        Examples
        --------
        >>> prop.getArea()
        """

class GNSSolidProperty(GNSProperty):
    """Handle to a solid (3D) property.

    Represents solid element properties. In addition to the inherited
    ``GNSProperty`` members it exposes the total solid volume.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getPropertyById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    """

    def getVolume(self) -> float:
        """Return the total volume of the solid elements of the property.

        Returns
        -------
        float
            The total solid volume.

        Examples
        --------
        >>> prop.getVolume()
        """

class GNSMassProperty(GNSProperty):
    """Handle to a mass property.

    Represents concentrated / lumped mass properties. In addition to the
    inherited ``GNSProperty`` members it exposes the mass value.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getPropertyById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    >>> mass = prop.getMass()
    """

    def getMass(self) -> float:
        """Return the mass value of the property.

        Returns
        -------
        float
            The mass (only for mass properties).

        Examples
        --------
        >>> prop.getMass()
        """

class GNSCompositeProperty(GNSProperty):
    """Handle to a composite property.

    Represents layered composite (laminate) properties. In addition to the
    inherited ``GNSProperty`` members it exposes the ply count, the individual
    plies and the total laminate thickness.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getPropertyById``) or a
    ``GNSModule``; not constructed directly. Individual plies are handled as
    ``GNSCompositePly`` objects.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    >>> plies = prop.getPlyList()
    """

    def getPlyNum(self) -> int:
        """Return the number of plies in the composite.

        Returns
        -------
        int
            The ply count.

        Examples
        --------
        >>> prop.getPlyNum()
        """

    def getPlyList(self, filter: str | None = None) -> list[GNSCompositePly]:
        """Return the composite plies, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every ply.

        Returns
        -------
        list of GNSCompositePly
            The matching ply handles.

        Examples
        --------
        >>> plies = prop.getPlyList()
        """

    def getThickness(self) -> float:
        """Return the total laminate thickness.

        Returns
        -------
        float
            The complete thickness, i.e. the sum of all ply thicknesses.

        Examples
        --------
        >>> prop.getThickness()
        """

class GNSCompositePly:
    """Handle to a single ply of a composite property.

    Exposes the ply's identity, material, thickness, orientation angle and the
    T/R/S direction vectors of its material coordinate system.

    Notes
    -----
    Obtained from a ``GNSCompositeProperty`` via
    ``GNSCompositeProperty.getPlyList``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    >>> plies = prop.getPlyList()
    >>> plymat = plies[0].getMaterial()
    """

    def getId(self) -> int:
        """Return the ply id.

        Returns
        -------
        int
            The composite ply id.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> plyId = ply.getId()
        """

    def getName(self) -> str:
        """Return the ply name.

        Returns
        -------
        str
            The composite ply name.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> plyname = ply.getName()
        """

    def getMaterial(self) -> GNSMaterial | None:
        """Return the material assigned to the ply.

        Returns
        -------
        GNSMaterial or None
            The ply material, or ``None`` if none is assigned.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> plyMat = ply.getMaterial()
        """

    def getThickness(self) -> float:
        """Return the ply thickness.

        Returns
        -------
        float
            The composite ply thickness.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> plyt = ply.getThickness()
        """

    def getOrientationAngle(self) -> float:
        """Return the ply orientation angle.

        Returns
        -------
        float
            The composite ply orientation angle.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> ori_angle = ply.getOrientationAngle()
        """

    def getTDirection(self) -> tuple[float, float, float]:
        """Return the ply T-direction vector.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` components of the T-direction vector.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> tvect = ply.getTDirection()
        """

    def getRDirection(self) -> tuple[float, float, float]:
        """Return the ply R-direction vector.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` components of the R-direction vector.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> rvect = ply.getRDirection()
        """

    def getSDirection(self) -> tuple[float, float, float]:
        """Return the ply S-direction vector.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` components of the S-direction vector.

        Examples
        --------
        >>> ply = prop.getPlyList()[0]
        >>> svect = ply.getSDirection()
        """

class GNSMaterial:
    """Handle to a model material.

    Exposes the material's identity and the physical constants that Animator
    reads from the model (density, Poisson's ratio, Young's modulus), together
    with the properties that reference the material.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getMaterialById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> mat = slot.getMaterialById(100)
    >>> id = mat.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this material.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = material.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this material.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = material.getSlot()
        """

    def getId(self) -> int:
        """Return the material's user id.

        Returns
        -------
        int
            The user-defined material id.

        Examples
        --------
        >>> material.getId()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module the material belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the material is not assigned to
            a module.

        Examples
        --------
        >>> material.getModule()
        """

    def getName(self) -> str:
        """Return the material name.

        Returns
        -------
        str
            The material name.

        Examples
        --------
        >>> material.getName()
        """

    def getPropertyList(self, filter: str | None = None) -> list[GNSProperty]:
        """Return the properties that reference this material, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            referencing property.

        Returns
        -------
        list of GNSProperty
            The matching property handles.

        Examples
        --------
        >>> material.getPropertyList()
        """

    def getColor(self, modelview: GNSModelView) -> GNSColor:
        """Return the material colour in the given model view.

        Parameters
        ----------
        modelview : GNSModelView
            The model view whose colouring is queried.

        Returns
        -------
        GNSColor
            The material colour.

        Examples
        --------
        >>> view = gns.getViewByName("Model")
        >>> color = material.getColor(view)
        """

    def getDensity(self) -> float | None:
        """Return the material density.

        Returns
        -------
        float or None
            The density if available, otherwise ``None``.

        Examples
        --------
        >>> density = material.getDensity()
        """

    def getPoissonsRatio(self) -> float | None:
        """Return the material Poisson's ratio.

        Returns
        -------
        float or None
            The Poisson's ratio if available, otherwise ``None``.

        Examples
        --------
        >>> poissonsRatio = material.getPoissonsRatio()
        """

    def getYoungsModulus(self) -> float | None:
        """Return the material Young's modulus.

        Returns
        -------
        float or None
            The Young's modulus if available, otherwise ``None``.

        Examples
        --------
        >>> youngsModulus = material.getYoungsModulus()
        """

class GNSImpactPoint:
    """Handle to an impact point.

    An impact point is a probe attached to the model (fixed or attached to a
    node/property) whose coordinates, displacement and result values can be
    queried across states.

    Notes
    -----
    Obtained from a ``GNSSlot`` via ``GNSSlot.getImpactPointById``; not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> ip = slot.getImpactPointById(100)
    >>> id = ip.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this impact point.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = impactpoint.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this impact point.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = impactpoint.getSlot()
        """

    def getId(self) -> int:
        """Return the impact point's user id.

        Returns
        -------
        int
            The user-defined impact point id.

        Examples
        --------
        >>> impactpoint.getId()
        """

    def getName(self) -> str:
        """Return the impact point name.

        Returns
        -------
        str
            The impact point name.

        Examples
        --------
        >>> impactpoint.getName()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module the impact point belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the impact point is not assigned
            to a module.

        Examples
        --------
        >>> impactpoint.getModule()
        """

    def getUDefCoordinates(self) -> tuple[float, float, float]:
        """Return the undeformed coordinates of the impact point.

        Returns
        -------
        tuple of float
            The undeformed position as ``(x, y, z)``.

        Examples
        --------
        >>> impactpoint.getUDefCoordinates()
        """

    def getCoordinates(
        self,
        stateset: GNSStateSet,
        state: GNSState,
    ) -> tuple[float, float, float]:
        """Return the coordinates of the impact point for a result state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate.
        state : GNSState
            The state to evaluate.

        Returns
        -------
        tuple of float
            The position as ``(x, y, z)`` for the active view, state set and
            state.

        Examples
        --------
        >>> view = gns.getViewList()[0]
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> impactpoint.getCoordinates(stateset, state)
        """

    def getDisplacement(
        self,
        stateset: GNSStateSet,
        state: GNSState | None = None,
    ) -> tuple[float, float, float]:
        """Return the displacement of the impact point for a result state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate.
        state : GNSState or None, optional
            The state to evaluate; ``None`` (default) evaluates the ZERO
            state.

        Returns
        -------
        tuple of float
            The displacement components ``(x, y, z)`` for the active view,
            state set and state.

        Notes
        -----
        The reference documentation additionally refers to a resultant
        component ``r`` alongside the ``(x, y, z)`` displacement.

        Examples
        --------
        >>> view = gns.getViewList()[0]
        >>> stateset = view.getActiveStateSet(slot)
        >>> state = view.getActiveState(slot)
        >>> impactpoint.getDisplacement(stateset, state)
        """

    def getFunctionValues(
        self,
        stateset: GNSStateSet,
        function: GNSFunction,
        state: GNSState | None = None,
    ) -> list[float]:
        """Return function values of the impact point for a result state.

        Parameters
        ----------
        stateset : GNSStateSet
            The state set to evaluate.
        function : GNSFunction
            The result function to evaluate.
        state : GNSState or None, optional
            The state to evaluate; ``None`` (default) evaluates the ZERO
            state.

        Returns
        -------
        list of float
            The function values for the given or active view, state set,
            function and state.

        Notes
        -----
        The shape of the result depends on the function type:

        * Scalar: a single value, e.g. ``6.3``.
        * Vector: direction and magnitude, e.g. ``(0.3, 0.4, 0.5, 6.3)``.
        * Tensor: eigenvalues and vectors.

        Examples
        --------
        >>> view = gns.getViewList()[0]
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> impactpoint.getFunctionValues(stateset, func, state)
        """

    def getOrientation(self) -> str:
        """Return the impact point orientation.

        Returns
        -------
        str
            The orientation, ``"top"`` or ``"normal"``.

        Examples
        --------
        >>> impactpoint.getOrientation()
        """

    def getStyle(self) -> str:
        """Return the impact point display style.

        Returns
        -------
        str
            The style, ``"2d"`` or ``"3d"``.

        Examples
        --------
        >>> impactpoint.getStyle()
        """

    def getType(self) -> str:
        """Return the impact point type.

        Returns
        -------
        str
            The type, ``"fixed"`` or ``"attached"``.

        Examples
        --------
        >>> impactpoint.getType()
        """

    def getItemType(self) -> str | None:
        """Return the type of item the impact point is attached to.

        Returns
        -------
        str or None
            ``"property"`` or ``"node"`` when the impact point is attached,
            otherwise ``None``.

        Examples
        --------
        >>> impactpoint.getItemType()
        """

    def getItemId(self) -> int | None:
        """Return the user id of the item the impact point is attached to.

        Returns
        -------
        int or None
            The attached item's user id, or ``None`` if the impact point is
            not attached.

        Examples
        --------
        >>> impactpoint.getItemId()
        """

    def getFollowNodes(self) -> list[GNSNode] | None:
        """Return the follow nodes of the impact point.

        Returns
        -------
        list of GNSNode or None
            The follow nodes if set, otherwise ``None``.

        Examples
        --------
        >>> impactpoint.getFollowNodes()
        """

    def getFunctionName(self) -> str | None:
        """Return the name of the function used to colour the impact point.

        Returns
        -------
        str or None
            The function name if function colouring is switched on, otherwise
            ``None``.

        Examples
        --------
        >>> impactpoint.getFunctionName()
        """

class GNSForce:
    """Handle to a concentrated force.

    Exposes the force's identity, the node it acts on, the property it belongs
    to, and its direction and magnitude.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getForceById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> force = slot.getForceById(100)
    >>> id = force.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this force.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = force.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this force.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = force.getSlot()
        """

    def getId(self) -> int:
        """Return the force's user id.

        Returns
        -------
        int
            The user-defined force id.

        Examples
        --------
        >>> force.getId()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module the force belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the force is not assigned to a
            module.

        Examples
        --------
        >>> module = force.getModule()
        """

    def getProperty(self) -> GNSProperty | None:
        """Return the property this force is associated with.

        Returns
        -------
        GNSProperty or None
            The associated property, or ``None`` if none applies.

        Examples
        --------
        >>> force.getProperty()
        """

    def getPart(self) -> GNSProperty | None:
        """Return the property this force is associated with (deprecated).

        Returns
        -------
        GNSProperty or None
            The associated property, or ``None`` if none applies.

        Notes
        -----
        Deprecated. Use ``getProperty`` instead.
        """

    def getNode(self) -> GNSNode:
        """Return the node this force acts on.

        Returns
        -------
        GNSNode
            The node the force is applied to.

        Examples
        --------
        >>> force.getNode()
        """

    def getDirection(self) -> tuple[float, float, float]:
        """Return the force direction vector.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` components of the force direction.

        Examples
        --------
        >>> force.getDirection()
        """

    def getMagnitude(self) -> float:
        """Return the force magnitude.

        Returns
        -------
        float
            The force magnitude.

        Examples
        --------
        >>> force.getMagnitude()
        """

class GNSMoment:
    """Handle to a concentrated moment.

    Exposes the moment's identity, the node it acts on, the property it belongs
    to, and its direction and magnitude.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getMomentById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> moment = slot.getMomentById(100)
    >>> id = moment.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this moment.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = moment.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this moment.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = moment.getSlot()
        """

    def getId(self) -> int:
        """Return the moment's user id.

        Returns
        -------
        int
            The user-defined moment id.

        Examples
        --------
        >>> moment.getId()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module the moment belongs to.

        Returns
        -------
        GNSModule or None
            The owning module, or ``None`` if the moment is not assigned to a
            module.

        Examples
        --------
        >>> module = moment.getModule()
        """

    def getProperty(self) -> GNSProperty | None:
        """Return the property this moment is associated with.

        Returns
        -------
        GNSProperty or None
            The associated property, or ``None`` if none applies.

        Examples
        --------
        >>> moment.getProperty()
        """

    def getPart(self) -> GNSProperty | None:
        """Return the property this moment is associated with (deprecated).

        Returns
        -------
        GNSProperty or None
            The associated property, or ``None`` if none applies.

        Notes
        -----
        Deprecated. Use ``getProperty`` instead.
        """

    def getNode(self) -> GNSNode:
        """Return the node this moment acts on.

        Returns
        -------
        GNSNode
            The node the moment is applied to.

        Examples
        --------
        >>> moment.getNode()
        """

    def getDirection(self) -> tuple[float, float, float]:
        """Return the moment direction vector.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` components of the moment direction.

        Examples
        --------
        >>> moment.getDirection()
        """

    def getMagnitude(self) -> float:
        """Return the moment magnitude.

        Returns
        -------
        float
            The moment magnitude.

        Examples
        --------
        >>> moment.getMagnitude()
        """

class GNSMpc:
    """Handle to a multi-point constraint (MPC).

    Exposes the constraint's identity, the associated property, the master node
    and the slave nodes.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getMpcById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> mpc = slot.getMpcById(100)
    >>> id = mpc.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this MPC.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = mpc.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this MPC.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = mpc.getSlot()
        """

    def getId(self) -> int:
        """Return the MPC's user id.

        Returns
        -------
        int
            The user-defined MPC id.

        Examples
        --------
        >>> mpc.getId()
        """

    def getProperty(self) -> GNSProperty | None:
        """Return the property attached to this MPC.

        Returns
        -------
        GNSProperty or None
            The attached property, or ``None`` if none applies.

        Examples
        --------
        >>> mpc.getProperty()
        """

    def getPart(self) -> GNSProperty | None:
        """Return the property attached to this MPC (deprecated).

        Returns
        -------
        GNSProperty or None
            The attached property, or ``None`` if none applies.

        Notes
        -----
        Deprecated. Use ``getProperty`` instead.
        """

    def getMasterNode(self) -> GNSNode | None:
        """Return the master node of the MPC.

        Returns
        -------
        GNSNode or None
            The master node, or ``None`` if none is defined.

        Examples
        --------
        >>> mpc.getMasterNode()
        """

    def getNumSlaveNodes(self) -> int:
        """Return the number of slave nodes.

        Returns
        -------
        int
            The slave node count.

        Examples
        --------
        >>> mpc.getNumSlaveNodes()
        """

    def getSlaveNodes(self) -> list[GNSNode]:
        """Return the slave nodes of the MPC.

        Returns
        -------
        list of GNSNode
            The slave node handles.

        Examples
        --------
        >>> mpc.getSlaveNodes()
        """

class GNSSpc:
    """Handle to a single-point constraint (SPC).

    Exposes the constraint's identity, the constrained degrees of freedom, the
    associated property and the constrained node.

    Notes
    -----
    Obtained from a ``GNSSlot`` (for example ``GNSSlot.getSpcById``) or a
    ``GNSModule``; not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> spc = slot.getSpcById(100)
    >>> id = spc.getId()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this SPC.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> slotid = spc.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this SPC.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> slot = spc.getSlot()
        """

    def getId(self) -> int:
        """Return the SPC's user id.

        Returns
        -------
        int
            The user-defined SPC id.

        Examples
        --------
        >>> spc.getId()
        """

    def getDOF(self) -> int:
        """Return the constrained degrees of freedom.

        Returns
        -------
        int
            The user-defined degree-of-freedom code.

        Examples
        --------
        >>> spc.getDOF()
        """

    def getProperty(self) -> GNSProperty | None:
        """Return the property attached to this SPC.

        Returns
        -------
        GNSProperty or None
            The attached property, or ``None`` if none applies.

        Examples
        --------
        >>> spc.getProperty()
        """

    def getPart(self) -> GNSProperty | None:
        """Return the property attached to this SPC (deprecated).

        Returns
        -------
        GNSProperty or None
            The attached property, or ``None`` if none applies.

        Notes
        -----
        Deprecated. Use ``getProperty`` instead.
        """

    def getNode(self) -> GNSNode:
        """Return the node this SPC constrains.

        Returns
        -------
        GNSNode
            The constrained node.

        Examples
        --------
        >>> spc.getNode()
        """

class GNSModelScan:
    """GNS model-scan handle object.

    A model-scan handle is the entry point for inspecting a result or database
    file before any data is imported. It exposes the slots, geometry, modules,
    displacements, state sets, states, functions, vectors and tensors that the
    scanned file contains, and can then read selected scan objects into a slot.
    For an Animator database the handle also exposes global/slot external files
    and curves.

    Notes
    -----
    Obtained from ``gns.getModelScanObject(interface, file)``, where ``gns`` is
    the global :class:`GNS` singleton (``gnspy.gns``), ``interface`` is
    the input-interface name (for example ``"Pamcrash"`` or ``"Database4"``) and
    ``file`` is the path to the file to scan.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> sgeom = sslot.getScanGeometry()
    >>> sstset = sslot.getScanStateSetList()[0]
    >>> sdisp = sstset.getScanDisplacements()
    >>> sfuncs = sstset.getScanFunctionList()
    >>> stens = sstset.getScanTensorList()
    >>> modelscan.read(sgeom)
    >>> modelscan.read(sdisp)
    >>> modelscan.read(sfuncs, stens)
    """

    def getScanSlotList(self, filter: str | None = None) -> list[GNSModelScanSlot]:
        """Return the scanned slots, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which slots to return;
            ``None`` (default) returns every scanned slot.

        Returns
        -------
        list of GNSModelScanSlot
            The matching scan-slot handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscan.getScanSlotList()
        """

    def getScanExternalFileList(self, filter: str | None = None) -> list[str]:
        """Return the scanned external file names, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which files to return;
            ``None`` (default) returns every scanned external file.

        Returns
        -------
        list of str
            The matching external file names, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscan.getScanExternalFileList()
        """

    def read(
        self,
        *scan_objects: (
            GNSModelScanSlot
            | GNSModelScanGeom
            | GNSModelScanModule
            | GNSModelScanStSet
            | GNSModelScanDisp
            | GNSModelScanFunc
            | GNSModelScanDbCurve
            | list[object]
            | tuple[object, ...]
        ),
        slot: int | str = "default",
    ) -> tuple[int, str, list[GNSResultVariable]]:
        """Read model data from the given scanned objects into a slot.

        At least one scan object must be supplied; there is no upper limit on the
        number of arguments. Each argument may be an individual scan handle
        (slot, geometry, module, state set, displacement, function or database
        curve) or a ``list``/``tuple`` of such handles.

        Parameters
        ----------
        *scan_objects : scan handle, or list or tuple of scan handles
            One or more scan handles (a :class:`GNSModelScanSlot`,
            :class:`GNSModelScanGeom`, :class:`GNSModelScanModule`,
            :class:`GNSModelScanStSet`, :class:`GNSModelScanDisp`,
            :class:`GNSModelScanFunc` or :class:`GNSModelScanDbCurve`), or
            lists/tuples of such handles, describing the data to read.
        slot : int or str, optional
            Target slot for the imported data. Both a slot id and a slot name are
            accepted. Use ``"new"`` to read into a newly created slot;
            ``"default"`` (the default) reads into the active slot.

        Returns
        -------
        tuple of (int, str, list of GNSResultVariable)
            A status code, a status message, and the result variables created by
            the read.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> geom = modelscan.getScanSlotList()[0].getScanGeometry()
        >>> modelscan.read(geom)
        """

class GNSModelScanSlot:
    """GNS model-scan slot handle object.

    Represents a single slot found in a scanned file. It exposes the slot's
    geometry, modules, state sets, external files and database curves, along with
    the slot's own attributes, and can be read into a slot via
    :meth:`GNSModelScan.read`.

    Notes
    -----
    Obtained from :meth:`GNSModelScan.getScanSlotList`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Database4", "Can.db4")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> modelscan.read(sslot)
    """

    def getLabel(self) -> str:
        """Return the slot label or title.

        Returns
        -------
        str
            The slot's label.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Nastran", "Can.op2")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getLabel()
        """

    def getSubtitle(self) -> str:
        """Return the slot subtitle if available.

        Returns
        -------
        str
            The slot's subtitle, empty if none is available.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Nastran", "Can.op2")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getSubtitle()
        """

    def getId(self) -> int:
        """Return the slot id.

        Returns
        -------
        int
            The slot's numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getId()
        """

    def hasGeometry(self) -> bool:
        """Return whether the scanned slot has any geometry.

        Returns
        -------
        bool
            ``True`` if the slot contains geometry, otherwise ``False``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.hasGeometry()
        """

    def getScanGeometry(self) -> GNSModelScanGeom | None:
        """Return the scanned geometry for this slot.

        Returns
        -------
        GNSModelScanGeom or None
            The geometry scan handle, or ``None`` if the slot has no geometry.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getScanGeometry()
        """

    def getScanExternalFileList(self, filter: str | None = None) -> list[str]:
        """Return the scanned external file names for this slot, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which files to return;
            ``None`` (default) returns every scanned external file.

        Returns
        -------
        list of str
            The matching external file names, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getScanExternalFileList()
        """

    def getScanModuleList(self, filter: str | None = None) -> list[GNSModelScanModule]:
        """Return the scanned modules for this slot, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which modules to return;
            ``None`` (default) returns every scanned module.

        Returns
        -------
        list of GNSModelScanModule
            The matching module scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getScanModuleList()
        """

    def getScanStateSetList(self, filter: str | None = None) -> list[GNSModelScanStSet]:
        """Return the scanned state sets for this slot, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which state sets to return;
            ``None`` (default) returns every scanned state set.

        Returns
        -------
        list of GNSModelScanStSet
            The matching state-set scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getScanStateSetList()
        """

    def getScanDatabaseCurveList(self, filter: str | None = None) -> list[GNSModelScanDbCurve]:
        """Return the scanned database curves for this slot, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which curves to return;
            ``None`` (default) returns every scanned database curve.

        Returns
        -------
        list of GNSModelScanDbCurve
            The matching database-curve scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Database4", "Can.gnsdb")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanslot.getScanDatabaseCurveList()
        """

class GNSModelScanStSet:
    """GNS model-scan state-set handle object.

    Represents a state set found within a scanned slot. It exposes the state
    set's displacements, functions, vectors, tensors and states, along with the
    state set's own attributes, and can be read into a slot via
    :meth:`GNSModelScan.read`.

    Notes
    -----
    Obtained from :meth:`GNSModelScanSlot.getScanStateSetList`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Database4", "Can.db4")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> sstset = sslot.getScanStateSetList()[0]
    >>> sstset.getLabel()
    >>> modelscan.read(sstset)
    """

    def getLabel(self) -> str:
        """Return the scanned state-set label.

        Returns
        -------
        str
            The state set's label.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getLabel()
        """

    def hasDisplacements(self) -> bool:
        """Return whether the scanned state set has any displacements.

        Returns
        -------
        bool
            ``True`` if the state set contains displacements, otherwise ``False``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.hasDisplacements()
        """

    def getScanStateList(self, filter: str | None = None) -> list[GNSModelScanState]:
        """Return the scanned states for this state set, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which states to return;
            ``None`` (default) returns every scanned state.

        Returns
        -------
        list of GNSModelScanState
            The matching state scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getScanStateList()
        """

    def getScanFunctionList(self, filter: str | None = None) -> list[GNSModelScanFunc]:
        """Return the scanned functions for this state set, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which functions to return;
            ``None`` (default) returns every scanned function.

        Returns
        -------
        list of GNSModelScanFunc
            The matching function scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getScanFunctionList()
        """

    def getScanVectorList(self, filter: str | None = None) -> list[GNSModelScanFunc]:
        """Return the scanned vectors for this state set, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which vectors to return;
            ``None`` (default) returns every scanned vector.

        Returns
        -------
        list of GNSModelScanFunc
            The matching vector scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getScanVectorList()
        """

    def getScanTensorList(self, filter: str | None = None) -> list[GNSModelScanFunc]:
        """Return the scanned tensors for this state set, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which tensors to return;
            ``None`` (default) returns every scanned tensor.

        Returns
        -------
        list of GNSModelScanFunc
            The matching tensor scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getScanTensorList()
        """

    def getScanDispFunctionList(self, filter: str | None = None) -> list[GNSModelScanFunc]:
        """Return the scanned displacement functions for this state set, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which functions to return;
            ``None`` (default) returns every scanned displacement function.

        Returns
        -------
        list of GNSModelScanFunc
            The matching displacement-function scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getScanDispFunctionList()
        """

    def getScanSlot(self) -> GNSModelScanSlot:
        """Return the scanned slot that owns this state set.

        Returns
        -------
        GNSModelScanSlot
            The parent scan-slot handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getScanSlot()
        """

    def getScanDisplacements(self) -> GNSModelScanDisp:
        """Return the scanned displacement object for this state set.

        Returns
        -------
        GNSModelScanDisp
            The displacement scan handle for this state set.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstset.getScanDisplacements()
        """

class GNSModelScanState:
    """GNS model-scan state handle object.

    Represents a single state found within a scanned state set or function. It
    exposes the state's id, label, analysis type and owning state set.

    Notes
    -----
    Obtained from :meth:`GNSModelScanStSet.getScanStateList` or
    :meth:`GNSModelScanFunc.getScanStateList`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> sstset = sslot.getScanStateSetList()[0]
    >>> svec = sstset.getScanVectorList()[0]
    >>> state = svec.getScanStateList()[0]
    >>> state.getLabel()
    >>> state.getId()
    """

    def getLabel(self) -> str:
        """Return the scanned state label.

        Returns
        -------
        str
            The state's label.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstate = modelscanstset.getScanStateList()[0]
        >>> modelscanstate.getLabel()
        """

    def getId(self) -> int:
        """Return the scanned state id.

        Returns
        -------
        int
            The state's numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstate = modelscanstset.getScanStateList()[0]
        >>> modelscanstate.getId()
        """

    def getAnalysisType(self) -> str:
        """Return the scanned state analysis type.

        Returns
        -------
        str
            The analysis type of the state, one of ``"STATIC"``,
            ``"TRANSIENT"``, ``"MODAL"`` or ``"FREQUENCY RESPONCE"``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstate = modelscanstset.getScanStateList()[0]
        >>> modelscanstate.getAnalysisType()
        """

    def getScanStateSet(self) -> GNSModelScanStSet:
        """Return the scanned state set that owns this state.

        Returns
        -------
        GNSModelScanStSet
            The parent state-set scan handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanstate = modelscanstset.getScanStateList()[0]
        >>> modelscanstate.getScanStateSet()
        """

class GNSModelScanGeom:
    """GNS model-scan geometry handle object.

    Represents the geometry found within a scanned slot. Its property filter can
    be configured before the geometry is read into a slot via
    :meth:`GNSModelScan.read`.

    Notes
    -----
    Obtained from :meth:`GNSModelScanSlot.getScanGeometry`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> sgeom = sslot.getScanGeometry()
    >>> modelscan.read(sgeom)
    """

    def setPropertiesFilter(self, properties: str = ...) -> bool:
        """Set the property filter applied when the geometry is read.

        Parameters
        ----------
        properties : str, optional
            A GNS list-filter expression (for example ``"100-140"``) selecting
            which properties to read. Default reads all properties (equivalent
            to ``"all"``).

        Returns
        -------
        bool
            ``True`` if the filter was accepted, otherwise ``False``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscangeom = modelscanslot.getScanGeometry()
        >>> modelscangeom.setPropertiesFilter("100-140")
        """

    def setPartsFilter(self, parts: str = ...) -> bool:
        """Set the parts filter applied when the geometry is read (deprecated).

        .. deprecated::
            Use :meth:`setPropertiesFilter` instead.

        Parameters
        ----------
        parts : str, optional
            A GNS list-filter expression selecting which parts to read. Default
            reads all parts (equivalent to ``"all"``).

        Returns
        -------
        bool
            ``True`` if the filter was accepted, otherwise ``False``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscangeom = modelscanslot.getScanGeometry()
        >>> modelscangeom.setPropertiesFilter("100-140")  # preferred replacement
        """

    def getScanSlot(self) -> GNSModelScanSlot:
        """Return the scanned slot that owns this geometry.

        Returns
        -------
        GNSModelScanSlot
            The parent scan-slot handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscangeom = modelscanslot.getScanGeometry()
        >>> modelscangeom.getScanSlot()
        """

class GNSModelScanFunc:
    """GNS model-scan function, vector or tensor handle object.

    Represents a scanned function, vector or tensor within a state set. It
    exposes the label, function category and available states, lets the read
    states be restricted, and can be read into a slot via
    :meth:`GNSModelScan.read`.

    Notes
    -----
    Obtained from :meth:`GNSModelScanStSet.getScanFunctionList`,
    :meth:`GNSModelScanStSet.getScanVectorList`,
    :meth:`GNSModelScanStSet.getScanTensorList` or
    :meth:`GNSModelScanStSet.getScanDispFunctionList`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> sstset = sslot.getScanStateSetList()[0]
    >>> svec = sstset.getScanVectorList()[0]
    >>> svec.getLabel()
    >>> modelscan.read(svec)
    """

    def getLabel(self) -> str:
        """Return the scanned function label.

        Returns
        -------
        str
            The function's label.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanfunc = modelscanstset.getScanFunctionList()[0]
        >>> modelscanfunc.getLabel()
        """

    def getScanFunctionCategory(self) -> str:
        """Return the scanned function category label.

        Returns
        -------
        str
            The function's category label.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanfunc = modelscanstset.getScanFunctionList()[0]
        >>> modelscanfunc.getScanFunctionCategory()
        """

    def getScanStateList(self, filter: str | None = None) -> list[GNSModelScanState]:
        """Return the scanned states for this function, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which states to return;
            ``None`` (default) returns every scanned state.

        Returns
        -------
        list of GNSModelScanState
            The matching state scan handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanfunc = modelscanstset.getScanFunctionList()[0]
        >>> modelscanfunc.getScanStateList()
        """

    def getScanStateSet(self) -> GNSModelScanStSet:
        """Return the scanned state set associated with this function.

        Returns
        -------
        GNSModelScanStSet
            The owning state-set scan handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanfunc = modelscanstset.getScanFunctionList()[0]
        >>> modelscanfunc.getScanStateSet()
        """

    def setStates(self, states: str = ...) -> bool:
        """Set the states read for this function.

        Parameters
        ----------
        states : str, optional
            A state range expression (for example ``"1-9"``) selecting which
            states to read. Default reads all states (equivalent to ``"all"``).

        Returns
        -------
        bool
            ``True`` if the state selection was accepted, otherwise ``False``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscanfunc = modelscanstset.getScanFunctionList()[0]
        >>> modelscanfunc.setStates("1-9")
        """

class GNSModelScanDisp:
    """GNS model-scan displacement handle object.

    Represents the displacements of a scanned state set. The read states can be
    restricted before the displacements are read into a slot via
    :meth:`GNSModelScan.read`.

    Notes
    -----
    Obtained from :meth:`GNSModelScanStSet.getScanDisplacements`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> sstset = sslot.getScanStateSetList()[0]
    >>> sdisp = sstset.getScanDisplacements()
    >>> modelscan.read(sdisp)
    """

    def setStates(self, states: str = ...) -> bool:
        """Set the states read for these displacements.

        Parameters
        ----------
        states : str, optional
            A state range expression selecting which states to read. Default
            reads all states.

        Returns
        -------
        bool
            ``True`` if the state selection was accepted, otherwise ``False``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscandisp = modelscanstset.getScanDisplacements()
        >>> modelscandisp.setStates()
        """

    def getScanStateSet(self) -> GNSModelScanStSet:
        """Return the scanned state set that owns these displacements.

        Returns
        -------
        GNSModelScanStSet
            The parent state-set scan handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanstset = modelscanslot.getScanStateSetList()[0]
        >>> modelscandisp = modelscanstset.getScanDisplacements()
        >>> modelscandisp.getScanStateSet()
        """

class GNSModelScanDbCurve:
    """GNS database scan curve handle object.

    Represents a curve found within a scanned Animator database slot. It exposes
    the curve name and owning slot, and can be read into a slot via
    :meth:`GNSModelScan.read`.

    Notes
    -----
    Obtained from :meth:`GNSModelScanSlot.getScanDatabaseCurveList`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Database4", "Can.gnsdb")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> scurve = sslot.getScanDatabaseCurveList()[0]
    >>> scurve.getName()
    >>> modelscan.read(scurve)
    """

    def getName(self) -> str:
        """Return the scanned curve name.

        Returns
        -------
        str
            The curve's name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Database4", "Can.gnsdb")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscandbcurve = modelscanslot.getScanDatabaseCurveList()[0]
        >>> modelscandbcurve.getName()
        """

    def getScanSlot(self) -> GNSModelScanSlot:
        """Return the scanned slot that owns this curve.

        Returns
        -------
        GNSModelScanSlot
            The parent scan-slot handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Database4", "Can.gnsdb")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscancurve = modelscanslot.getScanDatabaseCurveList()[0]
        >>> modelscancurve.getScanSlot()
        """

class GNSModelScanModule:
    """GNS model-scan module handle object.

    Represents a module (part group) found within a scanned slot. It exposes the
    module id, user id, name, parent module and owning slot, and can be read into
    a slot via :meth:`GNSModelScan.read`.

    Notes
    -----
    Obtained from :meth:`GNSModelScanSlot.getScanModuleList`.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.erfh5")
    >>> sslot = modelscan.getScanSlotList()[0]
    >>> smodule = sslot.getScanModuleList()[0]
    >>> smodule.getUserId()
    >>> modelscan.read(smodule)
    """

    def getId(self) -> int:
        """Return the scanned module id.

        Returns
        -------
        int
            The module's internal numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanmodule = modelscanslot.getScanModuleList()[0]
        >>> modelscanmodule.getId()
        """

    def getName(self) -> str:
        """Return the scanned module name.

        Returns
        -------
        str
            The module's name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanmodule = modelscanslot.getScanModuleList()[0]
        >>> modelscanmodule.getName()
        """

    def getUserId(self) -> int:
        """Return the scanned module user id.

        Returns
        -------
        int
            The module's user-facing numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanmodule = modelscanslot.getScanModuleList()[0]
        >>> modelscanmodule.getUserId()
        """

    def getParentScanModule(self) -> GNSModelScanModule | None:
        """Return the scanned parent module.

        Returns
        -------
        GNSModelScanModule or None
            The parent module scan handle, or ``None`` if the module has no
            parent (it is a top-level module).

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanmodule = modelscanslot.getScanModuleList()[0]
        >>> modelscanmodule.getParentScanModule()
        """

    def getScanSlot(self) -> GNSModelScanSlot:
        """Return the scanned slot that owns this module.

        Returns
        -------
        GNSModelScanSlot
            The parent scan-slot handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> modelscan = gns.getModelScanObject("Pamcrash", "Can.DSY.fz")
        >>> modelscanslot = modelscan.getScanSlotList()[0]
        >>> modelscanmodule = modelscanslot.getScanModuleList()[0]
        >>> modelscanmodule.getScanSlot()
        """

class GNSCurveScan:
    """Handle for scanning and reading curves from a solver result file.

    A curve-scan handle exposes the curve categories, subcases, functions and
    function items that a solver result file contains, and reads the selected
    curves into a slot as result variables.

    Notes
    -----
    Instances are obtained from :meth:`GNS.getCurveScanObject`, which takes an
    input-interface name and a result-file name; they are never constructed
    directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> curscan = gns.getCurveScanObject("Pamcrash", "Can.THP")
    >>> for cat in curscan.getCategoryList():
    ...     print(cat.getName())
    ...     for func in cat.getFunctionList():
    ...         print("  ", func.getName())
    ...         for funcItem in func.getFunctionItemList():
    ...             print("    ", funcItem.getName())
    """

    def getCategoryList(self, filter: str | None = None) -> list[GNSCurveScanCat]:
        """Return the scan's curve categories, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            category.

        Returns
        -------
        list of GNSCurveScanCat
            The matching category handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescan.getCategoryList()
        """

    def getCategory(self, name: str) -> GNSCurveScanCat | None:
        """Return the category with the given name.

        Parameters
        ----------
        name : str
            Name of the category to look up.

        Returns
        -------
        GNSCurveScanCat or None
            The matching category, or ``None`` if no category has that name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> cat = curvescan.getCategory("Node")
        """

    def readCurves(
        self,
        *objects: GNSCurveScanCat
        | GNSCurveScanSub
        | GNSCurveScanFunc
        | GNSCurveScanFuncItem
        | list[GNSCurveScanCat | GNSCurveScanSub | GNSCurveScanFunc | GNSCurveScanFuncItem]
        | tuple[GNSCurveScanCat | GNSCurveScanSub | GNSCurveScanFunc | GNSCurveScanFuncItem, ...],
        frequency_list: list[float] = ...,
        slot: str | int = "default",
    ) -> tuple[int, str, list[GNSResultVariable]]:
        """Read the curves selected by the given scan objects into a slot.

        Curves are selected by passing any combination of category, subcase,
        function and function-item handles; each argument may be a single handle
        or a list or tuple of handles.

        Parameters
        ----------
        *objects : GNSCurveScanCat or GNSCurveScanSub or GNSCurveScanFunc or GNSCurveScanFuncItem
            The scan objects whose curves are read. Lists and tuples of these
            handles are also accepted.
        frequency_list : list of float, optional
            Frequencies to read for Design Response curves; only curves matching
            a listed frequency are read. Default is an empty list ``[]``, which
            reads all frequencies.
        slot : str or int, optional
            Target slot, given by id or name. ``"new"`` reads into a new slot;
            ``"default"`` (the default) reads into the active slot.

        Returns
        -------
        tuple of (int, str, list of GNSResultVariable)
            A status code, a status message, and the result variables read.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> allcats = curvescan.getCategoryList()
        >>> curvescan.readCurves(allcats)  # read all curves
        """

class GNSCurveScanCat:
    """Handle for a single curve category within a curve scan.

    A category groups the subcases, functions and function items scanned for one
    result quantity, and carries the category's own attributes.

    Notes
    -----
    Instances are obtained from :meth:`GNSCurveScan.getCategoryList` and
    :meth:`GNSCurveScan.getCategory`; they are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> curscan = gns.getCurveScanObject("Pamcrash", "Can.THP")
    >>> cat = curscan.getCategoryList()[0]
    >>> cat.getName()
    """

    def getName(self) -> str:
        """Return the category name.

        Returns
        -------
        str
            The category's name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescancat.getName()
        """

    def getId(self) -> int:
        """Return the category id.

        Returns
        -------
        int
            The category's numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescancat.getId()
        """

    def getSubcaseList(self, filter: str | None = None) -> list[GNSCurveScanSub]:
        """Return the category's subcases, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            subcase.

        Returns
        -------
        list of GNSCurveScanSub
            The matching subcase handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescancat.getSubcaseList()
        """

    def getFunctionList(self, filter: str | None = None) -> list[GNSCurveScanFunc]:
        """Return the category's functions, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            function.

        Returns
        -------
        list of GNSCurveScanFunc
            The matching function handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescancat.getFunctionList()
        """

    def getSubcase(self, name: str) -> GNSCurveScanSub | None:
        """Return the subcase with the given name.

        Parameters
        ----------
        name : str
            Name of the subcase to look up.

        Returns
        -------
        GNSCurveScanSub or None
            The matching subcase, or ``None`` if no subcase has that name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategory("Node - modal frequency response")
        >>> curvescancat.getSubcase("SC2 - No_Label")
        """

    def getFunction(self, name: str) -> GNSCurveScanFunc | None:
        """Return the function with the given name.

        Parameters
        ----------
        name : str
            Name of the function to look up.

        Returns
        -------
        GNSCurveScanFunc or None
            The matching function, or ``None`` if no function has that name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategory("Node")
        >>> curvescancat.getFunction("X-Displacement")
        """

class GNSCurveScanFunc:
    """Handle for a single function within a curve-scan category.

    A function exposes its function items and its own attributes, including the
    frequencies of any associated Design Response curves.

    Notes
    -----
    Instances are obtained from :meth:`GNSCurveScanCat.getFunctionList`,
    :meth:`GNSCurveScanCat.getFunction`, :meth:`GNSCurveScanSub.getFunctionList`
    and :meth:`GNSCurveScanSub.getFunction`; they are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> curscan = gns.getCurveScanObject("Pamcrash", "Can.THP")
    >>> func = curscan.getCategoryList()[0].getFunctionList()[0]
    >>> func.getName()
    """

    def getName(self) -> str:
        """Return the function name.

        Returns
        -------
        str
            The function's name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfunc.getName()
        """

    def getId(self) -> int:
        """Return the function id.

        Returns
        -------
        int
            The function's numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfunc.getId()
        """

    def getCategory(self) -> GNSCurveScanCat:
        """Return the category this function belongs to.

        Returns
        -------
        GNSCurveScanCat
            The owning category handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfunc.getCategory()
        """

    def getSubcase(self) -> GNSCurveScanSub | None:
        """Return the subcase this function belongs to.

        Returns
        -------
        GNSCurveScanSub or None
            The owning subcase, or ``None`` if the function has no subcase.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfunc.getSubcase()
        """

    def getFunctionItemList(self, filter: str | None = None) -> list[GNSCurveScanFuncItem]:
        """Return the function's items, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            function item.

        Returns
        -------
        list of GNSCurveScanFuncItem
            The matching function-item handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfunc.getFunctionItemList()
        """

    def getFunctionItemById(self, id: int) -> GNSCurveScanFuncItem | None:
        """Return the function item with the given id.

        Parameters
        ----------
        id : int
            Numeric id of the function item to look up.

        Returns
        -------
        GNSCurveScanFuncItem or None
            The matching function item, or ``None`` if none has that id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategory("Node")
        >>> curvescanfunc = curvescancat.getFunction("X-Displacement")
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemById(100)
        """

    def getFunctionItemByName(self, name: str) -> GNSCurveScanFuncItem | None:
        """Return the function item with the given name.

        Parameters
        ----------
        name : str
            Name of the function item to look up.

        Returns
        -------
        GNSCurveScanFuncItem or None
            The matching function item, or ``None`` if none has that name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategory("Contact")
        >>> curvescanfunc = curvescancat.getFunction("Total force")
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemByName("AllContacts")
        """

    # ``getFunctionItem`` is deprecated; use ``getFunctionItemById`` or
    # ``getFunctionItemByName``. Overloaded stubs carry no docstring (ruff D418
    # forbids it on ``@overload``).
    @typing.overload
    def getFunctionItem(self, id: int) -> GNSCurveScanFuncItem | None: ...
    @typing.overload
    def getFunctionItem(self, name: str) -> GNSCurveScanFuncItem | None: ...
    def getFrequencyList(self) -> list[float]:
        """Return the function's Design Response frequencies.

        Returns
        -------
        list of float
            The frequencies, available for Design Response curves belonging to
            the ``FR<RESPONSE TYPE>`` response functions; empty otherwise.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Nastran", "Rohkarosserie.h5")
        >>> curvescancat = curvescan.getCategory("Design Response")
        >>> curvescansub = curvescancat.getSubcase("SC900 - Subcase-900")
        >>> curvescanfunc = curvescansub.getFunction("FRDISP-102-DIS_102")
        >>> curvescanfreq = curvescanfunc.getFrequencyList()
        """

class GNSCurveScanFuncItem:
    """Handle for a single function item within a curve-scan function.

    A function item is the finest curve-scan granularity and carries its own name,
    id, type and back-references to its function, subcase and category.

    Notes
    -----
    Instances are obtained from :meth:`GNSCurveScanFunc.getFunctionItemList`,
    :meth:`GNSCurveScanFunc.getFunctionItemById` and
    :meth:`GNSCurveScanFunc.getFunctionItemByName`; they are never constructed
    directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> curscan = gns.getCurveScanObject("Pamcrash", "Can.THP")
    >>> func = curscan.getCategoryList()[0].getFunctionList()[0]
    >>> funcItem = func.getFunctionItemList()[0]
    >>> funcItem.getName()
    """

    def getName(self) -> str:
        """Return the function-item name.

        Returns
        -------
        str
            The function item's name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemList()[0]
        >>> curvescanfuncitem.getName()
        """

    def getId(self) -> int:
        """Return the function-item id.

        Returns
        -------
        int
            The function item's numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemList()[0]
        >>> curvescanfuncitem.getId()
        """

    def getType(self) -> str:
        """Return the function-item type.

        Returns
        -------
        str
            The function item's type name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemList()[0]
        >>> curvescanfuncitem.getType()
        """

    def getFunction(self) -> GNSCurveScanFunc:
        """Return the function this item belongs to.

        Returns
        -------
        GNSCurveScanFunc
            The owning function handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemList()[0]
        >>> curvescanfuncitem.getFunction()
        """

    def getSubcase(self) -> GNSCurveScanSub | None:
        """Return the subcase this item belongs to.

        Returns
        -------
        GNSCurveScanSub or None
            The owning subcase, or ``None`` if the item has no subcase.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemList()[0]
        >>> curvescanfuncitem.getSubcase()
        """

    def getCategory(self) -> GNSCurveScanCat:
        """Return the category this item belongs to.

        Returns
        -------
        GNSCurveScanCat
            The owning category handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescanfunc = curvescancat.getFunctionList()[0]
        >>> curvescanfuncitem = curvescanfunc.getFunctionItemList()[0]
        >>> curvescanfuncitem.getCategory()
        """

class GNSCurveScanSub:
    """Handle for a single subcase within a curve-scan category.

    A subcase exposes the functions scanned under it and its own attributes.

    Notes
    -----
    Instances are obtained from :meth:`GNSCurveScanCat.getSubcaseList` and
    :meth:`GNSCurveScanCat.getSubcase`; they are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> curscan = gns.getCurveScanObject("Pamcrash", "Can.THP")
    >>> sub = curscan.getCategoryList()[0].getSubcaseList()[0]
    >>> sub.getName()
    """

    def getName(self) -> str:
        """Return the subcase name.

        Returns
        -------
        str
            The subcase's name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescansub = curvescancat.getSubcaseList()[0]
        >>> curvescansub.getName()
        """

    def getId(self) -> int:
        """Return the subcase id.

        Returns
        -------
        int
            The subcase's numeric id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescansub = curvescancat.getSubcaseList()[0]
        >>> curvescansub.getId()
        """

    def getCategory(self) -> GNSCurveScanCat:
        """Return the category this subcase belongs to.

        Returns
        -------
        GNSCurveScanCat
            The owning category handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescansub = curvescancat.getSubcaseList()[0]
        >>> curvescansub.getCategory()
        """

    def getFunctionList(self, filter: str | None = None) -> list[GNSCurveScanFunc]:
        """Return the subcase's functions, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            function.

        Returns
        -------
        list of GNSCurveScanFunc
            The matching function handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategoryList()[0]
        >>> curvescansub = curvescancat.getSubcaseList()[0]
        >>> curvescansub.getFunctionList()
        """

    def getFunction(self, name: str) -> GNSCurveScanFunc | None:
        """Return the function with the given name.

        Parameters
        ----------
        name : str
            Name of the function to look up.

        Returns
        -------
        GNSCurveScanFunc or None
            The matching function, or ``None`` if no function has that name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> curvescan = gns.getCurveScanObject("Pamcrash", "Can.THP")
        >>> curvescancat = curvescan.getCategory("Node - modal frequency response")
        >>> curvescansub = curvescancat.getSubcase("SC2 - No_Label")
        >>> curvescansub.getFunction("displacement - T1")
        """

class GNSPresentation:
    """Handle to a presentation document.

    A presentation groups one or more pages, each carrying plots, tables, text
    and other drawable items. The handle can also be used as a command target
    (passed as the ``target`` argument of :meth:`executeCommand`).

    Notes
    -----
    Presentation handles are obtained from the global GNS object, for example
    ``gnspy.gns.getPresentationList()``; they are not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> pres.getName()
    'Presentation_1'
    """

    def getName(self) -> str:
        """Return the presentation name.

        Returns
        -------
        str
            The presentation's display name.

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> pres.getName()
        'Presentation_1'
        """

    def getPageUnit(self) -> str:
        """Return the unit system used in the presentation.

        Returns
        -------
        str
            The unit system as its command token (for example ``'mm'``).

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> pres.getPageUnit()
        'mm'
        """

    def getId(self) -> int:
        """Return the presentation id.

        Returns
        -------
        int
            The unique integer identifier of the presentation.

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> pres.getId()
        1
        """

    def getSystemVariableList(self, filter: str | None = None) -> list[GNSSystemVariable]:
        """Return the presentation's system variables, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            presentation-scoped system variable.

        Returns
        -------
        list of GNSSystemVariable
            The matching system-variable handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> varlist = pres.getSystemVariableList()
        """

    def getSystemVariable(self, name: str) -> GNSSystemVariable | None:
        """Return the presentation system variable with the given name.

        Parameters
        ----------
        name : str
            The system-variable name to look up.

        Returns
        -------
        GNSSystemVariable or None
            The matching handle, or ``None`` if no such variable exists.

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> var = pres.getSystemVariable("time")
        """

    def getPageList(self) -> list[GNSPresentationPage]:
        """Return all pages of the presentation.

        Returns
        -------
        list of GNSPresentationPage
            The page handles in document order.

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> pagelist = pres.getPageList()
        """

    def getPageByName(self, name: str) -> GNSPresentationPage | None:
        """Return the page with the given name.

        Parameters
        ----------
        name : str
            The page name to look up.

        Returns
        -------
        GNSPresentationPage or None
            The matching page handle, or ``None`` if no page has that name.

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> page = pres.getPageByName("Page_1")
        """

    def getPageById(self, id: int) -> GNSPresentationPage | None:
        """Return the page with the given id.

        Parameters
        ----------
        id : int
            The page identifier to look up.

        Returns
        -------
        GNSPresentationPage or None
            The matching page handle, or ``None`` if no page has that id.

        Examples
        --------
        >>> import gnspy
        >>> pres = gnspy.gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        """

class GNSPresentationPage:
    """Handle to a single page of a presentation.

    A page owns the drawable items (plots, tables, lines, text and so on) that
    make up one sheet of a presentation, together with page-level properties
    such as size, orientation, margin and background colour.

    Notes
    -----
    Page handles are obtained from a :class:`GNSPresentation` object, for
    example ``GNSPresentation.getPageById`` or ``GNSPresentation.getPageList``;
    they are not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> pres = gnspy.gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    """

    def getId(self) -> int:
        """Return the page id.

        Returns
        -------
        int
            The unique integer identifier of the page.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getId()
        1
        """

    def getSize(self) -> tuple[float, float] | None:
        """Return the page height and width.

        Returns
        -------
        tuple of (float, float) or None
            The page ``(height, width)`` in the presentation's system units, or
            ``None`` if the size is unavailable.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getSize()
        (297.0, 210.0)
        """

    def getOrientation(self) -> PageOrientation:
        """Return the page orientation.

        Returns
        -------
        PageOrientation
            ``PageOrientation.Landscape`` or ``PageOrientation.Portrait``.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getOrientation()
        <PageOrientation.Portrait: ...>
        """

    def getBgColor(self) -> GNSColor:
        """Return the page background colour.

        Returns
        -------
        GNSColor
            The background colour of the page.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page_bg = page.getBgColor()
        """

    def getMargin(self) -> list[float]:
        """Return the page margin.

        Returns
        -------
        list of float
            The page margin values in the presentation's system units.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getMargin()
        [10.0, 10.0, 10.0, 10.0]
        """

    def getTemplate(self) -> GNSPresentationPage | None:
        """Return the page's template page.

        Returns
        -------
        GNSPresentationPage or None
            The template page handle, or ``None`` if the page has no template.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> template = page.getTemplate()
        """

    def getTitle(self) -> str:
        """Return the page title.

        Returns
        -------
        str
            The page title text.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getTitle()
        'My page'
        """

    def getSubTitle(self) -> str:
        """Return the page subtitle.

        Returns
        -------
        str
            The page subtitle text.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getSubTitle()
        'Detail view'
        """

    def getPageNumber(self) -> str:
        """Return the page number.

        Returns
        -------
        str
            The page number as displayed on the page.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getPageNumber()
        '1'
        """

    def getItemList(
        self, type: Presentation = ..., filter: str | None = None
    ) -> list[GNSPresentationCommon]:
        """Return the page's drawable items, optionally filtered by type.

        Parameters
        ----------
        type : Presentation, optional
            Presentation object-type flag selecting which items to return.
            Combine flags with ``|``. Default selects every presentation object
            type on the page.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSPresentationCommon
            The matching item handles, empty if none match. Each element is the
            most-derived handle for its item (for example ``GNSPresentationPlot``).

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> items = page.getItemList()
        >>> plots = page.getItemList(type=gnspy.Presentation.Plot)
        """

    def getSelectionList(
        self,
        type: Presentation = ...,
        slot: GNSSlot | None = None,
        filter: str | None = None,
    ) -> list[GNSPresentationCommon]:
        """Return the selected items of the page, optionally filtered.

        Parameters
        ----------
        type : Presentation, optional
            Presentation object-type flag selecting which items to consider.
            Combine flags with ``|``. Default selects every presentation object
            type on the page.
        slot : GNSSlot or None, optional
            Target slot whose selection is queried; the slot must be visible in
            the view. ``None`` (default) uses the active slots.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSPresentationCommon
            The selected item handles, empty if none are selected.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> first_slot = gns.getSlotList()[0]
        >>> page = gns.getPresentationList()[0].getPageById(1)
        >>> selected = page.getSelectionList(type=gnspy.Presentation.All, slot=first_slot)
        """

    def getName(self) -> str:
        """Return the page name.

        Returns
        -------
        str
            The page's display name.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> page.getName()
        'Page_1'
        """

class GNSPresentationCommon:
    """Base handle for every drawable item on a presentation page.

    Each item in a presentation (line, plot, table, text and so on) shares a
    common set of page-relative properties such as id, name, position, size,
    angle and colours. Item-specific subclasses add further members.

    Notes
    -----
    Item handles are obtained from a :class:`GNSPresentationPage`, for example
    ``GNSPresentationPage.getItemList`` or ``GNSPresentationPage.getSelectionList``;
    they are not constructed directly. ``getItemList`` returns the most-derived
    handle for each item, so an instance is usually of a subclass.

    Examples
    --------
    >>> import gnspy
    >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
    >>> common = page.getItemList()[0]
    """

    def getId(self) -> int:
        """Return the item id.

        Returns
        -------
        int
            The unique integer identifier of the item on its page.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> common.getId()
        1
        """

    def getPosition(self) -> tuple[float, float] | None:
        """Return the item position on the page.

        Returns
        -------
        tuple of (float, float) or None
            The item ``(x, y)`` position in the presentation's system units, or
            ``None`` if the position is unavailable.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> common.getPosition()
        (20.0, 30.0)
        """

    def getSize(self) -> tuple[float, float] | None:
        """Return the item size.

        Returns
        -------
        tuple of (float, float) or None
            The item ``(width, height)`` in the presentation's system units, or
            ``None`` if the size is unavailable.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> common.getSize()
        (100.0, 60.0)
        """

    def getFgColor(self, line: int = 1, char: int = 1) -> GNSColor:
        """Return the item's foreground colour.

        Parameters
        ----------
        line : int, optional
            One-based line number; only meaningful for a ``GNSPresentationText``
            item, where it selects the character whose colour is returned.
            Default is ``1``.
        char : int, optional
            One-based character number; only meaningful for a
            ``GNSPresentationText`` item. Default is ``1``.

        Returns
        -------
        GNSColor
            The foreground colour of the item (or of the selected character for
            a text item).

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> fg = common.getFgColor()
        """

    def getBgColor(self, line: int = 1, char: int = 1) -> GNSColor:
        """Return the item's background colour.

        Parameters
        ----------
        line : int, optional
            One-based line number; only meaningful for a ``GNSPresentationText``
            item, where it selects the character whose colour is returned.
            Default is ``1``.
        char : int, optional
            One-based character number; only meaningful for a
            ``GNSPresentationText`` item. Default is ``1``.

        Returns
        -------
        GNSColor
            The background colour of the item (or of the selected character for
            a text item).

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> bg = common.getBgColor()
        """

    def getAngle(self) -> float:
        """Return the item's rotation angle.

        Returns
        -------
        float
            The rotation angle of the item, in degrees.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> common.getAngle()
        0.0
        """

    def getType(self) -> Presentation:
        """Return the item's presentation object type.

        Returns
        -------
        Presentation
            The presentation object-type flag identifying this item.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> common.getType()
        <Presentation.Plot: ...>
        """

    def isSelected(self) -> bool:
        """Return whether the item is selected.

        Returns
        -------
        bool
            ``True`` if the item is currently selected, otherwise ``False``.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> common.isSelected()
        False
        """

    def getParent(self) -> GNSPresentationCommon | GNSPresentationPage:
        """Return the item's parent.

        Returns
        -------
        GNSPresentationCommon or GNSPresentationPage
            The parent item, or the owning page for a top-level item. For
            example the parent of a ``GNSPresentationTableField`` is its
            ``GNSPresentationTable``.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> parent = common.getParent()
        """

    def getName(self) -> str:
        """Return the item name.

        Returns
        -------
        str
            The item's display name.

        Examples
        --------
        >>> import gnspy
        >>> common = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList()[0]
        >>> name = common.getName()
        """

class GNSPresentationFrame(GNSPresentationCommon):
    """Base handle for framed presentation items.

    Some presentation items (text, legend, plot and so on) carry a rectangular
    frame whose per-side colour, line style and width can be queried. Adds the
    frame accessors to the common item properties of
    :class:`GNSPresentationCommon`.

    Notes
    -----
    Frame handles are obtained from a :class:`GNSPresentationPage`, for example
    ``GNSPresentationPage.getItemList(type=gnspy.Presentation.Text)``; they are
    not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
    >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
    """

    def getFrameColor(self, side: FrameSide = ...) -> GNSColor | None:
        """Return the frame colour of the whole frame or a single side.

        Parameters
        ----------
        side : FrameSide, optional
            The frame side to query. Default is ``FrameSide.All``, which queries
            every side at once.

        Returns
        -------
        GNSColor or None
            The frame colour for the requested side. When ``FrameSide.All`` is
            requested but the sides have different colours, ``None`` is returned.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
        >>> text.getFrameColor(side=gnspy.FrameSide.Top)
        """

    def getFrameStippling(self, side: FrameSide = ...) -> LineStyle | None:
        """Return the frame line style of the whole frame or a single side.

        Parameters
        ----------
        side : FrameSide, optional
            The frame side to query. Default is ``FrameSide.All``, which queries
            every side at once.

        Returns
        -------
        LineStyle or None
            The line style for the requested side. When ``FrameSide.All`` is
            requested but the sides differ, ``None`` is returned.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
        >>> text.getFrameStippling(side=gnspy.FrameSide.Top)
        """

    def getFrameWidth(self, side: FrameSide = ...) -> float:
        """Return the frame width of the whole frame or a single side.

        Parameters
        ----------
        side : FrameSide, optional
            The frame side to query. Default is ``FrameSide.All``, which queries
            every side at once.

        Returns
        -------
        float
            The frame width for the requested side. When ``FrameSide.All`` is
            requested but the sides have different widths, ``-1`` is returned.

        Examples
        --------
        >>> import gnspy
        >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
        >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
        >>> text.getFrameWidth(side=gnspy.FrameSide.Top)
        """

class GNSPresentationCurve(GNSPresentationCommon):
    """Base handle for a curve drawn inside a presentation plot.

    Provides the properties shared by the different curve kinds (line width,
    line style, title, backing data curve and legend membership). Adds these to
    the common item properties of :class:`GNSPresentationCommon`.

    Notes
    -----
    Curve handles are obtained from a :class:`GNSPresentationPlot`, for example
    ``GNSPresentationPlot.getCurveList`` or ``GNSPresentationPlot.getCurveById``;
    they are not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
    >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[0]
    >>> prescurve = plot.getCurveList()[0]
    """

    def getTitle(self) -> GNSPresentationText | None:
        """Return the curve's title.

        Returns
        -------
        GNSPresentationText or None
            The title item, or ``None`` if the curve has no title.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[0]
        >>> prescurve = plot.getCurveList()[0]
        >>> prescurve.getTitle()
        """

    def getCurve(self) -> GNSCurve:
        """Return the data curve backing this presentation curve.

        Returns
        -------
        GNSCurve
            The underlying data-curve handle.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[0]
        >>> prescurve = plot.getCurveList()[0]
        >>> prescurve.getCurve()
        """

    def getWidth(self) -> float:
        """Return the curve's line width.

        Returns
        -------
        float
            The line width of the curve.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[0]
        >>> prescurve = plot.getCurveList()[0]
        >>> prescurve.getWidth()
        1.0
        """

    def getStippling(self) -> LineStyle | None:
        """Return the curve's line style.

        Returns
        -------
        LineStyle or None
            The line style of the curve, or ``None`` if it is unavailable.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[0]
        >>> prescurve = plot.getCurveList()[0]
        >>> prescurve.getStippling()
        """

    def isInLegend(self) -> bool:
        """Return whether the curve appears in the plot's legend.

        Returns
        -------
        bool
            ``True`` if the curve is shown in the plot legend, otherwise
            ``False``.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[0]
        >>> prescurve = plot.getCurveList()[0]
        >>> prescurve.isInLegend()
        True
        """

class GNSPresentationLine(GNSPresentationCommon):
    """Handle to a straight-line item on a presentation page.

    Exposes the line's width, line style and optional arrow head, in addition
    to the common item properties of :class:`GNSPresentationCommon`.

    Notes
    -----
    Line handles are obtained from a :class:`GNSPresentationPage`, for example
    ``GNSPresentationPage.getItemList(type=gnspy.Presentation.Line)``; they are
    not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
    >>> line = page.getItemList(type=gnspy.Presentation.Line)[0]
    """

    def getWidth(self) -> float:
        """Return the line width.

        Returns
        -------
        float
            The width of the line.

        Examples
        --------
        >>> import gnspy
        >>> line = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Line)[0]
        >>> line.getWidth()
        1.0
        """

    def getStippling(self) -> LineStyle:
        """Return the line style.

        Returns
        -------
        LineStyle
            The line style of the line.

        Examples
        --------
        >>> import gnspy
        >>> line = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Line)[0]
        >>> line.getStippling()
        <LineStyle.Solid: ...>
        """

    def getArrowSize(self) -> float:
        """Return the arrow-head size.

        Returns
        -------
        float
            The size of the line's arrow head.

        Examples
        --------
        >>> import gnspy
        >>> line = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Line)[0]
        >>> line.getArrowSize()
        0.0
        """

    def getArrow(self) -> ArrowPosition:
        """Return the arrow-head position.

        Returns
        -------
        ArrowPosition
            The position of the arrow head on the line.

        Examples
        --------
        >>> import gnspy
        >>> line = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Line)[0]
        >>> line.getArrow()
        <ArrowPosition.None_: ...>
        """

class GNSPresentationPlot(GNSPresentationFrame):
    """Base handle for every plot type on a presentation page.

    Common base for the concrete plot kinds (``GNSPresentationXYPlot``,
    ``GNSPresentationBarChart``, ``GNSPresentationColorPlot``,
    ``GNSPresentationPolarPlot`` and ``GNSPresentation3dPlot``). Exposes the
    plot's title, subtitle, axes, curves, legend and grid styling, in addition
    to the frame properties of :class:`GNSPresentationFrame`.

    Notes
    -----
    Plot handles are obtained from a :class:`GNSPresentationPage`, for example
    ``GNSPresentationPage.getItemList(type=gnspy.Presentation.Plot)``; they are
    not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> page = gnspy.gns.getPresentationList()[0].getPageById(1)
    >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
    """

    def getTitle(self) -> GNSPresentationText | None:
        """Return the plot's title.

        Returns
        -------
        GNSPresentationText or None
            The title item, or ``None`` if the plot has no title.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getTitle()
        """

    def getSubtitle(self) -> GNSPresentationText | None:
        """Return the plot's subtitle.

        Returns
        -------
        GNSPresentationText or None
            The subtitle item, or ``None`` if the plot has no subtitle.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getSubtitle()
        """

    def getAxisById(self, id: int) -> GNSPresentationAxis | None:
        """Return the plot axis with the given id.

        Parameters
        ----------
        id : int
            The axis identifier. The primary axes are ``1`` (x-axis), ``2``
            (y-axis) and ``3`` (z-axis); additional parallel axes continue in
            steps of three (next x-axis ``4``, next y-axis ``5``, next z-axis
            ``6``, and so on).

        Returns
        -------
        GNSPresentationAxis or None
            The matching axis handle, or ``None`` if no axis has that id.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getAxisById(1)
        """

    def getCurveById(self, id: int) -> GNSPresentationCurve | None:
        """Return the curve in this plot with the given id.

        Parameters
        ----------
        id : int
            The curve identifier within this plot.

        Returns
        -------
        GNSPresentationCurve or None
            The matching curve handle, or ``None`` if no curve has that id.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getCurveById(100)
        """

    def getCurveByName(self, name: str) -> GNSPresentationCurve | None:
        """Return the curve in this plot with the given name.

        Parameters
        ----------
        name : str
            The curve name within this plot.

        Returns
        -------
        GNSPresentationCurve or None
            The matching curve handle, or ``None`` if no curve has that name.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getCurveByName("curve_1")
        """

    def getAxisList(self, filter: str | None = None) -> list[GNSPresentationAxis]:
        """Return the plot's axes, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every axis.

        Returns
        -------
        list of GNSPresentationAxis
            The matching axis handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getAxisList()
        """

    def getCurveList(self, filter: str | None = None) -> list[GNSPresentationCurve]:
        """Return the plot's curves, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every curve.

        Returns
        -------
        list of GNSPresentationCurve
            The matching curve handles, empty if none match.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getCurveList()
        """

    def getLegend(self) -> GNSPresentationLegend | None:
        """Return the plot's legend.

        Returns
        -------
        GNSPresentationLegend or None
            The legend item, or ``None`` if the plot has no legend.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getLegend()
        """

    def getGridWidth(self) -> float:
        """Return the plot's grid line width.

        Returns
        -------
        float
            The width of the plot's grid lines.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getGridWidth()
        0.5
        """

    def getGridStippling(self) -> LineStyle | None:
        """Return the plot's grid line style.

        Returns
        -------
        LineStyle or None
            The line style of the plot's grid, or ``None`` if it is unavailable.

        Examples
        --------
        >>> import gnspy
        >>> plot = gnspy.gns.getPresentationList()[0].getPageById(1).getItemList(
        ...     type=gnspy.Presentation.Plot)[-1]
        >>> plot.getGridStippling()
        """

class GNSPresentationGroup(GNSPresentationFrame):
    """Handle to a presentation group frame on a page.

    A group frame bundles several presentation objects so they can be managed
    together.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.Group)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> group = page.getItemList(type=gnspy.Presentation.Group)[0]
    """

    def getContentList(self) -> list[GNSPresentationCommon]:
        """Return the presentation objects contained in the group.

        Returns
        -------
        list of GNSPresentationCommon
            The grouped presentation objects, each as a
            :class:`GNSPresentationCommon` handle; empty if the group has no
            content.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> group = page.getItemList(type=gnspy.Presentation.Group)[0]
        >>> group.getContentList()
        [<GNSPresentationCommon>, <GNSPresentationCommon>]
        """

class GNSPresentationImage(GNSPresentationFrame):
    """Handle to an image frame on a presentation page.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.Image)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> image = page.getItemList(type=gnspy.Presentation.Image)[0]
    """

    def getImage(self) -> GNSImage | None:
        """Return the frame's image.

        Returns
        -------
        GNSImage or None
            The image displayed by the frame, or ``None`` if the frame has no
            image.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> image = page.getItemList(type=gnspy.Presentation.Image)[0]
        >>> image.getImage()
        <GNSImage>
        """

class GNSPresentationText(GNSPresentationFrame):
    """Handle to a text frame on a presentation page.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.Text)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
    """

    def getFont(self, line: int = 1, char: int = 1) -> GNSFont:
        """Return the font of the text, optionally for one character.

        Parameters
        ----------
        line : int, optional
            One-based line number. Must be ``>= 1``. Default is ``1``.
        char : int, optional
            One-based character position within ``line``. Must be ``>= 1``.
            Default is ``1``.

        Returns
        -------
        GNSFont
            The font. When ``line`` and ``char`` are supplied, the font of that
            specific character is returned.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
        >>> text.getFont()
        <GNSFont>
        """

    def getPadding(self) -> tuple[float, float]:
        """Return the horizontal and vertical padding of the text.

        Returns
        -------
        tuple of (float, float)
            The horizontal and vertical padding as ``(hor, ver)``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
        >>> text.getPadding()
        (2.0, 2.0)
        """

    def getText(self) -> str:
        """Return the entire text as a single string.

        Returns
        -------
        str
            The full text content of the frame.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
        >>> text.getText()
        'Title'
        """

    def getTextLines(self) -> list[str]:
        """Return the text as a list of lines.

        Returns
        -------
        list of str
            One string per line of the text content.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> text = page.getItemList(type=gnspy.Presentation.Text)[0]
        >>> text.getTextLines()
        ['line 1', 'line 2']
        """

class GNSPresentationLegend(GNSPresentationFrame):
    """Handle to the legend frame of a presentation plot.

    Notes
    -----
    Instances are obtained from a :class:`GNSPresentationPlot` via its
    ``getLegend`` method. Handle objects are not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
    >>> legend = plot.getLegend()
    """

    def getDefaultPosition(self) -> LegendPosition:
        """Return the legend's default position within the plot.

        Returns
        -------
        LegendPosition
            The default placement of the legend.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> legend = plot.getLegend()
        >>> legend.getDefaultPosition()
        <LegendPosition.TopRight>
        """

    def getTextFont(self) -> GNSFont | None:
        """Return the legend's text font.

        Returns
        -------
        GNSFont or None
            The text font, or ``None`` if the legend text is composed of more
            than one font.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> legend = plot.getLegend()
        >>> legend.getTextFont()
        <GNSFont>
        """

    def getAssociatedAxis(self, dim: int) -> GNSPresentationAxis | None:
        """Return the plot axis associated with the legend for a dimension.

        Parameters
        ----------
        dim : int
            The axis dimension: ``1`` for the X-axis, ``2`` for the Y-axis and
            ``3`` for the Z-axis.

        Returns
        -------
        GNSPresentationAxis or None
            The associated axis, or ``None`` if the legend is associated with
            all axes.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> legend = plot.getLegend()
        >>> legend.getAssociatedAxis(1)
        <GNSPresentationAxis>
        """

class GNSPresentationEllipse(GNSPresentationFrame):
    """Handle to an ellipse frame on a presentation page.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.Ellipse)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> ellipse = page.getItemList(type=gnspy.Presentation.Ellipse)[0]
    """

    def getAngleRange(self) -> tuple[float, float]:
        """Return the angular range of the ellipse.

        Returns
        -------
        tuple of (float, float)
            The start and end angle of the ellipse arc.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> ellipse = page.getItemList(type=gnspy.Presentation.Ellipse)[0]
        >>> ellipse.getAngleRange()
        (0.0, 360.0)
        """

    def getBorderMode(self) -> BorderMode:
        """Return the border mode of the ellipse.

        Returns
        -------
        BorderMode
            The border-drawing mode of the ellipse.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> ellipse = page.getItemList(type=gnspy.Presentation.Ellipse)[0]
        >>> ellipse.getBorderMode()
        <BorderMode.Solid>
        """

    def getWidth(self) -> float:
        """Return the border line width of the ellipse.

        Returns
        -------
        float
            The width of the ellipse border line.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> ellipse = page.getItemList(type=gnspy.Presentation.Ellipse)[0]
        >>> ellipse.getWidth()
        1.0
        """

    def getStippling(self) -> LineStyle:
        """Return the line style of the ellipse border.

        Returns
        -------
        LineStyle
            The stippling (dash pattern) of the ellipse border line.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> ellipse = page.getItemList(type=gnspy.Presentation.Ellipse)[0]
        >>> ellipse.getStippling()
        <LineStyle.Solid>
        """

    def getArrow(self) -> ArrowPosition:
        """Return the arrow position of the ellipse.

        Returns
        -------
        ArrowPosition
            Where arrow heads are drawn on the ellipse.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> ellipse = page.getItemList(type=gnspy.Presentation.Ellipse)[0]
        >>> ellipse.getArrow()
        <ArrowPosition.None_>
        """

    def getArrowSize(self) -> float:
        """Return the arrow-head size of the ellipse.

        Returns
        -------
        float
            The size of the arrow heads drawn on the ellipse.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> ellipse = page.getItemList(type=gnspy.Presentation.Ellipse)[0]
        >>> ellipse.getArrowSize()
        1.0
        """

class GNSPresentationEmbedView(GNSPresentationFrame):
    """Handle to an embedded 3D view frame on a presentation page.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.EmbedView)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> view = page.getItemList(type=gnspy.Presentation.EmbedView)[0]
    """

    def getView(self) -> GNSView | None:
        """Return the embedded view.

        Returns
        -------
        GNSView or None
            The embedded 3D view, or ``None`` if the frame has no view.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> view = page.getItemList(type=gnspy.Presentation.EmbedView)[0]
        >>> view.getView()
        <GNSView>
        """

class GNSPresentationFHL(GNSPresentationFrame):
    """Handle to a freehand-line frame on a presentation page.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.FHL)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> fhl = page.getItemList(type=gnspy.Presentation.FHL)[0]
    """

    def getWidth(self) -> float:
        """Return the line width of the freehand line.

        Returns
        -------
        float
            The width of the freehand line.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> fhl = page.getItemList(type=gnspy.Presentation.FHL)[0]
        >>> fhl.getWidth()
        1.0
        """

    def getStippling(self) -> LineStyle:
        """Return the line style of the freehand line.

        Returns
        -------
        LineStyle
            The stippling (dash pattern) of the freehand line.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> fhl = page.getItemList(type=gnspy.Presentation.FHL)[0]
        >>> fhl.getStippling()
        <LineStyle.Solid>
        """

    def getArrowSize(self) -> float:
        """Return the arrow-head size of the freehand line.

        Returns
        -------
        float
            The size of the arrow heads drawn on the freehand line.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> fhl = page.getItemList(type=gnspy.Presentation.FHL)[0]
        >>> fhl.getArrowSize()
        1.0
        """

    def getArrow(self) -> ArrowPosition:
        """Return the arrow position of the freehand line.

        Returns
        -------
        ArrowPosition
            Where arrow heads are drawn on the freehand line.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> fhl = page.getItemList(type=gnspy.Presentation.FHL)[0]
        >>> fhl.getArrow()
        <ArrowPosition.None_>
        """

    def getPoints(self) -> tuple[float, float]:
        """Return the point coordinates of the freehand line.

        These are the ``x``, ``y`` points captured when the freehand line was
        created.

        Returns
        -------
        tuple of (float, float)
            An ``(x, y)`` point coordinate.

        Notes
        -----
        The reference documentation describes this as a *list* of ``x``, ``y``
        points of the freehand line; the compiled binding types the result as a
        two-float tuple, which is preserved here. The concrete container arity
        could not be confirmed against a running module.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> fhl = page.getItemList(type=gnspy.Presentation.FHL)[0]
        >>> fhl.getPoints()
        (0.0, 0.0)
        """

class GNSPresentationPolygon(GNSPresentationFrame):
    """Handle to a polygon frame on a presentation page.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.Polygon)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> polygon = page.getItemList(type=gnspy.Presentation.Polygon)[0]
    """

    def getShape(self) -> PolygonType:
        """Return the shape type of the polygon.

        Returns
        -------
        PolygonType
            The polygon's shape.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> polygon = page.getItemList(type=gnspy.Presentation.Polygon)[0]
        >>> polygon.getShape()
        <PolygonType.Rectangle>
        """

    def getPoints(self) -> list[tuple[float, float]]:
        """Return the vertex coordinates of the polygon.

        Returns
        -------
        list of tuple of (float, float)
            The ``(x, y)`` coordinates of the polygon vertices.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> polygon = page.getItemList(type=gnspy.Presentation.Polygon)[0]
        >>> polygon.getPoints()
        [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
        """

    def getLineList(self) -> list[GNSPresentationLine]:
        """Return the edge lines of the polygon.

        Returns
        -------
        list of GNSPresentationLine
            The polygon's edges, each as a :class:`GNSPresentationLine` handle.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> polygon = page.getItemList(type=gnspy.Presentation.Polygon)[0]
        >>> polygon.getLineList()
        [<GNSPresentationLine>, <GNSPresentationLine>, <GNSPresentationLine>]
        """

class GNSPresentationTable(GNSPresentationFrame):
    """Handle to a table frame on a presentation page.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationPage` via
    ``getItemList(type=Presentation.Table)``. Handle objects are not
    constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
    """

    def getTitle(self) -> GNSPresentationText | None:
        """Return the table's title text.

        Returns
        -------
        GNSPresentationText or None
            The title as a :class:`GNSPresentationText` handle, or ``None`` if
            the table has no title.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
        >>> table.getTitle()
        <GNSPresentationText>
        """

    def getNumberOfRows(self) -> int:
        """Return the number of rows in the table.

        Returns
        -------
        int
            The row count of the table.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
        >>> table.getNumberOfRows()
        4
        """

    def getNumberOfColumns(self) -> int:
        """Return the number of columns in the table.

        Returns
        -------
        int
            The column count of the table.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
        >>> table.getNumberOfColumns()
        3
        """

    def getTableField(self, row: int, column: int) -> GNSPresentationTableField | None:
        """Return the field at a given row and column.

        Parameters
        ----------
        row : int
            Zero-based row index of the field.
        column : int
            Zero-based column index of the field.

        Returns
        -------
        GNSPresentationTableField or None
            The table field as a :class:`GNSPresentationTableField` handle, or
            ``None`` if no field exists at the given position.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
        >>> table.getTableField(0, 0)
        <GNSPresentationTableField>
        """

class GNSPresentationTableField(GNSPresentationFrame):
    """Handle to a single field (cell) of a presentation table.

    Notes
    -----
    Instances are obtained from :class:`GNSPresentationTable` via its
    ``getTableField`` method. Handle objects are not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
    >>> tablefield = table.getTableField(0, 0)
    """

    def getTitle(self) -> GNSPresentationText | None:
        """Return the field's text.

        Returns
        -------
        GNSPresentationText or None
            The field text as a :class:`GNSPresentationText` handle, or ``None``
            if the field has no text.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
        >>> tablefield = table.getTableField(0, 0)
        >>> tablefield.getTitle()
        <GNSPresentationText>
        """

    def getTitlePosition(
        self,
    ) -> tuple[tuple[LabelPosition, LabelPosition], tuple[LabelPosition, LabelPosition]]:
        """Return the horizontal and vertical label position of the field.

        Returns
        -------
        tuple of (tuple of (LabelPosition, LabelPosition), tuple of (LabelPosition, LabelPosition))
            The horizontal and vertical label positions of the field.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> table = page.getItemList(type=gnspy.Presentation.Table)[0]
        >>> tablefield = table.getTableField(0, 0)
        >>> tablefield.getTitlePosition()
        ((LabelPosition.Left, LabelPosition.Center), (LabelPosition.Top, LabelPosition.Center))
        """

class GNSPresentationAxis(GNSPresentationLine):
    """Handle to an axis of a presentation plot.

    Notes
    -----
    Instances are obtained from a :class:`GNSPresentationPlot` via its
    ``getAxisList`` method. Handle objects are not constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
    >>> axis = plot.getAxisList()[-1]
    """

    def getTitle(self) -> GNSPresentationText | None:
        """Return the axis title.

        Returns
        -------
        GNSPresentationText or None
            The title as a :class:`GNSPresentationText` handle, or ``None`` if
            the axis has no title.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getTitle()
        <GNSPresentationText>
        """

    def getUnits(self) -> GNSPresentationText | None:
        """Return the axis unit label.

        Returns
        -------
        GNSPresentationText or None
            The unit label as a :class:`GNSPresentationText` handle, or ``None``
            if the axis has no unit label.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getUnits()
        <GNSPresentationText>
        """

    def getRange(self) -> tuple[float, float]:
        """Return the value range of the axis.

        Returns
        -------
        tuple of (float, float)
            The minimum and maximum value of the axis.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getRange()
        (0.0, 100.0)
        """

    def getLog(self) -> float:
        """Return the logarithmic scale factor of the axis.

        Returns
        -------
        float
            The logarithmic scale of the axis.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getLog()
        0.0
        """

    def getFormat(self) -> str:
        """Return the number format of the axis.

        Returns
        -------
        str
            A C-style number format string (for example ``"10.4f"``, ``"12.6E"``
            or ``"8g"``), or ``"aut"`` for automatic formatting.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getFormat()
        'aut'
        """

    def getNumberOfTicks(self) -> tuple[int, int]:
        """Return the number of minor and major tick marks of the axis.

        Returns
        -------
        tuple of (int, int)
            The number of minor tick marks and the number of major tick marks.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getNumberOfTicks()
        (4, 10)
        """

    def getTickScale(self) -> float:
        """Return the tick scale of the axis.

        Returns
        -------
        float
            The tick scale of the axis.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getTickScale()
        1.0
        """

    def getLabelPosition(
        self,
    ) -> tuple[tuple[LabelPosition, LabelPosition], tuple[LabelPosition, LabelPosition]]:
        """Return the horizontal and vertical label position of the axis.

        Returns
        -------
        tuple of (tuple of (LabelPosition, LabelPosition), tuple of (LabelPosition, LabelPosition))
            The horizontal and vertical label positions of the axis.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getLabelPosition()
        ((LabelPosition.Left, LabelPosition.Center), (LabelPosition.Bottom, LabelPosition.Center))
        """

    def getTextFont(self) -> GNSFont | None:
        """Return the axis text font.

        Returns
        -------
        GNSFont or None
            The text font, or ``None`` if the axis text is composed of more than
            one font.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> plot = page.getItemList(type=gnspy.Presentation.Plot)[-1]
        >>> axis = plot.getAxisList()[-1]
        >>> axis.getTextFont()
        <GNSFont>
        """

class GNSPresentation3dPlot(GNSPresentationPlot):
    """Handle for a 3D plot inside a presentation page.

    A 3D plot displays one or more three-dimensional curves
    (:class:`GNSPresentationSet3d`). It inherits the common plot API from
    :class:`GNSPresentationPlot` (titles, axes, curves, legend and grid) and
    adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationPage.getItemList` by requesting the
    ``Presentation.ThreeDPlot`` item type; handles are never constructed
    directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> threedplot = page.getItemList(type=gnspy.Presentation.ThreeDPlot)[0]
    """

class GNSPresentationBarChart(GNSPresentationPlot):
    """Handle for a bar chart inside a presentation page.

    A bar chart displays one or more bar-set curves
    (:class:`GNSPresentationBarSet`). It inherits the common plot API from
    :class:`GNSPresentationPlot` (titles, axes, curves, legend and grid) and
    adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationPage.getItemList` by requesting the
    ``Presentation.BarChart`` item type; handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> barchart = page.getItemList(type=gnspy.Presentation.BarChart)[0]
    """

class GNSPresentationColorPlot(GNSPresentationPlot):
    """Handle for a color plot inside a presentation page.

    A color plot displays one or more color-map curves
    (:class:`GNSPresentationColorMap`). It inherits the common plot API from
    :class:`GNSPresentationPlot` (titles, axes, curves, legend and grid) and
    adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationPage.getItemList` by requesting the
    ``Presentation.ColorPlot`` item type; handles are never constructed
    directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> colorplot = page.getItemList(type=gnspy.Presentation.ColorPlot)[0]
    """

class GNSPresentationPolarPlot(GNSPresentationPlot):
    """Handle for a polar plot inside a presentation page.

    A polar plot displays one or more vector curves
    (:class:`GNSPresentationVector`). It inherits the common plot API from
    :class:`GNSPresentationPlot` (titles, axes, curves, legend and grid) and
    adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationPage.getItemList` by requesting the
    ``Presentation.PolarPlot`` item type; handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> polarplot = page.getItemList(type=gnspy.Presentation.PolarPlot)[0]
    """

class GNSPresentationXYPlot(GNSPresentationPlot):
    """Handle for an XY plot inside a presentation page.

    An XY plot displays one or more XY-set curves
    (:class:`GNSPresentationSet`). It inherits the common plot API from
    :class:`GNSPresentationPlot` (titles, axes, curves, legend and grid) and
    adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationPage.getItemList` by requesting the
    ``Presentation.XYPlot`` item type; handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> xyplot = page.getItemList(type=gnspy.Presentation.XYPlot)[0]
    """

class GNSPresentationBarSet(GNSPresentationCurve):
    """Handle for a single bar-set curve within a bar chart.

    A bar set is the bar-chart-specific curve type. It inherits the common curve
    API from :class:`GNSPresentationCurve` (title, backing curve, line width,
    stippling and legend membership) and adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationBarChart.getCurveList` (inherited from
    :class:`GNSPresentationPlot`); handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> barchart = page.getItemList(type=gnspy.Presentation.BarChart)[0]
    >>> barset = barchart.getCurveList()[0]
    """

class GNSPresentationColorMap(GNSPresentationCurve):
    """Handle for a single color-map curve within a color plot.

    A color map is the color-plot-specific curve type. It inherits the common
    curve API from :class:`GNSPresentationCurve` (title, backing curve, line
    width, stippling and legend membership) and adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationColorPlot.getCurveList` (inherited from
    :class:`GNSPresentationPlot`); handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> colorplot = page.getItemList(type=gnspy.Presentation.ColorPlot)[0]
    >>> colormap = colorplot.getCurveList()[0]
    """

class GNSPresentationSet(GNSPresentationCurve):
    """Handle for a single XY-set curve within an XY plot.

    An XY set is the XY-plot-specific curve type. In addition to the common
    curve API inherited from :class:`GNSPresentationCurve` it exposes the axes
    the set is plotted against and its marker style.

    Notes
    -----
    Obtained from :meth:`GNSPresentationXYPlot.getCurveList` (inherited from
    :class:`GNSPresentationPlot`); handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> xyplot = page.getItemList(type=gnspy.Presentation.XYPlot)[0]
    >>> xyset = xyplot.getCurveList()[0]
    """

    def getXAxis(self) -> GNSPresentationAxis | None:
        """Return the X axis this set is plotted against.

        Returns
        -------
        GNSPresentationAxis or None
            The associated X-axis handle, or ``None`` if the set has no
            associated X axis.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> xyplot = page.getItemList(type=gnspy.Presentation.XYPlot)[0]
        >>> xyset = xyplot.getCurveList()[0]
        >>> xyset.getXAxis()
        """

    def getYAxis(self) -> GNSPresentationAxis | None:
        """Return the Y axis this set is plotted against.

        Returns
        -------
        GNSPresentationAxis or None
            The associated Y-axis handle, or ``None`` if the set has no
            associated Y axis.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> xyplot = page.getItemList(type=gnspy.Presentation.XYPlot)[0]
        >>> xyset = xyplot.getCurveList()[0]
        >>> xyset.getYAxis()
        """

    def getSecondaryYAxis(self) -> GNSPresentationAxis | None:
        """Return the set's associated secondary Y axis.

        A secondary Y axis exists only for complex curves.

        Returns
        -------
        GNSPresentationAxis or None
            The secondary Y-axis handle, or ``None`` if the set has no secondary
            Y axis.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> xyplot = page.getItemList(type=gnspy.Presentation.XYPlot)[0]
        >>> xyset = xyplot.getCurveList()[0]
        >>> xyset.getSecondaryYAxis()
        """

    def getMarker(self) -> tuple[MarkerStyle, int, int]:
        """Return the set's marker style, increment and size.

        Returns
        -------
        tuple of (MarkerStyle, int, int)
            The marker style, the marker increment (how many data points are
            skipped between drawn markers) and the marker size.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> pres = gns.getPresentationList()[0]
        >>> page = pres.getPageById(1)
        >>> xyplot = page.getItemList(type=gnspy.Presentation.XYPlot)[0]
        >>> xyset = xyplot.getCurveList()[0]
        >>> mstyle, mincr, msize = xyset.getMarker()
        """

class GNSPresentationSet3d(GNSPresentationCurve):
    """Handle for a single 3D-set curve within a 3D plot.

    A 3D set is the 3D-plot-specific curve type. It inherits the common curve
    API from :class:`GNSPresentationCurve` (title, backing curve, line width,
    stippling and legend membership) and adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentation3dPlot.getCurveList` (inherited from
    :class:`GNSPresentationPlot`); handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> threedplot = page.getItemList(type=gnspy.Presentation.ThreeDPlot)[0]
    >>> threedset = threedplot.getCurveList()[0]
    """

class GNSPresentationVector(GNSPresentationCurve):
    """Handle for a single vector curve within a polar plot.

    A vector is the polar-plot-specific curve type. It inherits the common curve
    API from :class:`GNSPresentationCurve` (title, backing curve, line width,
    stippling and legend membership) and adds no members of its own.

    Notes
    -----
    Obtained from :meth:`GNSPresentationPolarPlot.getCurveList` (inherited from
    :class:`GNSPresentationPlot`); handles are never constructed directly.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> pres = gns.getPresentationList()[0]
    >>> page = pres.getPageById(1)
    >>> polarplot = page.getItemList(type=gnspy.Presentation.PolarPlot)[0]
    >>> polarvec = polarplot.getCurveList()[0]
    """

class GNSView:
    """GNS generic view handle object.

    A view handle exposes a single Animator view window: its name, id, geometry,
    parent, visible slots and view-scoped system variables. It is also a valid
    command target for :meth:`executeCommand`.

    Notes
    -----
    View handles are not constructed directly. Obtain one from the global GNS
    object with :meth:`GNS.getViewList`, :meth:`GNS.getViewByName` or
    :meth:`GNS.getViewById`::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> view = gns.getViewByName("Model")
        >>> view.getSize()
        >>> gns.executeCommand("col bac white", view)

    Depending on the view type the returned handle is one of the concrete
    subclasses :class:`GNSModelView`, :class:`GNSCurveView`, :class:`GNSFlcView`,
    :class:`GNSVideoView` or :class:`GNSPresentationView`.
    """

    def getName(self) -> str:
        """Return the view name.

        Returns
        -------
        str
            The view's name.

        Examples
        --------
        >>> view = gnspy.gns.getViewList()[0]
        >>> view.getName()
        """

    def getId(self) -> int:
        """Return the view id.

        Returns
        -------
        int
            The view's numeric id.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getId()
        """

    def getPosition(self) -> tuple[int, int]:
        """Return the position of the view window in the workspace.

        Returns
        -------
        tuple of int
            The ``(x, y)`` position of the view window, in pixels.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getPosition()
        """

    def getSize(self) -> tuple[int, int]:
        """Return the size of the view window in the workspace.

        Returns
        -------
        tuple of int
            The ``(width, height)`` of the view window, in pixels.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getSize()
        """

    def getParentView(self) -> GNSView | None:
        """Return the parent view.

        Returns
        -------
        GNSView or None
            The parent view, or ``None`` if the view has no parent.

        Examples
        --------
        >>> gns = gnspy.gns
        >>> gns.executeCommand("xcm vie new mod v1")
        >>> gns.executeCommand("v[v1]:xcm win add new cur v2")
        >>> parent_view = gns.getViewByName("v2").getParentView()
        """

    def getWindowState(self) -> str:
        """Return the window state of the view.

        Returns
        -------
        str
            The window state, one of ``"minimized"``, ``"normal"`` or
            ``"maximized"``.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getWindowState()
        """

    def executeCommand(
        self, command: str, slot: GNSSlot | None = None
    ) -> tuple[int, str, list[GNSResultVariable]]:
        """Execute an Animator command with this view as the target.

        Parameters
        ----------
        command : str
            The Animator command string to execute.
        slot : GNSSlot or None, optional
            An optional slot target for the command; ``None`` (default) executes
            the command without a slot target.

        Returns
        -------
        tuple of (int, str, list of GNSResultVariable)
            The command success status (``1`` on success, ``0`` on failure), any
            error or warning message text, and the result variables produced by
            the command.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> status, msg, resvars = view.executeCommand("col bac white")
        """

    def setActive(self) -> None:
        """Make this view the active view.

        This runs the ``vie swi on`` command with this view as the target.

        Returns
        -------
        None

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.setActive()
        """

    def getSystemVariableList(
        self, slot: GNSSlot | None = None, filter: str | None = None
    ) -> list[GNSSystemVariable]:
        """Return the view's system variables, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot or None, optional
            An optional slot, required for slot-based variables such as
            ``ACTSTATEID``; ``None`` (default) queries view-only variables.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSystemVariable
            The matching system variables, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewList()[0]
        >>> varlist = view.getSystemVariableList()
        """

    def getSystemVariable(self, name: str, slot: GNSSlot | None = None) -> GNSSystemVariable | None:
        """Return the view's system variable with the given name.

        Parameters
        ----------
        name : str
            The system variable name to look up.
        slot : GNSSlot or None, optional
            An optional slot, required for slot-based variables such as
            ``ACTSTATEID``; ``None`` (default) queries view-only variables.

        Returns
        -------
        GNSSystemVariable or None
            The matching system variable, or ``None`` if none has the given name.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> var = view.getSystemVariable("ACTSTATEID")
        """

    def getVisibleSlotList(self, filter: str | None = None) -> list[GNSSlot]:
        """Return the slots visible in the view, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSlot
            The visible (matching) slots, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewById(1)
        >>> visible_slots = view.getVisibleSlotList()
        """

class GNSModelView(GNSView):
    """GNS model view handle object.

    A model view exposes the 3D model window: its camera, the entities visible
    in it, view-based selections and identified items, distance/elongation/
    velocity measurements, and per-slot active state, state set and function. It
    is also a valid command target and can query function values on
    :class:`GNSNode`, :class:`GNSElement` and :class:`GNSProperty` objects.

    Notes
    -----
    Model view handles are not constructed directly. Obtain one from the global
    GNS object with :meth:`GNS.getViewByName` or the other view factories::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> view = gns.getViewByName("Model")
        >>> slot = gns.getSlotList()[0]
        >>> node = slot.getNodeById(100)
        >>> stateset = view.getActiveStateSet(slot)
        >>> func = view.getActiveFunction(slot)
        >>> state = view.getActiveState(slot)
        >>> node.getFunctionValues(stateset, func, state)
    """

    def getActiveStateSet(self, slot: GNSSlot) -> GNSStateSet:
        """Return the active state set of the given slot in the view.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.

        Returns
        -------
        GNSStateSet
            The slot's active state set in this view.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = view.getActiveStateSet(slot)
        """

    def getActiveState(self, slot: GNSSlot) -> GNSState:
        """Return the active state of the given slot in the view.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.

        Returns
        -------
        GNSState
            The slot's active state in this view.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> st = view.getActiveState(slot)
        """

    def getActiveFunction(self, slot: GNSSlot) -> GNSFunction:
        """Return the active function of the given slot in the view.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.

        Returns
        -------
        GNSFunction
            The slot's active function in this view.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> func = view.getActiveFunction(slot)
        """

    def getModelSize(self, slot: GNSSlot) -> tuple[float, float, float, float, float, float]:
        """Return the model-coordinate bounding box of the visible geometry.

        The bounding box is computed on the geometry visible in the view, taking
        the displacements of the active state and any exploded pids into account.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.

        Returns
        -------
        tuple of float
            Six values ``(min_x, min_y, min_z, max_x, max_y, max_z)`` giving the
            minimum and maximum corners of the bounding box.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> min_x, min_y, min_z, max_x, max_y, max_z = view.getModelSize(slot)

        Notes
        -----
        If the view shows no visible geometry, all six components are returned as
        ``None`` rather than as floats.

        See Also
        --------
        GNSSlot.getModelSize : Bounding box of all items, ignoring visibility.
        """

    def getVisibleElementList(
        self, slot: GNSSlot, type: Element = ..., filter: str | None = None
    ) -> list[GNSElement]:
        """Return the elements visible in the view, optionally typed and filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        type : Element, optional
            Element-type flag selecting which elements to return. Combine flags
            with ``|``. Default is ``Element.All`` (every element type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSElement
            The matching visible elements, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> elist = view.getVisibleElementList(slot, type=gnspy.Element.Hexa)
        """

    def getVisiblePropertyList(
        self, slot: GNSSlot, type: Property = ..., filter: str | None = None
    ) -> list[GNSProperty]:
        """Return the properties visible in the view, optionally typed and filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        type : Property, optional
            Property-type flag selecting which properties to return. Combine
            flags with ``|``. Default is ``Property.All`` (every property type).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSProperty
            The matching visible properties, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> plist = view.getVisiblePropertyList(slot, type=gnspy.Property.Hexa)
        """

    def getVisibleNodeList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSNode]:
        """Return the nodes visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSNode
            The matching visible nodes, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> nlist = view.getVisibleNodeList(slot)
        """

    def getVisibleMaterialList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSMaterial]:
        """Return the materials visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMaterial
            The matching visible materials, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> mlist = view.getVisibleMaterialList(slot)
        """

    def getVisibleSectionList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSSection]:
        """Return the sections visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSection
            The matching visible sections, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> slist = view.getVisibleSectionList(slot)
        """

    def getVisibleImpactPointList(
        self, slot: GNSSlot, filter: str | None = None
    ) -> list[GNSImpactPoint]:
        """Return the impact points visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSImpactPoint
            The matching visible impact points, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> iplist = view.getVisibleImpactPointList(slot)
        """

    def getVisibleSpcList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSSpc]:
        """Return the SPCs visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSSpc
            The matching visible SPCs, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> spclist = view.getVisibleSpcList(slot)
        """

    def getVisibleMpcList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSMpc]:
        """Return the MPCs visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMpc
            The matching visible MPCs, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> mpclist = view.getVisibleMpcList(slot)
        """

    def getVisibleForceList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSForce]:
        """Return the forces visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSForce
            The matching visible forces, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> flist = view.getVisibleForceList(slot)
        """

    def getVisibleMomentList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSMoment]:
        """Return the moments visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSMoment
            The matching visible moments, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> mlist = view.getVisibleMomentList(slot)
        """

    def getVisibleCoordList(self, slot: GNSSlot, filter: str | None = None) -> list[GNSCoord]:
        """Return the coordinate systems visible in the view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSCoord
            The matching visible coordinate systems, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> clist = view.getVisibleCoordList(slot)
        """

    def getVideoList(self, filter: str | None = None) -> list[GNSVideo]:
        """Return the videos in the view, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSVideo
            The matching videos, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> vlist = view.getVideoList()
        """

    def getImageList(self, filter: str | None = None) -> list[GNSImage]:
        """Return the images in the view, optionally filtered.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSImage
            The matching images, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> ilist = view.getImageList()
        """

    def getCameraPosition(self) -> tuple[float, float, float]:
        """Return the model view camera position.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` camera position in model coordinates.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getCameraPosition()
        """

    def getViewRefPoint(self) -> tuple[float, float, float]:
        """Return the model view camera reference point.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` camera reference point in model coordinates.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getViewRefPoint()
        """

    def getUpVector(self) -> tuple[float, float, float]:
        """Return the model view camera up vector.

        Returns
        -------
        tuple of float
            The ``(x, y, z)`` camera up vector.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getUpVector()
        """

    def getFrontClipPlane(self) -> float:
        """Return the model view camera front clip plane.

        Returns
        -------
        float
            The front clip-plane distance.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getFrontClipPlane()
        """

    def getBackClipPlane(self) -> float:
        """Return the model view camera back clip plane.

        Returns
        -------
        float
            The back clip-plane distance.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getBackClipPlane()
        """

    def getOrthoScaleFactor(self) -> float:
        """Return the model view camera orthographic scale factor.

        Returns
        -------
        float
            The orthographic scale factor.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getOrthoScaleFactor()
        """

    def getPerspectiveAngle(self) -> float:
        """Return the model view camera perspective angle.

        Returns
        -------
        float
            The perspective angle, in degrees.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getPerspectiveAngle()
        """

    def getDistance(
        self,
        item1: GNSNode | GNSElement | GNSProperty | GNSGroup,
        item2: GNSNode | GNSElement | GNSProperty | GNSGroup,
        direction: list[float] | None = None,
    ) -> tuple[float, float, float]:
        """Return the current distance between two model items.

        The result always refers to the view's active state set and state.

        Parameters
        ----------
        item1 : GNSNode, GNSElement, GNSProperty or GNSGroup
            The first item.
        item2 : GNSNode, GNSElement, GNSProperty or GNSGroup
            The second item.
        direction : list of float or None, optional
            A direction vector, given as a list of three floats, along which the
            distance is measured; ``None`` (default) measures the direct
            distance.

        Returns
        -------
        tuple of float
            The distance result.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> group = slot.getGroupByName("shell_group")
        >>> node = slot.getNodeById(100)
        >>> view.getDistance(node, group)
        >>> view.getDistance(node, group, [1, 0, 0])

        Notes
        -----
        The reference documentation describes the result as a direction together
        with a magnitude; only the three components present in the returned tuple
        are guaranteed here.
        """

    def getElongation(
        self,
        item1: GNSNode | GNSElement | GNSProperty | GNSGroup,
        item2: GNSNode | GNSElement | GNSProperty | GNSGroup,
    ) -> tuple[float, float, float, float]:
        """Return the current elongation between two model items.

        The result always refers to the view's active state set and state.

        Parameters
        ----------
        item1 : GNSNode, GNSElement, GNSProperty or GNSGroup
            The first item.
        item2 : GNSNode, GNSElement, GNSProperty or GNSGroup
            The second item.

        Returns
        -------
        tuple of float
            Four values giving the elongation direction and its magnitude.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> pid = slot.getPropertyByName("shell_prop")
        >>> node = slot.getNodeById(100)
        >>> view.getElongation(node, pid)
        """

    def getRelativeVelocity(
        self,
        item1: GNSNode | GNSElement | GNSProperty | GNSGroup,
        item2: GNSNode | GNSElement | GNSProperty | GNSGroup,
    ) -> tuple[float, float, float]:
        """Return the current relative velocity between two model items.

        The result always refers to the view's active state set and state.

        Parameters
        ----------
        item1 : GNSNode, GNSElement, GNSProperty or GNSGroup
            The first item.
        item2 : GNSNode, GNSElement, GNSProperty or GNSGroup
            The second item.

        Returns
        -------
        tuple of float
            The relative-velocity result.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> node1 = slot.getNodeById(1000)
        >>> node2 = slot.getNodeById(100)
        >>> view.getRelativeVelocity(node1, node2)

        Notes
        -----
        The reference documentation describes the result as a direction together
        with a magnitude; only the three components present in the returned tuple
        are guaranteed here.
        """

    def getSelectionList(
        self,
        type: Element | Property | Item,
        slot: GNSSlot | None = None,
        filter: str | None = None,
    ) -> list[GNSElement | GNSNode]:
        """Return the selected items of the given type in the view.

        Parameters
        ----------
        type : Element, Property or Item
            An element-type, property-type or entity-type flag selecting which
            selected items to return. Combine flags with ``|``.
        slot : GNSSlot or None, optional
            A slot that is visible in the view; ``None`` (default) uses the
            active slots.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of (GNSElement or GNSNode)
            The matching selected items, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewList()[-1]
        >>> first_slot = gnspy.gns.getSlotList()[0]
        >>> sel_quads = view.getSelectionList(gnspy.Element.Quad)
        >>> sel_pids = view.getSelectionList(gnspy.Property.All)
        >>> sel_slot_quads = view.getSelectionList(gnspy.Element.Quad, slot=first_slot)
        """

    def getSelection(
        self,
        type: Element | Property | Item,
        slot: GNSSlot | None = None,
        filter: str | None = None,
    ) -> list[GNSElement | GNSNode]:
        """Return the selected items of the given type in the view (deprecated).

        Parameters
        ----------
        type : Element, Property or Item
            An element-type, property-type or entity-type flag selecting which
            selected items to return. Combine flags with ``|``.
        slot : GNSSlot or None, optional
            A slot that is visible in the view; ``None`` (default) uses the
            active slots.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of (GNSElement or GNSNode)
            The matching selected items, empty if none match.

        Notes
        -----
        Deprecated. Use :meth:`getSelectionList` instead.
        """

    def getCrossSection(self, slot: GNSSlot, id: int) -> GNSCrossSection | None:
        """Return the cross section with the given id for the given slot.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        id : int
            The cross-section id, in the range 0 to 5.

        Returns
        -------
        GNSCrossSection or None
            The matching cross section, or ``None`` if none exists.

        Examples
        --------
        >>> view = gnspy.gns.getViewList()[-1]
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> vcs = view.getCrossSection(slot, 0)
        """

    def getSectionForceDrawStyle(self, slot: GNSSlot) -> str:
        """Return the section-force vector display style of the given slot.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.

        Returns
        -------
        str
            The section-force vector display style.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> view.getSectionForceDrawStyle(slot)
        """

    def getTextList(self, tfilter: str | None = None) -> list[GNSViewText]:
        """Return the view texts of the model view, optionally filtered.

        Parameters
        ----------
        tfilter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSViewText
            The matching view texts, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Model")
        >>> view.getTextList()
        """

    def pick(
        self, type: Element | Property | Item, slot: GNSSlot | None = None
    ) -> GNSElement | GNSNode:
        """Let the user interactively pick an item of the given type in the view.

        Parameters
        ----------
        type : Element, Property or Item
            An element-type, property-type or entity-type flag selecting which
            kind of item to pick.
        slot : GNSSlot or None, optional
            A slot that is visible in the view; ``None`` (default) uses the
            active slots.

        Returns
        -------
        GNSElement or GNSNode
            The picked item.

        Examples
        --------
        >>> view = gnspy.gns.getViewList()[-1]
        >>> quad = view.pick(gnspy.Element.Quad)
        >>> pid = view.pick(gnspy.Property.All)
        """

    def getIdentifiedList(
        self,
        type: Element | Property | Item,
        slot: GNSSlot | None = None,
        filter: str | None = None,
    ) -> list[GNSElement | GNSNode]:
        """Return the identified items of the given type in the view.

        Parameters
        ----------
        type : Element, Property or Item
            An element-type, property-type or entity-type flag selecting which
            identified items to return. Combine flags with ``|``.
        slot : GNSSlot or None, optional
            A slot that is visible in the view; ``None`` (default) uses the
            active slots.
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of (GNSElement or GNSNode)
            The matching identified items, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewList()[-1]
        >>> first_slot = gnspy.gns.getSlotList()[0]
        >>> ide_quads = view.getIdentifiedList(gnspy.Element.Quad)
        >>> ide_pids = view.getIdentifiedList(gnspy.Property.All)
        >>> ide_slot_quads = view.getIdentifiedList(gnspy.Element.Quad, slot=first_slot)
        """

class GNSCurveView(GNSView):
    """GNS curve view handle object.

    A curve view exposes the function-curve plot window: the curves it displays
    and its view texts. It is also a valid command target.

    Notes
    -----
    Curve view handles are not constructed directly. Obtain one from the global
    GNS object with :meth:`GNS.getViewByName` or the other view factories::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> view = gns.getViewByName("Curve")
        >>> vcurves = view.getCurveList()
    """

    def getCurveList(self, type: Item = ..., filter: str | None = None) -> list[GNSCurve]:
        """Return the curves in the curve view, optionally typed and filtered.

        Parameters
        ----------
        type : Item, optional
            Entity-type flag selecting which curves to return. Default is
            ``Item.Selected`` (only the selected curves).
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSCurve
            The matching curves, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Curve")
        >>> view.getCurveList()
        """

    def getTextList(self, slot: GNSSlot, tfilter: str | None = None) -> list[GNSViewText]:
        """Return the view texts of the curve view, optionally filtered.

        Parameters
        ----------
        slot : GNSSlot
            A slot that is visible in the view.
        tfilter : str or None, optional
            A GNS list-filter expression; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSViewText
            The matching view texts, empty if none match.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Curve")
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> view.getTextList(slot)
        """

class GNSFlcView(GNSView):
    """GNS FLC (forming-limit-curve) view handle object.

    An FLC view exposes the forming-limit-curve window. It carries no
    FLC-specific query methods of its own; use the inherited :class:`GNSView`
    members and :meth:`GNSView.executeCommand` to drive it.

    Notes
    -----
    FLC view handles are not constructed directly. Obtain one from the global
    GNS object with :meth:`GNS.getViewByName` or the other view factories::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> view = gns.getViewByName("FLC")
        >>> gns.executeCommand("vie flc act", view)
    """

class GNSVideoView(GNSView):
    """GNS video view handle object.

    A video view exposes the video playback window and the video it displays. It
    is also a valid command target.

    Notes
    -----
    Video view handles are not constructed directly. Obtain one from the global
    GNS object with :meth:`GNS.getViewByName` or the other view factories::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> view = gns.getViewByName("Video")
        >>> gns.executeCommand("vid ani for", view)
    """

    def getVideo(self) -> GNSVideo | None:
        """Return the video associated with this video view.

        Returns
        -------
        GNSVideo or None
            The associated video, or ``None`` if the view has none.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Video")
        >>> vid = view.getVideo()
        """

class GNSPresentationView(GNSView):
    """GNS presentation view handle object.

    A presentation view exposes the presentation window and the presentation it
    displays. It is also a valid command target.

    Notes
    -----
    Presentation view handles are not constructed directly. Obtain one from the
    global GNS object with :meth:`GNS.getViewByName` or the other view
    factories::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> view = gns.getViewByName("Presentation")
        >>> pres = view.getPresentation()
    """

    def getPresentation(self) -> GNSPresentation | None:
        """Return the presentation associated with this presentation view.

        Returns
        -------
        GNSPresentation or None
            The associated presentation, or ``None`` if the view has none.

        Examples
        --------
        >>> view = gnspy.gns.getViewByName("Presentation")
        >>> pres = view.getPresentation()
        """

class GNSViewText:
    """GNS view-text handle object.

    A view-text handle exposes a single text label placed in a view: its text,
    position, size, slot, view and the model item it is attached to.

    Notes
    -----
    View-text handles are not constructed directly. Obtain them from a
    :class:`GNSModelView` or :class:`GNSCurveView` with ``getTextList``::

        >>> import gnspy
        >>> gns = gnspy.gns
        >>> view = gns.getViewList(type=gnspy.ModelView)[0]
        >>> slot = gns.getSlotList()[0]
        >>> vtext = view.getTextList(slot)[0]
        >>> pos = vtext.getPosition()
    """

    def getSlotId(self) -> int:
        """Return the slot id of the view text.

        Returns
        -------
        int
            The id of the slot the view text belongs to.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> slotid = vtext.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot of the view text.

        Returns
        -------
        GNSSlot
            The slot the view text belongs to.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> slot = vtext.getSlot()
        """

    def getViewId(self) -> int:
        """Return the view id of the view text.

        Returns
        -------
        int
            The id of the view the view text belongs to.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> viewid = vtext.getViewId()
        """

    def getId(self) -> int:
        """Return the user id of the view text.

        Returns
        -------
        int
            The view text's user id.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> vtext.getId()
        """

    def getPosition(self) -> tuple[float, float] | None:
        """Return the position of the view text.

        Returns
        -------
        tuple of float, or None
            The ``(x, y)`` position of the view text, or ``None`` if it has no
            position.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> vtext.getPosition()
        """

    def getSize(self) -> tuple[float, float] | None:
        """Return the size of the view text.

        Returns
        -------
        tuple of float, or None
            The ``(width, height)`` of the view text, or ``None`` if it has no
            size.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> vtext.getSize()
        """

    def getText(self) -> str:
        """Return the text string of the view text.

        Returns
        -------
        str
            The view text's text string.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> vtext.getText()
        """

    def getItem(self) -> GNSElement | GNSNode:
        """Return the model item the view text is attached to.

        Returns
        -------
        GNSElement or GNSNode
            The attached item.

        Examples
        --------
        >>> vtext = view.getTextList(slot)[0]
        >>> vtext.getItem()
        """

class GNSVariable:
    """Handle to a GNS variable.

    A variable handle exposes a variable's name and current value. It is the
    base type for the concrete variable kinds :class:`GNSSystemVariable`,
    :class:`GNSUserVariable`, and :class:`GNSResultVariable`.

    Notes
    -----
    Handles are not constructed directly. They are obtained from ``GNSSlot``,
    ``GNSView``, or the global ``gns`` object (for example via
    ``gns.getUserVariableList`` or ``gns.getSystemVariableList``), or returned
    by executed commands.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> uvar = gns.getUserVariableList()[0]
    >>> uvar.getValue()
    """

    def getName(self) -> str:
        """Return the variable name.

        Returns
        -------
        str
            The name of the variable.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariableList()[0]
        >>> uvar.getName()
        'var1'
        """

    def getValue(self) -> int | float | str | bool | None:
        """Return the variable value.

        Returns
        -------
        int or float or str or bool or None
            The current value of the variable, or ``None`` if it is unset.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariableList()[0]
        >>> uvar.getValue()
        100
        """

class GNSSystemVariable(GNSVariable):
    """Handle to a GNS system variable.

    A system variable is a read-only variable maintained by Animator that
    reflects application or slot/view state.

    Notes
    -----
    Handles are not constructed directly. They are obtained from ``GNSSlot``,
    ``GNSView``, or the global ``gns`` object, for example via
    ``gns.getSystemVariableList`` or ``gns.getSystemVariable``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> svar = gns.getSystemVariableList()[0]
    >>> svar.getValue()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot the variable belongs to.

        Returns
        -------
        int
            The slot id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> svar = gns.getSystemVariableList()[0]
        >>> svar.getSlotId()
        1
        """

    def getSlot(self) -> GNSSlot | None:
        """Return the slot the variable belongs to.

        Returns
        -------
        GNSSlot or None
            The owning slot, or ``None`` if the variable is not bound to a slot.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> svar = slot.getSystemVariableList()[0]
        >>> slot = svar.getSlot()
        """

    def getViewId(self) -> int:
        """Return the id of the view the variable belongs to.

        Returns
        -------
        int
            The view id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> svar = gns.getSystemVariableList()[0]
        >>> svar.getViewId()
        1
        """

    def getAttributeList(self, path: str) -> list[GNSAttribute]:
        """Return the attributes of the variable at a user-action path.

        Only the ``TOOLBAR_ACTION`` system variable carries attributes: the
        properties of a user action (``checkstate``, ``icon``, ``type``, and
        ``shortcut``) are exposed as its attributes.

        Parameters
        ----------
        path : str
            The path of the user action whose attributes are requested.

        Returns
        -------
        list of GNSAttribute
            The attribute handles, empty if the path has none.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> svar = gns.getSystemVariable("TOOLBAR_ACTION")
        >>> attr = svar.getAttributeList("/User/Action")
        """

    def getAttributeByName(self, path: str, property: str) -> GNSAttribute | None:
        """Return a single named attribute of a user action.

        Parameters
        ----------
        path : str
            The path of the user action.
        property : str
            The property of the user action to return, one of ``checkstate``,
            ``icon``, ``type``, or ``shortcut``.

        Returns
        -------
        GNSAttribute or None
            The matching attribute handle, or ``None`` if none matches.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> svar = gns.getSystemVariable("TOOLBAR_ACTION")
        >>> attr = svar.getAttributeByName("/User/Action", "icon")
        """

class GNSUserVariable(GNSVariable):
    """Handle to a GNS user variable.

    A user variable is a user-defined, optionally writable variable.

    Notes
    -----
    Handles are not constructed directly. They are obtained from ``GNSSlot``
    or the global ``gns`` object, for example via ``gns.getUserVariableList``
    or ``gns.getUserVariable``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> uvar = gns.getUserVariableList()[0]
    >>> uvar.getValue()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot the variable belongs to.

        Returns
        -------
        int
            The slot id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariableList()[0]
        >>> uvar.getSlotId()
        1
        """

    def getSlot(self) -> GNSSlot | None:
        """Return the slot the variable belongs to.

        Returns
        -------
        GNSSlot or None
            The owning slot, or ``None`` if the variable is not bound to a slot.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> uvar = slot.getUserVariableList()[0]
        >>> slot = uvar.getSlot()
        """

    def setValue(self, value: float | str | bool) -> bool:
        """Set the variable value.

        Parameters
        ----------
        value : int or float or str or bool
            The new value to assign to the variable.

        Returns
        -------
        bool
            ``True`` if the value was set, ``False`` otherwise.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariable("var1")
        >>> uvar.setValue(100)
        True
        """

    def getAttributeList(self) -> list[GNSAttribute]:
        """Return the attributes of the variable.

        Returns
        -------
        list of GNSAttribute
            The attribute handles, empty if the variable has none.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariableList()[0]
        >>> uvar.getAttributeList()
        """

    def getRelevance(self) -> int:
        """Return the relevance of the user variable.

        Returns
        -------
        int
            The relevance value of the variable.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariable("var1")
        >>> uvar.getRelevance()
        0
        """

    def isConstant(self) -> bool:
        """Return whether the user variable is constant.

        Returns
        -------
        bool
            ``True`` if the variable is constant, ``False`` otherwise.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariable("var1")
        >>> uvar.isConstant()
        False
        """

    def getAttributeByName(self, name: str) -> GNSAttribute | None:
        """Return a single named attribute of the variable.

        Parameters
        ----------
        name : str
            The name of the attribute to return.

        Returns
        -------
        GNSAttribute or None
            The matching attribute handle, or ``None`` if none matches.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariableList()[0]
        >>> attr = uvar.getAttributeByName("Attr1")
        """

class GNSResultVariable(GNSVariable):
    """Handle to a GNS result variable.

    A result variable holds a value produced by an executed command.

    Notes
    -----
    Handles are not constructed directly. They are returned by
    ``GNS.executeCommand`` as the third element of its result tuple.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> status, msg, resvars = gns.executeCommand("ide nod 100")
    >>> dispResVar = None
    >>> for resvar in resvars:
    ...     if resvar.getName() == "_CT":
    ...         dispResVar = resvar
    ...         break
    >>> dispResVar.getValue()
    """

    def getAttributeList(self) -> list[GNSAttribute]:
        """Return the attributes of the variable.

        Returns
        -------
        list of GNSAttribute
            The attribute handles, empty if the variable has none.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> status, msg, resvars = gns.executeCommand('c2d cal nij')
        >>> resvar = resvars[0]
        >>> resvar.getAttributeList()
        """

    def getAttributeByName(self, name: str) -> GNSAttribute | None:
        """Return a single named attribute of the variable.

        Parameters
        ----------
        name : str
            The name of the attribute to return.

        Returns
        -------
        GNSAttribute or None
            The matching attribute handle, or ``None`` if none matches.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> status, msg, resvars = gns.executeCommand('c2d cal nij')
        >>> resvar = resvars[0]
        >>> attr = resvar.getAttributeByName("CE")
        """

class GNSAttribute:
    """Handle to a GNS variable attribute.

    An attribute is a named value attached to a variable, exposing its name
    and value.

    Notes
    -----
    Handles are not constructed directly. They are obtained from a variable
    handle, for example via ``GNSUserVariable.getAttributeList`` or
    ``GNSVariable``-derived ``getAttributeByName`` methods.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> uvar = gns.getUserVariableList()[0]
    >>> attr = uvar.getAttributeList()[0]
    >>> attr.getValue()
    """

    def getName(self) -> str:
        """Return the attribute name.

        Returns
        -------
        str
            The name of the attribute.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariableList()[0]
        >>> attr = uvar.getAttributeList()[0]
        >>> attr.getName()
        'Attr1'
        """

    def getValue(self) -> int | float | str | bool | None:
        """Return the attribute value.

        Returns
        -------
        int or float or str or bool or None
            The value of the attribute, or ``None`` if it is unset.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> uvar = gns.getUserVariableList()[0]
        >>> attr = uvar.getAttributeList()[0]
        >>> attr.getValue()
        """

class GNSColor:
    """Handle to a GNS color.

    A color handle carries a name and RGBA components.

    Notes
    -----
    Handles are not constructed directly. They are obtained from objects that
    expose a color, for example via ``GNSProperty.getColor``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> prop = slot.getPropertyById(100)
    >>> color = prop.getColor()
    >>> name = color.getName()
    """

    def getName(self) -> str:
        """Return the color name.

        Returns
        -------
        str
            The name of the color.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> prop = slot.getPropertyById(100)
        >>> color = prop.getColor()
        >>> name = color.getName()
        """

    def getRGBA(self) -> tuple[float, float, float, float]:
        """Return the color as an RGBA tuple.

        Returns
        -------
        tuple of (float, float, float, float)
            The red, green, blue, and alpha components, each in the range
            ``0.0`` to ``1.0``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> prop = slot.getPropertyById(100)
        >>> color = prop.getColor()
        >>> rgba = color.getRGBA()
        """

class GNSFont:
    """Handle to a GNS font.

    A font handle exposes a font's family, size, weight, and italic flag.

    Notes
    -----
    Handles are not constructed directly. They are obtained from the global
    ``gns`` object, for example via ``gns.getTextFont`` or
    ``gns.getLabelFont``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> textFont = gns.getTextFont()
    >>> textFont.getName()
    """

    def getName(self) -> str:
        """Return the font family name.

        Returns
        -------
        str
            The font family.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> labelFont = gns.getLabelFont()
        >>> labelFont.getName()
        'Arial'
        """

    def getPixelSize(self) -> float:
        """Return the font size in pixels.

        Returns
        -------
        float
            The font size in pixels.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> labelFont = gns.getLabelFont()
        >>> labelFont.getPixelSize()
        12.0
        """

    def getWeight(self) -> FontStyle:
        """Return the font weight as a font-style flag.

        Returns
        -------
        FontStyle
            The weight of the font, ``FontStyle.Normal`` or ``FontStyle.Bold``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> labelFont = gns.getLabelFont()
        >>> labelFont.getWeight()
        <FontStyle.Normal: 0>
        """

    def isItalic(self) -> bool:
        """Return whether the font is italic.

        Returns
        -------
        bool
            ``True`` if the font is italic, ``False`` otherwise.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> labelFont = gns.getLabelFont()
        >>> labelFont.isItalic()
        False
        """

class GNSCurve:
    """Handle to a curve (2D/3D plot data series) owned by a result slot.

    A curve carries its data points together with descriptive metadata: axis
    titles and units, physical dimensions, plot titles, ISO-MME channel
    information and the originating file and function names.

    Notes
    -----
    Curve handles are not constructed directly. Obtain one from a ``GNSSlot``
    (for example ``slot.getCurveById(100)`` or from ``slot.getCurveList()``).

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> curve = slot.getCurveById(100)
    >>> cymax = curve.getYMax()
    """

    def getSlotId(self) -> int:
        """Return the id of the slot that owns this curve.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> slotid = curve.getSlotId()
        """

    def getSlot(self) -> GNSSlot:
        """Return the slot that owns this curve.

        Returns
        -------
        GNSSlot
            The owning slot.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> slot = curve.getSlot()
        """

    def getId(self) -> int:
        """Return the identification number of the curve.

        Returns
        -------
        int
            The curve id.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getId()
        """

    def getName(self) -> str:
        """Return the name of the curve.

        Returns
        -------
        str
            The curve name.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getName()
        """

    def getNumPoints(self) -> int:
        """Return the number of curve points.

        Returns
        -------
        int
            The number of data points in the curve.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getNumPoints()
        """

    def getXMin(self) -> float:
        """Return the minimal x value of the curve.

        Returns
        -------
        float
            The smallest x value.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getXMin()
        """

    def getXMax(self) -> float:
        """Return the maximal x value of the curve.

        Returns
        -------
        float
            The largest x value.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getXMax()
        """

    def getYMax(self) -> float:
        """Return the maximal y value of the curve.

        Returns
        -------
        float
            The largest y value.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYMax()
        """

    def getYMin(self) -> float:
        """Return the minimal y value of the curve.

        Returns
        -------
        float
            The smallest y value.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYMin()
        """

    def getYMin_X(self) -> float:
        """Return the x value at which the minimal y value occurs.

        Returns
        -------
        float
            The x value corresponding to the smallest y value.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYMin_X()
        """

    def getYMax_X(self) -> float:
        """Return the x value at which the maximal y value occurs.

        Returns
        -------
        float
            The x value corresponding to the largest y value.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYMax_X()
        """

    def getCategory(self) -> str:
        """Return the name of the category of the curve.

        Returns
        -------
        str
            The curve category name.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getCategory()
        """

    def getSubcase(self) -> str:
        """Return the name of the subcase of the curve.

        Returns
        -------
        str
            The subcase name.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getSubcase()
        """

    def getFunctionName(self) -> str:
        """Return the name of the function represented by the curve.

        Returns
        -------
        str
            The function name.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getFunctionName()
        """

    def getXAxisTitle(self) -> str:
        """Return the title of the x-coordinate.

        Returns
        -------
        str
            The x-axis title.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getXAxisTitle()
        """

    def getXAxisUnit(self) -> str:
        """Return the physical unit of the x-coordinate.

        Returns
        -------
        str
            The x-axis unit.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getXAxisUnit()
        """

    def getYAxisTitle(self) -> str:
        """Return the title of the y-coordinate.

        Returns
        -------
        str
            The y-axis title.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYAxisTitle()
        """

    def getYAxisUnit(self) -> str:
        """Return the physical unit of the y-coordinate.

        Returns
        -------
        str
            The y-axis unit.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYAxisUnit()
        """

    def getItemId(self) -> int:
        """Return the identifier of the associated item.

        Returns
        -------
        int
            The id of the model item the curve is associated with.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getItemId()
        """

    def getItemName(self) -> str:
        """Return the name of the associated item.

        Returns
        -------
        str
            The name of the model item the curve is associated with.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getItemName()
        """

    def getModule(self) -> GNSModule | None:
        """Return the module of the associated item.

        Returns
        -------
        GNSModule or None
            The module owning the associated item, or ``None`` if the item has
            no module.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getModule()
        """

    def getItemType(self) -> str:
        """Return the type of the associated item.

        Returns
        -------
        str
            The type name of the model item the curve is associated with.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getItemType()
        """

    def getLegendLabel(self) -> str:
        """Return the legend label of the curve.

        Returns
        -------
        str
            The legend label.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getLegendLabel()
        """

    def getPlotTitle(self) -> str:
        """Return the plot title.

        Returns
        -------
        str
            The plot title.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getPlotTitle()
        """

    def getPlotSubTitle(self) -> str:
        """Return the plot subtitle.

        Returns
        -------
        str
            The plot subtitle.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getPlotSubTitle()
        """

    def getHistoryString(self) -> str:
        """Return the history of the curve's creation.

        Returns
        -------
        str
            A textual description of how the curve was created.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getHistoryString()
        """

    def getFileName(self) -> str:
        """Return the name of the file from which the curve was generated.

        Returns
        -------
        str
            The source file name.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getFileName()
        """

    def getOriginalName(self) -> str:
        """Return the original name of the curve.

        Returns
        -------
        str
            The original curve name.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getOriginalName()
        """

    def getXAxisPhyDim(self) -> str:
        """Return the physical dimension of the x-axis values.

        Returns
        -------
        str
            The physical dimension of the x values.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getXAxisPhyDim()
        """

    def getXAxisPhyDir(self) -> str:
        """Return the direction of the physical dimension of the x-values.

        Returns
        -------
        str
            The physical direction of the x values.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getXAxisPhyDir()
        """

    def getXAxisPhyDimRefSys(self) -> str:
        """Return the reference system of the direction of the x-values.

        Returns
        -------
        str
            The reference system for the x-value direction.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getXAxisPhyDimRefSys()
        """

    def getYAxisPhyDim(self) -> str:
        """Return the physical dimension of the y-axis values.

        Returns
        -------
        str
            The physical dimension of the y values.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYAxisPhyDim()
        """

    def getYAxisPhyDir(self) -> str:
        """Return the direction of the physical dimension of the y-values.

        Returns
        -------
        str
            The physical direction of the y values.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYAxisPhyDir()
        """

    def getYAxisPhyDimRefSys(self) -> str:
        """Return the reference system of the direction of the y-values.

        Returns
        -------
        str
            The reference system for the y-value direction.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getYAxisPhyDimRefSys()
        """

    def getDataTypeString(self) -> str:
        """Return the curve data-type string.

        The returned string is one of ``"XY-CURVE"`` (pairs of numeric values),
        ``"XY-BARSET"`` (pairs of categories and numeric values), ``"XYZ-CURVE"``
        (triples describing a space curve), ``"XYZ-MATRIX"`` (a surface where the
        z value depends on two numeric x/y values) or ``"XYZ-BARSET"`` (a matrix
        for a 3D bar chart where the z value depends on x/y categories).

        Returns
        -------
        str
            The data-type identifier for the curve.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getDataTypeString()
        'XY-CURVE'
        """

    def getISOMMEFilter(self) -> str:
        """Return the ISO-MME filter class.

        Returns
        -------
        str
            The ISO-MME filter class.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getISOMMEFilter()
        """

    def getISOMMEChannelCode(self) -> str:
        """Return the ISO-MME channel code.

        Returns
        -------
        str
            The ISO-MME channel code.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getISOMMEChannelCode()
        """

    def getISOMMEChannelName(self) -> str:
        """Return the ISO-MME channel name.

        Returns
        -------
        str
            The ISO-MME channel name.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getISOMMEChannelName()
        """

    def getISOMMEChannelLocation(self) -> str:
        """Return the ISO-MME channel location.

        Returns
        -------
        str
            The ISO-MME channel location.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getISOMMEChannelLocation()
        """

    def getData(
        self,
    ) -> (
        list[tuple[float, float]]
        | list[tuple[float, float, float]]
        | dict[str, list[int] | list[list[int]]]
    ):
        """Return the curve's data points.

        The concrete shape of the result depends on the curve's data type (see
        :meth:`getDataTypeString`).

        Returns
        -------
        list of tuple of float or dict
            The curve data, in one of three shapes:

            * A list of ``(x, y)`` pairs for an ``"XY-CURVE"``.
            * A list of triples for an ``"XY-COMPLEX-CURVE"``
              (``(x, y_real, y_imag)``), an ``"XY-BARSET"`` or an
              ``"XYZ-CURVE"`` (``(x, y, z)``).
            * A dict for an ``"XYZ-MATRIX"`` or ``"XYZ-BARSET"``, with keys
              ``"X_VALUES"`` (list of x values), ``"Y_VALUES"`` (list of y
              values) and ``"Z_VALUES"`` (a nested list
              ``[[z(x1, y1) ... z(xn, y1)] ... [z(x1, yn) ... z(xn, yn)]]``).
              For an ``"XYZ-BARSET"`` the x and y entries are categories rather
              than numeric values.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getData()
        """

    def getFrequency(self) -> float:
        """Return the frequency associated with the curve.

        Returns
        -------
        float
            The associated frequency; ``0`` by default when none is set.

        Examples
        --------
        >>> curve = gnspy.gns.getSlotList()[0].getCurveById(100)
        >>> curve.getFrequency()
        """

class GNSStateSet:
    """Handle to a set of result states owned by a result slot.

    A state set groups the states (time steps, modes or load steps) of one
    analysis together with the result functions defined over them. It can also
    be passed to ``GNSNode``, ``GNSElement`` and ``GNSProperty`` queries to
    evaluate function values.

    Notes
    -----
    State-set handles are not constructed directly. Obtain one from a
    ``GNSSlot`` (for example ``slot.getStateSetList()[0]``).

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> node = slot.getNodeById(100)
    >>> stset = slot.getStateSetList()[0]
    >>> func = stset.getFunctionList()[0]
    >>> st = stset.getStateList()[5]
    >>> fvalues = node.getFunctionValues(stset, func, st)
    """

    def getId(self) -> int:
        """Return the state-set id.

        Returns
        -------
        int
            The state-set id.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getId()
        """

    def getLabel(self) -> str:
        """Return the state-set label.

        Returns
        -------
        str
            The state-set label.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getLabel()
        """

    def getNumStates(self) -> int:
        """Return the number of states in this state set.

        Returns
        -------
        int
            The number of states.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getNumStates()
        """

    def getStateList(self, filter: str | None = None) -> list[GNSState]:
        """Return all or filtered states in this state set.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            state.

        Returns
        -------
        list of GNSState
            The matching state handles.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getStateList()
        """

    def getStateById(self, fid: float) -> GNSState | None:
        """Return the state with the given id.

        Parameters
        ----------
        fid : float
            The state identifier (may be an integer or a float).

        Returns
        -------
        GNSState or None
            The matching state, or ``None`` when the id is wrong or the state is
            unavailable.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getStateById(3.0)
        """

    def getStateByTime(self, time: float) -> GNSState | None:
        """Return the state at the given time.

        Parameters
        ----------
        time : float
            The state time.

        Returns
        -------
        GNSState or None
            The matching state, or ``None`` for a non-transient state set or a
            wrong or unavailable time.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getStateByTime(12.5)
        """

    def getFunctionList(self, filter: str | None = None) -> list[GNSFunction]:
        """Return all or filtered functions in this state set.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            function.

        Returns
        -------
        list of GNSFunction
            The matching function handles.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getFunctionList()
        """

    def getFunctionByName(self, function_name: str) -> GNSFunction | None:
        """Return the function with the given name.

        Parameters
        ----------
        function_name : str
            The name of the function to look up.

        Returns
        -------
        GNSFunction or None
            The matching function, or ``None`` when no function has that name.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getFunctionByName("Nodal: Total Velocity")
        """

    def hasDisplacements(self) -> bool:
        """Report whether displacements exist for this state set.

        Returns
        -------
        bool
            ``True`` if displacements exist for this state set.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.hasDisplacements()
        """

    def getType(self) -> Analysis:
        """Return the analysis-type flag for this state set.

        Returns
        -------
        Analysis
            The analysis type of the state set.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getType()
        """

    def getFrequency(self) -> float:
        """Return the frequency for this state set.

        Returns
        -------
        float
            The associated frequency.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getFrequency()
        """

    def getMode(self) -> int:
        """Return the mode for this state set.

        Returns
        -------
        int
            The mode number.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getMode()
        """

    def getSubcase(self) -> str:
        """Return the subcase name for this state set, if any.

        Returns
        -------
        str
            The subcase name, or an empty string when none is set.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> stateset.getSubcase()
        """

class GNSState:
    """Handle to a single result state within a state set.

    A state represents one time step, mode or load step. It exposes the state's
    identifier, time or degree, node coordinates and displacements, and the list
    of elements that failed in this state.

    Notes
    -----
    State handles are not constructed directly. Obtain one from a
    ``GNSStateSet`` (``getStateList``, ``getStateById`` or ``getStateByTime``)
    or from ``GNSView.getActiveState``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> stset = slot.getStateSetList()[0]
    >>> st = stset.getStateList()[5]
    >>> st.getTimeOrDegree()
    """

    def getId(self) -> float:
        """Return the state identifier.

        Returns
        -------
        float
            The state id (may be fractional).

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> state = stateset.getStateList()[-1]
        >>> state.getId()
        """

    def getName(self) -> str:
        """Return the state name.

        Returns
        -------
        str
            The state name.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> state = stateset.getStateList()[-1]
        >>> state.getName()
        """

    def getTimeOrDegree(self) -> float:
        """Return the state time or degree.

        Returns
        -------
        float
            The time (transient analyses) or degree/mode value of the state.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> state = stateset.getStateList()[-1]
        >>> state.getTimeOrDegree()
        """

    def getNodeCoordinates(self, nodes: list[GNSNode]) -> list[tuple[float, float, float]]:
        """Return the coordinates of the given nodes in this state.

        Parameters
        ----------
        nodes : list of GNSNode
            The nodes whose coordinates are required.

        Returns
        -------
        list of tuple of float
            One ``(x, y, z)`` coordinate tuple per node, in the same order as
            ``nodes``.

        Examples
        --------
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> view = gns.getViewList()[0]
        >>> state = view.getActiveState(slot)
        >>> nodes = slot.getNodeList()
        >>> state.getNodeCoordinates(nodes)
        """

    def hasDisplacements(self) -> bool:
        """Report whether displacements exist for this state.

        Returns
        -------
        bool
            ``True`` if displacements exist for this state.

        Examples
        --------
        >>> stateset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> state = stateset.getStateList()[-1]
        >>> state.hasDisplacements()
        """

    def getDisplacements(self, nodelist: list[GNSNode]) -> list[tuple[float, float, float]]:
        """Return the displacement values of the given nodes in this state.

        Parameters
        ----------
        nodelist : list of GNSNode
            The nodes whose displacements are required.

        Returns
        -------
        list of tuple of float
            One ``(dx, dy, dz)`` displacement tuple per node, in the same order
            as ``nodelist``.

        Examples
        --------
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> view = gns.getViewList()[0]
        >>> state = view.getActiveState(slot)
        >>> nodes = slot.getNodeList()
        >>> state.getDisplacements(nodes)
        """

    def setDisplacements(
        self, nodelist: list[GNSNode], values: list[tuple[float, float, float]]
    ) -> bool:
        """Set the displacement values of the given nodes in this state.

        Parameters
        ----------
        nodelist : list of GNSNode
            The nodes whose displacements are set.
        values : list of tuple of float
            One ``(dx, dy, dz)`` displacement per node, in the same order as
            ``nodelist``. Lists of three-element lists are also accepted.

        Returns
        -------
        bool
            ``True`` on success.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = slot.getStateSetList()[0]
        >>> state = stset.getStateList()[4]
        >>> nodes = slot.getNodeList()
        >>> disps = state.getDisplacements(nodes)
        >>> state.setDisplacements(nodes, disps)
        True
        """

    def getFailedElementList(self, filter: str | None = None) -> list[GNSElement]:
        """Return all or filtered failed elements in this state.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression; ``None`` (default) returns every
            failed element.

        Returns
        -------
        list of GNSElement
            The elements that failed in this state.

        Examples
        --------
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> view = gns.getViewList()[0]
        >>> state = view.getActiveState(slot)
        >>> state.getFailedElementList()
        """

class GNSFunction:
    """Handle to a result function defined over a state set.

    A function may be a scalar, vector or tensor field evaluated on nodes,
    elements or properties (parts). It provides access to its label, kind and
    item type, and reads or writes real and complex values at a given state.

    Notes
    -----
    Function handles are not constructed directly. Obtain one from a
    ``GNSStateSet`` (``getFunctionList`` or ``getFunctionByName``).

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> node = slot.getNodeById(100)
    >>> stset = slot.getStateSetList()[0]
    >>> func = stset.getFunctionByName("Nodal: Total Velocity")
    >>> st = stset.getStateList()[5]
    >>> fvalues = node.getFunctionValues(stset, func, st)
    """

    def getLabel(self) -> str:
        """Return the function's label.

        Returns
        -------
        str
            The function label.

        Examples
        --------
        >>> stset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> func = stset.getFunctionList()[0]
        >>> func.getLabel()
        """

    def hasValues(self, state: GNSState) -> bool:
        """Report whether the function has values for the given state.

        Parameters
        ----------
        state : GNSState
            The state to test.

        Returns
        -------
        bool
            ``True`` if the function has values for ``state``.

        Examples
        --------
        >>> stset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> state = stset.getStateList()[-1]
        >>> func = stset.getFunctionList()[0]
        >>> func.hasValues(state)
        """

    def getItemType(self) -> FunctionItem:
        """Return the function's item type.

        Returns
        -------
        FunctionItem
            One of ``FunctionItem.Node``, ``FunctionItem.Element``,
            ``FunctionItem.Property`` or ``FunctionItem.NodeElement``.

        Examples
        --------
        >>> stset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> func = stset.getFunctionList()[0]
        >>> func.getItemType()
        """

    def getType(self) -> Function:
        """Return the function's kind.

        Returns
        -------
        Function
            One of ``Function.Function`` (scalar), ``Function.Vector`` or
            ``Function.Tensor``.

        Examples
        --------
        >>> stset = gnspy.gns.getSlotList()[0].getStateSetList()[0]
        >>> func = stset.getFunctionList()[0]
        >>> func.getType()
        """

    def getValues(
        self, state: GNSState, items: list[GNSNode] | list[GNSElement] | list[GNSProperty]
    ) -> list[tuple[float, float]]:
        """Return the function values of the given items at the given state.

        Parameters
        ----------
        state : GNSState
            The state at which values are read.
        items : list of GNSNode or list of GNSElement or list of GNSProperty
            The nodes, elements or properties (parts) to evaluate.

        Returns
        -------
        list of tuple of float
            One entry per item, in the same order as ``items``.

        Notes
        -----
        The static return type is a simplification of a polymorphic result. For
        a scalar function one value is returned per item; for a vector function
        the components ``[Vx, Vy, Vz, Vmag]`` are returned per item; for a
        tensor function twelve values (two eigenvectors, the third orthogonal
        eigenvector and three eigenvalues) are returned per item. The compiled
        module cannot be executed here to confirm the exact tuple arity.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = slot.getStateSetList()[0]
        >>> state = stset.getStateList()[6]
        >>> func = stset.getFunctionByName("Shell: Max. v. Mises stress over thickness")
        >>> nodes = slot.getNodeList()
        >>> func.getValues(state, nodes)
        """

    def getComplexValues(
        self, state: GNSState, items: list[GNSNode] | list[GNSElement] | list[GNSProperty]
    ) -> list[list[tuple[float, float]]]:
        """Return the complex function values of the given items at the given state.

        Parameters
        ----------
        state : GNSState
            The state at which values are read.
        items : list of GNSNode or list of GNSElement or list of GNSProperty
            The nodes, elements or properties (parts) to evaluate.

        Returns
        -------
        list of list of tuple of float
            One entry per item; each entry is a list of ``(real, imag)`` complex
            pairs, one pair per function/vector/tensor component.

        Notes
        -----
        The number of components per item depends on the function kind (scalar,
        vector or tensor). The compiled module cannot be executed here to
        confirm the exact per-item arity.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = slot.getStateSetList()[0]
        >>> state = stset.getStateList()[6]
        >>> func = stset.getFunctionByName("Nodal Y-Displacement")
        >>> nodes = slot.getNodeList()
        >>> func.getComplexValues(state, nodes)
        """

    def setValues(
        self,
        state: GNSState,
        items: list[GNSNode] | list[GNSElement] | list[GNSProperty],
        values: list[float] | list[list[float]],
    ) -> bool:
        """Set the function values of the given items at the given state.

        Parameters
        ----------
        state : GNSState
            The state at which values are written.
        items : list of GNSNode or list of GNSElement or list of GNSProperty
            The nodes, elements or properties (parts) to update.
        values : list of float or list of list of float
            One value per item. Scalars are plain floats; vectors are
            ``[Vx, Vy, Vz]``, ``[Vx, Vy, Vz, Vmag]`` or ``[i, j, k, Vmag]``;
            tensors are 9 values (3 normal and 6 shear) or 12 values (two
            eigenvectors, the third orthogonal eigenvector and three
            eigenvalues, as returned by :meth:`getValues`).

        Returns
        -------
        bool
            ``True`` on success.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = slot.getStateSetList()[0]
        >>> state = stset.getStateList()[2]
        >>> fun = stset.getFunctionByName("newFunc")
        >>> bars = [slot.getElementById(39000620), slot.getElementById(39000622)]
        >>> fun.setValues(state, bars, [0.05, 0.05])
        True
        """

    def setComplexValues(
        self,
        state: GNSState,
        items: list[GNSNode] | list[GNSElement] | list[GNSProperty],
        values: list[list[tuple[float, float]]],
    ) -> bool:
        """Set the complex function values of the given items at the given state.

        Parameters
        ----------
        state : GNSState
            The state at which values are written.
        items : list of GNSNode or list of GNSElement or list of GNSProperty
            The nodes, elements or properties (parts) to update.
        values : list of list of tuple of float
            One entry per item; each entry is a list of ``(real, imag)`` complex
            pairs, one pair per function/vector/tensor component.

        Returns
        -------
        bool
            ``True`` on success.

        Examples
        --------
        >>> slot = gnspy.gns.getSlotList()[0]
        >>> stset = slot.getStateSetList()[0]
        >>> state = stset.getStateList()[2]
        >>> fun = stset.getFunctionByName("newCmplxFunc")
        >>> tetra = [slot.getElementById(2381), slot.getElementById(1594)]
        >>> fun.setComplexValues(state, tetra, [[(0.05, 0.05)], [(0.05, 0.05)]])
        True
        """

class GNSImage:
    """Handle to an image loaded into a slot.

    Notes
    -----
    Image handles are not constructed directly. Obtain one from a
    :class:`GNSSlot` (e.g. ``slot.getImageById``) or from the global ``gns``
    object (``gns.getImageById``, ``gns.getImageByName``, ``gns.getImageList``),
    then query its geometry and source data through the getters below.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> image = slot.getImageById(100)
    >>> image.getId()
    100
    """

    def getSlotId(self) -> int:
        """Return the id of the slot the image belongs to.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> slotid = image.getSlotId()
        """

    def getSlot(self) -> GNSSlot | None:
        """Return the slot the image belongs to.

        Returns
        -------
        GNSSlot or None
            The owning slot, or ``None`` if the image has no associated slot.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> slot = image.getSlot()
        """

    def getId(self) -> int:
        """Return the image id.

        Returns
        -------
        int
            The image id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getId()
        100
        """

    def getName(self) -> str:
        """Return the image name.

        Returns
        -------
        str
            The image name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getName()
        'image_1'
        """

    def getWidth(self) -> int:
        """Return the image width in pixels.

        Returns
        -------
        int
            The image width.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getWidth()
        1920
        """

    def getHeight(self) -> int:
        """Return the image height in pixels.

        Returns
        -------
        int
            The image height.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getHeight()
        1080
        """

    def getXposition(self) -> float:
        """Return the image x position.

        Returns
        -------
        float
            The image x position.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getXposition()
        0.0
        """

    def getYposition(self) -> float:
        """Return the image y position.

        Returns
        -------
        float
            The image y position.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getYposition()
        0.0
        """

    def getImagetype(self) -> str:
        """Return the image type.

        Returns
        -------
        str
            The image type.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getImagetype()
        'png'
        """

    def getFilename(self) -> str:
        """Return the image file name.

        Returns
        -------
        str
            The image source file name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> image = slot.getImageById(100)
        >>> image.getFilename()
        'background.png'
        """

class GNSVideo:
    """Handle to a video loaded into a slot.

    Notes
    -----
    Video handles are not constructed directly. Obtain one from a
    :class:`GNSSlot` (e.g. ``slot.getVideoById``) or from the global ``gns``
    object (``gns.getVideoById``, ``gns.getVideoByName``, ``gns.getVideoList``),
    then query its frame range, sensor and lens-distortion parameters through
    the getters below.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> vid = slot.getVideoById(100)
    >>> vid.getId()
    100
    """

    def getSlotId(self) -> int:
        """Return the id of the slot the video belongs to.

        Returns
        -------
        int
            The owning slot's id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> slotid = video.getSlotId()
        """

    def getSlot(self) -> GNSSlot | None:
        """Return the slot the video belongs to.

        Returns
        -------
        GNSSlot or None
            The owning slot, or ``None`` if the video has no associated slot.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> slot = video.getSlot()
        """

    def getId(self) -> int:
        """Return the video id.

        Returns
        -------
        int
            The video id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getId()
        1
        """

    def getName(self) -> str:
        """Return the video name.

        Returns
        -------
        str
            The video name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getName()
        'crash_cam'
        """

    def getNumberOfFrames(self) -> int:
        """Return the number of frames in the video.

        Returns
        -------
        int
            The total frame count.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getNumberOfFrames()
        300
        """

    def getSensorWidth(self) -> int:
        """Return the video sensor width.

        Returns
        -------
        int
            The sensor width.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getSensorWidth()
        1920
        """

    def getSensorHeight(self) -> int:
        """Return the video sensor height.

        Returns
        -------
        int
            The sensor height.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getSensorHeight()
        1080
        """

    def getCodec(self) -> str:
        """Return the video codec.

        Returns
        -------
        str
            The codec identifier.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getCodec()
        'h264'
        """

    def getInputFiletype(self) -> str:
        """Return the video input file type.

        Returns
        -------
        str
            The input file type.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getInputFiletype()
        'mp4'
        """

    def getInputFileName(self) -> str:
        """Return the video input file name.

        Returns
        -------
        str
            The input file name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getInputFileName()
        'crash.mp4'
        """

    def getStartTime(self) -> float:
        """Return the video start time.

        Returns
        -------
        float
            The start time.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getStartTime()
        0.0
        """

    def getEndTime(self) -> float:
        """Return the video end time.

        Returns
        -------
        float
            The end time.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getEndTime()
        10.0
        """

    def getFirstFrame(self) -> int:
        """Return the video first frame.

        Returns
        -------
        int
            The first frame index.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getFirstFrame()
        0
        """

    def getLastFrame(self) -> int:
        """Return the video last frame.

        Returns
        -------
        int
            The last frame index.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getLastFrame()
        299
        """

    def getPrinciplePointX(self) -> float:
        """Return the x position of the principal point in pixels.

        Returns
        -------
        float
            The principal point x coordinate, in pixels.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getPrinciplePointX()
        960.0
        """

    def getPrinciplePointY(self) -> float:
        """Return the y position of the principal point in pixels.

        Returns
        -------
        float
            The principal point y coordinate, in pixels.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getPrinciplePointY()
        540.0
        """

    def getFocalLength(self) -> float:
        """Return the focal length in millimetres.

        Returns
        -------
        float
            The focal length, in mm.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getFocalLength()
        35.0
        """

    def getPixelDistanceX(self) -> float:
        """Return the pixel distance in x in millimetres.

        Returns
        -------
        float
            The pixel distance in x, in mm.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getPixelDistanceX()
        0.01
        """

    def getPixelDistanceY(self) -> float:
        """Return the pixel distance in y in millimetres.

        Returns
        -------
        float
            The pixel distance in y, in mm.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getPixelDistanceY()
        0.01
        """

    def getLengthUnitOfParameters(self) -> str:
        """Return the unit of the distortion parameters.

        Returns
        -------
        str
            The distortion-parameter unit, either ``"mm"`` or ``"px"``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getLengthUnitOfParameters()
        'mm'
        """

    def getParameterA(self) -> list[float]:
        """Return the radial symmetrical distortion coefficients.

        Returns
        -------
        list of float
            The radial symmetrical distortion parameters (A).

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getParameterA()
        [0.0, 0.0, 0.0]
        """

    def getParameterB(self) -> list[float]:
        """Return the radial asymmetrical distortion coefficients.

        Returns
        -------
        list of float
            The radial asymmetrical distortion parameters (B).

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getParameterB()
        [0.0, 0.0]
        """

    def getParameterC(self) -> list[float]:
        """Return the affinity distortion coefficients.

        Returns
        -------
        list of float
            The affinity distortion parameters (C).

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getParameterC()
        [0.0, 0.0]
        """

    def getParameterR(self) -> float:
        """Return the zero crossing of the distortion curve.

        Returns
        -------
        float
            The zero crossing of the distortion curve (R).

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> slot = gns.getSlotList()[0]
        >>> video = slot.getVideoById(1)
        >>> video.getParameterR()
        0.0
        """

class GNSInclude:
    """Handle to a single include (source) file of the model.

    Notes
    -----
    Include handles are not constructed directly. Obtain one from a
    :class:`GNSSlot` (e.g. ``slot.getTopLevelIncludes()``) or from a
    :class:`GNSKeyword` (``keyword.getFile()``). Includes form a tree; use
    :meth:`getParent` and :meth:`getChildren` to navigate it.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> slot = gns.getSlotList()[0]
    >>> include = slot.getTopLevelIncludes()[0]
    >>> include.getPath()
    'main.inc'
    """

    def getChildren(self) -> list[GNSInclude]:
        """Return the child includes of this include.

        Returns
        -------
        list of GNSInclude
            The child include files, empty if this include has no children.

        Examples
        --------
        >>> for child in include.getChildren():
        ...     print(child.getPath())
        """

    def getParent(self) -> GNSInclude | None:
        """Return the parent include of this include.

        Returns
        -------
        GNSInclude or None
            The parent include, or ``None`` if this include is top level.

        Examples
        --------
        >>> parent_include = include.getParent()
        >>> if parent_include:
        ...     print(parent_include.getPath())
        """

    def getPath(self) -> str:
        """Return the include file name.

        The returned path may be relative or absolute.

        Returns
        -------
        str
            The include file name.

        Examples
        --------
        >>> print(include.getPath())
        main.inc
        """

class GNSKeyword:
    """Handle to a solver keyword (a single input-deck entry).

    A keyword wraps one entry of a solver input deck (e.g. LS-Dyna,
    PAM-CRASH). Its parameters, cards, comments, id, name and type can be read
    and modified, and the keywords it references or that reference it can be
    traversed.

    Notes
    -----
    Keyword handles are not constructed directly. Obtain existing ones from the
    global ``gns`` object (``gns.getKeywordList``) or from a :class:`GNSSlot`
    (``slot.getKeywordById``, ``slot.getKeywordByIndex``); create new ones with
    ``slot.createKeyword``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> keyword = gns.getKeywordList()[0]
    >>> keyword.getId()
    1
    """

    def addCard(self, name: str) -> None:
        """Add an optional or repeated card to the keyword.

        Parameters
        ----------
        name : str
            The name of the card to add.

        Raises
        ------
        Exception
            If the named card does not exist for this keyword.

        Examples
        --------
        >>> keyword = gns.getKeywordList("GROUP")[0]
        >>> keyword.addCard("META Card")
        """

    def getComment(self) -> list[str]:
        """Return the comment lines at the top of the keyword.

        Each returned line includes the leading comment character(s).

        Returns
        -------
        list of str
            The comment lines.

        Examples
        --------
        >>> keyword = gns.getKeywordList("GROUP")[0]
        >>> keyword.getComment()
        ['$ This is Group', '$ for the initial velocity']
        """

    def getFile(self) -> GNSInclude:
        """Return the include file the keyword belongs to.

        Returns
        -------
        GNSInclude
            The include (source) file that contains the keyword.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList()[0]
        >>> keyword.getFile().getPath()
        'include.inc'
        """

    def getGES(self, index: int = 0) -> list[tuple[str, list[str]]]:
        """Return the general entity selection (GES) at the given index.

        This is a PAM-CRASH-only feature.

        Parameters
        ----------
        index : int, optional
            The index of the GES to return. Default is ``0``.

        Returns
        -------
        list of tuple of (str, list of str)
            The GES entries, each a ``(type, selection)`` pair.

        Raises
        ------
        Exception
            If no GES exists at the given index.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("CNTAC")[0]
        >>> params = keyword.getGES()
        >>> print(params)
        (('NOD', ('1', '5:10')), ('ELE', ('50-100')))
        """

    def getId(self) -> int:
        """Return the keyword id.

        Returns
        -------
        int
            The keyword id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList()[0]
        >>> keyword.getId()
        1
        """

    def getLinkedKeyword(self, name: str, index: int = 0) -> GNSKeyword | None:
        """Return the linked keyword in another solver.

        A linked keyword is one where a change in either keyword may affect the
        other, and where deleting one deletes the other.

        Parameters
        ----------
        name : str
            The name of the solver whose linked keyword is requested.
        index : int, optional
            The index of the linked keyword when several exist. Default is
            ``0``.

        Returns
        -------
        GNSKeyword or None
            The linked keyword, or ``None`` if none is linked.

        Examples
        --------
        >>> pam_keyword = gns.getKeywordById("GROUP", solver='PAM-CRASH')
        >>> dyna_keyword = pam_keyword.getLinkedKeyword('LS-Dyna')
        >>> print(dyna_keyword.getType())
        SET_NODE
        """

    def getModule(self) -> GNSModule | None:
        """Return the module the keyword belongs to.

        Returns
        -------
        GNSModule or None
            The keyword's module, or ``None`` if it has none.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList()[0]
        >>> keyword.getModule()
        """

    def getName(self) -> str:
        """Return the keyword title.

        Returns
        -------
        str
            The keyword title.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList()[0]
        >>> keyword.getName()
        'Mat 1'
        """

    def getParam(self, name: str) -> int | float | str | bool | None:
        """Return the value of a single parameter of the keyword.

        If multiple values exist for the parameter, the first is returned.

        Parameters
        ----------
        name : str
            The parameter name.

        Returns
        -------
        int or float or str or bool or None
            The parameter value, or ``None`` if the parameter is not found.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("MATER")[0]
        >>> keyword.getParam("E")
        21000000.0
        """

    def getParamList(self, filter: str | None = None) -> list[tuple[str, int | float | str | bool]]:
        """Return the keyword's parameters as ``(name, value)`` pairs.

        Parameters
        ----------
        filter : str or None, optional
            A GNS list-filter expression selecting which parameters to return;
            ``None`` (default) returns all parameters.

        Returns
        -------
        list of tuple of (str, int or float or str or bool)
            The ``(name, value)`` pairs.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("MATER")[0]
        >>> keyword.getParamList()
        [['ID', 5], ['TITLE', 'title'], ['E', 21000000.0]]
        """

    def getParams(self, name: str) -> list[int | float | str | bool]:
        """Return all values for a single parameter of the keyword.

        Parameters
        ----------
        name : str
            The parameter name.

        Returns
        -------
        list of (int or float or str or bool)
            The parameter values, empty if the parameter does not exist.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("FUNCT")[0]
        >>> keyword.getParams("X")
        [0.0, 1.0, 2.2, 3.1]
        """

    def getReferencedKeyword(self, name: str, index: int = 0) -> GNSKeyword | None:
        """Return the keyword referenced by a given parameter.

        Parameters
        ----------
        name : str
            The parameter whose referenced keyword is requested.
        index : int, optional
            The index of the referenced keyword when the parameter references
            several. Default is ``0``.

        Returns
        -------
        GNSKeyword or None
            The referenced keyword, or ``None`` if nothing is found.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("BDFOR")[0]
        >>> sensor = keyword.getReferencedKeyword("ISENS")
        >>> print(sensor.getId())
        20
        """

    def getReferencesList(
        self, ignoreNodesAndElements: bool = False, filter: str | None = None
    ) -> list[GNSKeyword]:
        """Return all keywords that reference this keyword.

        Parameters
        ----------
        ignoreNodesAndElements : bool, optional
            If ``True``, exclude node and element keywords from the result.
            Default is ``False``.
        filter : str or None, optional
            A GNS list-filter expression selecting which referencing keywords to
            return; ``None`` (default) applies no filter.

        Returns
        -------
        list of GNSKeyword
            The keywords that reference this keyword.

        Examples
        --------
        >>> keyword = gns.getKeywordById("GROUP", solver='PAM-CRASH')
        >>> refer_keywords = keyword.getReferencesList(ignoreNodesAndElements=True)
        >>> kw = refer_keywords[0]
        >>> print(kw.getType())
        PART
        """

    def getSolver(self) -> str:
        """Return the solver the keyword belongs to.

        Returns
        -------
        str
            The solver name, e.g. ``"LS-Dyna"`` or ``"PAM-CRASH"``.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList()[0]
        >>> keyword.getSolver()
        'LS-Dyna'
        """

    def getType(self) -> str:
        """Return the keyword type.

        The returned type includes any keyword options (for LS-Dyna).

        Returns
        -------
        str
            The keyword type.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList()[0]
        >>> keyword.getType()
        'PART'
        """

    def removeCard(self, name: str) -> bool:
        """Remove an optional or repeated card from the keyword.

        If several repeated cards share the name, all are removed.

        Parameters
        ----------
        name : str
            The name of the card to remove.

        Returns
        -------
        bool
            ``True`` if the card could be removed, ``False`` otherwise.

        Raises
        ------
        Exception
            If the named card does not exist for this keyword.

        Examples
        --------
        >>> keyword = gns.getKeywordList("GROUP")[0]
        >>> if not keyword.removeCard("META Card"):
        ...     print("META section was not active")
        """

    def setComment(self, comment: list[str]) -> None:
        """Set the comment lines at the top of the keyword.

        Any line that does not already begin with the comment character(s) has
        them prepended.

        Parameters
        ----------
        comment : list of str
            The comment lines to set.

        Returns
        -------
        None

        Examples
        --------
        >>> keyword = gns.getKeywordList("GROUP")[0]
        >>> keyword.setComment(['This is a Group', 'for the initial velocity'])
        >>> keyword.getComment()
        ['$ This is Group', '$ for the initial velocity']
        """

    def setGES(self, ges: list[tuple[str, list[str]]], index: int = 0) -> None:
        """Set the general entity selection (GES) at the given index.

        This is a PAM-CRASH-only feature.

        Parameters
        ----------
        ges : list of tuple of (str, list of str)
            The GES entries to set, each a ``(type, selection)`` pair.
        index : int, optional
            The index of the GES to set. Default is ``0``.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If no GES exists at the given index.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("CNTAC")[0]
        >>> keyword.setGES((('NOD', ('1', '5:10')), ('ELE', ('50-100'))), index=0)
        """

    def setId(self, id: int) -> None:
        """Set the keyword id.

        Parameters
        ----------
        id : int
            The new keyword id.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the keyword does not have an id.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("MATER")[0]
        >>> keyword.setId(100001)
        """

    def setName(self, name: str) -> None:
        """Set the keyword name.

        Parameters
        ----------
        name : str
            The new keyword name.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the keyword does not have a name.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("MATER")[0]
        >>> keyword.setName('Mat 1')
        """

    def setParam(self, name: str, value: float | str | bool) -> None:
        """Set a single parameter of the keyword.

        Parameters
        ----------
        name : str
            The parameter name.
        value : int or float or str or bool
            The value to set.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the named parameter does not exist.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("MATER")[0]
        >>> keyword.setParam("TITLE", "new title")
        """

    def setParamList(self, params: list[tuple[str, int | float | str | bool]]) -> None:
        """Set several parameters of the keyword from ``(name, value)`` pairs.

        Parameters
        ----------
        params : list of tuple of (str, int or float or str or bool)
            The ``(name, value)`` pairs to set.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If any of the given names does not exist.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("MATER")[0]
        >>> keyword.setParamList((("TITLE", "new title"), ("E", 2.1E7)))
        """

    def setParams(self, name: str, values: list[int | float | str | bool]) -> None:
        """Set all values for a single parameter of the keyword.

        Parameters
        ----------
        name : str
            The parameter name.
        values : list of (int or float or str or bool)
            The values to set for the parameter.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the named parameter does not exist.

        Examples
        --------
        >>> import gnspy
        >>> gns = gnspy.gns
        >>> keyword = gns.getKeywordList("FUNCT")[0]
        >>> keyword.setParams("X", (1.0, 2.0, 3.0))
        >>> keyword.setParams("Y", (4.0, 5.0, 6.0))
        """

    def setType(self, type: str) -> None:
        """Set the keyword type.

        The new type must be similar to the current type (e.g. ``MTOJNT`` and
        ``KJOIN``) or an exception is raised. In LS-Dyna the type must be given
        without options (e.g. ``"PART"`` rather than ``"PART_CONTACT"``); use
        ``setParam('option<n>', '<string>')`` to change an option.

        Parameters
        ----------
        type : str
            The new keyword type.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the new type does not match the current type.

        Examples
        --------
        >>> keyword = gns.getKeywordByIndex("KJOIN", 0)
        >>> keyword.setType("MTOJNT")
        """

    def toStrings(self) -> list[str]:
        """Return the keyword as the lines that would be exported to a file.

        Returns
        -------
        list of str
            The keyword rendered as export lines.

        Examples
        --------
        >>> keyword = gns.getKeywordList("PART")[0]
        >>> keyword.toStrings()
        ['$ This is a PART', '*PART', 'Property 1', '         1         1']
        """

class GNSPattern(GNSVariable):
    """Handle to a referenced pattern variable.

    A referenced pattern is a named pattern variable of the model; it exposes
    the same accessors as its base :class:`GNSVariable` (``getName`` and
    ``getValue``).

    Notes
    -----
    Pattern handles are not constructed directly. Obtain one from the global
    ``gns`` object with ``gns.getReferencedPattern(name)`` or
    ``gns.getReferencedPatternList()``.

    Examples
    --------
    >>> import gnspy
    >>> gns = gnspy.gns
    >>> rpat = gns.getReferencedPatternList()[0]
    >>> rpat.getValue()
    """
