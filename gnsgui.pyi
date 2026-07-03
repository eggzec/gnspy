"""GNS Animator4 Python GUI toolkit.

``gnsgui`` is the compiled Python extension that lets scripts build native,
Qt-based user interfaces (dialogs, dock widgets and their child widgets) that run
inside GNS Animator4. It complements :mod:`gnspy`: a script drives the model and
results through ``gnspy`` and presents controls or output to the user through
``gnsgui``.

Notes
-----
:class:`Widget` is the root of the widget hierarchy; concrete controls such as
:class:`Label`, :class:`PushButton` and :class:`ComboBox` derive from it, while
:class:`HBoxLayout`, :class:`VBoxLayout` and :class:`GridLayout` derive from
:class:`Layout`. Widgets are constructed directly (for example
``Label(parent, "Name")``) and arranged with layouts. User interaction is handled
through callbacks registered with the ``on...`` methods.
"""

import enum
import typing

class Widget:
    """Base class for all GUI widgets, usable as an empty container.

    A ``Widget`` is the superclass of every widget in ``gnsgui``. It can also be
    instantiated directly and used as an empty container to be filled with other
    widgets through a layout.

    Notes
    -----
    Construct a plain container with ``Widget(parent)`` and add it to a layout,
    or subclass-widgets (``Label``, ``PushButton``, ...) that inherit these
    methods.
    """

    def __init__(self, parent: Widget) -> None:
        """Construct a container widget to be filled with other widgets.

        Parameters
        ----------
        parent : Widget
            The parent widget that owns this widget.

        Examples
        --------
        >>> widget = gnsgui.Widget(parent)
        >>> parentLayout.addWidget(widget)
        """

    def app(self) -> App:
        """Return the application object this widget belongs to.

        Returns
        -------
        App
            The owning application.

        Examples
        --------
        >>> vbox = VBoxLayout(dialog)
        >>> hbox = HBoxLayout(dialog.app())
        >>> vbox.addLayout(hbox)
        """

    def delete(self) -> None:
        """Delete the widget.

        Notes
        -----
        Using ``del`` on the Python reference does not delete the widget, because
        the parent or application still holds a reference to it; call this method
        to remove it.
        """

    def hide(self) -> None:
        """Hide the widget."""

    def isEnabled(self) -> bool:
        """Return whether the widget is enabled.

        Returns
        -------
        bool
            ``True`` if the widget is enabled, ``False`` otherwise.
        """

    def isVisible(self) -> bool:
        """Return whether the widget is currently visible.

        Returns
        -------
        bool
            ``True`` if the widget is visible, ``False`` otherwise.
        """

    def setEnabled(self, flag: bool) -> None:
        """Enable or disable the widget.

        Parameters
        ----------
        flag : bool
            ``True`` to enable the widget, ``False`` to disable it.
        """

    def setToolTip(self, toolTip: str) -> None:
        """Set the widget's tooltip.

        Parameters
        ----------
        toolTip : str
            The tooltip text shown on hover.
        """

    def show(self) -> None:
        """Show the widget.

        Notes
        -----
        All widgets other than dialogs are shown by default.
        """

    def toolTip(self) -> str:
        """Return the widget's current tooltip.

        Returns
        -------
        str
            The current tooltip text.
        """

class Layout:
    """Base class for all layouts; cannot be constructed directly.

    Notes
    -----
    Instances are created through concrete subclasses such as ``HBoxLayout``,
    ``VBoxLayout`` and ``GridLayout``; this base class cannot be instantiated on
    its own.
    """

    def delete(self) -> None:
        """Delete the layout.

        Notes
        -----
        Using ``del`` on the Python reference does not delete the layout, because
        the parent or application still holds a reference to it; call this method
        to remove it.
        """

class App:
    """The application object; only one instance may exist.

    Notes
    -----
    Construct a single ``App`` at the start of a GUI script, create dialogs or
    dock widgets, then enter the event loop with :meth:`exec`.
    """

    def __init__(self) -> None:
        """Construct the base application for the script.

        Examples
        --------
        >>> app = gnsgui.App()
        """

    def exec(self) -> None:
        """Enter the event loop and process GUI interaction until closed.

        A dialog or dock widget must have been created before calling this
        method. The loop finishes once the final dock widget or parentless
        dialog has been destroyed.

        Notes
        -----
        The application is destroyed after this function returns; do not use the
        ``App`` instance again afterwards.

        Examples
        --------
        >>> app = gnsgui.App()
        >>> dialog = gnsgui.Dialog(app)
        >>> dialog.show()
        >>> app.exec()
        """

    def interrupt(self, arg0: typing.Callable[[], None]) -> None:
        """Interrupt the running event loop by scheduling a callable.

        Parameters
        ----------
        arg0 : callable
            A callable taking no arguments and returning nothing; it is invoked
            in the same thread as the application.

        Notes
        -----
        This only makes sense when :meth:`interrupt` is called from another
        thread than the one running :meth:`exec`.

        Examples
        --------
        >>> def setlabel():
        ...     time.sleep(5)
        ...     app.interrupt(lambda: label.setText("Interrupted!"))
        >>> threading.Thread(target=setlabel).start()
        >>> app.exec()
        """

    def killTimer(self, timerIdentifier: int) -> None:
        """Stop a previously started timer.

        Parameters
        ----------
        timerIdentifier : int
            The identifier returned by :meth:`startTimer`. If no timer with this
            identifier exists, the call is ignored.

        Examples
        --------
        >>> timerId = -1
        >>> def runOnceAndStop():
        ...     global timerId
        ...     app.killTimer(timerId)
        ...     timerId = -1
        >>> timerId = app.startTimer(1000, runOnceAndStop)
        """

    def startSingleTimer(self, milliseconds: int, callback: typing.Callable[[], None]) -> int:
        """Start a one-shot timer that fires the callback once.

        Parameters
        ----------
        milliseconds : int
            Approximate delay before the callback is invoked.
        callback : callable
            A callable taking no arguments and returning nothing, invoked once
            after the delay.

        Returns
        -------
        int
            An identifier for the timer.

        Examples
        --------
        >>> def update():
        ...     print("Updated")
        >>> app.startSingleTimer(1000, update)
        """

    def startTimer(self, milliseconds: int, callback: typing.Callable[[], None]) -> int:
        """Start a repeating timer that fires the callback periodically.

        Parameters
        ----------
        milliseconds : int
            Approximate interval between callback invocations.
        callback : callable
            A callable taking no arguments and returning nothing, invoked on each
            tick.

        Returns
        -------
        int
            A non-negative identifier that can be passed to :meth:`killTimer` to
            stop the timer.

        Notes
        -----
        If timeouts cannot all be delivered because other code is still running,
        they are silently discarded. Using a short interval (below roughly 0.5 s)
        causes high CPU usage by the Python process.

        Examples
        --------
        >>> def update():
        ...     print("Updating")
        >>> app.startTimer(1000, update)
        """

