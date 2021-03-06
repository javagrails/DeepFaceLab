﻿import os
import sys
import operator
import numpy as np
import cv2
from tqdm import tqdm
from shutil import copyfile

from pathlib import Path
from utils import Path_utils
from utils import image_utils
from utils.DFLPNG import DFLPNG
from utils.DFLJPG import DFLJPG
from utils.cv2_utils import *
from facelib import LandmarksProcessor
from utils.SubprocessorBase import SubprocessorBase
import multiprocessing

def convert_png_to_jpg_file (filepath):
    filepath = Path(filepath)
    
    if filepath.suffix != '.png': 
        return  
    dflpng = DFLPNG.load (str(filepath), print_on_no_embedded_data=True)
    if dflpng is None: 
        return
    
    dfl_dict = dflpng.getDFLDictData()
    
    img = cv2_imread (str(filepath))
    new_filepath = str(filepath.parent / (filepath.stem + '.jpg'))
    cv2_imwrite ( new_filepath, img, [int(cv2.IMWRITE_JPEG_QUALITY), 85])

    DFLJPG.embed_data( new_filepath, 
                       face_type=dfl_dict.get('face_type', None),
                       landmarks=dfl_dict.get('landmarks', None),
                       yaw_value=dfl_dict.get('yaw_value', None),
                       pitch_value=dfl_dict.get('pitch_value', None),
                       source_filename=dfl_dict.get('source_filename', None),
                       source_rect=dfl_dict.get('source_rect', None),
                       source_landmarks=dfl_dict.get('source_landmarks', None) )
                       
    filepath.unlink()
        
def convert_png_to_jpg_folder (input_path):
    input_path = Path(input_path)

    print ("Converting PNG to JPG...\r\n")

    for filepath in tqdm( Path_utils.get_image_paths(input_path), desc="Converting", ascii=True):
        filepath = Path(filepath)
        convert_png_to_jpg_file(filepath)
