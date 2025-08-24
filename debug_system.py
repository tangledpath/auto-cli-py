#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')
from cls_example import DataProcessor
from auto_cli.cli import CLI
import argparse

# Create a debug version to see what's happening
cli = CLI(DataProcessor, enable_completion=True)
parser = cli.create_parser()

# Find both parsers
system_parser = None
config_parser = None

for action in parser._actions:
    if isinstance(action, argparse._SubParsersAction) and action.choices:
        if 'system' in action.choices:
            system_parser = action.choices['system']
        if 'config-management' in action.choices:
            config_parser = action.choices['config-management']

print('System parser has _commands?', hasattr(system_parser, '_commands'))
print('Config parser has _commands?', hasattr(config_parser, '_commands'))

if hasattr(system_parser, '_commands'):
    print('System commands:', system_parser._commands)
if hasattr(config_parser, '_commands'):
    print('Config commands:', config_parser._commands)

# Check if system parser has sub-global arguments
required_args, optional_args = [], []
for action in system_parser._actions:
    if action.dest != 'help' and hasattr(action, 'option_strings') and action.option_strings:
        if hasattr(action, 'required') and action.required:
            required_args.append(action.option_strings[-1])
        else:
            optional_args.append(action.option_strings[-1])

print('System has sub-global args?', bool(required_args or optional_args))
print('System sub-global args:', required_args + optional_args)

# Check config-management
required_args2, optional_args2 = [], []
for action in config_parser._actions:
    if action.dest != 'help' and hasattr(action, 'option_strings') and action.option_strings:
        if hasattr(action, 'required') and action.required:
            required_args2.append(action.option_strings[-1])
        else:
            optional_args2.append(action.option_strings[-1])

print('Config has sub-global args?', bool(required_args2 or optional_args2))
print('Config sub-global args:', required_args2 + optional_args2)

# Now check the inner system groups (completion and tune-theme)
def find_subparser(parent_parser, subcmd_name):
    for act in parent_parser._actions:
        if isinstance(act, argparse._SubParsersAction):
            if subcmd_name in act.choices:
                return act.choices[subcmd_name]
    return None

completion_parser = find_subparser(system_parser, 'completion')
tune_theme_parser = find_subparser(system_parser, 'tune-theme')

print('\n--- Completion Parser ---')
print('Has _commands?', hasattr(completion_parser, '_commands'))
if hasattr(completion_parser, '_commands'):
    print('Commands:', completion_parser._commands)

# Check completion sub-global args
comp_args = []
for action in completion_parser._actions:
    if action.dest != 'help' and hasattr(action, 'option_strings') and action.option_strings:
        comp_args.append(action.option_strings[-1])
print('Completion sub-global args:', comp_args)

print('\n--- Tune-Theme Parser ---')
print('Has _commands?', hasattr(tune_theme_parser, '_commands'))
if hasattr(tune_theme_parser, '_commands'):
    print('Commands:', tune_theme_parser._commands)

# Check tune-theme sub-global args
tt_args = []
for action in tune_theme_parser._actions:
    if action.dest != 'help' and hasattr(action, 'option_strings') and action.option_strings:
        tt_args.append(action.option_strings[-1])
print('Tune-theme sub-global args:', tt_args)