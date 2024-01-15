#!/usr/bin/env python

from tools import cli, service_instance, tasks, pchelper

def abc(*args):
    print(str(args))


abc(cli.Argument.MOUNT, cli.Argument.DATACENTER_NAME)