SELECT
bank_internal_rate.currency1 as 'Валюта',
bank_internal_rate.rate as 'Курс',
bank_internal_rate.date as 'Дата и время'
FROM bank_internal_rate
order by bank_internal_rate.date;