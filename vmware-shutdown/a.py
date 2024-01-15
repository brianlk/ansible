#!/usr/bin/env python

from tools import cli, service_instance, tasks, pchelper

def abc(*args):
    print(len(args))


abc(cli.Argument.DATACENTER_NAME)