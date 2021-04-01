#  Raymond Kirk (Tunstill) Copyright (c) 2020
#  Email: ray.tunstill@gmail.com
import pathlib
from collections import OrderedDict
from os import PathLike
from typing import Union

import cv2
import numpy as np

__all__ = ["COCOPlayer", "COCOVisualiser", "Visualiser"]

from rays_pycocotools.coco import COCO

from raytils.display import OpenCVDisplay

_COLORS = np.array([0.000, 0.447, 0.741, 0.850, 0.325, 0.098, 0.929, 0.694, 0.125, 0.494, 0.184, 0.556, 0.466, 0.674,
                    0.188, 0.301, 0.745, 0.933, 0.635, 0.078, 0.184, 0.300, 0.300, 0.300, 0.600, 0.600, 0.600, 1.000,
                    0.000, 0.000, 1.000, 0.500, 0.000, 0.749, 0.749, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 1.000,
                    0.667, 0.000, 1.000, 0.333, 0.333, 0.000, 0.333, 0.667, 0.000, 0.333, 1.000, 0.000, 0.667, 0.333,
                    0.000, 0.667, 0.667, 0.000, 0.667, 1.000, 0.000, 1.000, 0.333, 0.000, 1.000, 0.667, 0.000, 1.000,
                    1.000, 0.000, 0.000, 0.333, 0.500, 0.000, 0.667, 0.500, 0.000, 1.000, 0.500, 0.333, 0.000, 0.500,
                    0.333, 0.333, 0.500, 0.333, 0.667, 0.500, 0.333, 1.000, 0.500, 0.667, 0.000, 0.500, 0.667, 0.333,
                    0.500, 0.667, 0.667, 0.500, 0.667, 1.000, 0.500, 1.000, 0.000, 0.500, 1.000, 0.333, 0.500, 1.000,
                    0.667, 0.500, 1.000, 1.000, 0.500, 0.000, 0.333, 1.000, 0.000, 0.667, 1.000, 0.000, 1.000, 1.000,
                    0.333, 0.000, 1.000, 0.333, 0.333, 1.000, 0.333, 0.667, 1.000, 0.333, 1.000, 1.000, 0.667, 0.000,
                    1.000, 0.667, 0.333, 1.000, 0.667, 0.667, 1.000, 0.667, 1.000, 1.000, 1.000, 0.000, 1.000, 1.000,
                    0.333, 1.000, 1.000, 0.667, 1.000, 0.333, 0.000, 0.000, 0.500, 0.000, 0.000, 0.667, 0.000, 0.000,
                    0.833, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 0.167, 0.000, 0.000, 0.333, 0.000, 0.000, 0.500,
                    0.000, 0.000, 0.667, 0.000, 0.000, 0.833, 0.000, 0.000, 1.000, 0.000, 0.000, 0.000, 0.167, 0.000,
                    0.000, 0.333, 0.000, 0.000, 0.500, 0.000, 0.000, 0.667, 0.000, 0.000, 0.833, 0.000, 0.000, 1.000,
                    0.000, 0.000, 0.000, 0.143, 0.143, 0.143, 0.857, 0.857, 0.857, 1.000, 1.000, 1.000]
                   ).astype(np.float32).reshape(-1, 3)


def rgb_to_hls(red, green, blue):
    max_channel_value = max(red, green, blue)
    min_channel_value = min(red, green, blue)
    lightness = (min_channel_value + max_channel_value) / 2.0
    if min_channel_value == max_channel_value:
        return 0.0, lightness, 0.0
    if lightness <= 0.5:
        saturation = (max_channel_value - min_channel_value) / (max_channel_value + min_channel_value)
    else:
        saturation = (max_channel_value - min_channel_value) / (2.0 - max_channel_value - min_channel_value)
    rc = (max_channel_value - red) / (max_channel_value - min_channel_value)
    gc = (max_channel_value - green) / (max_channel_value - min_channel_value)
    bc = (max_channel_value - blue) / (max_channel_value - min_channel_value)
    if red == max_channel_value:
        hue = bc - gc
    elif green == max_channel_value:
        hue = 2.0 + rc - bc
    else:
        hue = 4.0 + gc - rc
    hue = (hue / 6.0) % 1.0
    return hue, lightness, saturation


