from torchvision import transforms
import torchvision.transforms.functional as TF
import random
from torchvision.datasets.voc import VOCSegmentation

class JointTransform:
    def __init__(self, size=(256, 256)):  # or (512, 512), depending on your model
        self.size = size

    def __call__(self, image, mask):
        # Resize both image and mask to same size
        image = TF.resize(image, self.size, interpolation=TF.InterpolationMode.BILINEAR)
        mask = TF.resize(mask, self.size, interpolation=TF.InterpolationMode.NEAREST)

        # Optional random flip
        if random.random() > 0.5:
            image = TF.hflip(image)
            mask = TF.hflip(mask)

        image = TF.to_tensor(image)
        mask = TF.pil_to_tensor(mask).long().squeeze(0)

        return image, mask
        
class VOCSegmentationWithJointTransform(VOCSegmentation):
    def __init__(self, root, year, image_set, download, joint_transform):
        super().__init__(root=root, year=year, image_set=image_set, download=download)
        self.joint_transform = joint_transform

    def __getitem__(self, index):
        image, mask = super().__getitem__(index)
        if self.joint_transform:
            image, mask = self.joint_transform(image, mask)
        return image, mask
