from setup import *

trade_date = input("Please input the report date [format=YYYYMMDD]: ") or dt.datetime.now().strftime("%Y%m%d")
trade_year = trade_date[0:4]

while True:
    u_disk_sign = input("Please input the U-Disk sign [Default is 'H']: ").upper() or "H"
    src_dir = os.path.join("{}:\\".format(u_disk_sign), "报表", trade_date[0:4])
    if not os.path.exists(src_dir):
        print("| {} | Error | {} | does not exist, please check again |".format(dt.datetime.now(), src_dir))
    else:
        break

dst_dir = os.path.join(OUT_PUT_DIR, trade_year)
check_and_mkdir(dst_dir)
dst_dir = os.path.join(dst_dir, trade_date)
check_and_mkdir(dst_dir)

i = 0
for iter_file in os.listdir(src_dir):
    if iter_file.find(trade_date) < 0:
        continue

    copyfile(
        src=os.path.join(src_dir, iter_file),
        dst=os.path.join(dst_dir, iter_file)
    )

    print("| {} | {:>02d} | {} | copied |".format(dt.datetime.now(), i, iter_file))
    i += 1

print(SEP_LINE)
print("| {} | {} | A total of {} files copied |".format(dt.datetime.now(), trade_date, i))
