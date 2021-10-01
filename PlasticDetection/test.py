import argparse
import json
import os
import sys
from pathlib import Path
from threading import Thread

import numpy as np
import torch
from tqdm import tqdm

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = ROOT.relative_to(Path.cwd())  # relative

from models.experimental import attempt_load
from utils.datasets import create_dataloader
from utils.general import coco80_to_coco91_class, check_dataset, check_img_size, check_requirements, \
    check_suffix, check_yaml, box_iou, non_max_suppression, scale_coords, xyxy2xywh, xywh2xyxy, set_logging, \
    increment_path, colorstr, print_args
from utils.metrics import ap_per_class, ConfusionMatrix
from utils.plots import output_to_target, plot_images, plot_val_study
from utils.torch_utils import select_device, time_sync
from utils.callbacks import Callbacks


@torch.no_grad()
def run():
        
    data= 'data.yaml'
    weights= ['./yolov5-weights/weights/best.pt']
    batch_size= 32
    imgsz= 416
    conf_thres= 0.4
    iou_thres= 0.6
    task= 'val'
    device= 'cpu'
    save_hybrid = False
    augment = False
    single_cls= True
    save_txt= False
    project= 'runs/val'
    name= 'exp'
    exist_ok= False
    half= False
    dataloader= None
    save_dir= '.'
    
    device = select_device(device, batch_size=batch_size)
    
    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    check_suffix(weights, '.pt')
    model = attempt_load(weights, map_location=device)  # load FP32 model
    gs = max(int(model.stride.max()), 32)  # grid size (max stride)
    imgsz = check_img_size(imgsz, s=gs)  # check image size

    model.float()

    # Configure
    model.eval()

    # Dataloader
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    
    pimages_path = "deeptrash\mytest\images"
    dataloader = create_dataloader(pimages_path, imgsz, batch_size, gs, single_cls, pad=0.5, rect=True, prefix=colorstr(f'{task}: '))[0]

    names = {0: 'plastic'}
    
    for batch_i, (img, targets, paths, shapes) in enumerate(dataloader):
        
        img = img.to(device, non_blocking=True)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        targets = targets.to(device)
        nb, _, height, width = img.shape  # batch size, channels, height, width

        # Run model
        out, train_out = model(img, augment=augment)  # inference and training outputs

        # Run NMS
        targets[:, 2:] *= torch.Tensor([width, height, width, height]).to(device)  # to pixels
        lb = [targets[targets[:, 0] == i, 1:] for i in range(nb)] if save_hybrid else []  # for autolabelling
        out = non_max_suppression(out, conf_thres, iou_thres, labels=lb, multi_label=True, agnostic=single_cls)
        

        # Plot images
        f = save_dir / f'val_batch{batch_i}_pred.jpg'  # predictions
        Thread(target=plot_images, args=(img, output_to_target(out), paths, f, names), daemon=True).start()

if __name__ == "__main__":
    run()