import pandas as pd
import os
import sys
from skyrim.winterhold import get_mix_string_len


def print_by_security(t_df: pd.DataFrame, t_trade_date: str):
    print("=" * 120)
    print("交易日:{1}{0}按证券代码汇总".format(" " * (105 - 14), t_trade_date))
    print("-" * 120)
    print("|   资金帐号 | 买入数量(千股[张]) | 买入金额(万元) | 卖出数量(千股[张]) | 卖出金额(万元) | 证券名称     |")
    for account_id, sec_id in t_df.index:
        b_qty_sum = t_df.loc[(account_id, sec_id), ("成交数量", "证券买入")] if ("成交数量", "证券买入") in t_df.columns else 0
        b_amt_sum = t_df.loc[(account_id, sec_id), ("成交金额", "证券买入")] if ("成交金额", "证券买入") in t_df.columns else 0
        s_qty_sum = t_df.loc[(account_id, sec_id), ("成交数量", "证券卖出")] if ("成交数量", "证券卖出") in t_df.columns else 0
        s_amt_sum = t_df.loc[(account_id, sec_id), ("成交金额", "证券卖出")] if ("成交金额", "证券卖出") in t_df.columns else 0
        sec_id_len = get_mix_string_len(sec_id, 12)
        row_format = "| {:>10s} | {:>18.2f} | {:>14.2f} | {:>18.2f} | {:>14.2f} | {:<" + str(sec_id_len) + "s} |"
        print(row_format.format(account_id, b_qty_sum / 1e3, b_amt_sum / 1e4, s_qty_sum / 1e3, s_amt_sum / 1e4, sec_id))
    return 0


def print_by_account(t_df: pd.DataFrame, t_trade_date: str):
    print("=" * 120)
    print("交易日:{1}{0}按资金账户汇总".format(" " * (105 - 14), t_trade_date))
    print("-" * 120)
    print("|   资金帐号 | 买入数量(千股[张]) | 买入金额(万元) | 卖出数量(千股[张]) | 卖出金额(万元) |")
    for account_id in t_df.index:
        b_qty_sum = t_df.loc[account_id, ("成交数量", "证券买入")] if ("成交数量", "证券买入") in t_df.columns else 0
        b_amt_sum = t_df.loc[account_id, ("成交金额", "证券买入")] if ("成交金额", "证券买入") in t_df.columns else 0
        s_qty_sum = t_df.loc[account_id, ("成交数量", "证券卖出")] if ("成交数量", "证券卖出") in t_df.columns else 0
        s_amt_sum = t_df.loc[account_id, ("成交金额", "证券卖出")] if ("成交金额", "证券卖出") in t_df.columns else 0
        print("| {:>10s} | {:>18.2f} | {:>14.2f} | {:>18.2f} | {:>14.2f} |".format(
            account_id, b_qty_sum / 1e3, b_amt_sum / 1e4, s_qty_sum / 1e3, s_amt_sum / 1e4))
    return 0


def print_sum(t_df: pd.DataFrame, t_trade_date: str):
    print("=" * 120)
    print("交易日:{1}{0}总体汇总".format(" " * (105 - 8), t_trade_date))
    print("-" * 120)
    b_qty_sum = t_df[("成交数量", "证券买入")].sum() if ("成交数量", "证券买入") in t_df.columns else 0
    b_amt_sum = t_df[("成交金额", "证券买入")].sum() if ("成交金额", "证券买入") in t_df.columns else 0
    s_qty_sum = t_df[("成交数量", "证券卖出")].sum() if ("成交数量", "证券卖出") in t_df.columns else 0
    s_amt_sum = t_df[("成交金额", "证券卖出")].sum() if ("成交数量", "证券卖出") in t_df.columns else 0
    print("|   资金帐号 | 买入数量(千股[张]) | 买入金额(万元) | 卖出数量(千股[张]) | 卖出金额(万元) |")
    print("| {:>10s} | {:>18.2f} | {:>14.2f} | {:>18.2f} | {:>14.2f} |".format(
        "--", b_qty_sum / 1e3, b_amt_sum / 1e4, s_qty_sum / 1e3, s_amt_sum / 1e4))
    return 0


pd.set_option("display.width", 0)

os.system("")  # Or output may not be interpreted correctly in powershell

trade_date = sys.argv[1]
trade_year = trade_date[0:4]

selected_columns = [
    "机构名称",
    "资金帐号",
    "证券帐号",
    "市  场",
    "证券代码",
    "证券名称",
    "买卖标识",
    "委托价格",
    "委托数量",
    "成交数量",
    "撤单数量",
    "成交金额",
    "委托状态",
    "撤单标志",
]

src_file = "traded.{}.csv".format(trade_date)
src_path = os.path.join("G:", "柜台数据", trade_year, trade_date, src_file)
if not os.path.exists(src_path):
    print("... Warning! Source path:\033[33m{}\033[0m does NOT EXIST, please check again.".format(src_path))
    sys.exit()

src_df = pd.read_csv(src_path, encoding="gb18030", usecols=selected_columns, dtype={"资金帐号": str, "证券代码": str})
src_df = src_df.loc[src_df["机构名称"] != "合计:"]

by_security_df = pd.pivot_table(
    data=src_df,
    index=["资金帐号", "证券名称"],
    columns=["买卖标识"],
    values=["成交数量", "成交金额"],
    aggfunc=sum
).fillna(0)
cb_by_security_df = by_security_df.loc[("1003000010",):]
by_account_df = pd.pivot_table(
    data=src_df,
    index=["资金帐号"],
    columns=["买卖标识"],
    values=["成交数量", "成交金额"],
    aggfunc=sum
).fillna(0)

print_by_security(t_df=by_security_df, t_trade_date=trade_date)
print_by_account(t_df=by_account_df, t_trade_date=trade_date)
print_sum(t_df=by_account_df, t_trade_date=trade_date)
print_by_security(t_df=cb_by_security_df, t_trade_date=trade_date)
print("=" * 120)
