$trade_date = Read-Host -Prompt "Please input the report date to merge, format = [YYYYMMDD]`nOr you can hit ENTER key directly to use the default value, which is today"
if (-not($trade_date)) {
    $trade_date = Get-Date -Format yyyyMMdd
}
python .\check_1003.py $trade_date
Pause
