import os.path as osp
from glob import glob

from ...functional import FlowAugmentor
from .base_dataset import BaseDataset


class FlyingThings3D(BaseDataset):
    """
    Dataset Class for preparing the Flying Things 3D Synthetic dataset for training and validation.

    Parameters
    ----------
    root_dir : str
        path of the root directory for the flying things 3D dataset
    split : str, default : "training"
        specify the training or validation split
    dstype : str, default : "frames_cleanpass"
        specify dataset type
    is_prediction : bool, default : False
        If True, only image data are loaded for prediction otherwise both images and flow data are loaded
    init_seed : bool, default : False
        If True, sets random seed to worker
    append_valid_mask : bool, default :  False
    crop: bool, default : True
        Whether to perform cropping
    crop_size : :obj:`tuple` of :obj:`int`
        The size of the image crop
    crop_type : :obj:`str`, default : 'center'
        The type of croppping to be performed, one of "center", "random"
        If True, appends the valid flow mask to the original flow mask at dim=0
    augment : bool, default : True
        If True, applies data augmentation
    aug_params : :obj:`dict`, optional
        The parameters for data augmentation
    """

    def __init__(
        self,
        root_dir,
        split="training",
        dstype="frames_cleanpass",
        is_prediction=False,
        init_seed=False,
        append_valid_mask=False,
        crop=False,
        crop_size=(256, 256),
        crop_type="center",
        augment=True,
        aug_params={
            "color_aug_params": {"aug_prob": 0.2},
            "eraser_aug_params": {"aug_prob": 0.5},
            "spatial_aug_params": {"aug_prob": 0.8},
        },
    ):
        super(FlyingThings3D, self).__init__(
            init_seed=init_seed,
            is_prediction=is_prediction,
            append_valid_mask=append_valid_mask,
            crop=crop,
            crop_size=crop_size,
            crop_type=crop_type,
            augment=augment,
            aug_params=aug_params,
            sparse_transform=False,
        )
        assert (
            split.lower() == "training" or split.lower() == "validation"
        ), "Incorrect split values. Accepted split values: training, validation"

        self.is_prediction = is_prediction
        self.append_valid_mask = append_valid_mask

        if augment:
            self.augmentor = FlowAugmentor(crop_size=crop_size, **aug_params)

        if split.lower() == "training":
            split = "TRAIN"

        if split.lower() == "validation":
            split = "TEST"

        for cam in ["left"]:
            for direction in ["into_future", "into_past"]:
                image_dirs = sorted(glob(osp.join(root_dir, dstype, split + "/*/*")))
                image_dirs = sorted([osp.join(f, cam) for f in image_dirs])

                flow_dirs = sorted(
                    glob(osp.join(root_dir, "optical_flow/", split + "/*/*"))
                )
                flow_dirs = sorted([osp.join(f, direction, cam) for f in flow_dirs])

                for idir, fdir in zip(image_dirs, flow_dirs):
                    images = sorted(glob(osp.join(idir, "*.png")))
                    flows = sorted(glob(osp.join(fdir, "*.pfm")))
                    for i in range(len(flows) - 1):
                        if direction == "into_future":
                            self.image_list += [[images[i], images[i + 1]]]
                            self.flow_list += [flows[i]]
                        elif direction == "into_past":
                            self.image_list += [[images[i + 1], images[i]]]
                            self.flow_list += [flows[i + 1]]


class FlyingThings3DSubset(BaseDataset):
    """
    Dataset Class for preparing the Flying Things 3D Subset Synthetic dataset for training and validation.

    Parameters
    ----------
    root_dir : str
        path of the root directory for the flying things 3D dataset
    split : str, default : "training"
        specify the training or validation split
    is_prediction : bool, default : False
        If True, only image data are loaded for prediction otherwise both images and flow data are loaded
    init_seed : bool, default : False
        If True, sets random seed to worker
    append_valid_mask : bool, default :  False
        If True, appends the valid flow mask to the original flow mask at dim=0
    augment : bool, default : True
        If True, applies data augmentation
    aug_param : :obj:`dict`, optional
        The parameters for data augmentation
    """
    '''
    def __init__(
        self,
        root_dir,
        split="training",
        is_prediction=False,
        init_seed=False,
        append_valid_mask=False,
        augment=True,
        aug_params={
            "crop_size": (224, 224),
            "color_aug_params": {"aug_prob": 0.2},
            "eraser_aug_params": {"aug_prob": 0.5},
            "spatial_aug_params": {"aug_prob": 0.8},
        },
    ):
        super(FlyingThings3DSubset, self).__init__(
            augment, aug_params, is_prediction, init_seed, append_valid_mask
        )
    '''
    def __init__(
        self,
        root_dir,
        split="training",
        is_prediction=False,  
        init_seed=False,    
        append_valid_mask=False,  
        crop=False,                #add
        crop_size=(256, 256),     #add
        crop_type="center",       #add
        augment=True,    
        aug_params={    
            "color_aug_params": {"aug_prob": 0.2},
            "eraser_aug_params": {"aug_prob": 0.5},
            "spatial_aug_params": {"aug_prob": 0.8},
        },
    ):
        super(FlyingThings3DSubset, self).__init__(
            init_seed=init_seed,    
            is_prediction=is_prediction,     
            append_valid_mask=append_valid_mask,   
            crop=crop,              #add
            crop_size=crop_size,    #add
            crop_type=crop_type,    #add
            augment=augment,
            aug_params=aug_params,
            sparse_transform=False,
        )
        assert (
            split.lower() == "training" or split.lower() == "validation"
        ), "Incorrect split values. Accepted split values: training, validation"

        self.is_prediction = is_prediction
        self.append_valid_mask = append_valid_mask

        if augment:
            self.augmentor = FlowAugmentor(crop_size=crop_size, **aug_params)

        if split.lower() == "training":
            split = "train"

        if split.lower() == "validation":
            split = "val"

        image_list = []
        flow_list = []
        img_dir = osp.join(root_dir, split, "image_clean")
        flow_dir = osp.join(root_dir, split, "flow")

        for cam in ["left", "right"]:
            for direction in ["into_future", "into_past"]:
                im_paths = sorted(glob(osp.join(img_dir, cam, "*.png")))

                if direction == "into_past":
                    im_paths = im_paths[::-1]

                for idx in range(len(im_paths) - 1):
                    cur_fn = im_paths[idx]
                    nxt_fn = im_paths[idx + 1]
                    _, base_name = osp.split(cur_fn)
                    flow_fn = osp.join(
                        flow_dir, cam, direction, base_name[:-4] + ".flo"
                    )

                    if osp.exists(flow_fn):
                        image_list.append([cur_fn, nxt_fn])
                        flow_list.append(flow_fn)

        self.image_list = image_list
        self.flow_list = flow_list
