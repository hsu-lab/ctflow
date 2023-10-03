import ctflow.run_inference as ct_infer


if __name__ == '__main__':
    path_to_test_data = '/data/example_LIDC-IDRI'
    ct_infer.execute(path_to_test_data, data_ext='dcm', tau=0.8, conf='medium/25', use_gpu=[], out_to='lidcOut')