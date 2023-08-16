# CUDA

## Installing

Follow the instructions [here | Fedora](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#fedora). Video [here](https://youtu.be/lN2q-KIbYE4).

```shell
 ❮onyr ★ kenzael❯ ❮client❯❯ hostnamectl | grep "System"
Operating System: Fedora Linux 37 (Workstation Edition)
```

First, you need to identify if everything is compatible. Check for GPUs with `lspci | grep VGA`

```shell
 ❮onyr ★ kenzael❯ ❮~❯❯ lspci | grep VGA
00:02.0 VGA compatible controller: Intel Corporation Alder Lake-P Integrated Graphics Controller (rev 0c)
01:00.0 VGA compatible controller: NVIDIA Corporation GA104 [Geforce RTX 3070 Ti Laptop GPU] (rev a1)
```

0. If kernel headers are available for you current kernel, install them with recommended command ` sudo dnf install kernel-devel-$(uname -r) kernel-headers-$(uname -r)`. If there is nothing, then install the latest available kernel headers with  `sudo dnf install gcc kernel-devel kernel-headers`. This will require you to update you kernel to match the latest version.

Notes for myself: Since I have a multi-partition system, I needed first to install the latest Fedora kernel with `sudo dnf update kernel`. Then, I needed to update EFI for Fedora with `sudo grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg` or GRUB with `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`. (I choose EFI, but I leave the other command there just in case...). Then I had to reboot to TUXEDO (Ubuntu) OS, since the main GRUB is there (first installed OS). You can edit the GRUB config file with `sudo nano /etc/default/grub`, and then update GRUB `sudo update-grub`. It should be written that Fedora is detected as a foreign OS during the process.

1. First, check that kernel matched the kernel-headers correctly, after previous step.

```shell
 ❮onyr ★ kenzael❯ ❮~❯❯ uname -r
6.4.8-100.fc37.x86_64
 ❮onyr ★ kenzael❯ ❮~❯❯ rpm -q kernel-devel
kernel-devel-6.4.8-100.fc37.x86_64
```

## Uninstall NVIDIA toolkit

> **WARN:** Be sure that no important package is going to be remove. Check what packages are removed before applying changes.

```
sudo dnf remove "cuda*" "*cublas*" "*cufft*" "*cufile*" "*curand*" \
 "*cusolver*" "*cusparse*" "*gds-tools*" "*npp*" "*nvjpeg*" "nsight*" "*nvvm*"
```

```shell
Removing:
 cuda                            x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-12-2                       x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-cccl-12-2                  x86_64 12.2.128-1            @cuda-fedora37-x86_64  13 M
 cuda-command-line-tools-12-2    x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-compiler-12-2              x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-crt-12-2                   x86_64 12.2.128-1            @cuda-fedora37-x86_64 998 k
 cuda-cudart-12-2                x86_64 12.2.128-1            @cuda-fedora37-x86_64 727 k
 cuda-cudart-devel-12-2          x86_64 12.2.128-1            @cuda-fedora37-x86_64 6.4 M
 cuda-cuobjdump-12-2             x86_64 12.2.128-1            @cuda-fedora37-x86_64 576 k
 cuda-cupti-12-2                 x86_64 12.2.131-1            @cuda-fedora37-x86_64 107 M
 cuda-cuxxfilt-12-2              x86_64 12.2.128-1            @cuda-fedora37-x86_64 1.0 M
 cuda-demo-suite-12-2            x86_64 12.2.128-1            @cuda-fedora37-x86_64  12 M
 cuda-documentation-12-2         x86_64 12.2.128-1            @cuda-fedora37-x86_64 520 k
 cuda-driver-devel-12-2          x86_64 12.2.128-1            @cuda-fedora37-x86_64 125 k
 cuda-drivers                    x86_64 535.86.10-1           @cuda-fedora37-x86_64   0  
 cuda-gdb-12-2                   x86_64 12.2.128-1            @cuda-fedora37-x86_64  16 M
 cuda-libraries-12-2             x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-libraries-devel-12-2       x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-nsight-12-2                x86_64 12.2.128-1            @cuda-fedora37-x86_64 113 M
 cuda-nsight-compute-12-2        x86_64 12.2.1-1              @cuda-fedora37-x86_64 7.3 k
 cuda-nsight-systems-12-2        x86_64 12.2.1-1              @cuda-fedora37-x86_64 1.9 k
 cuda-nvcc-12-2                  x86_64 12.2.128-1            @cuda-fedora37-x86_64 182 M
 cuda-nvdisasm-12-2              x86_64 12.2.128-1            @cuda-fedora37-x86_64  48 M
 cuda-nvml-devel-12-2            x86_64 12.2.128-1            @cuda-fedora37-x86_64 655 k
 cuda-nvprof-12-2                x86_64 12.2.131-1            @cuda-fedora37-x86_64  11 M
 cuda-nvprune-12-2               x86_64 12.2.128-1            @cuda-fedora37-x86_64 167 k
 cuda-nvrtc-12-2                 x86_64 12.2.128-1            @cuda-fedora37-x86_64  58 M
 cuda-nvrtc-devel-12-2           x86_64 12.2.128-1            @cuda-fedora37-x86_64  73 M
 cuda-nvtx-12-2                  x86_64 12.2.128-1            @cuda-fedora37-x86_64 405 k
 cuda-nvvm-12-2                  x86_64 12.2.128-1            @cuda-fedora37-x86_64  63 M
 cuda-nvvp-12-2                  x86_64 12.2.131-1            @cuda-fedora37-x86_64 128 M
 cuda-opencl-12-2                x86_64 12.2.128-1            @cuda-fedora37-x86_64  90 k
 cuda-opencl-devel-12-2          x86_64 12.2.128-1            @cuda-fedora37-x86_64 573 k
 cuda-profiler-api-12-2          x86_64 12.2.128-1            @cuda-fedora37-x86_64  71 k
 cuda-runtime-12-2               x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-sanitizer-12-2             x86_64 12.2.128-1            @cuda-fedora37-x86_64  36 M
 cuda-toolkit-12-2               x86_64 12.2.1-1              @cuda-fedora37-x86_64 3.0 k
 cuda-toolkit-12-2-config-common noarch 12.2.128-1            @cuda-fedora37-x86_64   0  
 cuda-toolkit-12-config-common   noarch 12.2.128-1            @cuda-fedora37-x86_64  44  
 cuda-toolkit-config-common      noarch 12.2.128-1            @cuda-fedora37-x86_64  41  
 cuda-tools-12-2                 x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 cuda-visual-tools-12-2          x86_64 12.2.1-1              @cuda-fedora37-x86_64   0  
 gds-tools-12-2                  x86_64 1.7.1.12-1            @cuda-fedora37-x86_64  60 M
 libcublas-12-2                  x86_64 12.2.4.5-1            @cuda-fedora37-x86_64 596 M
 libcublas-devel-12-2            x86_64 12.2.4.5-1            @cuda-fedora37-x86_64 885 M
 libcufft-12-2                   x86_64 11.0.8.91-1           @cuda-fedora37-x86_64 172 M
 libcufft-devel-12-2             x86_64 11.0.8.91-1           @cuda-fedora37-x86_64 378 M
 libcufile-12-2                  x86_64 1.7.1.12-1            @cuda-fedora37-x86_64 3.1 M
 libcufile-devel-12-2            x86_64 1.7.1.12-1            @cuda-fedora37-x86_64  26 M
 libcurand-12-2                  x86_64 10.3.3.129-1          @cuda-fedora37-x86_64  92 M
 libcurand-devel-12-2            x86_64 10.3.3.129-1          @cuda-fedora37-x86_64  95 M
 libcusolver-12-2                x86_64 11.5.1.129-1          @cuda-fedora37-x86_64 189 M
 libcusolver-devel-12-2          x86_64 11.5.1.129-1          @cuda-fedora37-x86_64 146 M
 libcusparse-12-2                x86_64 12.1.2.129-1          @cuda-fedora37-x86_64 252 M
 libcusparse-devel-12-2          x86_64 12.1.2.129-1          @cuda-fedora37-x86_64 539 M
 libnpp-12-2                     x86_64 12.2.0.5-1            @cuda-fedora37-x86_64 234 M
 libnpp-devel-12-2               x86_64 12.2.0.5-1            @cuda-fedora37-x86_64 244 M
 libnvjpeg-12-2                  x86_64 12.2.1.2-1            @cuda-fedora37-x86_64 6.4 M
 libnvjpeg-devel-12-2            x86_64 12.2.1.2-1            @cuda-fedora37-x86_64 6.7 M
 nsight-compute-2023.2.1         x86_64 2023.2.1.3-1          @cuda-fedora37-x86_64 1.4 G
 nsight-systems-2023.2.3         x86_64 2023.2.3.1001_32894139v0-0
                                                              @cuda-fedora37-x86_64 742 M
Removing unused dependencies:
 libnvjitlink-12-2               x86_64 12.2.128-1            @cuda-fedora37-x86_64  47 M
 libnvjitlink-devel-12-2         x86_64 12.2.128-1            @cuda-fedora37-x86_64  60 M
 nvidia-driver-cuda              x86_64 3:535.86.10-1.fc37    @cuda-fedora37-x86_64 1.5 M
 nvidia-persistenced             x86_64 3:535.86.10-1.fc37    @cuda-fedora37-x86_64  73 k
 opencl-filesystem               noarch 1.0-16.fc37           @fedora                 0  

```

```
sudo dnf module remove --all nvidia-driver
```

```shell
Removing:
 kmod-nvidia-latest-dkms     x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64    70 M
 nvidia-driver               x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   207 M
 nvidia-driver-NVML          x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   1.7 M
 nvidia-driver-NvFBCOpenGL   x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   131 k
 nvidia-driver-cuda-libs     x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   175 M
 nvidia-driver-devel         x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   193  
 nvidia-driver-libs          x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   433 M
 nvidia-kmod-common          noarch   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   2.7 k
 nvidia-libXNVCtrl           x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64    59 k
 nvidia-libXNVCtrl-devel     x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   254 k
 nvidia-modprobe             x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64    64 k
 nvidia-settings             x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   2.1 M
 nvidia-xconfig              x86_64   3:535.86.10-1.fc37    @cuda-fedora37-x86_64   271 k
Removing unused dependencies:
 dkms                        noarch   3.0.11-1.fc37         @updates                192 k
 egl-wayland                 x86_64   1.1.12-2.fc37         @updates                 79 k
 kernel-devel-matched        x86_64   6.4.8-100.fc37        @updates                  0  
 openssl                     x86_64   1:3.0.9-1.fc37        @updates                1.8 M
Disabling module profiles:
 nvidia-driver/default 
```

```
sudo dnf module reset nvidia-driver
```
