import torch
import numpy as np

def train_collate(batch):
    batch_size = len(batch)
    inputs = torch.stack([batch[b][0] for b in range(batch_size)], 0)
    bboxes = [batch[b][1] for b in range(batch_size)]
    labels = [batch[b][2] for b in range(batch_size)]
    truth_masks = [batch[b][3] for b in range(batch_size)]
    masks = [batch[b][4] for b in range(batch_size)]

    # 规范维度：truth_masks/masks 保证都是 4D
    norm_truth = []
    for m in truth_masks:
        if m.ndim == 3:           # 只有一个 mask
            norm_truth.append(m[np.newaxis, ...])
        elif m.ndim == 4:
            norm_truth.append(m)
        else:
            raise ValueError(f'bad truth_masks ndim {m.ndim}')
    truth_masks = norm_truth

    norm_masks = []
    for m in masks:
        if m.ndim == 3:
            norm_masks.append(m[np.newaxis, ...])
        elif m.ndim == 4:
            norm_masks.append(m)
        else:
            raise ValueError(f'bad masks ndim {m.ndim}')
    masks = norm_masks

    # pad bboxes / labels 与之前保持一致
    max_boxes = max(len(box) for box in bboxes) if bboxes else 0
    padded_bboxes = []
    for box in bboxes:
        if len(box) < max_boxes:
            pad = np.zeros((max_boxes - len(box), 6), dtype=box.dtype)
            padded_box = np.concatenate([box, pad], axis=0)
        else:
            padded_box = box
        padded_bboxes.append(padded_box)
    padded_bboxes = np.array(padded_bboxes)

    max_labels = max(len(lab) for lab in labels) if labels else 0
    padded_labels = []
    for lab in labels:
        if len(lab) < max_labels:
            pad = np.full((max_labels - len(lab),), -1, dtype=lab.dtype)
            padded_lab = np.concatenate([lab, pad], axis=0)
        else:
            padded_lab = lab
        padded_labels.append(padded_lab)
    padded_labels = np.array(padded_labels)

    # pad truth_masks / masks 至相同的“最大 mask 数”
    max_masks = max(m.shape[0] for m in truth_masks + masks) if (truth_masks + masks) else 0
    target_shape = (max_masks, 128, 128, 128)

    def pad_volumes(vols, target_shape):
        padded = []
        for v in vols:
            p = np.zeros(target_shape, dtype=v.dtype)
            cs = tuple(min(a, b) for a, b in zip(v.shape, target_shape))
            slices = tuple(slice(0, s) for s in cs)
            p[slices] = v[slices]
            padded.append(p)
        return np.array(padded)

    padded_truth_masks = pad_volumes(truth_masks, target_shape)
    padded_masks = pad_volumes(masks, target_shape)

    return [inputs, padded_bboxes, padded_labels, padded_truth_masks, padded_masks]

# def train_collate(batch):  # to solve ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (4,) + inhomogeneous part.
#     batch_size = len(batch)
#     inputs = torch.stack([batch[b][0] for b in range(batch_size)], 0)
#     bboxes = [batch[b][1] for b in range(batch_size)]
#     labels = [batch[b][2] for b in range(batch_size)]
#     truth_masks = [batch[b][3] for b in range(batch_size)]
#     masks = [batch[b][4] for b in range(batch_size)]

#     return [inputs, bboxes, labels, truth_masks, masks]


def eval_collate(batch):
    batch_size = len(batch)
    inputs = torch.stack([batch[b][0]for b in range(batch_size)], 0)
    bboxes = [batch[b][1] for b in range(batch_size)]
    labels = [batch[b][2] for b in range(batch_size)]
    images = [batch[b][3] for b in range(batch_size)]

    return [inputs, bboxes, labels, images]


def test_collate(batch):
    batch_size = len(batch)
    for b in range(batch_size): 
        inputs = torch.stack([batch[b][0]for b in range(batch_size)], 0)
        images = [batch[b][1] for b in range(batch_size)]

    return [inputs, images]
