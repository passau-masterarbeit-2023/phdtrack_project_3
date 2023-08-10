# Server

### System info

```shell
(base) root@compute-container-rascoussie-65745f46f6-bvtsx:~/phdtrack/phdtrack_project_3# neofetch
            .-/+oossssoo+/-.               root@compute-container-rascoussie-65745f46f6-bvtsx 
        `:+ssssssssssssssssss+:`           -------------------------------------------------- 
      -+ssssssssssssssssssyyssss+-         OS: Ubuntu 20.04.6 LTS x86_64 
    .ossssssssssssssssssdMMMNysssso.       Host: AS -4124GS-TNR 0123456789 
   /ssssssssssshdmmNNmmyNMMMMhssssss/      Kernel: 5.4.0-153-generic 
  +ssssssssshmydMMMMMMMNddddyssssssss+     Uptime: 36 days, 23 hours, 43 mins 
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/    Packages: 487 (dpkg) 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Shell: bash 5.0.17 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Resolution: 1024x768 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   Terminal: /dev/pts/0 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   CPU: AMD EPYC 7662 (256) @ 2.000GHz 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Memory: 61487MiB / 515845MiB 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.
 /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/                  
  +sssssssssdmydMMMMMMMMddddyssssssss+                   
   /ssssssssssshdmNNNNmyNMMMMhssssss/
    .ossssssssssssssssssdMMMNysssso.
      -+sssssssssssssssssyyyssss+-
        `:+ssssssssssssssssss+:`
            .-/+oossssoo+/-.

```

**GPU:** NVIDIA RTX A6000

**CUDA:** NVIDIA-SMI 470.161.03   Driver Version: 470.161.03   CUDA Version: 11.4

**RAM:** 503Gi

## Conda

I had to update (here, remove and install) `conda` to latest version.

Before creating the conda environment, need to install some packages using `apt-get`: `apt-get install graphviz graphviz-dev`

Create conda env using: `conda env create -f environment.yml`
