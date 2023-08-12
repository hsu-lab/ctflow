import ctflow.run_inference as ct_infer


if __name__ == '__main__':
    path_to_test_data = '/path_to_test_set'
    ct_infer.execute(path_to_test_data, data_ext='data_type_of_test_set', tau=0.8, conf='mapping_conditoin', use_gpu=[], out_to='path_to_save_results')