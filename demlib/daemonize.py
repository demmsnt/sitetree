#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', pidfile='./pid'):
    '''This forks the current process into a daemon.
    The stdin, stdout, and stderr arguments are file names that
    will be opened and be used to replace the standard file descriptors
    in sys.stdin, sys.stdout, and sys.stderr.
    These arguments are optional and default to /dev/null.
    Note that stderr is opened unbuffered, so
    if it shares a file with stdout then interleaved output
    may not appear in the order that you expect.
    '''

    # Finish up with the current stdout/stderr
    sys.stdout.flush()
    sys.stderr.flush()

    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.stdout.close()
            sys.exit(0)  # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Decouple from parent environment.
    # os.chdir("/")
    # os.umask(0)
    # os.setsid()

    # Do second fork.
    # try:
    #    pid = os.fork()
    #    if pid > 0:
    #        sys.stdout.close()
    #        sys.exit(0) # Exit second parent.
    # except OSError, e:
    #    sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror)    )
    #    sys.exit(1)

    # Now I am a daemon!

    # Redirect standard file descriptors.
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    #save pid into file
    print >>open(pidfile, "w"), os.getpid()

