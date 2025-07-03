from enum import StrEnum, unique
from pathlib import Path
from typing import Sequence

from src.utils import path_utils

from .api_item import ApiItem


@unique
class SideItem(StrEnum):
    STOCK_HIST = "股票历史数据"
    FUND_OPEN_HIST = "联接基金历史数据"
    FUND_MONEY_HIST = "货币基金历史数据"
    FUND_ETF_HIST = "场内ETF基金历史数据"
    FUND_HK_HIST = "香港基金历史数据"
    BOND_HS_HIST = "沪深债券历史数据"

    @property
    def api_items(self) -> Sequence[str]:
        match self:
            case SideItem.STOCK_HIST:
                return [
                    ApiItem.EASTMONEY.value,
                    ApiItem.SINA.value,
                    ApiItem.TENCENT.value,
                ]
            case SideItem.FUND_OPEN_HIST:
                return [ApiItem.EASTMONEY.value]
            case SideItem.FUND_MONEY_HIST:
                return [ApiItem.EASTMONEY.value]
            case SideItem.FUND_ETF_HIST:
                return [ApiItem.EASTMONEY.value]
            case SideItem.FUND_HK_HIST:
                return [ApiItem.EASTMONEY.value]
            case SideItem.BOND_HS_HIST:
                return [ApiItem.SINA.value]

    @property
    def template_fpath(self) -> Path:
        return path_utils.res_path(self.template_fname)

    @property
    def template_fname(self) -> str:
        match self:
            case SideItem.STOCK_HIST:
                return "Input Sheet模板-股票.xlsx"
            case SideItem.FUND_OPEN_HIST:
                return "Input Sheet模板-联接基金.xlsx"
            case SideItem.FUND_ETF_HIST:
                return "Input Sheet模板-场内ETF基金.xlsx"
            case SideItem.FUND_MONEY_HIST:
                return "Input Sheet模板-货币基金.xlsx"
            case SideItem.FUND_HK_HIST:
                return "Input Sheet模板-香港基金.xlsx"
            case SideItem.BOND_HS_HIST:
                return "Input Sheet模板-沪深债券.xlsx"

    @property
    def indicator_items(self) -> Sequence[str]:
        match self:
            case SideItem.STOCK_HIST:
                return ["历史行情数据"]
            case SideItem.FUND_OPEN_HIST:
                return [
                    "单位净值走势",
                    "累计净值走势",
                    "累计收益率走势",
                    "分红送配详情",
                    "拆分详情",
                ]
            case SideItem.FUND_ETF_HIST:
                return ["历史净值数据"]
            case SideItem.FUND_MONEY_HIST:
                return ["历史净值数据"]
            case SideItem.FUND_HK_HIST:
                return ["历史净值明细", "分红送配详情"]
            case SideItem.BOND_HS_HIST:
                return ["历史行情数据"]
