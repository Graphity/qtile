import os
from libqtile.config import Key, Screen, Group, Drag, Click, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

colors={
    'blue': '#0061ff',
    'blue_purple': '#5555ff',
    'blue_dark': '#004fcf',
    'blue_light_pale': '#78bbd9',
    'blue_dark_pale': '#6681bd',
    'blue_arch': '#0f94d2',

    'pink': '#f92672',

    'cyan': '#55ffff',
    'cyan_light': '#50e5e5',
    'cyan_dark': '#23cdcd',
    
    'green_light': '#55ff55',
    'green_dark': '#3eb83f',
    
    'teal': '#46a6a8',
    'teal_dark': '#2f8384',

    
    'red': '#f50042',
    'red_light': '#e26d74',
    'red_dark': '#9c1439',

    'purple': '#7b13ef',
    'purple_light': '#37245d',
    'purple_dark': '#1c0525'
}

mod = "mod4"

keys = [
    Key([mod], 'space', lazy.layout.next()),
    Key([mod], 'Tab', lazy.next_layout()),
   
    Key([mod], 'p', lazy.layout.up()),
    Key([mod], 'n', lazy.layout.down()),
    Key([mod], 'b', lazy.layout.left()),
    Key([mod], 'f', lazy.layout.right()),
    
    Key([mod], 'k', lazy.layout.grow()),
    Key([mod], 'l', lazy.layout.shrink()),
    Key([mod], 'i', lazy.layout.normalize()),
    Key([mod], 'o', lazy.layout.maximize()),
    
    Key([mod], 'w', lazy.window.kill()),
    Key([mod], 'r', lazy.spawncmd()),

    
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),

    
    Key([mod, 'shift'], 'p', lazy.layout.shuffle_up()),
    Key([mod, 'shift'], 'n', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'b', lazy.layout.shuffle_left()),
    Key([mod, 'shift'], 'f', lazy.layout.shuffle_right()),

    Key([mod, 'shift'], 'b', lazy.layout.swap_left()),
    Key([mod, 'shift'], 'f', lazy.layout.swap_right()),

    
    Key([mod, 'shift'], 'space', lazy.layout.flip()),
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),
    
    Key([mod], 'Return', lazy.spawn('kitty')),

    
    Key([], 'F11', lazy.group['scratchpad'].dropdown_toggle('term1')),
    Key([], 'F12', lazy.group['scratchpad'].dropdown_toggle('term2'))
]

names_labels = {
    's': '',
    'd': '',
    'z': '',
    'x': '',
    'c': '',
    'v': ''
}

groups = [Group(name, label=label) for name, label in names_labels.items()]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, 'shift'], i.name, lazy.window.togroup(i.name))
    ])

groups.append(
    ScratchPad("scratchpad", [
        DropDown("term1", "nitrogen", opacity=0.8),

        DropDown("term2", "kitty",
                 x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
                 on_focus_lost_hide=True) ])
)

common_theme = {
    'border_focus': colors['purple_light'],  # '#700104',
    'border_width': 1
}

layouts = [
    layout.MonadTall(
        **common_theme,
        margin=10,
        single_margin=15
    ),
    layout.Bsp(
        **common_theme,
        margin=0,
        border_normal='#000000'
    ),
    layout.Max()
]

widget_defaults = dict(
    font='sans',
    fontsize=14,
    padding=4,
)
    
extension_defaults = widget_defaults.copy()
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method='text',
                    borderwidth=2,
                    rounded=False,
                    this_current_screen_border=colors['purple_light'],
                    active=colors['red'],
                    inactive='606060',
                    fontsize=18,
                    padding=0
                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=['/home/graphity/.config/qtile/icons/']
                ),
                widget.CurrentLayout(
                    foreground=colors['red']
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=60
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=80
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=100
                ),
                widget.Mpris2(
                    name='spotify',
                    display_metadata=['xesam:title', 'xesam:artist'],
                    objname='org.mpris.MediaPlayer2.spotify',
                    stop_pause_text='. . .',
                    scroll_chars=None,
                    foreground=colors['red_dark']
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=100
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=80
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=60
                ),
                widget.Prompt(
                    foreground=colors['red'],
                    cursor_color=colors['purple']
                ),
                widget.Spacer(
                    length=bar.STRETCH,
                    width=None
                ),
                widget.Systray(
                    icon_size=20
                ),
                widget.Spacer(
                    length=5,
                    width=None
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=60
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=80
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=100
                ),
                widget.TextBox(
                    text='',
                    width=bar.CALCULATED,
                    foreground=colors['red'],
                    fontsize=18
                ),
                widget.CPUGraph(
                    border_color=colors['purple_dark'],
                    fill_color='f50042.3',
                    graph_color=colors['red'],
                    line_width=1,
                    samples=40,
                    frequency=0.1,
                    border_width=1
                ),
                widget.TextBox(
                    text='',
                    width=bar.CALCULATED,
                    foreground=colors['red'],
                    fontsize=18
                ),
                widget.HDDBusyGraph(
                    border_color=colors['purple_dark'],
                    fill_color='f50042.3',
                    graph_color=colors['red'],
                    line_width=1,
                    samples=40,
                    frequency=0.1,
                    border_width=1
                ),
                widget.Image(
                    filename='~/.config/qtile/icons/red_headphones.png'
                ),
                widget.Volume(
                    foreground=colors['red']
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=60
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=80
                ),
                widget.Image(
                    filename='~/.config/qtile/icons/red_pacman.png'
                ),
                widget.CheckUpdates(
                    display_format='{updates}',
                    colour_have_updates=colors['red_light'],
                    colour_no_updates=colors['red']
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=80
                ),
                widget.Sep(
                    height_percent=None,
                    foreground=colors['purple_light'],
                    size_percent=60
                ),
                widget.TextBox(
                    text='',
                    width=bar.CALCULATED,
                    foreground=colors['red'],
                    fontsize=18
                ),
                widget.Clock(
                    format='%a, %d %b ',
                    foreground=colors['red']
                ),
                widget.Clock(
                    format='%I:%M:%S %p',
                    background=colors['red'],
                    foreground='000000'
                )
            ],
            24,
            background=colors['purple_dark']
        ),
    ),
]

mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
Floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])

auto_fullscreen = False
focus_on_window_activation = "smart"
wmname = "qtile"


def set_wallpaper():
    path = '~/Wallpapers/shitcraft/arch_threelines.png'
    os.system(f'feh --bg-scale {path}')


@hook.subscribe.startup
def autostart():
    set_wallpaper()

