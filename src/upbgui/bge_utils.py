from .system import System as BguiSystem
from .widget import Widget, BGUI_MOUSE_NONE, BGUI_MOUSE_CLICK, BGUI_MOUSE_RELEASE, BGUI_MOUSE_ACTIVE
from .text.blf import BlfTextLibrary
from . import key_defs
from bge import logic, events, render
import collections
from collections import deque, OrderedDict
import sys, traceback, operator
def _get_tbstr(exc_info=None):
    if exc_info == None:
        exc_info = sys.exc_info()
    return "".join(traceback.format_exception(*tuple(exc_info)+(None,)))
CALL_LIST_SUPER = list
class _CallList(CALL_LIST_SUPER):
    def __call__(self, *a, **k):
        def _itmcall(i):
            try:
                return i(*a, **k)
            except:
                print(_get_tbstr())
                return True
        torm = deque(filter(_itmcall, self))
        while torm:
            self.remove(torm.popleft())
class Layout(Widget):
    """A base layout class to be used with the BGESystem"""

    def __init__(self, sys, data):
        """
        :param sys: The BGUI system
        :param data: User data
        """

        super().__init__(sys, size=[1,1])
        self.data = data

    def update(self):
        """A function that is called by the system to update the widget (subclasses should override this)"""
        pass


class System(BguiSystem):
    """A system that is intended to be used with BGE games"""
    #_scene = None
    __pdlgetter = None
    __pre_render = None
    __post_render = None
    __pend_remove = None
    @property
    def pre_render(self):
        return self.__pre_render
    @property
    def post_render(self):
        return self.__post_render
    @property
    def post_draw_list(self):
        return self._System__pdlgetter(self)
    def get_key_inputs(self):
        return (logic.keyboard.inputs)
    def get_mouse_inputs(self):
        return (logic.mouse.inputs)
    def get_mouse_position(self):
        return (logic.mouse.position)
    def __init__(self, theme=None, scene=None, pdlgetter=None, pend_remove=None):
        """
        :param theme: the path to a theme directory

        """
        super().__init__(BlfTextLibrary(), theme)

        self.mouse = logic.mouse
        # All layouts will be a widget subclass, so we can just keep track of one widget
        self.layout = None

        # We can also add 'overlay' layouts
        self.overlays = collections.OrderedDict()

        # Now we generate a dict to map BGE keys to bgui keys
        self.keymap = {getattr(events, val): getattr(key_defs, val) for val in dir(events) if val.endswith('KEY') or val.startswith('PAD')}
        # Make a reversed mapping.
        self.invkeymap = {v: k for k, v in self.keymap.items()}
        self.keystates = {k: False for k in self.keymap}
        # Now setup the scene callback so we can draw
        if callable(pdlgetter):
            self._System__pdlgetter = pdlgetter
        else:
            if scene is None:
                scene = logic.getCurrentScene()
            self._System__pdlgetter = lambda *a, **k: scene.post_draw
        #self._scene = scene
        self._System__pre_render = _CallList()
        self._System__post_render = _CallList()
        if not callable(pend_remove):
            pend_remove = lambda this: this.post_draw_list.remove(this)
        self._System__pend_remove = pend_remove
        self.post_draw_list.append(self._render)

    def load_layout(self, layout, data=None):
        """Load a layout and replace any previously loaded layout

        :param layout: The layout to load (None to have no layouts loaded)
        :param data: User data to send to the layout's constructor
        """

        if self.layout:
            self._remove_widget(self.layout)

        if layout:
                self.layout = layout(self, data)
        else:
            self.layout = None

    def add_overlay(self, overlay, data=None):
        """Add an overlay layout, which sits on top of the currently loaded layout

        :param overlay: The layout to add as an overlay
        :param data: User data to send to the layout's constructor"""

        name = overlay.__class__.__name__

        if name in self.overlays:
            print("Overlay: %s, is already added" % name)
            return

        self.overlays[overlay.__class__.__name__] = overlay(self, data)

    def remove_overlay(self, overlay):
        """Remove an overlay layout by name

        :param overlay: the class name of the overlay to remove (this is the same name as the layout used to add the overlay)
        """

        name = overlay.__class__.__name__

        if name in self.overlays:
            self._remove_widget(self.overlays[name])
            del self.overlays[name]
        else:
            print("WARNING: Overlay: %s was not found, nothing was removed" % name)

    def toggle_overlay(self, overlay, data=None):
        """Toggle an overlay (if the overlay is active, remove it, otherwise add it)

        :param overlay: The class name of the layout to toggle
        :param data: User data to send to the layout's constructor
        """

        if overlay.__class__.__name__ in self.overlays:
            self.remove_overlay(overlay)
        else:
            self.add_overlay(overlay, data)
    def _render(self):
        self.pre_render(self)
        try:
            super().render()
        except:
            # If there was a problem with rendering, stop so we don't spam the console
            import traceback
            traceback.print_exc()
            #self.post_draw_list.remove(self._render)
            self._System__pend_remove(self)
        self.post_render(self)
    def run(self):
        """A high-level method to be run every frame"""

        if not self.layout:
            return

        # Update the layout and overlays
        self.layout.update()

        for key, value in self.overlays.items():
            value.update()

        # Handle the mouse
        # mouse = self.mouse
        #mouse_events = mouse.events
        mouse_events = self.get_mouse_inputs()
        #pos = list(mouse.position[:])
        pos = list(self.get_mouse_position())
        pos[0] *= render.getWindowWidth()
        pos[1] = render.getWindowHeight() - (render.getWindowHeight() * pos[1])
        kija = logic.KX_INPUT_JUST_ACTIVATED
        kia = logic.KX_INPUT_ACTIVE
        #if mouse_events[events.LEFTMOUSE] == logic.KX_INPUT_JUST_ACTIVATED:
        if mouse_events[events.LEFTMOUSE].activated:
            mouse_state = BGUI_MOUSE_CLICK
        elif mouse_events[events.LEFTMOUSE].released:
            mouse_state = BGUI_MOUSE_RELEASE
        elif mouse_events[events.LEFTMOUSE].active:
            mouse_state = BGUI_MOUSE_ACTIVE
        else:
            mouse_state = BGUI_MOUSE_NONE

        self.update_mouse(pos, mouse_state)

        # Handle the keyboard
        # keyboard = logic.keyboard

        #key_events = keyboard.events
        key_events = self.get_key_inputs()
        is_shifted = key_events[events.LEFTSHIFTKEY].active or \
                    key_events[events.RIGHTSHIFTKEY].active
        
        for key, state in key_events.items():
            if key in self.keymap:
                kc = self.keymap[key]
                oldval = self.keystates.get(kc, False)
                self.keystates[kc] = newval = bool(state.activated or state.active)
                if (not oldval) and (newval):
                    self.update_keyboard(kc, is_shifted)
