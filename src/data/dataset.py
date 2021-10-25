import torch
import torchaudio
import h5py
import numpy as np
from torch.utils.data import Dataset
from torch.utils import data
from src.utils import file_io_interface


# 데이터셋의 속도를 가속화 시킬 필요성이 있음 (필수) 어떻게 하면 빨리할 수 있을까 고민해보아야 할듯

class DirectWaveformDataset(Dataset):
    def __init__(self, directory_path, audio_window=20480):
        self.directory_path = directory_path
        self.audio_window = audio_window
        self.file_list = []
        id_data = open(self.directory_path, 'r')
        # strip() 함수를 사용해서 뒤에 개행을 제거
        self.file_list = [x.strip() for x in id_data.readlines()]
        id_data.close()

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, index):
        audio_file = self.file_list[index]
        audio_file = audio_file[4:]
        # torchaudio로 읽음
        waveform, sampling_rate = torchaudio.load("{}".format(audio_file), normalization=False)
        # sampling rate가 16000가 아니면 에러 메시지를 띄워줄 수 있도록 함
        assert (
            sampling_rate == 16000
        ), "sampling rate is not consistent throughout the dataset"
        audio_length = waveform.shape[1]

        random_index = np.random.randint(audio_length - self.audio_window + 1)
        return waveform[:, random_index:random_index + self.audio_window]


class WaveformDataset(Dataset):
    def __init__(self, hdf5_file, id_file, audio_window=20480):
        self.hdf5_file = h5py.File(hdf5_file, 'r')
        self.audio_window = audio_window
        self.audio_id_list = []

        id_data = open(id_file, 'r')
        # strip() 함수를 사용해서 뒤에 개행을 제거
        id_list = [x.strip() for x in id_data.readlines()]
        id_data.close()

        # We train on sampled audio windows of length 20480
        # 논문상 학습을 시킬때 20480 길이로 잘라서 학습을 진행하였다고 함. 그래서 음원의 길이가 20480보다 짧으면 리스트에서 없애버
        for data in id_list:
            temp = self.hdf5_file[data].shape[1]
            if temp > audio_window:
                self.audio_id_list.append(data)

    def __len__(self):
        return len(self.audio_id_list)

    def __getitem__(self, index):
        # We train on sampled audio windows of length 20480
        audio_id = self.audio_id_list[index]
        item = torch.tensor(self.hdf5_file[audio_id])
        audio_length = item.shape[1]
        random_index = np.random.randint(audio_length - self.audio_window + 1)
        return item[0, random_index:random_index + self.audio_window]


class SpeakerClassificationDataset(DirectWaveformDataset):
    def __init__(self, speaker_index_file, directory_path, audio_window=20480):
        super(DirectWaveformDataset, self).__init__()
        DirectWaveformDataset.__init__(self, directory_path=directory_path, audio_window=audio_window)
        self.speaker2index = {}
        speaker_data = open(speaker_index_file, 'r')
        speaker_list = [x.strip() for x in speaker_data]
        for i in speaker_list:
            self.speaker2index[i.split(' ')[0]] = int(i.split(' ')[1])

    def __getitem__(self, index):
        item = DirectWaveformDataset.__getitem__(self, index=index)
        audio_file = self.file_list[index]
        audio_file_name = file_io_interface.get_pure_filename(audio_file)
        label = torch.tensor(self.speaker2index[audio_file_name.split('-')[0]])
        return item, label


def get_dataloader(dataset, id_set, audio_window, batch_size, num_workers=8, shuffle=True, pin_memory=False):
    dataset = WaveformDataset(hdf5_file=dataset, id_file=id_set, audio_window=audio_window)
    # sampler = DistributedSampler(dataset)
    temp = data.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory,
        # sampler=sampler
    )
    return temp


def get_dataloader_type_direct(directory_path, audio_window, batch_size, num_workers, shuffle, pin_memory):
    dataset = DirectWaveformDataset(directory_path=directory_path, audio_window=audio_window)
    temp = data.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory
    )
    return temp


def get_dataloader_speaker_classification(directory_path, audio_window,
                                          batch_size, num_workers, shuffle, pin_memory, speaker_index_file):
    dataset = SpeakerClassificationDataset(speaker_index_file=speaker_index_file,
                                           directory_path=directory_path,
                                           audio_window=audio_window)
    temp = data.DataLoader(dataset=dataset,
                           batch_size=batch_size,
                           shuffle=shuffle,
                           num_workers=num_workers,
                           pin_memory=pin_memory
    )
    return temp


if __name__ == '__main__':
    # temp_id = open('../dataset/test-librispeech.txt', 'r')
    # sample = temp_id.readline().strip()
    # print(sample)
    # file = h5py.File('../dataset/test-librispeech.h5', 'r')
    # data = torch.tensor(file[sample])
    # print(len(data[0]))
    # print(len(data[0, 0:20480]))

    get_dataloader_speaker_classification(
        directory_path='../../dataset/test-list-librispeech.txt',
        audio_window=20480,
        batch_size=8,
        num_workers=8,
        shuffle=True,
        pin_memory=False,
        speaker_index_file='../../dataset/test-speaker-list-librispeech.txt'
    )