class Color:
    """A color defined by RGBA components and an optional name.

    Notes
    -----
    Construct a color from a 4-element RGBA sequence or a 3-element RGB sequence
    (in which case the alpha channel defaults to ``255``), each component in the
    range 0-255.
    """

    @typing.overload
    def __init__(self, rgba: tuple[int, int, int, int], name: str = "") -> None: ...
    @typing.overload
    def __init__(self, rgba: tuple[int, int, int], name: str = "") -> None:
        """Construct a color from RGB(A) components and an optional name.

        Parameters
        ----------
        rgba : tuple of int
            Either a 4-tuple ``(red, green, blue, alpha)`` or a 3-tuple
            ``(red, green, blue)``; in the 3-tuple form the alpha channel is set
            to ``255``. Each component is in the range 0-255.
        name : str, optional
            A human-readable name for the color. Default is ``""``.

        Examples
        --------
        >>> red = gnsgui.Color((255, 0, 0, 255), "red")
        >>> green = gnsgui.Color((0, 255, 0), "green")
        """

    def name(self) -> str:
        """Return the name of the color.

        Returns
        -------
        str
            The color's name, or an empty string if none was given.
        """

    def rgba(self) -> tuple[int, int, int, int]:
        """Return the color's RGBA components.

        Returns
        -------
        tuple of int
            The ``(red, green, blue, alpha)`` components, each in the range
            0-255.
        """

class Label(Widget):
    """A widget that displays static text or an image.

    Notes
    -----
    Construct with ``Label(text, parent)`` and add it to a layout.
    """

    class Alignment(enum.IntEnum):
        """Alignment of the text within the label.

        Attributes
        ----------
        Left : Alignment
            Align the text to the left-hand side.
        Right : Alignment
            Align the text to the right-hand side.
        Center : Alignment
            Align the text to the center of the widget.
        """

        Center = 0
        Left = 1
        Right = 2

    #: Alias for :attr:`Alignment.Center`.
    Center: typing.ClassVar[Alignment]
    #: Alias for :attr:`Alignment.Left`.
    Left: typing.ClassVar[Alignment]
    #: Alias for :attr:`Alignment.Right`.
    Right: typing.ClassVar[Alignment]

    def __init__(self, text: str, parent: Widget) -> None:
        """Construct a label.

        Parameters
        ----------
        text : str
            The text shown on the label.
        parent : Widget
            The parent widget that owns this label.
        """

    def alignment(self) -> Label.Alignment:
        """Return the current text alignment.

        Returns
        -------
        Label.Alignment
            The current alignment.
        """

    def setAlignment(self, alignment: Label.Alignment) -> None:
        """Set the text alignment.

        Parameters
        ----------
        alignment : Label.Alignment
            The alignment to apply.
        """

    def setIcon(self, image: str) -> None:
        """Set the image of the label (deprecated).

        Parameters
        ----------
        image : str
            Path to the image to display.

        Notes
        -----
        Deprecated; use :meth:`setImage` instead.
        """

    def setImage(self, image: str) -> None:
        """Set the image displayed by the label.

        Parameters
        ----------
        image : str
            Path to the image to display.
        """

    def setText(self, text: str) -> None:
        """Set the text of the label.

        Parameters
        ----------
        text : str
            The new text.
        """

    def setWordWrap(self, flag: bool) -> None:
        """Enable or disable wrapping of the label text at word breaks.

        Parameters
        ----------
        flag : bool
            If ``True``, the text wraps at word breaks. Default is ``False``.
        """

    def text(self) -> str:
        """Return the text of the label.

        Returns
        -------
        str
            The current text.
        """

    def wordWrap(self) -> bool:
        """Return the current word-wrapping policy.

        Returns
        -------
        bool
            ``True`` if word wrapping is enabled, ``False`` otherwise.
        """

class LineEdit(Widget):
    """A single-line text entry widget.

    Notes
    -----
    Construct with ``LineEdit(parent)`` and add it to a layout.
    """

    def __init__(self, parent: Widget) -> None:
        """Construct a line edit.

        Parameters
        ----------
        parent : Widget
            The parent widget that owns this line edit.
        """

    def onChange(self, callback: typing.Callable[[str], None]) -> None:
        """Register a callback invoked whenever the text changes.

        Parameters
        ----------
        callback : callable
            A callable taking the current text as a single ``str`` argument and
            returning nothing. It is called on every change to the text.

        Examples
        --------
        >>> def lineEdit_changed(text):
        ...     print('text is now: ' + text)
        >>> lineEdit = gnsgui.LineEdit(dialog)
        >>> lineEdit.onChange(lineEdit_changed)
        """

    def onEditingFinish(self, callback: typing.Callable[[str], None]) -> None:
        """Register a callback invoked when editing finishes.

        Parameters
        ----------
        callback : callable
            A callable taking the current text as a single ``str`` argument and
            returning nothing. It is called when the user presses Enter or the
            line edit loses focus.

        Examples
        --------
        >>> def lineEdit_editingFinished(text):
        ...     print('user has finished editing: ' + text)
        >>> lineEdit = gnsgui.LineEdit(dialog)
        >>> lineEdit.onEditingFinish(lineEdit_editingFinished)
        """

    def setText(self, text: str) -> None:
        """Set the text of the line edit.

        Parameters
        ----------
        text : str
            The new text.
        """

    def text(self) -> str:
        """Return the text of the line edit.

        Returns
        -------
        str
            The current text.
        """

class TextEdit(Widget):
    """A multi-line text entry widget.

    Notes
    -----
    Construct with ``TextEdit(parent)`` and add it to a layout.
    """

    def __init__(self, parent: Widget) -> None:
        """Construct a text edit.

        Parameters
        ----------
        parent : Widget
            The parent widget that owns this text edit.
        """

    def appendText(self, text: str, prependNewLine: bool = True) -> None:
        """Append text to the existing content.

        Parameters
        ----------
        text : str
            The text to append.
        prependNewLine : bool, optional
            If ``True`` (default), a new line is inserted before the appended
            text when the text edit already contains text.
        """

    def readOnly(self) -> bool:
        """Return whether the text is read-only.

        Returns
        -------
        bool
            ``True`` if the user cannot edit the text. Default is ``True``.
        """

    def scrollToBottom(self) -> None:
        """Scroll to the bottom of the text.

        Notes
        -----
        The cursor is placed at the end of the text.
        """

    def scrollToTop(self) -> None:
        """Scroll to the top of the text.

        Notes
        -----
        The cursor is placed at the start of the text.
        """

    def setHTML(self, flag: bool) -> None:
        """Set whether text is interpreted as HTML.

        Parameters
        ----------
        flag : bool
            If ``True``, text passed to :meth:`setText` and :meth:`appendText`
            is interpreted as HTML. Default is ``False``.
        """

    def setMonospace(self, flag: bool) -> None:
        """Set whether the text edit uses a monospace font.

        Parameters
        ----------
        flag : bool
            If ``True``, a monospace font is used. Default is ``False``.
        """

    def setReadOnly(self, flag: bool) -> None:
        """Set whether the user can edit the text.

        Parameters
        ----------
        flag : bool
            If ``True``, the text becomes read-only. Default is ``True``.
        """

    def setText(self, text: str) -> None:
        """Set the text of the text edit.

        Parameters
        ----------
        text : str
            The new text.
        """

    def setWordWrap(self, flag: bool) -> None:
        """Set whether long lines wrap.

        Parameters
        ----------
        flag : bool
            If ``True``, lines wrap when too long. Default is ``True``.
        """

    def text(self) -> str:
        """Return the text of the text edit.

        Returns
        -------
        str
            The current text.
        """

    def wordWrap(self) -> bool:
        """Return whether long lines wrap.

        Returns
        -------
        bool
            ``True`` if lines wrap when too long. Default is ``True``.
        """

