import torch
import torch.nn as nn
from models2D.utils import _inconv, _down, _outconv, _up


class UNet(nn.Module):
    r""" Simple UNet architecture from https://github.com/milesial/Pytorch-UNet"""

    def __init__(self, n_channels: int = 1, n_classes: int = 3, activation: bool = False):
        super(UNet, self).__init__()
        self.inc = _inconv(n_channels, 64, False)
        self.down1 = _down(64, 128, False)
        self.down2 = _down(128, 256, False)
        self.down3 = _down(256, 512, False)
        self.down4 = _down(512, 512, False)
        self.up1 = _up(1024, 256, False)
        self.up2 = _up(512, 128, False)
        self.up3 = _up(256, 64, False)
        self.up4 = _up(128, 64, False)
        self.outc = _outconv(64, n_classes)
        self.activation = activation

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.outc(x)
        if self.activation:
            x = torch.sigmoid(x)
        return x
