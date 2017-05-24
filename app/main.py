# -*- coding: utf-8 -*-

import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

TRAIN = True if 'TRAIN' in map(str.upper, sys.argv[1:]) else False
EVAL = True if 'EVAL' in map(str.upper, sys.argv[1:]) else False
XGB = True if 'XGB' in map(str.upper, sys.argv[1:]) else False

if 'ENSEMBLE' in map(str.upper, sys.argv[1:]):
    from .settings import EPOCHS
    TRAIN = EVAL = True
    ENSEMBLE = EPOCHS
else:
    ENSEMBLE = 1

if __name__ == '__main__':
    if not any([TRAIN, EVAL, ENSEMBLE]):
        raise ValueError('missing mode flags.\n\n'
                         'require one of following:\n'
                         'TRAIN, EVAL for convolutional neural net.')
    elif XGB and EVAL:
        from .xgb.metadata import xgb_prob
        from .engine.ovr import final_probs as cnn_prob
        from .settings import TAGS, TAGS_THRESHOLDS, IMAGE_PATH
        from .controllers import submit
        p = .7
        avg_prob = p * cnn_prob + (1 - p) * xgb_prob
        submit(avg_prob, IMAGE_PATH + 'test', TAGS, TAGS_THRESHOLDS)
    elif TRAIN or EVAL:
        from .engine import ovr
    elif XGB:
        from .xgb import metadata
