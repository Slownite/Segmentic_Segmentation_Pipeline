import torch
from torch.quantization import fuse_modules
import torch.nn as nn

class Wrapper(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):
        return self.model(x)['out']  # x is already a tensor now
        
def fuse_all_conv_bn(model):
    fused_count = 0

    def fuse_inside(module, prefix=''):
        nonlocal fused_count
        for name, child in module.named_children():
            full_name = f"{prefix}.{name}" if prefix else name

            # Recursively search child modules
            fuse_inside(child, full_name)

            # Detect Conv2dNormActivation and fuse ['0', '1'] inside it
            if isinstance(child, nn.Sequential) or isinstance(child, nn.Module):
                try:
                    sublayers = list(child.named_children())
                    subnames = [n for n, _ in sublayers]
                    if len(subnames) >= 2 and all(s in subnames for s in ['0', '1']):
                        fuse_modules(child, ['0', '1'], inplace=True)
                        print(f"Fused Conv+BN in: {full_name}")
                        fused_count += 1
                except:
                    continue

    model.eval()
    fuse_inside(model.backbone)
    print(f"\n✅ Done fusing {fused_count} Conv+BN pairs in backbone.")