def hls_to_rgb(hue, lightness, saturation):
    def _v(m_1, m_2, hue_v):
        hue_v = hue_v % 1.0
        if hue_v < (1.0 / 6.0):
            return m_1 + (m_2 - m_1) * hue_v * 6.0
        if hue_v < 0.5:
            return m_2
        if hue_v < (2.0 / 3.0):
            return m_1 + (m_2 - m_1) * ((2.0 / 3.0) - hue_v) * 6.0
        return m_1

    if saturation == 0.0:
        return lightness, lightness, lightness
    if lightness <= 0.5:
        m2 = lightness * (1.0 + saturation)
    else:
        m2 = lightness + saturation - (lightness * saturation)
    m1 = 2.0 * lightness - m2
    return _v(m1, m2, hue + (1.0 / 3.0)), _v(m1, m2, hue), _v(m1, m2, hue - (1.0 / 3.0))


def random_color(rgb=False, maximum=255):
    """
    Args:
        rgb (bool): whether to return RGB colors or BGR colors.
        maximum (int): either 255 or 1

    Returns:
        ndarray: a vector of 3 numbers
    """
    idx = np.random.randint(0, len(_COLORS))
    ret = _COLORS[idx] * maximum
    if not rgb:
        ret = ret[::-1]
    return ret


