import json

configuration = {
    # definition
    "use_cuda": True,
    "audio_window": 32000, # 20480 # 15200
    "sampling_rate": 16000,
    "epoch": 500,
    "batch_size": 16,
    "learning_rate": 0.00005,

    # dataset
    "dataset_type": "BaselineWaveformDatasetByBYOL",
    "dataset_name": "FSD50K",
    "train_dataset": "./dataset/FSD50K-train.txt",
    "test_dataset": "./dataset/FSD50K-test.txt",
    "train_augmentation": True,
    "test_augmentation": False,
    "full_audio": False,
    "use_librosa": True,

    # dataloader
    "num_workers": 16,
    "dataset_shuffle": True,
    "pin_memory": False,

    # model
    "pretext_model_name": "WaveBYOLEfficientB4Mix",
    "pre_input_dims": 1,
    "pre_hidden_dims": 512,
    "pre_filter_sizes": [10, 8, 4, 4, 4],
    "pre_strides": [5, 4, 2, 2, 2],
    "pre_paddings": [2, 2, 2, 2, 1],
    "dimension": 16384, # 15200: 86016 # 20480: 114688
    "hidden_size": 2048, # 512 # 2048
    "projection_size": 4096,
    "ema_decay": 0.9,
    # optimizer
    "optimizer_name": "AdamP",
    # checkpoint
    "checkpoint_save_directory_path": "./checkpoint",
}


if __name__ == '__main__':
    name = "pretext-{}-{}-{}-{}".format(
        configuration['pretext_model_name'],
        configuration['dataset_name'],
        configuration['audio_window'],
        configuration['hidden_size']
    )

    configuration["log_filename"] = "./log/{}".format(name)
    configuration["tensorboard_writer_name"] = "./runs/{}".format(name)
    configuration["checkpoint_file_name"] = "{}".format(name)

    filename = 'config-{}.json'.format(name)
    with open('./{}'.format(filename), 'w', encoding='utf-8') as config_file:
        json.dump(configuration, config_file, indent='\t')
