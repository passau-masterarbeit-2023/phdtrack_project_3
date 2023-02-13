# phdtrack_project_3

A repo following the advancement of PhDTrack Project.

## Organisations

[SmartVMI.org](http://www.smartvmi.org/)

## repos

[Smart-and-Naive-SSH-Key-Extraction](https://github.com/smartvmi/Smart-and-Naive-SSH-Key-Extraction): code for bruteforce algorithms to extract SSH keys from OpenSSH.

[SSHKex](https://github.com/smartvmi/SSHKex): code for OpenSSH memory and internet traffic captation.

[smartvmi](https://github.com/smartvmi/smartvmi): Organisation GitHub repo

## datasets

[Zenodo dataset](https://zenodo.org/record/6537904): Data are dowloaded from [Zenodo](https://zenodo.org/record/6537904) inside the folder `../phdtrack_data` .

## Env

`conda env export --no-builds > environment.yml` : export conda env to yml file.

## Notes

PCAP file ? https://wiki.wireshark.org/Development/LibpcapFileFormat

### Get key in heap dump raw file from json data

To get a key in a given heap dump raw file, we can use its associated .json file. Each given key comes with its address as an hex number. However, the raw heap dump lines of hex memory starts at address 0x0, whereas the address in the json are given relative to the real memory address in the sampled data. As the address of the start of the head dump file (0x0) is given from real memory (`"HEAP_START": "55a6d2356000"`), we can compute the address given relative to the raw file (given_json_key_addr - HEAP_START).

Example: *302-1644391327.json*

```
{
    "KEY_A_ADDR": "55a6d236ba10", 
    "KEY_A_LEN": "16", 
    "KEY_A_REAL_LEN": "16", 
    "KEY_A": "8d08ff65b3bfcd8b91ca995ad5b764af",
    "HEAP_START": "55a6d2356000"
}
```

computation: addr in file = 55a6d236ba10 - 55a6d2356000 = **15A10**

Searching for **15A10** in vim: `/15a10`: Open vim with `vim 302-1644391327-heap.raw`, parse the raw bytes with `xxd` usinf vim command `:%!xxd`, and the search for pattern with `/pattern`, here `/15a10`.

> tips: to ease the search for patterns in vim, remove the whitespaces created by `xxd` with the vim command: `:%s/\s\+//g`

> WARNING: `xxd` addresses are presented as addresses of the first byte of a given line ! So addresses are incremented from one line to another by leaps of 16. This is coherent with the storing of addresses in memory (json file addresses).

![search in vim for address A](img/vim/2023-01-15_09-04-16.png)

#### search for pointers

Using vim regex, run `:%!xxd`, then `:%s/\s\+//g`, then search for pointers with: `:/[0-9a-f]\{12}0\{4}`.

> WARN: The pointers in the raw heap dump files are coded using LITTLE-ENDIANNESS. They are coded as 8 byte-aligned memory blocks.

#### Search for datastructures

Data structures starts with the number of bytes allocated (in heap).

Search for memalloc headers `:/[0-9a-f]\{4}0\{12}`.

![search for data structure](./img/vim/discovering_data_structure.png)

Here you can see a 4x16 char blocks which represents a data structure of 32 bytes ((4x16)x4)/8. The value `2100000000000000` is the malloc header in little endian format which represents 33. It is probably the number of bytes to leap through to avoid this data strucure.

#### Organisation of memory in heap dump files

##### start of file

As we can see, raw heap dump files all starts with a null block (blocks are of size 8 bytes (16 chars "0" using `vim`)). Then we call always see a malloc header of size `5102` (little-endian, equivalent to 593). This is probably the master data structure being allocated. 

##### max memalloc size

Long story short, there is probably no max size. More info [here](https://stackoverflow.com/a/57687432/10798114). On my PC, we got:

```shell
(base) onyr@aezyr:~$ sudo cat /proc/sys/vm/overcommit_memory 
[sudo] password for onyr: 
0

```

Meaning there is no limit to memalloc.
