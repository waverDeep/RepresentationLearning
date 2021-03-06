import torchaudio
from torch.utils import data
import src.data.dataset_librispeech as dataset_librispeech
import src.data.dataset_byol_audio as dataset_byol_audio
import src.data.dataset_voxceleb as dataset_voxceleb
import src.data.dataset_baseline as dataset_baseline
import src.data.dataset_urbansound8k as dataset_urbansound8k
import src.data.dataset_speech_command as dataset_speech_command
import src.data.dataset_byol_light as dataset_byol_light
torchaudio.set_audio_backend("sox_io")


def get_dataloader(config, mode='train'):
    dataset_type = config['dataset_type']
    waveform_dataset = None



    if dataset_type == 'BYOLAudioDataset':
        dataset = dataset_byol_audio.BYOLAudioDataset(
            directory_path=config['{}_dataset'.format(mode)],
            audio_window=config['audio_window'],
            full_audio=config['full_audio'],
            use_librosa=config['use_librosa'],
            config=config,
            mode=mode
        )

        dataloader = data.DataLoader(
            dataset=dataset,
            batch_size=config['batch_size'],
            shuffle=config['dataset_shuffle'],
            num_workers=config['num_workers'],
            pin_memory=config['pin_memory'],
        )

        return dataloader, dataset

    if dataset_type == 'WaveBYOLDataset':
        waveform_dataset = dataset_byol_light.WaveformDatasetByWaveBYOL(
            file_path=config['{}_dataset'.format(mode)],
            audio_window=config['audio_window'],
            sampling_rate=config['sampling_rate'],
            augmentation=config['{}_augmentation'.format(mode)]
        )

        dataloader = data.DataLoader(
            dataset=waveform_dataset,
            batch_size=config['batch_size'],
            shuffle=config['dataset_shuffle'],
            num_workers=config['num_workers'],
            pin_memory=config['pin_memory'],
        )

        return dataloader, waveform_dataset


    if dataset_type == 'BaselineWaveformDataset':
        waveform_dataset = dataset_baseline.BaselineWaveformDataset
    elif dataset_type == 'BaselineWaveformDatasetByBYOL':
        waveform_dataset = dataset_baseline.BaselineWaveformDatasetByBYOL
    elif dataset_type == 'LibriSpeechWaveformDataset':
        waveform_dataset = dataset_librispeech.LibriSpeechWaveformDataset
    elif dataset_type == 'LibriSpeechWaveformDatasetByBYOL':
        waveform_dataset = dataset_librispeech.LibriSpeechWaveformDatasetByBYOL
    elif dataset_type == 'VoxCelebWaveformDataset':
        waveform_dataset = dataset_voxceleb.VoxCelebWaveformDataset
    elif dataset_type == 'UrbanSound8KWaveformDataset':
        waveform_dataset = dataset_urbansound8k.UrbanSound8KWaveformDataset
    elif dataset_type == 'SpeechCommandWaveformDataset':
        waveform_dataset = dataset_speech_command.SpeechCommandWaveformDataset

    dataset = waveform_dataset(
        file_path=config['{}_dataset'.format(mode)],
        audio_window=config['audio_window'],
        sample_rate=config['sampling_rate'],
        full_audio=config['full_audio'],
        augmentation=config['{}_augmentation'.format(mode)]
    )

    dataloader = data.DataLoader(
        dataset=dataset,
        batch_size=config['batch_size'],
        shuffle=config['dataset_shuffle'],
        num_workers=config['num_workers'],
        pin_memory=config['pin_memory'],
    )

    return dataloader, dataset


if __name__ == '__main__':
    config = {
        "audio_window": 20480,
        "batch_size": 1,
        # dataset
        "dataset_type": "VoxCelebWaveformDataset",
        "train_dataset": "../../dataset/voxceleb01-train.txt",
        "test_dataset": "../../dataset/voxceleb01-train.txt",
        "num_workers": 16,
        "dataset_shuffle": True,
        "pin_memory": True,
    }
    train_loader, train_dataset = get_dataloader(config=config, mode='train')
    for data in train_loader:
        _waveform, _out_filename, _speaker_id = data
        break


