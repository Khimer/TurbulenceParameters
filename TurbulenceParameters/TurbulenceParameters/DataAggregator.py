import numpy as np


class DataAggregator:
    def __init__(self):
        self.amountAggregatedData = 100

    def aggregate(self, data):
        num_raw = len(data[0])
        len_aggregated_data = num_raw - num_raw % self.amountAggregatedData
        aggregated_data = np.zeros([7, len_aggregated_data//self.amountAggregatedData])
        for quantity in range(7):
            aggregated_data[quantity] =\
                data[quantity][:len_aggregated_data].reshape(-1, self.amountAggregatedData).mean(axis=-1)
        return aggregated_data
