# kvm-mergeide
kvm-mergeide.sh - Apply the mergeide.reg hack to kvm compatible windows images.

The mergeide fix relaxes the annoying windows requirements for same
hardware. This avoids 0x0000007B errors after you move system disks
to other hardware, e.g., from physical to virtual hardware.

This script applies the fix automatically.

More:
* http://support.microsoft.com/kb/314082

## Usage

    sudo ./mergeide.sh WINDOWS_IMAGE
