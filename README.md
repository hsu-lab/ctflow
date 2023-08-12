# CTFlow
#### Official CTFlow Repository: Using Normalizing Flow for CT Harmonization <br><br>

The repository contains a conditional normalizing flow approach to harmonize CT scans that are acquired and reconstructed with different CT parameters (i.e., Kernel, Dose etc.) to a reference reconstruction. The novelty of this work inclues:
* A novel autoencoding technique to manipulate the latent space that results in better generalization on external datasets.
* It allows for the measurement of uncertainty using diverse output images that are obtained
by sampling the latent space.

#### Invertible Flow Operation
![Flow Operation](./readme_utils/CTFlow.gif?raw=true "Title")

# Getting Started

### Setup Data

Current implementation expects input data to be in either [NRRD](https://pynrrd.readthedocs.io/en/stable/), [DICOM](https://pydicom.github.io/pydicom/stable/tutorials/installation.html) or [NIfTI](https://nipy.org/nibabel/). Please format the test data to follow a directory structue as shown below.
> If the data type is other than `DICOM`, the model assumes that the voxels are in Hounsfield Units (HU). Please ensure that the `NRRD` or `NIfTI` data has been preprocessed to be in HU
```
├── Nrrd_Data
│   ├── case_1.nrrd
│   ├── case_2.nrrd   
│   ├── ...
│  
├── Nifti_Data
│   ├── case_1.nii.gz
│   ├── case_2.nii.gz
│   ├── ...
│
├── Dicom_Data
│   ├── case_1
│   │   ├── dicom_0.dcm
│   │   ├── dicom_1.dcm
│   │   ├── dicom_2.dcm
│   │   ├── ...
│   ├── case_2
│   │   ├── dicom_0.dcm
│   │   ├── dicom_1.dcm
│   │   ├── dicom_2.dcm
│   │   ├── ...
│   ├── ...
```

###  Setup Environment

The application is containerized within a docker image (```ayadav01/mii-nvidia_flow:1.1```) available via docker hub.

* Pull the docker container

```docker
docker pull ayadav01/mii-nvidia_flow:1.1
```

### Download ```main.py```

Only download the ```main.py``` file from this repository. Change the required arguments as explained below.

```python 
import ctflow.run_inference as ct_infer


if __name__ == '__main__':
    path_to_test_data = '/path_to_test_set'
    ct_infer.execute(path_to_test_data, data_ext='data_format_of_test_set', tau=0.8, conf='mapping_conditoin', use_gpu=[], out_to='path_to_save_results')
```
* *path_to_test_data* = Proivde path to where all the test cases are.
> Make sure the path provided here is the mounted data path in docker. Explained in step 3 below. 
* *data_ext* = Provide the data type. Use `'nrrd'`, `'dcm'` or `'nii'` for this argument.
* *tau* = Temperature parameter. Varying this will change the output texture of the image. We found `0.8` to be the optimal setting.
* *conf* = The mapping weights to use for inference. We trained several CT mapping. Use one of the following:
  * `'smooth/10'`
  * `'smooth/25'`
  * `'medium/10'`
  * `'medium/25'`
  * `'sharp/10'`
  * `'sharp/25'`
* *use_gpu* = provide a gpu id inside the list if available. If left empty, inference will occur on cpu.
* *out_to* = Provide path to where the harmonized CT should be saved. Default path is `'./results'`.

### Usage (Run Docker)

Run docker container. We mount two directores inside the container:
* Mount the `main.py` file directory.
* Mount the test data directory.
```docker
docker run --name <name_of_container> --shm-size=<memory_size> -it --rm -v <path_to_main.py_directory>:/workspace/ctflow_test  -v <path_to_test_data>:/data -v /etc/localtime:/etc/localtime:ro ayadav01/mii-nvidia_flow:1.1
```
* *name_of_container* = Provide any name for the container.
* *memory_size* = Shared memory size. Use `2g` or `4g` or `6g` here, depending on available memory. 
* *path_to_main.py_directory* = Provide the path to where the `main.py` file is. This will be the working dirctory inside docker container.
* *path_to_test_data* = Provide path to where the test cases are.
> In the `main.py` file, provide the mounted data path (`'/data'`)

### Run `main.py`

Within docker container, navigate to where the `main.py` file is.
```bash
cd /workspace/ctflow_test
python main.py
```
<br><br>

# Why Normalizing Flow ?

Please read this quick introduction to Normalizing Flow by the authors of the SRFlow paper [[Blog]](https://bit.ly/320bAkH).


### SRFlow Paper
[[Paper] ECCV 2020 Spotlight](https://bit.ly/2XcmSks)

```bibtex
@inproceedings{lugmayr2020srflow,
  title={SRFlow: Learning the Super-Resolution Space with Normalizing Flow},
  author={Lugmayr, Andreas and Danelljan, Martin and Van Gool, Luc and Timofte, Radu},
  booktitle={ECCV},
  year={2020}
}
```
[![SRFlow](https://user-images.githubusercontent.com/11280511/98149322-7ed5c580-1ecd-11eb-8279-f02de9f0df12.gif)](https://bit.ly/3jWFRcr)

- **Sampling:** SRFlow outputs many different images for a single input.
- **Stable Training:** SRFlow has much fewer hyperparameters than GAN approaches, and we did not encounter training stability issues.
- **Convergence:** While GANs cannot converge, conditional Normalizing Flows converge monotonic and stable.
- **Higher Consistency:** When downsampling the super-resolution, one obtains almost the exact input.

<br><br>
