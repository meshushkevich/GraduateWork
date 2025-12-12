import torch
from predictor.builtin.datastream.smart_homes_temp import SmartHomesTempDatastream
from predictor.models.builtin.dense_net import DenseNet
from predictor.models.builtin.linear_regression import LinearRegression

HORIZONT = 16
BATCH_SIZE = 32

dataset = SmartHomesTempDatastream(
    period_for_sample_ms=0, sensor_name="Indoor_temperature_room"
)
model = DenseNet(
    datastream=dataset,
    horizont=HORIZONT,
)
for _ in range(50000):
    batch_x, batch_y = dataset.get_batches(BATCH_SIZE, HORIZONT)
    batch_x = torch.tensor(batch_x)
    batch_y = torch.tensor(batch_y).view(-1, 1)
    model.online_fit(batch_x, batch_y)
