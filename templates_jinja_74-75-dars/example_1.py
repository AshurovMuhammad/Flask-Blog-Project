# 74-dars: Freamworklar bilan tanishuv, (ORM, Shablonizator)  // 50  // 76
# WSGI (Web Server Gateway Interface) // Web server shlyuz interfeysi
# ORM (Object-Relation Mapping) // Obyekt bilan aloqador xaritalash


# Flask
# Django

# Jinja

from jinja2 import Template, Environment, FileSystemLoader

# # name = "Igor"
# # age = 28
#
# per = {'name': 'Igor', 'age': 28}
#
# # tm = Template("Privet {{ p.name }}. Mne {{ p.age*2 }} let.")
# tm = Template("Privet {{ p['name'] }}. Mne {{ p['age'] }} let.")
#
# msg = tm.render(p=per)
#
# print(msg)


# Jinja shablonizatorini classlarda qo'llash
# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def get_name(self):
#         return self.name
#
#     def get_age(self):
#         return self.age
#
#
# per = Person("Igor", 28)
#
# tm = Template("Privet {{ p.get_name() }}. Mne {{ p.get_age() }} let.")
# msg = tm.render(p=per)
# print(msg)


# data = """Modul Jinja vmesto
# opredeleniya {{ name }}
# podstavit cootvetsvuyushee znacheniye
# """
#
# tm = Template(data)
# msg = tm.render(name="Igor")
# print(msg)

# ======================================================================================================================
# {% raw %} blogi
# data = """{% raw %}Modul Jinja vmesto
# opredeleniya {{ name }}
# podstavit cootvetsvuyushee znacheniye{% endraw %}
# """
#
# tm = Template(data)
# msg = tm.render(name="Igor")
# print(msg)

# экранирование // result: &lt;a href=&#39;#&#39;&gt;Ssilka&lt;/a&gt;
# link = "<a href='#'>Ssilka</a>"
# tm = Template("{{link | e}}")
# msg = tm.render(link=link)
# print(msg)


# {% for %} blogi
# cities = [
#     {'id': 1, 'city': 'Moskva'},
#     {'id': 2, 'city': 'Smolensk'},
#     {'id': 3, 'city': 'Minsk'},
#     {'id': 4, 'city': 'Djitomir'},
#     {'id': 5, 'city': 'Yaroslavl'},
# ]
#
# link = """<select name='cities'>
# {% for c in cities -%}
#     <option value="{{ c['id'] }}">{{ c['city'] }}</option>
# {% endfor -%}
# </select>"""
#
# tm = Template(link)
# msg = tm.render(cities=cities)
# print(msg)


# {% if %} blogi
# cities = [
#     {'id': 1, 'city': 'Moskva'},
#     {'id': 2, 'city': 'Smolensk'},
#     {'id': 3, 'city': 'Minsk'},
#     {'id': 4, 'city': 'Djitomir'},
#     {'id': 5, 'city': 'Yaroslavl'},
# ]
#
# link = """<select name='cities'>
# {% for c in cities -%}
#     {% if c.id > 3 -%}
#         <option value="{{ c['id'] }}">{{ c['city'] }}</option>
#     {% elif c.city == "Moskva" -%}
#         <option>{{ c['city'] }}</option>
#     {% else -%}
#         {{ c['city'] }}
#     {% endif -%}
# {% endfor -%}
# </select>"""
#
# tm = Template(link)
# msg = tm.render(cities=cities)
# print(msg)


# Praktika
# menu = [
#     {'href': '/index', 'name': 'Glavnaya'},
#     {'href': '/news', 'name': 'Novosti'},
#     {'href': '/about', 'name': 'O kompanii'},
#     {'href': '/shop', 'name': 'Magazin'},
#     {'href': '/contacts', 'name': 'Kontakt'}
# ]
#
# active = "active"
#
# res = """<ul>
# {% for m in menu -%}
# {% if m.name == 'Glavnaya' -%}
#     <li><a href="{{ m.href }}" class="{{a}}">{{ m.name }}</a></li>
# {% else -%}
#     <li><a href="{{ m.href }}">{{ m.name }}</a></li>
# {% endif -%}
# {% endfor -%}
# </ul>"""
#
# tm = Template(res)
# msg = tm.render(menu=menu, a=active)
# print(msg)


# filtrlash
# first example
# cars = [
#     {'model': 'Audi', 'price': 23000},
#     {'model': 'Skoda', 'price': 17000},
#     {'model': 'Renault', 'price': 44000},
#     {'model': 'Wolkvagen', 'price': 21000}
# ]
#
# # tpl = "Avtomobillarni umumiy narxlari {{ cs | sum(attribute='price') }}"   # sum() - filter sum narxlar yigindisini qaytaradi
# # tpl = "Avtomobillar ichida eng qimmat mashinani aniqlabberadi {{ cs | max(attribute='price') }}"  # max() - filter max narxlarni eng balandini qaytaradi
# # tpl = "Avtomobillarni ichida eng qimmatini modeli {{ (cs | max(attribute='price')).model }}"  # eng qimmat mashina modelini qaytaradi
# # tpl = "Tasodifiy avtomobil {{ (cs | random).model }}"   # Tasodifiy avtomobilni generatsiya qilib beradi
# tpl = "Avtomobillar ro'yxati {{ cs | replace('model', 'brand') }}"  # lugat kalitini boshqa qiymatga o'zgartirish
#
# tm = Template(tpl)
# msg = tm.render(cs=cars)
# print(msg)
#
# # second example
# # lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# #
# # tpl = "Avtomobillarni umumiy narxlari {{ cs | sum() }}"
# #
# # tm = Template(tpl)
# # msg = tm.render(cs=lst)
# # print(msg)
# ======================================================================================================================
# 75-dars.  // 51 // 77


