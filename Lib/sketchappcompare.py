#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#  S K E T C H A P P 2 P Y
#
#  Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#  www.pagebot.io
#  Licensed under MIT conditions
#
#  Supporting DrawBot, www.drawbot.com
#  Supporting Flat, xxyxyz.org/flat
#  Supporting Sketch, https://github.com/Zahlii/python_sketch_api
# -----------------------------------------------------------------------------
#
#  sketchcompare.py
#
#  Take two SketchApp files and compare them. 
#  Output an oveview of differences.
#
import os
from sketchclasses import *
from sketchappreader import SketchAppReader
from sketchappwriter import SketchAppWriter

CHECK_ID = True

IGNORE = ['userInfo']
if not CHECK_ID:
    IGNORE.append('do_objectID')

def _compare(d1, d2, result, path=None):
    if path is None:
        path = ''

    if isinstance(d1, SketchBase):
        if not isinstance(d2, SketchBase):
            result.append("%s is not SketchBase instance" % d2)
        else:
            for attrName in d1.ATTRS:
                if attrName in IGNORE:
                    continue
                v1 = getattr(d1, attrName)
                v2 = getattr(d2, attrName)
                _compare(v1, v2, result, path + '/' + attrName)
    elif isinstance(d1, (list, tuple)):
        if not isinstance(d2,  (list, tuple)):
            result.append("%s is not List/Tuple instance" % d2)
        elif (len(d1) != len(d2)):
            result.append("%s Lists not same length %d - %d" % (path, d1, d2))
        else:
            for index, dd1 in enumerate(d1):
                dd2 = d2[index]
                _compare(dd1, dd2, result)
    elif d1 != d2:
        result.append("%s: %s %s" % (path, d1, d2))


def sketchCompare(sketchFile1, sketchFile2):
    """
    >>> from sketchappreader import SketchAppReader
    >>> testFileNames = ('TestImage.sketch',
    ...     'TestRectangles.sketch',
    ...     'TestStar.sketch',
    ...     'TestPolygon.sketch',
    ...     'TestOval.sketch',
    ...     'TestABC.sketch',
    ... )
    >>> for fileName in testFileNames:
    ...     reader = SketchAppReader()
    ...     readPath = '../Test/' + fileName
    ...     skf1 = reader.read(readPath)
    ...     writePath = readPath.replace('.sketch', 'Write.sketch')
    ...     writer = SketchAppWriter()
    ...     writer.write(writePath, skf1)
    ...     skf2 = reader.read(writePath)
    ...     sketchCompare(skf1, skf2) # Should not give any differences
    """
    result = []
    _compare(sketchFile1.document, sketchFile2.document, result)
    _compare(sketchFile1.user, sketchFile2.user, result)
    _compare(sketchFile1.meta, sketchFile2.meta, result)

    if result:
        return result
    return None

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
