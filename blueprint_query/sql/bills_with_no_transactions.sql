SELECT bill_number, currency, balance, new_balance_date FROM bill
LEFT JOIN (
	select bill_a FROM client_transfer_history
	where year(date) = '$year' AND month(date) = '$month'
	group by bill_a
) CTH2020
ON bill_id = CTH2020.bill_a
	WHERE bill_a IS NULL;
