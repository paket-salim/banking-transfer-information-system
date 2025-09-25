SELECT bill_number, balance
FROM bill
WHERE bill_number IN ('$account_from', '$account_to')
