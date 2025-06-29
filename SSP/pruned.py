import torch
import torch.nn.utils.prune as prune
def pruned_conv_layer(model, amount=0.4):
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            prune.l1_unstructured(module, name='weight', amount=amount)
            if module.bias is not None:
                prune.l1_unstructured(module, name='bias', amount=amount)
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            try:
                prune.remove(module, 'weight')
                if module.bias is not None and hasattr(module, 'bias_mask'):
                    prune.remove(module, 'bias')
            except ValueError:
                pass  