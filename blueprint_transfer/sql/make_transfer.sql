INSERT INTO client_transfer_history (sum1, sum2, internal_rate, date, bill_a, bill_b)
VALUES (%(amount)f, %(amount_received)f, %(exchange_rate)f, %(current_date)s, %(account_from)d, %(account_to)d);


UPDATE bill
SET balance = balance - %(amount)f,
    new_balance_date = %(current_date)s
WHERE bill_id = %(account_from)d;


UPDATE bill
SET balance = balance + %(amount_received)f,
    new_balance_date = %(current_date)s
WHERE bill_id = %(account_to)d;