class PushButton(Widget):
    """A clickable push button.

    Notes
    -----
    Construct with ``PushButton(text, parent)`` and connect a handler with
    :meth:`onClick` or the ``onClickCallback`` constructor argument.
    """

    def __init__(
        self,
        text: str,
        parent: Widget,
        onClickCallback: typing.Callable[[], None] | None = None,
        *,
        icon: str = "",
    ) -> None:
        """Construct a push button.

        Parameters
        ----------
        text : str
            The text shown on the button.
        parent : Widget
            The parent widget that owns this button.
        onClickCallback : callable or None, optional
            A callable taking no arguments and returning nothing, invoked when
            the button is clicked; an alternative to calling :meth:`onClick`.
            Default is ``None``.
        icon : str, optional
            Icon to set on the button; see :meth:`setIcon` for accepted values.
            Default is ``""`` (no icon).
        """

    def onClick(self, callback: typing.Callable[[], None]) -> None:
        """Register a callback invoked when the button is clicked.

        Parameters
        ----------
        callback : callable
            A callable taking no arguments and returning nothing.

        Examples
        --------
        >>> def pushButton_clicked():
        ...     print('you pushed me!')
        >>> pushButton = gnsgui.PushButton('Push', dialog)
        >>> pushButton.onClick(pushButton_clicked)
        >>> closeButton = gnsgui.PushButton('Close', dialog)
        >>> closeButton.onClick(dialog.close)
        """

    def setIcon(self, icon: str) -> None:
        """Set the button's icon.

        Parameters
        ----------
        icon : str
            The icon, given as an internal icon name (e.g. ``":/python"``), a
            path to a PNG image, or the name of a Qt standard icon.
        """

    def setIconSize(self, width: int, height: int = -1) -> None:
        """Set the size of the button's icon.

        Parameters
        ----------
        width : int
            The icon width in pixels.
        height : int, optional
            The icon height in pixels. If omitted (``-1``, the default), a square
            icon of the given width is used.
        """

    def setText(self, text: str) -> None:
        """Set the text of the button.

        Parameters
        ----------
        text : str
            The new text.
        """

    def text(self) -> str:
        """Return the text of the button.

        Returns
        -------
        str
            The current text.
        """

class CheckBox(Widget):
    """An option box that can be checked or unchecked.

    Notes
    -----
    Construct with ``CheckBox(text, parent)`` and add it to a layout.
    """

    def __init__(self, text: str, parent: Widget) -> None:
        """Construct a check box.

        Parameters
        ----------
        text : str
            The text shown next to the check box.
        parent : Widget
            The parent widget that owns this check box.
        """

    def isChecked(self) -> bool:
        """Return whether the check box is checked.

        Returns
        -------
        bool
            ``True`` if checked, ``False`` otherwise.
        """

    def onClick(self, callback: typing.Callable[[], None]) -> None:
        """Register a callback invoked when the check box is clicked.

        Parameters
        ----------
        callback : callable
            A callable taking no arguments and returning nothing.

        Examples
        --------
        >>> def checkBox_clicked():
        ...     print('you clicked me!')
        >>> checkBox = gnsgui.CheckBox("Check", dialog)
        >>> checkBox.onClick(checkBox_clicked)
        """

    def onToggle(self, callback: typing.Callable[[bool], None]) -> None:
        """Register a callback invoked when the checked state changes.

        Parameters
        ----------
        callback : callable
            A callable taking the current checked state as a single ``bool``
            argument and returning nothing.

        Examples
        --------
        >>> def checkBox_toggled(checked):
        ...     print('toggled!')
        >>> checkBox = gnsgui.CheckBox("Check", dialog)
        >>> checkBox.onToggle(checkBox_toggled)
        """

    def setChecked(self, flag: bool) -> None:
        """Set the checked state of the check box.

        Parameters
        ----------
        flag : bool
            ``True`` to check the box, ``False`` to uncheck it.
        """

    def setText(self, text: str) -> None:
        """Set the text of the check box.

        Parameters
        ----------
        text : str
            The new text.
        """

    def text(self) -> str:
        """Return the text of the check box.

        Returns
        -------
        str
            The current text.
        """

class RadioButton(Widget):
    """An option button that can be checked or unchecked.

    Notes
    -----
    Radio buttons sharing the same parent are mutually exclusive: only one can be
    checked at a time. Construct with ``RadioButton(text, parent)``.
    """

    def __init__(self, text: str, parent: Widget, data: str = "") -> None:
        """Construct a radio button.

        Parameters
        ----------
        text : str
            The text shown next to the radio button.
        parent : Widget
            The parent widget that owns this radio button.
        data : str, optional
            Data passed to the :meth:`onSelect` callback. Default is ``""``.
        """

    def data(self) -> str:
        """Return the data passed into the constructor.

        Returns
        -------
        str
            The ``data`` value given at construction.
        """

    def isChecked(self) -> bool:
        """Return whether the radio button is checked.

        Returns
        -------
        bool
            ``True`` if checked, ``False`` otherwise.
        """

    def onClick(self, callback: typing.Callable[[], None]) -> None:
        """Register a callback invoked when the radio button is clicked.

        Parameters
        ----------
        callback : callable
            A callable taking no arguments and returning nothing.

        Examples
        --------
        >>> def radioButton_clicked():
        ...     print('you clicked me!')
        >>> radioButton = gnsgui.RadioButton("Radio", dialog)
        >>> radioButton.onClick(radioButton_clicked)
        """

    def onSelect(self, callback: typing.Callable[[str], None]) -> None:
        """Register a callback invoked when the selection state changes.

        Parameters
        ----------
        callback : callable
            A callable taking a single ``str`` argument (the ``data`` passed to
            the constructor) and returning nothing.

        Examples
        --------
        >>> def radioButton_selected(str):
        ...     print('you selected ' + str)
        >>> radioButton = gnsgui.RadioButton("Radio1", dialog, "radio_1")
        >>> radioButton.onSelect(radioButton_selected)
        >>> radioButton = gnsgui.RadioButton("Radio2", dialog, "radio_2")
        >>> radioButton.onSelect(radioButton_selected)
        """

    def onToggle(self, callback: typing.Callable[[bool], None]) -> None:
        """Register a callback invoked when the checked state changes.

        Parameters
        ----------
        callback : callable
            A callable taking the current checked state as a single ``bool``
            argument and returning nothing.

        Examples
        --------
        >>> def radioButton_toggled(checked):
        ...     print('toggled!')
        >>> radioButton = gnsgui.RadioButton("Radio", dialog)
        >>> radioButton.onToggle(radioButton_toggled)
        """

    def setChecked(self, flag: bool) -> None:
        """Set the checked state of the radio button.

        Parameters
        ----------
        flag : bool
            ``True`` to check the button, ``False`` to uncheck it.
        """

    def setText(self, text: str) -> None:
        """Set the text of the radio button.

        Parameters
        ----------
        text : str
            The new text.
        """

    def text(self) -> str:
        """Return the text of the radio button.

        Returns
        -------
        str
            The current text.
        """

