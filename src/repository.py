from typing import Literal

import akshare as ak

from .enums import ApiItem, SideItem


def from_side_item(
    side_item: SideItem,
    code: str,
    date: str,
    timeout: int,
    api_item: ApiItem,
    indicator_item: str,
):
    match side_item:
        case SideItem.STOCK_HIST:
            return fetch_stock(
                api_item=api_item,
                code=code,
                date=date,
                timeout=timeout,
            )
        case SideItem.FUND_OPEN_HIST:
            return fetch_fund_open(
                code=code,
                indicator=indicator_item,
                period="成立来",
            )
        case SideItem.FUND_MONEY_HIST:
            return fetch_fund_money(code=code)
        case SideItem.FUND_ETF_HIST:
            return fetch_fund_etf(code=code, date=date)
        case SideItem.FUND_HK_HIST:
            return fetch_fund_hk(code=code, indicator=indicator_item)
        case SideItem.BOND_HS_HIST:
            return fetch_bond_hs(code=code)


def fetch_stock(api_item: ApiItem, code: str, date: str, timeout: int = 5):
    match api_item:
        case ApiItem.EASTMONEY:
            return _fetch_stock_eastmoney(code, date, timeout)
        case ApiItem.SINA:
            return _fetch_stock_sina(code, date)
        case ApiItem.TENCENT:
            return _fetch_stock_tencent(code, date, timeout)


def fetch_fund_open(
    code: str,
    indicator: (
        Literal[
            "单位净值走势", "累计净值走势", "累计收益率走势", "分红送配详情", "拆分详情"
        ]
        | str
    ),
    period: Literal["1月", "3月", "6月", "1年", "3年", "5年", "今年来", "成立来"],
):
    return _fetch_fund_open_eastmoney(code, indicator, period)


def fetch_fund_money(code: str):
    return _fetch_fund_money_eastmoney(code)


def fetch_fund_etf(code: str, date: str):
    return _fetch_fund_etf_eastmoney(code=code, date=date)


def fetch_fund_hk(code: str, indicator: Literal["历史净值明细", "分红送配详情"] | str):
    return _fetch_fund_hk_eastmoney(code=code, indicator=indicator)


def fetch_bond_hs(code: str):
    return _fetch_bond_hs_sina(code)


def _fetch_stock_eastmoney(code: str, date: str, timeout: int = 5):
    return ak.stock_zh_a_hist(
        symbol=code,
        period="daily",
        start_date=date,
        end_date=date,
        adjust="",
        timeout=timeout,
    )


def _fetch_stock_sina(code: str, date: str):
    return ak.stock_zh_a_daily(
        symbol=_add_prefix(code),
        start_date=date,
        end_date=date,
        adjust="",
    )


def _fetch_stock_tencent(code: str, date: str, timeout: int = 5):
    return ak.stock_zh_a_hist_tx(
        symbol=_add_prefix(code),
        start_date=date,
        end_date=date,
        adjust="",
        timeout=timeout,
    )


def _fetch_fund_open_eastmoney(code: str, indicator: str, period: str):
    return ak.fund_open_fund_info_em(symbol=code, indicator=indicator, period=period)


def _fetch_fund_money_eastmoney(code: str):
    return ak.fund_money_fund_info_em(symbol=code)


def _fetch_fund_etf_eastmoney(code: str, date: str):
    return ak.fund_etf_fund_info_em(fund=code, start_date=date, end_date=date)


def _fetch_fund_hk_eastmoney(code: str, indicator: str):
    return ak.fund_hk_fund_hist_em(code=code, symbol=indicator)


def _fetch_bond_hs_sina(code: str):
    return ak.bond_zh_hs_daily(symbol=code)


# a helper function to add prefix to stock code
def _add_prefix(code: str):
    code = code.strip()
    if not (code.isdigit() and len(code) == 6):
        raise ValueError(f"请检查股票代码正确性: {code}")

    if code.startswith("6"):
        return f"sh{code}"

    if code.startswith(("0", "3")):
        return f"sz{code}"

    raise ValueError(f"请检查股票代码正确性: {code}")