class GenericMask:
    def __init__(self, mask_or_polygons, height, width):
        self._mask = self._polygons = None
        self.height = height
        self.width = width

        m = mask_or_polygons

        if isinstance(m, list):
            self._polygons = [np.asarray(x).reshape(-1) for x in m]
            return

        if isinstance(m, np.ndarray):  # assumed to be a binary mask
            assert m.shape[1] != 2, m.shape
            assert m.shape == (height, width), m.shape
            self._mask = m.astype("uint8")
            return

        raise ValueError("GenericMask cannot handle object {} of type '{}'".format(m, type(m)))

    @property
    def polygons(self):
        if self._polygons is None:
            mask = np.ascontiguousarray(self._mask)
            res = cv2.findContours(mask.astype("uint8"), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
            hierarchy = res[-1]
            if hierarchy is None:  # empty mask
                return [], False
            has_holes = (hierarchy.reshape(-1, 4)[:, 3] >= 0).sum() > 0
            res = res[-2]
            res = [x.flatten() for x in res]
            res = [x for x in res if len(x) >= 6]
            self._polygons = res
        return self._polygons


class Visualiser:
    """Visualise bounding boxes/masks from on images

    Examples:
        To display a bounding box on an image

        >>> vis = Visualiser(cv2.imread("image.png"))
        >>> vis.draw_box([0, 0, 10, 10], (255, 255, 255))  # draw a white box at x1=0,x2=10,y1=0,y2=10
        >>> cv2.imshow('', vis.get_image(overlay_alpha=0.5))
        >>> cv2.waitKey(0)

    """

    def __init__(self, img_rgb):
        self.img = np.asarray(img_rgb).clip(0, 255).astype(np.uint8)
        self.height, self.width = self.img.shape[:2]

        # Layers of the final visualisation
        self._overlay = np.zeros(self.img.shape) - 1  # -1 is the invalid overlay value
        self._text = np.zeros(self.img.shape) - 1

        self._min_text_height = 12
        self._max_text_height = self.img.shape[0] // 3

    def draw_coco_detections(self, annotations: list, category_id_to_name=None):
        boxes = []
        masks = []
        labels = []
        assigned_colors = []
        alpha = 0.5

        for ann in annotations:
            x1, y1, w, h = ann["bbox"]
            x2, y2 = x1 + w, y1 + h
            boxes.append([x1, y1, x2, y2])
            # TODO: implement_masks
            # if ann["segmentation"]:
            #     masks.append(GenericMask(ann["segmentation"], height, width))
            class_label = ann["category_id"]
            if category_id_to_name:
                class_label = category_id_to_name[class_label]
            instance_id = ann.get("instance_id", " ")
            assigned_colors.append(_COLORS[int(instance_id % len(_COLORS))])
            labels.append(f"{class_label}{instance_id}")

        self.overlay_instances(boxes, labels, masks or None, assigned_colors or None, alpha)

    def overlay_instances(self, boxes=None, labels=None, masks=None, assigned_colors=None, alpha=0.5):
        num_instances = None
        if boxes is not None:
            boxes = self._convert_boxes(boxes)
            num_instances = len(boxes)
        if masks is not None:
            masks = self._convert_masks(masks)
            if num_instances:
                assert len(masks) == num_instances
            else:
                num_instances = len(masks)

        if labels is not None:
            assert len(labels) == num_instances
        if assigned_colors is None:
            assigned_colors = [random_color(rgb=True, maximum=1) for _ in range(num_instances)]
        if num_instances == 0:
            return

        # Display largest to smallest (less occlusion)
        areas = None
        if boxes is not None:
            areas = np.prod(boxes[:, 2:] - boxes[:, :2], axis=1)

        if areas is not None:
            sorted_idxs = np.argsort(-areas).tolist()
            boxes = boxes[sorted_idxs] if boxes is not None else None
            labels = [labels[k] for k in sorted_idxs] if labels is not None else None
            masks = [masks[idx] for idx in sorted_idxs] if masks is not None else None
            assigned_colors = [assigned_colors[idx] for idx in sorted_idxs]

        for i in range(num_instances):
            color = assigned_colors[i]

            if boxes is not None:
                self.draw_box(boxes[i], edge_color=color)

            if masks is not None:
                for segment in masks[i].polygons:
                    self.draw_polygon(segment.reshape(-1, 2), color, alpha=alpha)

            if labels is not None:
                lighter_color = self._change_color_brightness(color, brightness_factor=0.7)
                self.draw_text_for_box(labels[i], bbox=boxes[i], color=lighter_color, thickness=1)

    def get_image(self, overlay_alpha=0.5):
        canvas = self.img.copy()
        overlay_valid = np.where(self._overlay != -1)
        canvas[overlay_valid] = (canvas[overlay_valid] * (1 - overlay_alpha)) + (self._overlay[overlay_valid] *
                                                                                 overlay_alpha)
        text_valid = np.where(self._text != -1)
        canvas[text_valid] = self._text[text_valid]
        return canvas

    """
    Primitive drawing functions:
    """

    def draw_text_for_box(self, text, bbox, font_scale=None, color=None, origin="above top left", thickness=1,
                          bbox_scale=1.0 / 8.0):
        # If box height is passed scale relative to box height * font_scale
        font = cv2.FONT_HERSHEY_COMPLEX

        x0, y0, x1, y1 = bbox
        bbox_height = y1 - y0

        # Use 1/8th bbox or min as min_text_height
        text_height = min(max(self._min_text_height, bbox_height * bbox_scale), self._max_text_height)

        if not font_scale:
            # apt version of opencv doesn't have this function
            if hasattr(cv2, "getFontScaleFromHeight"):
                font_scale = cv2.getFontScaleFromHeight(font, int(text_height), thickness)
            else:  # Reasonable default for cv2.FONT_HERSHEY_COMPLEX
                font_ascii = (9 + 12 * 16) + (16 << 8) + (32 << 8)
                font_base_line = font_ascii & 15
                font_cap_line = (font_ascii >> 4) & 15
                font_scale = (int(text_height) - (thickness + 1) / 2.0) / (font_cap_line + font_base_line)

        (label_width, label_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        pad = 0.7
        box_pad = min(int((1 - pad) * label_width), int((1 - pad) * label_height))
        label_height += box_pad
        position = (x0 if "left" in origin else x1, y0 if "top" in origin else y1 - label_height - box_pad)
        if "above" in origin:
            position = (position[0], position[1] - label_height - box_pad)
        elif "below" in origin:
            position = (position[0], position[1] + label_height + box_pad)
        self.draw_text(text, position, font_scale, color, font, thickness)

    def draw_text(self, text, position, font_scale=1.0, color=None, font=None, thickness=1):
        if color is None:
            color = np.asarray((1.0, 1.0, 1.0))

        color = np.maximum(list(color), 0.2)
        color[np.argmax(color)] = max(0.8, np.max(color))
        color = tuple(int(i * 255) for i in color)
        position = tuple(int(i) for i in position)

        if font is None:
            font = cv2.FONT_HERSHEY_COMPLEX

        scale = font_scale
        (label_width, label_height), baseline = cv2.getTextSize(text, font, scale, thickness)

        pad = 0.7
        box_pad = min(int((1 - pad) * label_width), int((1 - pad) * label_height))
        box_cords = (position[0], position[1],
                     position[0] + label_width + (box_pad * 2), position[1] + label_height + (box_pad * 2))
        self.draw_box(box_cords, np.asarray((0, 0, 0)), fill=True)

        position = (position[0] + box_pad, position[1] + box_pad + label_height)
        cv2.putText(self._text, text, position, font, scale, color, thickness, cv2.LINE_AA)

    def draw_box(self, box_coord, edge_color, fill=False):
        x0, y0, x1, y1 = [int(i) for i in box_coord]
        line_width = -1 if fill else 2
        edge_color = (edge_color * 255).astype(int).tolist()
        cv2.rectangle(self._overlay, (x0, y0), (x1, y1), edge_color, line_width)

    def draw_polygon(self, segment, color, edge_color=None, alpha=0.5):
        if edge_color is None:
            # Edge is brighter
            edge_color = np.asarray(self._change_color_brightness(color, brightness_factor=0.7))

        color = list((color * 255).astype(int))
        edge_color = list((edge_color * 255.0).astype(int))
        edge_thickness = 2
        segment = segment.reshape((-1, 1, 2))
        cv2.fillPoly(self._overlay, segment, color)
        cv2.polylines(self._overlay, segment, False, edge_color, edge_thickness)

    """
    Internal methods:
    """

    def _change_color_brightness(self, color, brightness_factor):
        assert brightness_factor >= -1.0 and brightness_factor <= 1.0
        polygon_color = rgb_to_hls(*list(color))
        modified_lightness = polygon_color[1] + (brightness_factor * polygon_color[1])
        modified_lightness = 0.0 if modified_lightness < 0.0 else modified_lightness
        modified_lightness = 1.0 if modified_lightness > 1.0 else modified_lightness
        modified_color = hls_to_rgb(polygon_color[0], modified_lightness, polygon_color[2])
        return modified_color

    def _convert_boxes(self, boxes):
        return np.asarray(boxes)

    def _convert_masks(self, masks_or_polygons):
        m = masks_or_polygons
        ret = []
        for x in m:
            if isinstance(x, GenericMask):
                ret.append(x)
            else:
                ret.append(GenericMask(x, self.height, self.width))
        return ret


class COCOVisualiser:
    """Visualise bounding boxes/masks from on images from a coco dataset

    Examples:
        To display a COCO dataset

        >>> for vis_img in COCOVisualiser("coco_dataset.json", sort=True):
        >>>     cv2.imshow('', vis_img)
        >>>     cv2.waitKey(0)

    """

    def __init__(self, coco_path: Union[PathLike, str], image_root=None, sort=False):
        if isinstance(coco_path, (str, PathLike)):
            coco = pathlib.Path(coco_path)
        else:
            raise TypeError(f"PathLike or str paths required not {type(coco_path)}")
        if image_root is None:
            image_root = coco.parent
        self.image_root = image_root
        self.coco = COCO(str(coco))
        self.images = self.coco.imgs
        if sort:
            self.images = OrderedDict(sorted(self.images.items()))
        self.idx_to_id = dict(enumerate(self.images.keys()))
        self.img_to_annotations = self.coco.imgToAnns
        self.cat_id_to_name = {i: v["name"] for i, v in self.coco.cats.items()}

    def __len__(self):
        return len(self.images)

    def __iter__(self):
        for i in range(self.__len__()):
            yield self.__getitem__(i)

    def __getitem__(self, item):
        image_id = self.idx_to_id[item]
        image_info = self.images[image_id]
        image_path = str(self.image_root / image_info["file_name"])
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not valid from path {image_path}")
        visualiser = Visualiser(img)
        annotations = self.img_to_annotations.get(image_info["id"], None)
        if annotations:
            visualiser.draw_coco_detections(self.img_to_annotations[image_info["id"]], self.cat_id_to_name)
        return visualiser.get_image(overlay_alpha=0.5)


class COCOPlayer:
    """Open an interactive COCO dataset viewer.

    Examples:
        To display a COCO dataset

        >>> # Use controls a=back, d=forward, r=restart, e=end, q=quit, space=play/pause
        >>> COCOPlayer("coco_dataset.json", sort=True).show()

    """

    def __init__(self, coco_path, sort=False):
        self.paused = False
        self.display = OpenCVDisplay(window_name=str(coco_path))
        self.display.register_key(37, self.prev)  # left key
        self.display.register_key(39, self.prev)  # right key
        self.display.register_key(97, self.prev)  # a key
        self.display.register_key(100, self.next)  # d key
        self.display.register_key(114, self.restart)  # r key
        self.display.register_key(101, self.end)  # e key
        self.display.register_key(32, self.play_pause)  # space key
        self.display.register_key(127, self.display.stop)  # escape key
        self.display.register_key(113, self.display.stop)  # q key
        self.current_image = 0
        self.coco_visualiser = COCOVisualiser(coco_path, sort=sort)

    def __exit__(self):
        self.display.stop()

    def show(self):
        while self.display.is_running():
            self.current_image = max(0, min(self.current_image, len(self.coco_visualiser) - 1))
            self.display.show(frame=self.coco_visualiser[self.current_image])
            if not self.paused:
                self.next()

    def prev(self):
        if self.current_image > 0:
            self.current_image -= 1

    def next(self):
        if self.current_image <= len(self.coco_visualiser):
            self.current_image += 1
        else:
            self.paused = True

    def play_pause(self):
        self.paused = not self.paused

    def restart(self):
        self.paused = True
        self.current_image = 0

    def end(self):
        self.paused = True
        self.current_image = len(self.coco_visualiser) - 1
