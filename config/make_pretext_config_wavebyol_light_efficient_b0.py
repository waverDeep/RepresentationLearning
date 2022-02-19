import json

configuration = {
    # definition
    "use_cuda": True,
    "audio_window": 20480,
    "sampling_rate": 16000,
    "epoch": 500,
    "batch_size": 48,
    "learning_rate": 0.0003,

    # dataset
    "dataset_type": "WaveBYOLDataset",
    "dataset_name": "FSD50K",
    "train_dataset": "./dataset/FSD50K.dev_audio_16k.txt",
    "test_dataset": "./dataset/FSD50K.eval_audio_16k.txt",
    "train_augmentation": [2, 3, 5, 6],
    "test_augmentation": [],

    # dataloader
    "num_workers": 16,
    "dataset_shuffle": True,
    "pin_memory": False,

    # model
    "pretext_model_name": "WaveBYOLLightEfficientB0",
    "encoder_input_dim": 1,
    "encoder_hidden_dim": 512,
    "encoder_filter_size": [10, 8, 4, 4],
    "encoder_stride": [5, 4, 2, 2],
    "encoder_padding": [2, 2, 2, 1],
    "efficientnet_version": "nob0",
    "mlp_input_dim": 1280,
    "mlp_hidden_dim": 4096,
    "mlp_output_dim": 4096,
    "ema_decay": 0.99,
    # optimizer
    "optimizer_name": "Adam", # Adam # AdamP
    # checkpoint
    "checkpoint_save_directory_path": "./checkpoint",
    "checkpoint":"./checkpoint/pretext-WaveBYOLLightEfficientB0-FSD50K-20480/pretext-WaveBYOLLightEfficientB0-FSD50K-20480-model-best-2022_2_15_13_9_9-epoch-98.pt",
}


if __name__ == '__main__':
    name = "pretext-{}-{}-{}".format(
        configuration['pretext_model_name'],
        configuration['dataset_name'],
        configuration['audio_window']
    )

    configuration["log_filename"] = "./log/{}".format(name)
    configuration["tensorboard_writer_name"] = "./runs/{}".format(name)
    configuration["checkpoint_file_name"] = "{}".format(name)

    filename = 'config-{}.json'.format(name)
    with open('./{}'.format(filename), 'w', encoding='utf-8') as config_file:
        json.dump(configuration, config_file, indent='\t')