select
    trans_year as 'Год',
    trans_month as 'Месяц',
    bill_number as 'Номер счёта',
    sum_trans as 'Оборот денежных средств'
from bank_accounts.report2
where trans_year = "$year_" and trans_month = "$month_"