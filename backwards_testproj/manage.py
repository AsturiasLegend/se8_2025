#!/usr/bin/env python
# 该文件不要修改
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backwards_testproj.settings") #设置后端settings位置
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django with run config, please check your environment"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
