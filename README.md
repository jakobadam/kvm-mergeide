# mergeide
kvm-mergeide.sh - Apply the mergeide.reg hack to kvm compatible windows images.

The fix relaxes the annoying windows requirements for same
hardware. This avoids 0x0000007B errors after you move system disks
to other hardware, e.g., from physical to virtual hardware.

More:
* http://support.microsoft.com/kb/314082

## Install dependencies

   sudo apt-get install libguestfs-tools

## Usage

    sudo ./mergeide.sh WINDOWS_IMAGE
