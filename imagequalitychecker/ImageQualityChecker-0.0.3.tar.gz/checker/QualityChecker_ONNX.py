import numpy as np
import albumentations as A
import cv2
from albumentations.pytorch.transforms import ToTensorV2
import onnxruntime


class QualityChecker_ONNX:
    transform = A.Compose([
        A.Resize(224, 224),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    category_mapping = dict(zip(
        [0, 1, 2],
        ['normal', 'soil', 'defocusing']
    ))

    session = onnxruntime.InferenceSession("efficientnet_b3_qualitycheck.onnx")

    @classmethod
    def preprocess_one_image(cls, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_aug = cls.transform(image=image)['image']
        # convert to correct format
        image_aug = image_aug.transpose(2, 0, 1)
        image_aug = np.expand_dims(image_aug, axis=0)
        return image_aug

    @classmethod
    def inference_one_image(cls, image_path):
        input = cls.preprocess_one_image(image_path)
        output = cls.session.run(None, {'input': input})
        pred = np.argmax(output[0], 1)[0]
        return cls.category_mapping[pred]

    @classmethod
    def preprocess_multiple_image(cls, image_paths):
        images = []
        for path in image_paths:
            images.append(cls.preprocess_one_image(path))
        return np.vstack(images)

    @classmethod
    def inference_images(cls, image_paths):
        inputs = cls.preprocess_multiple_image(image_paths)
        outputs = cls.session.run(None, {'input': inputs})
        preds = np.argmax(outputs[0], axis=1)
        return [cls.category_mapping[pred] for pred in preds]
