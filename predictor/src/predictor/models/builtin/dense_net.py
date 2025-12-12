import torch
from sensors.data import SensorData

from predictor.data.stream import DataStream
from predictor.logger import log_info
from predictor.models.base import BaseModel


class DenseNet(BaseModel):
    def __init__(self, datastream: DataStream, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = torch.nn.Sequential(
            torch.nn.Linear(
                in_features=self.horizont, out_features=self.horizont * 2, bias=True
            ),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=self.horizont * 2, out_features=1, bias=True),
        )
        self._stream = datastream
        self._criterion = torch.nn.MSELoss()
        self._optimizer = torch.optim.SGD(self._model.parameters(), lr=0.00001)

    def predict(self, data: torch.Tensor) -> torch.Tensor:
        return self._model(data)

    def online_fit(self, batch_x: torch.Tensor, batch_y: torch.Tensor):
        self._optimizer.zero_grad()
        y_pred = self.predict(batch_x)
        loss = self._criterion(y_pred, batch_y)
        loss.backward()
        self._optimizer.step()
        log_info("Updated model!")
        log_info(f"Loss: {loss.item()}")
