SELECT
client.client_id as 'id клиента',
client.phone_number as 'Телефон',
bill.bill_id as 'Номер счёта',
bill.currency as 'Валюта',
bill.balance as 'Баланс',
bill.new_balance_date as 'Дата пополнения'
FROM client
LEFT JOIN bill
ON client.client_id = bill.client_id
order by client.client_id;