class ComboBox(Widget):
    """A drop-down menu of selectable items.

    Notes
    -----
    Construct with ``ComboBox(parent)`` and populate it with :meth:`addItem`.
    """

    def __init__(self, parent: Widget) -> None:
        """Construct a combo box.

        Parameters
        ----------
        parent : Widget
            The parent widget that owns this combo box.
        """

    def addItem(self, item: str, data: str = "", icon: str = "") -> None:
        """Add an item to the combo box.

        Parameters
        ----------
        item : str
            The text of the item.
        data : str, optional
            Custom data associated with the item, retrievable with
            :meth:`itemData`. Default is ``""``.
        icon : str, optional
            An icon for the item; see :meth:`setItemIcon` for accepted values.
            Default is ``""`` (no icon).
        """

    def clear(self) -> None:
        """Remove all items from the combo box."""

    def count(self) -> int:
        """Return the number of items in the combo box.

        Returns
        -------
        int
            The item count.
        """

    def currentIndex(self) -> int:
        """Return the index of the currently selected item.

        Returns
        -------
        int
            The current item index.
        """

    def itemData(self, index: int) -> str:
        """Return the data of the item at the given index.

        Parameters
        ----------
        index : int
            The item index.

        Returns
        -------
        str
            The item's custom data.
        """

    def itemText(self, index: int) -> str:
        """Return the text of the item at the given index.

        Parameters
        ----------
        index : int
            The item index.

        Returns
        -------
        str
            The item's text.
        """

    def onIndexChange(self, callback: typing.Callable[[int], None]) -> None:
        """Register a callback invoked when the current item changes.

        Parameters
        ----------
        callback : callable
            A callable taking the current index as a single ``int`` argument and
            returning nothing.

        Examples
        --------
        >>> def item_changed(i):
        ...     print('current item is now ' + comboBox.itemText(i))
        >>> comboBox = gnsgui.ComboBox(dialog)
        >>> comboBox.addItem('Item 1', 'item1')
        >>> comboBox.addItem('Item 2', 'item2')
        >>> comboBox.onIndexChange(item_changed)
        """

    def removeItem(self, index: int) -> None:
        """Remove the item at the given index.

        Parameters
        ----------
        index : int
            The index of the item to remove.
        """

    def setCurrentIndex(self, index: int) -> None:
        """Set the currently selected item by index.

        Parameters
        ----------
        index : int
            The index to select.
        """

    def setIconSize(self, width: int, height: int = -1) -> None:
        """Set the icon size for items in the combo box.

        Parameters
        ----------
        width : int
            The icon width in pixels.
        height : int, optional
            The icon height in pixels. If omitted (``-1``, the default), a square
            icon of the given width is used.
        """

    def setItemIcon(self, index: int, icon: str) -> None:
        """Set the icon of the item at the given index.

        Parameters
        ----------
        index : int
            The item index.
        icon : str
            The icon, given as an internal icon name (e.g. ``":/python"``), a
            path to a PNG image, or the name of a Qt standard icon.
        """

class ListWidget(Widget):
    """A list of selectable items.

    Notes
    -----
    Construct with ``ListWidget(parent)`` and populate it with :meth:`addItem`
    or :meth:`addItems`. Enable multi-selection with :meth:`setSelectMultiple`.
    """

    def __init__(self, parent: Widget) -> None:
        """Construct a list widget.

        Parameters
        ----------
        parent : Widget
            The parent widget that owns this list widget.
        """

    def addItem(self, item: str, data: str = "") -> None:
        """Add an item to the list.

        Parameters
        ----------
        item : str
            The text of the item.
        data : str, optional
            Custom data associated with the item, retrievable with
            :meth:`itemData`. Default is ``""``.
        """

    def addItems(self, items: list[str], datas: list[str] = ...) -> None:
        """Add several items to the list.

        Parameters
        ----------
        items : list of str
            The texts of the items to add.
        datas : list of str, optional
            Custom data for each item, retrievable with :meth:`itemData`.
            Default is an empty list (no data).
        """

    def clear(self) -> None:
        """Remove all items from the list."""

    def count(self) -> int:
        """Return the number of items in the list.

        Returns
        -------
        int
            The item count.
        """

    def currentSelection(self) -> list[int]:
        """Return the indices of the currently selected items.

        Returns
        -------
        list of int
            The selected item indices.
        """

    def insertItem(self, index: int, item: str, data: str = "") -> None:
        """Insert an item at the given index.

        Parameters
        ----------
        index : int
            The index at which to insert the item.
        item : str
            The text of the item.
        data : str, optional
            Custom data associated with the item, retrievable with
            :meth:`itemData`. Default is ``""``.
        """

    def itemData(self, index: int) -> str:
        """Return the data of the item at the given index.

        Parameters
        ----------
        index : int
            The item index.

        Returns
        -------
        str
            The item's custom data.
        """

    def itemText(self, index: int) -> str:
        """Return the text of the item at the given index.

        Parameters
        ----------
        index : int
            The item index.

        Returns
        -------
        str
            The item's text.
        """

    def onSelectionChange(self, callback: typing.Callable[[list[int]], None]) -> None:
        """Register a callback invoked when the selection changes.

        Parameters
        ----------
        callback : callable
            A callable taking the current selection as a single ``list`` of
            ``int`` indices and returning nothing.

        Examples
        --------
        >>> def selection_changed(l):
        ...     print('number of selected items is now ' + str(len(l)))
        >>> list = gnsgui.ListWidget(dialog)
        >>> list.addItem('Item 1', 'item1')
        >>> list.addItem('Item 2', 'item2')
        >>> list.onSelectionChange(selection_changed)
        """

    def removeItem(self, index: int) -> None:
        """Remove the item at the given index.

        Parameters
        ----------
        index : int
            The index of the item to remove.
        """

    def removeItems(self, indexes: list[int]) -> None:
        """Remove the items at the given indices.

        Parameters
        ----------
        indexes : list of int
            The indices of the items to remove.
        """

    def setSelectMultiple(self, flag: bool) -> None:
        """Set whether multiple items may be selected.

        Parameters
        ----------
        flag : bool
            If ``True``, multiple items can be selected. Default is ``False``.
        """

class ColorSelector(Widget):
    """A color-selecting widget, roughly the size of a combo box.

    Notes
    -----
    Construct with ``ColorSelector(initialColor, parent)`` and optionally supply
    an ``onChangeCallback``, or connect one later with :meth:`onChange`.
    """

    def __init__(
        self,
        initialColor: Color,
        parent: Widget,
        onChangeCallback: typing.Callable[[Color], None] | None = None,
    ) -> None:
        """Construct a color selector.

        Parameters
        ----------
        initialColor : Color
            The initially selected color.
        parent : Widget
            The parent widget that owns this color selector.
        onChangeCallback : callable or None, optional
            A callable taking the new :class:`Color` as its single argument and
            returning nothing, invoked when the current color changes; an
            alternative to calling :meth:`onChange`. Default is ``None``.
        """

    def current(self) -> Color:
        """Return the currently selected color.

        Returns
        -------
        Color
            The current color.
        """

    def onChange(self, callback: typing.Callable[[Color], None]) -> None:
        """Register a callback invoked when the current color changes.

        Parameters
        ----------
        callback : callable
            A callable taking the new :class:`Color` as its single argument and
            returning nothing.

        Examples
        --------
        >>> def colorChanged(color):
        ...     print(color.name)
        >>> cs = gnsgui.ColorSelector(gnsgui.Color((255, 0, 0, 255), "red"), dialog)
        >>> cs.onChange(colorChanged)
        """

    def setCurrent(self, color: Color) -> None:
        """Set the currently selected color.

        Parameters
        ----------
        color : Color
            The color to select.
        """

