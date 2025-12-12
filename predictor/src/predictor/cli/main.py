#!/usr/bin/env python3

import click
import pytorch_lightning as pl

from predictor.models.builtin.lstm import LSTMModel
from predictor.models.builtin.tcn import TCNModel
from predictor.models.builtin.transformer import TransformerModelWrapper


@click.group()
def cli():
    """Predictive Maintenance Tool - CLI для прогнозирования отказа оборудования"""
    pass


@cli.command()
@click.option(
    "--dataset", type=str, default="Intel Lab", help="Тип датасета для обучения"
)
@click.option("--data-path", type=str, required=True, help="Путь к данным")
@click.option(
    "--model",
    type=click.Choice(["lstm", "tcn", "transformer"]),
    default="lstm",
    help="Тип модели для обучения",
)
@click.option(
    "--output-path", type=str, required=True, help="Путь для сохранения модели"
)
@click.option("--target", type=str, default=None, help="Целевая колонка")
@click.option(
    "--features",
    type=str,
    default=None,
    help="Список признаков через запятую (если None, использовать все)",
)
@click.option("--epochs", type=int, default=50, help="Количество эпох обучения")
@click.option("--batch-size", type=int, default=32, help="Размер batch")
@click.option(
    "--sequence-length",
    type=int,
    default=10,
    help="Длина последовательности для временных рядов",
)
@click.option(
    "--validation-split",
    type=float,
    default=0.2,
    help="Доля данных для валидации",
)
@click.option("--seed", type=int, default=42, help="Random seed")
def train(
    dataset,
    data_path,
    model,
    output_path,
    target,
    features,
    epochs,
    batch_size,
    sequence_length,
    validation_split,
    seed,
):
    """Обучение модели на данных"""
    pl.seed_everything(seed)

    # Создание и обучение модели
    click.echo(f"Создание модели {model}")

    # Здесь будет загружаться и обрабатываться датасет
    # Но для демонстрации, просто создадим модель

    if model == "lstm":
        model_instance = LSTMModel(
            epochs=epochs,
            batch_size=batch_size,
            sequence_length=sequence_length,
        )
    elif model == "tcn":
        model_instance = TCNModel(
            epochs=epochs,
            batch_size=batch_size,
            sequence_length=sequence_length,
        )
    elif model == "transformer":
        model_instance = TransformerModelWrapper(
            epochs=epochs,
            batch_size=batch_size,
            sequence_length=sequence_length,
        )

    click.echo("Модель успешно создана")
    click.echo(f"Для обучения нужен датасет: {dataset}")
    click.echo(f"Путь к данным: {data_path}")


if __name__ == "__main__":
    cli()
