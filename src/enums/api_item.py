from enum import StrEnum, unique


@unique
class ApiItem(StrEnum):
    EASTMONEY = "东方财富"
    SINA = "新浪财经"
    TENCENT = "腾讯财经"