class Dialog(Widget):
    """A top-level dialog window shown on the screen.

    A dialog must be the parent of the widgets the user interacts with.

    Notes
    -----
    Construct directly with :class:`Dialog`. Note that :meth:`show` must be
    called for the dialog to become visible. A parentless dialog (constructed
    with an :class:`App`) is destroyed by default when closed; a dialog with a
    widget parent is not (see :meth:`setDeleteOnClose`). ``App.exec`` finishes
    when the last :class:`DockWidget` or parentless dialog is destroyed.
    """

    @typing.overload
    def __init__(self, app: App) -> None:
        """Construct a dialog without a parent.

        Parameters
        ----------
        app : App
            The application object that owns the dialog.

        Notes
        -----
        The dialog is not shown until :meth:`show` is called. It is destroyed
        by default when closed (see :meth:`setDeleteOnClose`). ``App.exec``
        finishes when the last dock widget or parentless dialog is destroyed.
        """

    @typing.overload
    def __init__(self, parent: Widget) -> None:
        """Construct a dialog as a child of a widget.

        Parameters
        ----------
        parent : Widget
            The parent widget of the dialog.

        Notes
        -----
        The dialog is not shown until :meth:`show` is called. It is not
        destroyed by default when closed (see :meth:`setDeleteOnClose`).
        """

    def close(self) -> None:
        """Hide the dialog.

        Notes
        -----
        Whether the dialog is also deleted is governed by
        :meth:`setDeleteOnClose`.
        """

    def onClose(self, callback: typing.Callable[[], None]) -> None:
        """Register a callback invoked when the dialog is closed.

        Parameters
        ----------
        callback : callable
            A function taking no arguments and returning nothing. It is called
            when the dialog is closed.

        Examples
        --------
        >>> def dialog_closed():
        ...     print('Dialog closed')
        >>> dialog = Dialog(app)
        >>> dialog.onClose(dialog_closed)
        >>> dialog.show()
        >>> app.exec()
        """

    def position(self) -> tuple[int, int]:
        """Return the position of the dialog.

        Returns
        -------
        tuple of int
            The ``(x, y)`` position of the dialog in pixels.
        """

    def setDeleteOnClose(self, flag: bool) -> None:
        """Set whether the dialog is deleted when closed.

        Parameters
        ----------
        flag : bool
            If ``True``, the dialog is deleted when closed. The default is
            ``True`` when the dialog has the :class:`App` as a parent, and
            ``False`` when it has a widget parent.
        """

    def setPosition(self, xy: tuple[int, int]) -> None:
        """Set the position of the dialog.

        Parameters
        ----------
        xy : tuple of int
            The ``(x, y)`` position of the dialog in pixels.
        """

    def setSize(self, width_height: tuple[int, int]) -> None:
        """Set the size of the dialog.

        Parameters
        ----------
        width_height : tuple of int
            The ``(width, height)`` of the dialog in pixels.
        """

    def setWindowTitle(self, title: str) -> None:
        """Set the window title of the dialog.

        Parameters
        ----------
        title : str
            The text shown in the dialog's title bar.
        """

    def size(self) -> tuple[int, int]:
        """Return the size of the dialog.

        Returns
        -------
        tuple of int
            The ``(width, height)`` of the dialog in pixels.
        """

class DockWidget(Widget):
    """A dockable widget attached to the main window.

    Notes
    -----
    Construct directly with :class:`DockWidget`. By default the dock widget is
    not deleted when closed, so the user can show it again by right-clicking
    the menu bar (see :meth:`setDeleteOnClose`).
    """

    def __init__(self, title: str, app: App) -> None:
        """Construct a dock widget.

        Parameters
        ----------
        title : str
            The title of the dock widget.
        app : App
            The application object that owns the dock widget.
        """

    def close(self) -> None:
        """Hide the dock widget.

        Notes
        -----
        Whether the dock widget is also deleted is governed by
        :meth:`setDeleteOnClose`.
        """

    def isFloating(self) -> bool:
        """Return whether the dock widget is floating.

        Returns
        -------
        bool
            ``True`` if the dock widget is currently floating.
        """

    def onClose(self, callback: typing.Callable[[], None]) -> None:
        """Register a callback invoked when the dock widget is closed.

        Parameters
        ----------
        callback : callable
            A function taking no arguments and returning nothing. It is called
            when the dock widget is closed.

        Examples
        --------
        >>> def dock_closed():
        ...     print('DockWidget closed')
        >>> dock = DockWidget('Tools', app)
        >>> dock.onClose(dock_closed)
        >>> app.exec()
        """

    def position(self) -> tuple[int, int]:
        """Return the position of the dock widget.

        Returns
        -------
        tuple of int
            The ``(x, y)`` position of the dock widget in pixels.
        """

    def setDeleteOnClose(self, flag: bool) -> None:
        """Set whether the dock widget is deleted when closed.

        Parameters
        ----------
        flag : bool
            If ``True``, the dock widget is deleted when closed. Default is
            ``False``.
        """

    def setFloating(self, floating: bool) -> None:
        """Enable or disable floating of the dock widget.

        Parameters
        ----------
        floating : bool
            If ``True``, the dock widget floats free of the main window.
        """

    def setPosition(self, xy: tuple[int, int]) -> None:
        """Set the position of the dock widget.

        Parameters
        ----------
        xy : tuple of int
            The ``(x, y)`` position of the dock widget in pixels.

        Notes
        -----
        The position can only be set while the dock widget is floating.
        """

    def setSize(self, width_height: tuple[int, int]) -> None:
        """Set the size of the dock widget.

        Parameters
        ----------
        width_height : tuple of int
            The ``(width, height)`` of the dock widget in pixels.

        Notes
        -----
        The size can only be set while the dock widget is floating.
        """

    def setWidget(self, widget: Widget) -> None:
        """Set the widget contained by the dock widget.

        Parameters
        ----------
        widget : Widget
            The widget to place inside the dock widget.
        """

    def size(self) -> tuple[int, int]:
        """Return the size of the dock widget.

        Returns
        -------
        tuple of int
            The ``(width, height)`` of the dock widget in pixels.
        """

    def widget(self) -> Widget:
        """Return the widget contained by the dock widget.

        Returns
        -------
        Widget
            The widget currently held by the dock widget.
        """

