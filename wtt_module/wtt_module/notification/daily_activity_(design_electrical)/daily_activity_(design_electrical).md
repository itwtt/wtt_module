*Date:* {{ doc.get_formatted('date') }}.
*Employee Name:* {{ doc.employee_name }}.
*Department:* {{ doc.department }}.
{% if doc.activity %}
*Daily Activity*
{%- for row in doc.activity -%}.
>{{row.idx}}. {% if row.activity_type %}{{ row.activity_type }} - {% endif %}{% if row.project %}{{row.project}} - {% endif %}{% if row.hours %}{{ row.hours }}{% endif %}
{%- endfor %}
{% endif %}
*{{ doc.employee_name }}'s Total Hours: {{ doc.total_hours }}*