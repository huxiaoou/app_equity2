import os
import sys
import datetime as dt
from skyrim.winterhold import check_and_mkdir
from shutil import copyfile

SEP_LINE = "=" * 120

REPORTS_SN_TO_CHS_NAME = {
    "00": "交易指令单",
    "01": "投资管理总部交易指令单",
    "02": "当日成交",
    "03": "当日成交汇总",
    "03-L": "当日成交汇总-L",
    "04": "持仓情况明细表",
    "05": "盈亏情况明细表",
    "06": "风险限额监控表",
    # "07": "交易详情日报表",
}

ACCOUNT_ID = "1003000010"

OUT_PUT_DIR = os.path.join("E:\\", "Works", "Trade", "Reports_Equity2", "output")
