import sys, os
sys.path.append("..")
from exp_00_base import *

NODE_COEF=0.50
EDGE_COEF=1-NODE_COEF

EXPERIMENT_PARAMS["loss_params"]["edge_coef"] = EDGE_COEF
EXPERIMENT_PARAMS["loss_params"]["node_coef"] = NODE_COEF