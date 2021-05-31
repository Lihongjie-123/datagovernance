#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from optparse import OptionParser
import logging.config
from bin import _load  # nopep8

workdir = os.path.dirname(__file__)  # nopep8
if "lib" == os.path.basename(workdir):
    workdir = os.path.dirname(workdir)


def _handle_cmd_line(args=None):
    parser = OptionParser()

    parser.add_option("--id", dest="id", action="store",
                      type="string", default="0",
                      help="id use guard and create log file")
    parser.add_option("--logconfig", dest="logconfig", action="store",
                      type="string",
                      default=os.path.join(
                          workdir, 'etc', 'log.conf'),
                      help="log config file [%default]")

    (options, args) = parser.parse_args(args=args)
    return options, args


def main():
    options, _args = _handle_cmd_line()
    if options.logconfig:
        defaults = {"id": options.id}
        logging.config.fileConfig(options.logconfig, defaults)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
