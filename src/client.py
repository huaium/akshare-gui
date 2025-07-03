import time
from concurrent.futures import ALL_COMPLETED, wait
from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np
import pandas as pd
from requests.exceptions import RequestException
from urllib3.exceptions import HTTPError

from . import repository
from .enums import ApiItem, SideItem
from .utils import thread_utils
from .widgets import TextOutput


class Client:
    @dataclass
    class StockInfo:
        code: str
        date: str

    def __init__(self, side_item: SideItem, text_output: TextOutput | None = None):
        self._side_item = side_item
        self._text_output: TextOutput | None = text_output
        self._running: bool = False

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value: bool):
        self._running = value

    @property
    def text_output(self):
        if not self._text_output:
            raise ValueError("text_output not initialized")
        return self._text_output

    @text_output.setter
    def text_output(self, value: TextOutput):
        if self._text_output:
            raise ValueError("text_output already initialized")
        self._text_output = value

    def _send_message(
        self,
        message: str,
        exception: Exception | None = None,
        end: str = "\n",
        color: Literal["red"] | None = None,
    ):
        if not self.text_output:
            return

        self.text_output.send_message(
            message, exception=exception, end=end, color=color
        )

    def _read_to_info(self, df: pd.DataFrame) -> Sequence[StockInfo]:
        match self._side_item:
            case SideItem.FUND_HK_HIST:  # format: 0000000000
                return [
                    self.StockInfo(
                        str(getattr(row, "代码文本")).zfill(10),
                        str(getattr(row, "日期文本")),
                    )
                    for row in df.itertuples(index=False)
                ]
            case SideItem.BOND_HS_HIST:  # format: sh000000 / sz000000
                return [
                    self.StockInfo(
                        str(getattr(row, "代码文本")), str(getattr(row, "日期文本"))
                    )
                    for row in df.itertuples(index=False)
                ]

        return [
            self.StockInfo(
                str(getattr(row, "代码文本")).zfill(6), str(getattr(row, "日期文本"))
            )
            for row in df.itertuples(index=False)
        ]

    def _fetch_retry_with_info(
        self,
        stock_info: StockInfo,
        timeout=5,
        max_retries=3,
    ):
        retries = 0

        while retries < max_retries:
            try:
                df = repository.from_side_item(
                    side_item=self._side_item,
                    code=stock_info.code,
                    date=stock_info.date,
                    timeout=timeout,
                    api_item=self._api_item,
                    indicator_item=self._indicator_item,
                )

                df["代码"] = stock_info.code

                if retries > 0:
                    self._send_message(
                        f"查询 {stock_info.code} 成功，重试次数: {retries}"
                    )

                return df

            except (RequestException, HTTPError) as e:
                if retries < max_retries:
                    retries += 1
                    self._send_message(
                        message=f"查询 {stock_info.code} 时请求失败，尝试重试 {retries}/{max_retries}",
                        exception=e,
                    )

                    time.sleep(1)

            except Exception:
                raise

        return pd.DataFrame()

    def _fetch_with_info(self, stock_info_seq: Sequence[StockInfo]):
        dfs = []

        for stock_info in stock_info_seq:
            try:
                df = self._fetch_retry_with_info(stock_info)

                if df.empty:
                    self._send_message(
                        f"查询 {stock_info.code} 成功，但数据为空，将跳过该标的，请核实日期及该标的具体情况",
                        color="red",
                    )
                else:
                    dfs.append(df)
            except Exception as e:
                self._send_message(
                    message=f"查询 {stock_info.code} 时始终请求失败，将跳过该标的，请核实日期及该标的具体情况",
                    color="red",
                    exception=e,
                )

        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    def _save_to_excel(self, dfs: Sequence[pd.DataFrame]):
        if not dfs:
            self._send_message("查询失败，没有可保存的数据", color="red")
            return

        self._send_message("查询完成，正在保存到 Excel 文件...")

        df = pd.concat(dfs, ignore_index=True)
        df.to_excel(self._output_fpath_str, index=False)

        self._send_message(
            f"处理完成，共 {len(df)} 条数据，已存入 {self._output_fpath_str}\n"
        )

    def _read_to_df(self):
        columns = pd.read_excel(
            self._input_fpath_str, nrows=0, usecols=[0, 1, 2, 3]
        ).columns.tolist()

        return pd.read_excel(
            self._input_fpath_str,
            usecols=[0, 1, 2, 3],
            dtype={columns[1]: str, columns[3]: str},
        ).dropna(how="all")

    def _worker(
        self,
        thread_id: int,
        df: pd.DataFrame,
    ):
        stock_info_seq = self._read_to_info(df)
        self._send_message(f"线程 {thread_id}: 读取完成，正在查询标的历史数据...")

        return self._fetch_with_info(stock_info_seq)

    def _process_futures(self, df: pd.DataFrame):
        return [
            thread_utils.thread_it(
                func=lambda this_i=i, this_df=split_df: self._worker(
                    thread_id=this_i + 1,
                    df=this_df,
                ),
                join=False,
            )
            for i, split_df in enumerate(self._split(df))
        ]

    def _split(self, df: pd.DataFrame) -> Sequence[pd.DataFrame]:
        if df.empty:
            return []

        batch_size = int(np.ceil(len(df) / thread_utils.max_workers))
        return [df.iloc[i : i + batch_size] for i in range(0, len(df), batch_size)]

    def _initialize(
        self,
        input_fpath_str: str,
        output_fpath_str: str,
        api_item: ApiItem,
        indicator_item: str,
    ):
        self._input_fpath_str: str = input_fpath_str
        self._output_fpath_str: str = output_fpath_str
        self._api_item: ApiItem = api_item
        self._indicator_item: str = indicator_item

    def _run(
        self,
        input_fpath_str: str,
        output_fpath_str: str,
        api_item: ApiItem,
        indicator_item: str,
    ):
        self._initialize(input_fpath_str, output_fpath_str, api_item, indicator_item)

        self._send_message(f"待处理的标的信息工作表: {input_fpath_str}")

        df_input = self._read_to_df()
        if df_input.empty:
            self._send_message("没有待处理的标的，请检查 Input Sheet", color="red")
            return

        done_futures, _ = wait(
            self._process_futures(df_input), return_when=ALL_COMPLETED
        )
        self._save_to_excel([future.result() for future in done_futures])

    def run(
        self,
        input_fpath_str: str,
        output_fpath_str: str,
        api_item: ApiItem,
        indicator_item: str,
    ):
        if self.running:
            return

        self.running = True
        self._run(input_fpath_str, output_fpath_str, api_item, indicator_item)
        self.running = False
