Description
-----------

Python package to read a CZI image containing a z-stack and extract all the slices in PNG format.


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

The output directory should not already exist, it will be created by the script.


Author
------

Copyright © 2023-Present Luis Carlos Garcia Peraza Herrera (luiscarlos.gph@gmail.com).


License
-------

This code repository is shared under an [MIT license](LICENSE).
