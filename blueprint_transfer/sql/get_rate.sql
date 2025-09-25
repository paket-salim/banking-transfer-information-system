SELECT rate
FROM bank_internal_rate AS bir
JOIN bill AS b1 ON b1.bill_number = "$account_from"
JOIN bill AS b2 ON b2.bill_number = "$account_to"
WHERE bir.currency1 = b1.currency
  AND bir.currency2 = b2.currency