class FileDialog:
    """Modal dialogs for selecting files and directories.

    Notes
    -----
    This class is a namespace for static file-selection dialogs; it is not
    instantiated. Call the methods on the class, e.g. ``FileDialog.openFile``.
    """

    @staticmethod
    def openDirectory(app: App, directory: str = "", windowTitle: str = "") -> str:
        """Prompt the user to select an existing directory.

        Parameters
        ----------
        app : App
            The application object.
        directory : str, optional
            The directory the dialog opens in. Default is ``''``.
        windowTitle : str, optional
            The dialog window title. Default is ``''``.

        Returns
        -------
        str
            The selected directory path, empty if the user cancels.

        Examples
        --------
        >>> directory = FileDialog.openDirectory(app, "/tmp")
        """

    @staticmethod
    def openFile(
        app: App, filters: list[str] = ..., directory: str = "", windowTitle: str = ""
    ) -> str:
        """Prompt the user to select a single existing file.

        Parameters
        ----------
        app : App
            The application object.
        filters : list of str, optional
            File-type filters, each of the form ``"Description *.ext"``.
            Default is ``['All Files *']``.
        directory : str, optional
            The directory the dialog opens in. Default is ``''``.
        windowTitle : str, optional
            The dialog window title. Default is ``''``.

        Returns
        -------
        str
            The selected file path, empty if the user cancels.

        Examples
        --------
        >>> file = FileDialog.openFile(app, ["All Files *"], "/tmp", "Open a file")
        """

    @staticmethod
    def openFiles(
        app: App, filters: list[str] = ..., directory: str = "", windowTitle: str = ""
    ) -> list[str]:
        """Prompt the user to select any number of existing files.

        Parameters
        ----------
        app : App
            The application object.
        filters : list of str, optional
            File-type filters, each of the form ``"Description *.ext"``.
            Default is ``['All Files *']``.
        directory : str, optional
            The directory the dialog opens in. Default is ``''``.
        windowTitle : str, optional
            The dialog window title. Default is ``''``.

        Returns
        -------
        list of str
            The selected file paths, empty if the user cancels.

        Examples
        --------
        >>> fileList = FileDialog.openFiles(app, ["All Files *"], "/tmp")
        """

    @staticmethod
    def saveFile(
        app: App, filters: list[str] = ..., directory: str = "", windowTitle: str = ""
    ) -> str:
        """Prompt the user to select a file to save.

        Parameters
        ----------
        app : App
            The application object.
        filters : list of str, optional
            File-type filters, each of the form ``"Description *.ext"``.
            Default is ``['All Files *']``.
        directory : str, optional
            The directory the dialog opens in. Default is ``''``.
        windowTitle : str, optional
            The dialog window title. Default is ``''``.

        Returns
        -------
        str
            The chosen file path, empty if the user cancels.

        Examples
        --------
        >>> file = FileDialog.saveFile(app, ["Python Files *.py"], "/tmp")
        """

class GridLayout(Layout):
    """A layout that arranges widgets and child layouts in a grid.

    Notes
    -----
    Construct directly with :class:`GridLayout`, either standalone (to nest in
    another layout) or with a widget parent (to become that widget's main
    layout).
    """

    @typing.overload
    def __init__(self, app: App) -> None:
        """Construct a grid layout for use inside another layout.

        Parameters
        ----------
        app : App
            The application object that owns the layout.

        Examples
        --------
        >>> layout = GridLayout(app)
        >>> otherLayout.addLayout(layout)
        """

    @typing.overload
    def __init__(self, parent: Widget) -> None:
        """Construct a grid layout as the main layout of a widget.

        Parameters
        ----------
        parent : Widget
            The widget for which this becomes the main layout.

        Examples
        --------
        >>> dialog = Dialog(app)
        >>> layout = GridLayout(dialog)
        """

    def addLayout(
        self, layout: Layout, row: int, column: int, rowspan: int = 1, colspan: int = 1
    ) -> None:
        """Add a child layout at the given grid cell.

        Parameters
        ----------
        layout : Layout
            The child layout to add.
        row : int
            The starting row of the cell.
        column : int
            The starting column of the cell.
        rowspan : int, optional
            The number of rows the layout spans. Default is ``1``.
        colspan : int, optional
            The number of columns the layout spans. Default is ``1``.
        """

    def addWidget(
        self, widget: Widget, row: int, column: int, rowspan: int = 1, colspan: int = 1
    ) -> None:
        """Add a widget at the given grid cell.

        Parameters
        ----------
        widget : Widget
            The widget to add.
        row : int
            The starting row of the cell.
        column : int
            The starting column of the cell.
        rowspan : int, optional
            The number of rows the widget spans. Default is ``1``.
        colspan : int, optional
            The number of columns the widget spans. Default is ``1``.
        """

    def setColumnStretch(self, column: int, stretch: int) -> None:
        """Set the stretch factor of a column.

        Parameters
        ----------
        column : int
            The column index.
        stretch : int
            How much this column stretches relative to other columns. The
            default stretch is zero.
        """

    def setRowStretch(self, row: int, stretch: int) -> None:
        """Set the stretch factor of a row.

        Parameters
        ----------
        row : int
            The row index.
        stretch : int
            How much this row stretches relative to other rows. The default
            stretch is zero.
        """

class GroupBox(Widget):
    """A visual box drawn around a group of widgets.

    A group box can carry a title and can optionally be checkable.

    Notes
    -----
    Construct directly with :class:`GroupBox`.
    """

    @typing.overload
    def __init__(self, title: str, parent: Widget) -> None:
        """Construct a group box with a title.

        Parameters
        ----------
        title : str
            The title of the group box.
        parent : Widget
            The parent widget.
        """

    @typing.overload
    def __init__(self, parent: Widget) -> None:
        """Construct a group box without a title.

        Parameters
        ----------
        parent : Widget
            The parent widget.
        """

    def isChecked(self) -> bool:
        """Return whether the group box is checked.

        Returns
        -------
        bool
            ``True`` if the group box is currently checked.
        """

    def onToggle(self, callback: typing.Callable[[bool], None]) -> None:
        """Register a callback invoked when the checked state changes.

        Parameters
        ----------
        callback : callable
            A function taking the current checked state as a single ``bool``
            argument and returning nothing.

        Examples
        --------
        >>> def groupBox_toggled(checked):
        ...     print('toggled!')
        >>> groupBox = GroupBox("Title", dialog)
        >>> groupBox.onToggle(groupBox_toggled)
        """

    def setCheckable(self, flag: bool) -> None:
        """Set whether the group box is checkable.

        Parameters
        ----------
        flag : bool
            If ``True``, the group box shows a checkbox in its title.
        """

    def setChecked(self, flag: bool) -> None:
        """Set the checked state of the group box.

        Parameters
        ----------
        flag : bool
            The new checked state.
        """

class HBoxLayout(Layout):
    """A layout that arranges widgets and child layouts horizontally.

    Notes
    -----
    Construct directly with :class:`HBoxLayout`, either standalone (to nest in
    another layout) or with a widget parent (to become that widget's main
    layout).
    """

    @typing.overload
    def __init__(self, app: App) -> None:
        """Construct a horizontal layout for use inside another layout.

        Parameters
        ----------
        app : App
            The application object that owns the layout.

        Examples
        --------
        >>> layout = HBoxLayout(app)
        >>> otherLayout.addLayout(layout)
        """

    @typing.overload
    def __init__(self, parent: Widget) -> None:
        """Construct a horizontal layout as the main layout of a widget.

        Parameters
        ----------
        parent : Widget
            The widget for which this becomes the main layout.

        Examples
        --------
        >>> dialog = Dialog(app)
        >>> layout = HBoxLayout(dialog)
        """

    def addLayout(self, layout: Layout, stretch: int = 0) -> None:
        """Add a child layout to this layout.

        Parameters
        ----------
        layout : Layout
            The child layout to add.
        stretch : int, optional
            The relative stretch of this layout versus others in this layout.
            Default is ``0``.
        """

    def addSeparator(self) -> None:
        """Add a vertical separator to the layout."""

    def addStretch(self) -> None:
        """Add stretchable spacing that expands as the dialog grows."""

    def addWidget(self, widget: Widget, stretch: int = 0) -> None:
        """Add a widget to this layout.

        Parameters
        ----------
        widget : Widget
            The widget to add.
        stretch : int, optional
            The relative stretch of this widget versus others in this layout.
            Default is ``0``.
        """

