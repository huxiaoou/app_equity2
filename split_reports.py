from setup import *
import xlwings as xw

report_date = input("Please input the report date [format=YYYYMMDD]: ") or dt.datetime.now().strftime("%Y%m%d")

# --- load report template
src_file = "一、衍生品当日报表-汇总（资金账户{}）-{}.xlsx".format(ACCOUNT_ID, report_date)
src_path = os.path.join(OUT_PUT_DIR, report_date[0:4], report_date, src_file)
if not os.path.exists(src_path):
    print("| {} | {} | ERROR | src file = '{}' does not exist, please check again |".format(dt.datetime.now(), report_date, src_file))
else:
    # wb = xlrd.open_workbook(src_path, on_demand=True)
    wb = xw.Book(src_path)
    for report_sn, chs_name in REPORTS_SN_TO_CHS_NAME.items():
        # save path
        save_file = "{}_{}_股票可转债_{}_{}.xlsx".format(report_sn, chs_name, ACCOUNT_ID, report_date)
        save_path = os.path.join(OUT_PUT_DIR, report_date[0:4], report_date, save_file)
        if os.path.exists(save_path):
            os.remove(save_path)

        ws = wb.sheets[report_sn]
        new_wb = xw.Book()
        ws.api.Copy(Before=new_wb.sheets(1).api)
        new_wb.sheets[report_sn].name = "可转债2"
        new_wb.sheets["Sheet1"].delete()
        new_wb.save(save_path)

        print("| {} | {} | {} | copied |".format(dt.datetime.now(), report_sn, chs_name))
    wb.close()
