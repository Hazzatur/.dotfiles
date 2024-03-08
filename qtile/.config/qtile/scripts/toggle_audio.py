#!/usr/bin/env python3

import re
import subprocess
from subprocess import Popen, PIPE


def run_command(command, return_output=False, shell=True):
    """Execute a system command. Optionally return its output."""
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=shell)
    if return_output:
        return process.stdout.strip()


def get_sinks():
    """Retrieve available sinks and their status."""
    output = run_command('pactl list short sinks', return_output=True)
    available_sinks = {}
    for line in output.split('\n'):
        parts = line.split('\t')
        if len(parts) >= 2:
            # Extracting sink ID and name, and removing extra details for clarity
            sink_id, sink_name = parts[0], re.sub(r'\s+.*$', '', parts[1])
            available_sinks[sink_id] = sink_name
    return available_sinks


def show_rofi(options, prompt='Select Sink:'):
    """Show options in rofi and return the selected index."""
    # Joining the options with newline characters
    options_str = "\n".join(options)
    # Command to invoke rofi with the required options
    rofi_command = ["rofi", "-dmenu", "-p", prompt, "-i", "-config", "~/.config/rofi/rofidmenu.rasi"]

    # Using Popen to pipe the options to rofi
    with Popen(["echo", options_str], stdout=PIPE) as p1, \
            Popen(rofi_command, stdin=p1.stdout, stdout=PIPE, text=True) as p2:
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        selected_option, _ = p2.communicate()
        selected_option = selected_option.strip()

    # Attempt to return the index of the selected option, or None if invalid
    try:
        return options.index(selected_option)
    except ValueError:
        return None


def set_default_sink(sink):
    """Set the default sink."""
    run_command(f'pactl set-default-sink {sink}')


# Get the current sink to set as rofi title
current_sink = run_command('pactl get-default-sink', return_output=True)
print("Current sink:", current_sink)

# Fetch all available sinks
sinks = get_sinks()

# Extract sink names for display, excluding the current sink
available_options = [name for sid, name in sinks.items() if name != current_sink]
print("Available sinks:", available_options)

# Use rofi to let the user select a new sink
choice_index = show_rofi(available_options, prompt=current_sink)

if choice_index is not None:
    selected_sink_name = available_options[choice_index]
    # Find the sink ID based on the selected name
    for sid, name in sinks.items():
        if name == selected_sink_name:
            # Set the chosen sink as the default
            set_default_sink(sid)
            print("New default sink set:", name)
            break
else:
    print("No sink selected or an error occurred.")