# Filter
# person = [
#     {"name": "Aleksey", 'year': 18, "weight": 78.5},
#     {"name": "Nikita", 'year': 28, "weight": 82.3},
#     {"name": "Vataliy", 'year': 33, "weight": 94.0},
# ]
#
# tpl = """
# {%- for user in users -%}
# {# {% filter upper %}{{ user.name }}{% endfilter %} #}
# {% filter string %}{{ user.year }} - {{ user.weight }}{% endfilter %}
# {% endfor -%}
# """
#
# tm = Template(tpl)
# msg = tm.render(users=person)
# print(msg)


# macro aniqlash
# html = """
# {% macro input(name, value='', type='text', size='20') -%}
#     <input type="{{ type }}" name="{{ name }}", value="{{ value }}">
# {%- endmacro -%}
#
# <p> {{ input('username', 'Vvedite imya') }} </p>
# <p> {{ input('email', 'Vvedite email') }} </p>
# <p> {{ input('password') }} </p>
# """
# tm = Template(html)
# msg = tm.render()
# print(msg)


# Praktika 1-usul
# users = [
#     {"firstname": "Imya"},
#     {"lastname": "Familiya"},
#     {"address": "Address"},
#     {"phone": "Telefon"},
#     {"email": "Pochta"}
# ]
#
# html = """
# {%- macro kiritish(en, ru, type="text") -%}
#     <input type="{{ type }}" name="{{ en }}" placeholder="{{ ru }}">
# {%- endmacro %}
# {% for user in users -%}
# {% for e, r in user.items() -%}
# {% if e== 'phone' -%}
# <p>{{ kiritish(e, r, "tel") }}</p>
# {%- elif e== 'email' -%}
# <p>{{ kiritish(e, r, "email") }}</p>
# {%- else -%}
# <p>{{ kiritish(e, r) }}</p>
# {%- endif %}
# {%- endfor %}
# {% endfor %}
# """
#
# tm = Template(html)
# msg = tm.render(users=users)
# print(msg)


# Praktika 2-usul
# html = """
# {% macro kiritish(name, placeholder, type="text") -%}
#     <input type="{{ type }}" name="{{ name }}" placeholder="{{ placeholder }}">
# {%- endmacro %}
# <p>{{ kiritish("firstname", "Ism") }}</p>
# <p>{{ kiritish("lastname", "Familiya") }}</p>
# <p>{{ kiritish("address", "Address") }}</p>
# <p>{{ kiritish("phone", "Telefon", "phone") }}</p>
# <p>{{ kiritish("email", "Pochta", "email") }}</p>
# """
# tm = Template(html)
# msg = tm.render()
# print(msg)


# {% call %} blogi
# person = [
#     {"name": "Aleksey", 'year': 18, "weight": 78.5},
#     {"name": "Nikita", 'year': 28, "weight": 82.3},
#     {"name": "Vataliy", 'year': 33, "weight": 94.0},
# ]
#
# html = """
# {% macro list_users(lst) %}
# <ul>
# {% for u in lst -%}
#     <li>{{ u.name }} {{ caller(u) }}</li>
# {% endfor -%}
# </ul>
# {%- endmacro %}
#
# {% call(user) list_users(users) %}
#     <ul>
#         <li>age: {{user.year}}</li>
#         <li>weight: {{user.weight}}</li>
#     </ul>
# {% endcall %}
# """
#
# tm = Template(html)
# msg = tm.render(users=person)
# print(msg)


# cars = [
#     {"brand": "Ford", "color": "black", "price": 225000},
#     {"brand": "Chevrolet", "color": "red", "price": 335000},
#     {"brand": "Daewoo", "color": "yellow", "price": 500000},
#     {"brand": "GM", "color": "white", "price": 150000},
# ]
#
# html = """
# {% macro info(lst) %}
# <ul>
# {% for car in lst -%}
#     <li>{{ car.brand }} {{ caller(car) }}</li>
# {% endfor -%}
# </ul>
# {%- endmacro %}
#
# {% call(auto) info(auto) %}
#      <ul>
#         <li>color: {{auto.color}}</li>
#         <li>price: {{auto.price}}</li>
#     </ul>
# {% endcall %}
# """
#
# tm = Template(html)
# res = tm.render(auto=cars)
# print(res)


# HTML fayl bilan ishlash
subs = ["Kultura", "Nauqa", "Politika", "Sport"]
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

tm = env.get_template('about.html')
res = tm.render(list_table=subs)
print(res)
