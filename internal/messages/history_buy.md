{% for deal in deals %}
*id сделки:* `{{deal.id}}`
*Категория:* `{{deal.category}}`
*Подкатегория:* `{{deal.subcategory}}`
*Название аккаунта:* `{{deal.name}}`
*Стоимость:* `{{deal.price}}$`
*Описание:* `{{deal.description}}`
*Данные:*
`{{deal.data}}`
*Дата покупки:* `{{deal.date}}`
{%if deal.payment == 0%}*Сделка не оплачена*{% endif %}{%if deal.payment == 1%}*Сделка оплачена с гарантом, но еще не
подтверждена*{% endif %}{%if deal.payment == 2%}*Сделка оплачена*{% endif %}
{% if deal.guarantor == True %}*Покупка совершена с гарантом*
{% else %}*Покупка совершена без гаранта*{% endif %}
{% endfor %}