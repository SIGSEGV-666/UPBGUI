from .widget import Widget, BGUI_DEFAULT, BGUI_NO_THEME, BGUI_CENTERED
from .frame import Frame
from .label import Label

FBSTYLE_CLASSIC = 0
FBSTYLE_SOLID = 1
class FrameButton(Widget):
    """A clickable frame-based button."""
    theme_section = 'FrameButton'
    theme_options = {
                'Color': (0.4, 0.4, 0.4, 1),
                'BorderSize': 1,
                'BorderColor': (0, 0, 0, 1),
                'LabelSubTheme': '',
                'SolidBaseColor': (0.4, 0.4, 0.4, 1.0),
                'SolidHoverColor': (0.6, 0.6, 0.6, 1.0),
                'SolidClickColor': (0.9, 0.9, 0.9, 1.0)
                }

    def __init__(self, parent, name=None, base_color=None, text="", font=None,
                    pt_size=None, aspect=None, size=[1, 1], pos=[0, 0], sub_theme='', text_color=None, border_size=None, border_color=None, style=FBSTYLE_CLASSIC, hover_color=None, click_color=None, options=BGUI_DEFAULT):
        """
        :param parent: the widget's parent
        :param name: the name of the widget
        :param base_color: the color of the button
        :param text: the text to display (this can be changed later via the text property)
        :param font: the font to use
        :param pt_size: the point size of the text to draw (defaults to 30 if None)
        :param aspect: constrain the widget size to a specified aspect ratio
        :param size: a tuple containing the width and height
        :param pos: a tuple containing the x and y position
        :param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
        :param options: various other options
        """

        Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)
        self.style = style
        self.frame = Frame(self, size=[1, 1], pos=[0, 0], options=BGUI_NO_THEME)
        self.label = Label(self, text=text, font=font, pt_size=pt_size, pos=[0, 0], sub_theme=self.theme['LabelSubTheme'], options=BGUI_DEFAULT | BGUI_CENTERED)
        if self.style == FBSTYLE_SOLID:
            self.solid_basecolor = (self.theme['SolidBaseColor'] if not base_color else (base_color))
            self.solid_hovercolor = (self.theme['SolidHoverColor'] if not hover_color else (hover_color))
            self.solid_clickcolor = (self.theme['SolidClickColor'] if not click_color else (click_color))
        if not base_color:
            base_color = self.theme['Color']
        self.base_color = base_color
        self.frame.border = (border_size if border_size is not None else self.theme['BorderSize'])
        self.frame.border_color = (border_color if border_color else self.theme['BorderColor'])

        self.light = [
            self.base_color[0] + 0.15,
            self.base_color[1] + 0.15,
            self.base_color[2] + 0.15,
            self.base_color[3]]
        self.dark = [
            self.base_color[0] - 0.15,
            self.base_color[1] - 0.15,
            self.base_color[2] - 0.15,
            self.base_color[3]]
        if text_color:
            self.label.color = text_color
        if self.style == FBSTYLE_CLASSIC:
            self.frame.colors = (self.dark, self.dark, self.light, self.light)
        elif self.style == FBSTYLE_SOLID:
            self.frame.colors = (self.solid_basecolor,)*4
    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, value):
        self.label.text = value

    @property
    def color(self):
        if self.style == FBSTYLE_CLASSIC:
            return self.base_color
        elif self.style == FBSTYLE_SOLID:
            return self.solid_basecolor
    @color.setter
    def color(self, value):
        if self.style == FBSTYLE_CLASSIC:
            self.base_color = value
            self.light = (
                self.base_color[0] + 0.15,
                self.base_color[1] + 0.15,
                self.base_color[2] + 0.15,
                self.base_color[3])
            self.dark = (
                self.base_color[0] - 0.15,
                self.base_color[1] - 0.15,
                self.base_color[2] - 0.15,
                self.base_color[3])
            self.frame.colors = (self.dark, self.dark, self.light, self.light)
        elif self.style == FBSTYLE_SOLID:
            self.solid_basecolor = value
    def _handle_hover(self):
        if self.style == FBSTYLE_CLASSIC:
            light = self.light[:]
            dark = self.dark[:]

            # Lighten button when hovered over.
            for n in range(3):
                light[n] += .1
                dark[n] += .1
            self.frame.colors = (dark, dark, light, light)
        elif self.style == FBSTYLE_SOLID:
            self.frame.colors = (self.solid_hovercolor,)*4

    def _handle_active(self):
        if self.style == FBSTYLE_CLASSIC:
            light = self.light[:]
            dark = self.dark[:]

            # Darken button when clicked.
            for n in range(3):
                light[n] -= .1
                dark[n] -= .1
            self.frame.colors = (light, light, dark, dark)
        elif self.style == FBSTYLE_SOLID:
            self.frame.colors = (self.solid_clickcolor,)*4

    def _draw(self):
        """Draw the button"""

        # Draw the children before drawing an additional outline
        Widget._draw(self)

        # Reset the button's color
        if self.style == FBSTYLE_CLASSIC:
            self.frame.colors = (self.dark, self.dark, self.light, self.light)
        elif self.style == FBSTYLE_SOLID:
            self.frame.colors = (self.solid_basecolor,)*4
