# Graphite: qtile
#
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
from schemer import colors

from libqtile.config import Key, Screen, Group, Drag, Click, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

mod = 'mod4'

keys = [
    Key([mod], 'n', lazy.layout.down()),
    Key([mod], 'p', lazy.layout.up()),
    Key([mod], 'b', lazy.layout.left()),
    Key([mod], 'f', lazy.layout.right()),

    Key([mod], 'w', lazy.window.kill()),
    Key([mod], 'r', lazy.spawncmd()),

    Key([mod], 'm', lazy.layout.shrink()),
    Key([mod], 'u', lazy.layout.grow()),
    Key([mod], 'i', lazy.layout.normalize()),
    Key([mod], 'o', lazy.layout.maximize()),

    Key([mod], 'Tab', lazy.next_layout()),
    Key([mod], 'space', lazy.layout.next()),

    Key([mod, 'shift'], 'n', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'p', lazy.layout.shuffle_up()),
    Key([mod, 'shift'], 'b', lazy.layout.shuffle_left()),
    Key([mod, 'shift'], 'f', lazy.layout.shuffle_right()),

    Key([mod, 'shift'], 'space', lazy.layout.rotate()),
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),
    Key([mod, 'control'], 'space', lazy.layout.flip()),
    
    Key([mod, 'control'], 'n', lazy.layout.grow_down()),
    Key([mod, 'control'], 'p', lazy.layout.grow_up()),
    Key([mod, 'control'], 'b', lazy.layout.grow_left()),
    Key([mod, 'control'], 'f', lazy.layout.grow_right()),

    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),
    
    Key([mod, 'mod1'], 'n', lazy.layout.flip_down()),
    Key([mod, 'mod1'], 'p', lazy.layout.flip_up()),
    Key([mod, 'mod1'], 'b', lazy.layout.flip_left()),
    Key([mod, 'mod1'], 'f', lazy.layout.flip_right()),

    Key([mod], 'Return', lazy.spawn('kitty')),
    Key([mod], '1', lazy.spawn('chromium --incognito')),
    Key([mod], '2', lazy.spawn('emacs')),
    Key([mod], '3', lazy.spawn('kitty ranger')),
    Key([mod], '4', lazy.spawn('kitty htop')),
    Key([mod], '0', lazy.spawn('scrot')),
    
    Key([mod], 'F11', lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], 'F12', lazy.group['scratchpad'].dropdown_toggle('nitrogen'))
]


group_config = { 
    'a': {
        'spawn': 'chromium',
        'layout': 'bsp',
        'label': 'web'
    },
    's': {
        'spawn': 'emacs',
        'layout': 'max',
        'label': 'emacs'
    },
    'd': {
        'layout': 'monadwide',
        'label': 'terms'
    },
    'v': {
        'spawn': 'discord',
        'layout':'max',
        'label': 'discord'
    },
    'c': {
        'spawn': 'spotify',
        'layout': 'bsp',
        'label': 'media'
    },
    'x': {
        'spawn': 'kitty htop',
        'layout': 'monadwide',
        'label': 'system'
    },
    'z': {
        'layout': 'max',
        'label': 'etc'
    }
}

groups = []

for name, config in group_config.items():
    groups.append(Group(name, **config))

    keys.extend([
        Key([mod], name, lazy.group[name].toscreen()),
        Key([mod, 'shift'], name, lazy.window.togroup(name))
    ])

groups.append(
    ScratchPad('scratchpad', [
        DropDown('nitrogen', 'nitrogen', opacity=1),
        DropDown('term', 'kitty', opacity=1)
    ])
)

common_theme = {
    'border_focus': '1f232a',
    'border_normal': '000000',
    'border_width': 1
}

layouts = [
    layout.Bsp(
        **common_theme,
        margin=0
    ),
    layout.MonadTall(
        **common_theme,
        margin=10,
        single_margin=15
    ),
    layout.MonadWide(
        **common_theme,
        margin=10,
        single_margin=15
    ),
    layout.Max()
]

widget_defaults = dict(
    font='sans',
    fontsize=14,
    padding=4,
)
extension_defaults = widget_defaults.copy()

sep_common = {
    'height_percent': None,
    'foreground': colors['m']
}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method='text',
                    this_current_screen_border=colors['S'],
                    active=colors['m'],
                    inactive=colors['m'],
                    padding=0,
                    urgent_alert_method='line',
                    urgent_border=colors['s'],
                    urgent_text=colors['s']
                ),
                widget.Sep(**sep_common),
                
                widget.CurrentLayout(
                    foreground=colors['m']
                ),
                widget.Prompt(
                    foreground=colors['M'],
                    cursor_color=colors['S']
                ),
                widget.Spacer(
                    length=bar.STRETCH,
                    width=None
                ),
                widget.Systray(
                ),
                widget.Spacer(
                    length=5,
                    width=None
                ),
                widget.Sep(**sep_common),

                widget.TextBox(
                    text='',
                    width=bar.CALCULATED,
                    foreground=colors['m'],
                    fontsize=18
                ),
                widget.Volume(
                    foreground=colors['m']
                ),
                widget.Sep(**sep_common),

                widget.CheckUpdates(
                    colour_have_updates=colors['S'],
                    colour_no_updates=colors['m'],
                    display_format='Pacman: {updates}'
                ),
                widget.Sep(**sep_common),

                widget.TextBox(
                    text='',
                    width=bar.CALCULATED,
                    foreground=colors['m'],
                    fontsize=18
                ),
                widget.Clock(
                    format='%a, %d %b',
                    foreground=colors['m']
                ),
                widget.Clock(
                    format='%I:%M:%S %p',
                    foreground=colors['S']
                )
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
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
floating_layout = layout.Floating(float_rules=[
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


def set_wallpaper(path=None):
    if path is None:
        path = '~/pics/Wallpapers/current'
    os.system(f'feh --bg-scale {path}')


def sync_packages():
    os.system('sudo pacman -Sy')


@hook.subscribe.startup
def autostart():
    set_wallpaper()
    sync_packages()