class MessageBox:
    """Modal message dialogs for informing or prompting the user.

    Notes
    -----
    This class is a namespace for static message dialogs; it is not
    instantiated. Call the methods on the class, e.g. ``MessageBox.info``.
    Button labels may be any of: ``OK``, ``Open``, ``Save``, ``Cancel``,
    ``Close``, ``Discard``, ``Don't Save``, ``Apply``, ``Reset``,
    ``Restore Defaults``, ``Help``, ``Save All``, ``Yes``, ``Yes to All``,
    ``No``, ``No to All``, ``Abort``, ``Retry`` and ``Ignore``. The first
    button is selected when the user presses Enter; if the user dismisses the
    dialog with Escape, an appropriate reject button is returned.
    """

    @staticmethod
    def critical(app: App, windowTitle: str, message: str, buttons: list[str] = ...) -> str:
        """Show the user an error dialog and return the chosen button label.

        Parameters
        ----------
        app : App
            The application object.
        windowTitle : str
            The dialog window title.
        message : str
            The error message shown to the user.
        buttons : list of str, optional
            The button labels to display. Default is ``['OK']``.

        Returns
        -------
        str
            The label of the button the user pressed.

        Examples
        --------
        >>> response = MessageBox.critical(app, 'Error', 'Save?', ["Cancel", "No", "Yes"])
        """

    @staticmethod
    def info(app: App, windowTitle: str, message: str) -> None:
        """Show the user an information dialog with an OK button.

        Parameters
        ----------
        app : App
            The application object.
        windowTitle : str
            The dialog window title.
        message : str
            The message shown to the user.

        Examples
        --------
        >>> MessageBox.info(app, 'Info', 'Hello World!')
        """

    @staticmethod
    def question(app: App, windowTitle: str, message: str, buttons: list[str] = ...) -> str:
        """Ask the user a question and return the chosen button label.

        Parameters
        ----------
        app : App
            The application object.
        windowTitle : str
            The dialog window title.
        message : str
            The question shown to the user.
        buttons : list of str, optional
            The button labels to display. Default is ``['No', 'Yes']``.

        Returns
        -------
        str
            The label of the button the user pressed.

        Examples
        --------
        >>> response = MessageBox.question(app, 'Question', 'Delete the file?', ["No", "Yes"])
        """

    @staticmethod
    def warning(app: App, windowTitle: str, message: str, buttons: list[str] = ...) -> str:
        """Show the user a warning dialog and return the chosen button label.

        Parameters
        ----------
        app : App
            The application object.
        windowTitle : str
            The dialog window title.
        message : str
            The warning message shown to the user.
        buttons : list of str, optional
            The button labels to display. Default is ``['OK']``.

        Returns
        -------
        str
            The label of the button the user pressed.

        Examples
        --------
        >>> response = MessageBox.warning(app, 'Warning', 'Are you sure?', ["Cancel", "No", "Yes"])
        """

class ProgressBar(Widget):
    """A bar displaying the progress of a task.

    Notes
    -----
    Construct directly with :class:`ProgressBar`. See also
    :class:`ProgressDialog`.
    """

    def __init__(self, parent: Widget, min: int, max: int, format: str = "%p%") -> None:
        """Construct a progress bar.

        Parameters
        ----------
        parent : Widget
            The parent widget.
        min : int
            The minimum value of the range (see :meth:`setRange`).
        max : int
            The maximum value of the range (see :meth:`setRange`).
        format : str, optional
            The text format shown in the bar (see :meth:`setFormat`). Default
            is ``'%p%'``.

        Notes
        -----
        The value is uninitialized, so no progress is displayed until
        :meth:`setValue` is called (when ``min != max``).
        """

    def range(self) -> tuple[int, int]:
        """Return the current range.

        Returns
        -------
        tuple of int
            The ``(min, max)`` range of the progress bar.
        """

    def setFormat(self, format: str) -> None:
        """Set the text format displayed in the bar.

        Parameters
        ----------
        format : str
            The format string; ``'%p'`` is replaced by the current percentage.
            Default is ``'%p%'``. When ``min == max`` no text is displayed.
        """

    def setRange(self, range: tuple[int, int]) -> None:
        """Set the current range.

        Parameters
        ----------
        range : tuple of int
            The ``(min, max)`` range. When ``min == max`` the bar shows a
            moving display and :meth:`setValue` need not be called.
        """

    def setValue(self, value: int) -> None:
        """Set the current value.

        Parameters
        ----------
        value : int
            The current progress value.
        """

    def value(self) -> int:
        """Return the current value.

        Returns
        -------
        int
            The current progress value.
        """

class ProgressDialog(Widget):
    """A dialog displaying the progress of a task.

    Notes
    -----
    Construct directly with :class:`ProgressDialog`. It is not deleted when
    hidden and must be deleted explicitly with ``delete``. See also
    :class:`ProgressBar`.
    """

    def __init__(
        self, parent: App, label: str, min: int, max: int, cancelText: str = "Cancel"
    ) -> None:
        """Construct a progress dialog.

        Parameters
        ----------
        parent : App
            The application object that owns the dialog.
        label : str
            The label shown above the progress bar.
        min : int
            The minimum value of the range (see :meth:`setRange`).
        max : int
            The maximum value of the range (see :meth:`setRange`).
        cancelText : str, optional
            The label of the Cancel button. Default is ``'Cancel'``. If empty,
            no Cancel button is shown.

        Notes
        -----
        The dialog is not deleted when hidden; it must be deleted in the script
        using ``delete``.
        """

    def range(self) -> tuple[int, int]:
        """Return the current range.

        Returns
        -------
        tuple of int
            The ``(min, max)`` range of the dialog.
        """

    def setLabel(self, label: str) -> None:
        """Set the label shown above the progress bar.

        Parameters
        ----------
        label : str
            The new label text.
        """

    def setRange(self, range: tuple[int, int]) -> None:
        """Set the current range.

        Parameters
        ----------
        range : tuple of int
            The ``(min, max)`` range. When ``min == max`` the dialog shows a
            moving display and :meth:`setValue` need not be called.
        """

    def setValue(self, value: int) -> None:
        """Set the current value.

        Parameters
        ----------
        value : int
            The current progress value.
        """

    def setWindowTitle(self, windowTitle: str) -> None:
        """Set the window title of the progress dialog.

        Parameters
        ----------
        windowTitle : str
            The text shown in the dialog's title bar.
        """

    def value(self) -> int:
        """Return the current value.

        Returns
        -------
        int
            The current progress value.
        """

    def wasCanceled(self) -> bool:
        """Return whether the user pressed the Cancel button.

        Returns
        -------
        bool
            ``True`` if the user pressed Cancel.

        Notes
        -----
        The dialog is hidden when the user presses the button. To reset this
        state and reuse the dialog, call ``setValue`` with the range minimum.
        """

class ScrollArea(Widget):
    """A scrollable area that provides scroll bars on demand.

    Notes
    -----
    Construct directly with :class:`ScrollArea`.
    """

    def __init__(self, parent: Widget) -> None:
        """Construct a scroll area.

        Parameters
        ----------
        parent : Widget
            The parent widget.
        """

    def setHorizontalScrolling(self, flag: bool) -> None:
        """Set whether the horizontal scroll bar may appear.

        Parameters
        ----------
        flag : bool
            If ``False``, the widget cannot be scrolled horizontally.
        """

    def setVerticalScrolling(self, flag: bool) -> None:
        """Set whether the vertical scroll bar may appear.

        Parameters
        ----------
        flag : bool
            If ``False``, the widget cannot be scrolled vertically.
        """

    def setWidget(self, widget: Widget) -> None:
        """Set the central widget of the scroll area.

        Parameters
        ----------
        widget : Widget
            The widget to display. Any previous widget is deleted.
        """

    def widget(self) -> Widget:
        """Return the central widget of the scroll area.

        Returns
        -------
        Widget
            The current central widget.
        """

