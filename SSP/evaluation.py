import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
from tqdm import tqdm
import time

def test(model, dataloader, device, num_classes):
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_pixels = 0

    iou_per_class = torch.zeros(num_classes, dtype=torch.float64)
    union_per_class = torch.zeros(num_classes, dtype=torch.float64)

    criterion = torch.nn.CrossEntropyLoss(ignore_index=255)

    total_images = 0
    start_time = time.time()  # Start timer

    with torch.no_grad():
        for images, masks in tqdm(dataloader, desc="Testing"):
            images, masks = images.to(device), masks.to(device)
            batch_size = images.size(0)
            total_images += batch_size

            inference_start = time.time()
            outputs = model(images)['out']  # [B, C, H, W]
            inference_end = time.time()

            loss = criterion(outputs, masks)
            total_loss += loss.item()

            preds = torch.argmax(outputs, dim=1)  # [B, H, W]

            valid = masks != 255
            total_correct += (preds[valid] == masks[valid]).sum().item()
            total_pixels += valid.sum().item()

            for cls in range(num_classes):
                if cls == 255:
                    continue
                pred_inds = (preds == cls)
                target_inds = (masks == cls)
                intersection = (pred_inds & target_inds).sum().item()
                union = (pred_inds | target_inds).sum().item()
                if union > 0:
                    iou_per_class[cls] += intersection
                    union_per_class[cls] += union

    end_time = time.time()  # End timer

    avg_loss = total_loss / len(dataloader)
    accuracy = 100.0 * total_correct / total_pixels
    ious = iou_per_class / union_per_class.clamp(min=1e-6)
    mean_iou = ious.mean().item()

    total_inference_time = end_time - start_time
    avg_time_per_image = total_inference_time / total_images
    fps = total_images / total_inference_time

    print(f"\nTest Loss: {avg_loss:.4f}")
    print(f"Pixel Accuracy: {accuracy:.2f}%")
    print(f"Mean IoU: {mean_iou:.4f}")
    print(f"Total Inference Time: {total_inference_time:.2f} seconds")
    print(f"Avg Time/Image: {avg_time_per_image:.4f} seconds")
    print(f"Inference Speed: {fps:.2f} FPS")



