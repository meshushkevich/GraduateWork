import torch
from sensors.data import SensorData

from predictor.data.stream import DataStream
from predictor.logger import log_info
from predictor.models.base import BaseModel


class LinearRegression(BaseModel):
    def __init__(self, datastream: DataStream, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = torch.nn.Linear(
            in_features=self.horizont, out_features=1, bias=True
        )
        self._stream = datastream
        self._criterion = torch.nn.L1Loss()
        self._optimizer = torch.optim.SGD(self._model.parameters(), lr=0.00001)

    def predict(self, data: list[SensorData]) -> torch.Tensor:
        values = [d.value for d in data]
        values = torch.tensor(values, dtype=torch.float32)
        return self._model(values)

    def online_fit(self):
        if batch := self._stream.get_batch(batch_size=self.horizont + 1):
            log_info("Loaded batch!")
        else:
            log_info("No batch available!")
            return

        self._optimizer.zero_grad()
        y_pred = self.predict(batch[:-1])
        y_true = torch.tensor([batch[-1].value], dtype=torch.float32)
        loss = self._criterion(y_pred, y_true)
        loss.backward()
        self._optimizer.step()
        log_info("Updated model!")
        log_info(f"Loss: {loss.item()}")
