Description
-----------

Python package to read a CZI image containing a z-stack and extract all the slices in PNG format.

Besides extracting the confocal microscopy slices, this code comes with 
additional feaures listed below.

Features:
   * Maximum intensity projection of the z-stack (saved with the suffix `_mip.png` in the output folder).
   * Average intentity projection of the z-stack (saved with the suffix `_aip.png` in the output folder).


Install
-------

```bash
$ python setup.py install --user
```


Run
---

```bash
$ python -m czi_extractor.run --input <path_to_your_czi_image> --output <path_to_output_directory>
```

The output directory will be created by the script (i.e. the output directory should not already exist).


Author
------

Copyright © 2023-Present Luis Carlos Garcia Peraza Herrera (luiscarlos.gph@gmail.com).


License
-------

This code repository is shared under an [MIT license](LICENSE).
