#!/usr/bin/python

import avro.schema
import logging
import pykwalify
import pykwalify.core
import glob

from termcolor import cprint

pykwalify.init_logging(logging.FATAL)

passed = failed = 0

for file in glob.iglob('./*/package.yaml'):
    c = pykwalify.core.Core(
        source_file=file,
        schema_files=['./package.schema.yaml'],
    )
    c.validate(raise_exception=False)
    if c.validation_errors:
        cprint(file + ':', 'red')
        for error in c.validation_errors:
            cprint('  - ' + error, 'red')
        failed += 1
    else:
        passed += 1


for file in glob.iglob('./*/plugins/*.yaml', recursive=True):
    c = pykwalify.core.Core(
        source_file=file,
        schema_files=['./plugin.schema.yaml'],
    )
    c.validate(raise_exception=False)
    if c.validation_errors:
        cprint(file + ':', 'red')
        for error in c.validation_errors:
            cprint('  - ' + error, 'red')
        failed += 1
    else:
        passed += 1

cprint(f'\n{passed} passed, {failed} failed, {passed+failed} total files validated', 'white')
