import io
import textwrap
import threading
from typing import Final, TypeAlias

import matplotlib
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

matplotlib.use('agg')

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


def wrap_text(text, width):
    return "\n".join(textwrap.wrap(text, width))


def make_remaining_diagram(df: pd.DataFrame) -> bytes:
    with threading.RLock():
        df['товар'] = df['товар'].apply(lambda x: wrap_text(x, 70))
        df.columns = df.columns.str.replace('_', ' ')

        fig, ax = plt.subplots(figsize=(15, 7))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

        # Настройка стиля таблицы
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(2, 2)
        table.auto_set_column_width(col=list(range(len(df.columns))))

        for (row, col), cell in table.get_celld().items():
            if (row == 0) or (col == -1):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))

        for cell in table._cells:
            if cell[0] == 0:
                table._cells[cell].set_fontsize(14)

        # Настройка размера ячеек
        for (i, j), cell in table.get_celld().items():
            cell.set_edgecolor('k')
            cell.set_linewidth(0.5)
            cell.set_height(0.2)

        plt.show()

        buffer = io.BytesIO()
        plt.savefig(buffer, **image_settings)
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()


def make_predict_end_diagram(df: pd.DataFrame) -> bytes:
    with threading.RLock():
        sns.set_theme(style="darkgrid")
        sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 2.})
        fig, ax = plt.subplots(figsize=(10, 1.5 * df['товар'].nunique()))
        sns.barplot(df, x="количество", y="товар", ax=ax, palette="magma")
        ax.yaxis.grid(True)  # Hide the horizontal gridlines
        ax.xaxis.grid(True)  # Show the vertical gridlines

        buffer = io.BytesIO()
        plt.savefig(buffer, **image_settings)
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()


def make_predict_buy_diagram(df: pd.DataFrame) -> bytes:
    with threading.RLock():
        sns.set_theme(style="darkgrid")
        sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 2.})
        fig, ax = plt.subplots(figsize=(15, 1.5 * df['товар'].nunique()))
        sns.barplot(df, x="количество", y="товар", hue='type', ax=ax, palette="magma")
        ax.yaxis.grid(True)  # Hide the horizontal gridlines
        ax.xaxis.grid(True)  # Show the vertical gridlines

        buffer = io.BytesIO()
        plt.savefig(buffer, **image_settings)
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()