class Splitter(Widget):
    """A container that lets the user resize widgets by dragging boundaries.

    Notes
    -----
    Construct directly with :class:`Splitter`.
    """

    class Orientation(enum.IntEnum):
        """The layout orientation of a :class:`Splitter`."""

        Horizontal = 0
        """Lay the widgets out horizontally."""
        Vertical = 1
        """Lay the widgets out vertically."""

    @typing.overload
    def __init__(self, parent: Widget) -> None:
        """Construct a splitter with the default orientation.

        Parameters
        ----------
        parent : Widget
            The parent widget.
        """

    @typing.overload
    def __init__(self, orientation: Splitter.Orientation, parent: Widget) -> None:
        """Construct a splitter with the given orientation.

        Parameters
        ----------
        orientation : Splitter.Orientation
            The layout orientation of the splitter.
        parent : Widget
            The parent widget.
        """

    def addWidget(self, widget: Widget) -> None:
        """Add a widget to the splitter.

        Parameters
        ----------
        widget : Widget
            The widget to append.
        """

    def count(self) -> int:
        """Return the number of widgets in the splitter.

        Returns
        -------
        int
            The widget count.
        """

    def insertWidget(self, index: int, widget: Widget) -> None:
        """Insert a widget at the given index.

        Parameters
        ----------
        index : int
            The position at which to insert the widget.
        widget : Widget
            The widget to insert.
        """

    def orientation(self) -> Splitter.Orientation:
        """Return the orientation of the splitter.

        Returns
        -------
        Splitter.Orientation
            The current orientation.
        """

    def setOrientation(self, orientation: Splitter.Orientation) -> None:
        """Set the orientation of the splitter.

        Parameters
        ----------
        orientation : Splitter.Orientation
            The new orientation.
        """

    def setSizes(self, list: list[int]) -> None:
        """Set the sizes of the widgets in the splitter.

        Parameters
        ----------
        list : list of int
            The size of each widget in pixels. For a horizontal splitter these
            are widths from left to right; for a vertical splitter they are
            heights from top to bottom. Extra values are ignored, and a size of
            ``0`` makes a widget invisible.
        """

    def setStretchFactor(self, index: int, stretch: int) -> None:
        """Set the relative stretch of the widget at the given index.

        Parameters
        ----------
        index : int
            The index of the widget.
        stretch : int
            How much the widget grows relative to others when the dialog is
            resized. A widget with a stretch of 2 grows twice as quickly as one
            with a stretch of 1. The default is ``0``, meaning the widget does
            not stretch when other widgets have a stretch value.
        """

    def sizes(self) -> list[int]:
        """Return the sizes of the widgets in the splitter.

        Returns
        -------
        list of int
            The size of each widget in pixels. For a horizontal splitter these
            are widths from left to right; for a vertical splitter they are
            heights from top to bottom.

        Notes
        -----
        Non-zero results are only returned once the widgets have been shown on
        the screen.
        """

    def widget(self, index: int) -> Widget:
        """Return the widget at the given index.

        Parameters
        ----------
        index : int
            The index of the widget.

        Returns
        -------
        Widget
            The widget at ``index``.
        """

class TabWidget(Widget):
    """A widget presenting its child widgets on selectable tabs.

    Notes
    -----
    Construct directly with :class:`TabWidget`.
    """

    def __init__(self, parent: Widget) -> None:
        """Construct a tab widget.

        Parameters
        ----------
        parent : Widget
            The parent widget.
        """

    def addTab(self, widget: Widget, tabTitle: str) -> None:
        """Add a tab holding the given widget.

        Parameters
        ----------
        widget : Widget
            The widget shown on the tab.
        tabTitle : str
            The title of the tab.
        """

    def count(self) -> int:
        """Return the number of tabs.

        Returns
        -------
        int
            The tab count.
        """

    def currentIndex(self) -> int:
        """Return the index of the current tab.

        Returns
        -------
        int
            The current tab index.
        """

    def insertTab(self, index: int, widget: Widget, tabTitle: str) -> None:
        """Insert a tab at the given index.

        Parameters
        ----------
        index : int
            The position at which to insert the tab.
        widget : Widget
            The widget shown on the tab.
        tabTitle : str
            The title of the tab.
        """

    def onIndexChange(self, callback: typing.Callable[[int], None]) -> None:
        """Register a callback invoked when the current tab changes.

        Parameters
        ----------
        callback : callable
            A function taking the current tab index as a single ``int``
            argument and returning nothing.

        Examples
        --------
        >>> def tab_changed(i):
        ...     print('current tab is now ' + str(i))
        >>> tab = TabWidget(dialog)
        >>> tab.onIndexChange(tab_changed)
        """

    def removeTab(self, index: int) -> None:
        """Remove the tab at the given index.

        Parameters
        ----------
        index : int
            The index of the tab to remove.

        Notes
        -----
        The widget on the tab is not deleted.
        """

    def setCurrentIndex(self, index: int) -> None:
        """Set the current tab index.

        Parameters
        ----------
        index : int
            The index of the tab to make current.
        """

    def text(self, index: int) -> str:
        """Return the title of the tab at the given index.

        Parameters
        ----------
        index : int
            The index of the tab.

        Returns
        -------
        str
            The tab title.
        """

    def widget(self, index: int) -> Widget:
        """Return the widget on the tab at the given index.

        Parameters
        ----------
        index : int
            The index of the tab.

        Returns
        -------
        Widget
            The widget shown on the tab.
        """

class VBoxLayout(Layout):
    """A layout that arranges widgets and child layouts vertically.

    Notes
    -----
    Construct directly with :class:`VBoxLayout`, either standalone (to nest in
    another layout) or with a widget parent (to become that widget's main
    layout).
    """

    @typing.overload
    def __init__(self, app: App) -> None:
        """Construct a vertical layout for use inside another layout.

        Parameters
        ----------
        app : App
            The application object that owns the layout.

        Examples
        --------
        >>> layout = VBoxLayout(app)
        >>> otherLayout.addLayout(layout)
        """

    @typing.overload
    def __init__(self, parent: Widget) -> None:
        """Construct a vertical layout as the main layout of a widget.

        Parameters
        ----------
        parent : Widget
            The widget for which this becomes the main layout.

        Examples
        --------
        >>> dialog = Dialog(app)
        >>> layout = VBoxLayout(dialog)
        """

    def addLayout(self, layout: Layout, stretch: int = 0) -> None:
        """Add a child layout to this layout.

        Parameters
        ----------
        layout : Layout
            The child layout to add.
        stretch : int, optional
            The relative stretch of this layout versus others in this layout.
            Default is ``0``.
        """

    def addSeparator(self) -> None:
        """Add a horizontal separator to the layout."""

    def addStretch(self) -> None:
        """Add stretchable spacing that expands as the dialog grows."""

    def addWidget(self, widget: Widget, stretch: int = 0) -> None:
        """Add a widget to this layout.

        Parameters
        ----------
        widget : Widget
            The widget to add.
        stretch : int, optional
            The relative stretch of this widget versus others in this layout.
            Default is ``0``.
        """
