import os
import warnings

import pandas as pd
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger

from model_utils.chest_xray_detection import *

setup_logger()
warnings.filterwarnings("ignore")

from configs.common import *
from configs.chest_abnormalities_detection import ChestAbnormalitiesDetectron2Config
from model_utils.contours import *


class ChestXrayDetectionDetectronRunner():

    def __init__(self):

        self.config = ChestAbnormalitiesDetectron2Config()
        c = get_cfg()
        model_cfg = model_zoo.get_config_file(self.config.model_base)
        c.merge_from_file(model_cfg)
        c.MODEL.WEIGHTS = os.path.join(self.config.weights)  # path to the model we just trained
        c.MODEL.DEVICE = self.config.device
        c.MODEL.ROI_HEADS.NUM_CLASSES = len(self.config.labels)
        c.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.config.conf_thres
        self.predictor = DefaultPredictor(c)
    
    def predict(self, img, img_id):
        """
        Input: BGR images
        """

        pr_viz = predict_and_visualize(self.predictor, img, self.config.labels, viz_size=(img.shape[1], img.shape[0]))
        return pr_viz
