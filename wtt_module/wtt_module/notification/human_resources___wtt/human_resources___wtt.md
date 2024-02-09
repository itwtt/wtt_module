*Happy Morning All*.
Date: {{ doc.get_formatted('date') }}.
Department: {{ doc.department }}.
{% if doc.entries %}
*Say It Do It Entries*
{%- for row in doc.entries -%}.
>{{row.idx}}. {{ row.employee_name }} - {{ row.say_it_do_it }}
{%- endfor %}
{% endif %}

{% if doc.no_entries %}
*No Entries*
{%- for row in doc.no_entries -%}.
>{{row.idx}}. {{ row.employee_name }}
{%- endfor %}
{% endif %}