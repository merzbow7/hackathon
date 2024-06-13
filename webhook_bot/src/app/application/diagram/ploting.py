import io
import threading
from typing import Final, Any, TypeAlias

import pandas as pd
from matplotlib import pyplot as plt

SettingValue: TypeAlias = str | int | dict[str, int]
image_settings: Final[dict[str, SettingValue]] = {
    "format": 'jpg',
    "dpi": 300,
    "bbox_inches": 'tight',
    "pil_kwargs": {
        'quality': 20,
        'subsampling': 10
    }
}


def make_remaining_diagram(data: list[dict]) -> bytes:
    with threading.RLock():
        df = pd.DataFrame(data)
        plt.bar(df["name"], df["count"])
        plt.xlabel('Название')
        plt.ylabel('Количестов')
        plt.title('Остатки')
        plt.xticks(rotation=45, ha="right")

        buffer = io.BytesIO()
        plt.savefig(buffer, **image_settings)
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()


def make_predict_diagram(data: dict[str, dict]) -> bytes:
    with threading.RLock():
        df = pd.DataFrame(data)
        df.plot(kind='bar', figsize=(10, 7))
        plt.xlabel('Кварталы')
        plt.ylabel('Количество')
        plt.title('Столбчатая диаграмма по категориям и кварталам')
        plt.legend(title='Категории')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, **image_settings)
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()
