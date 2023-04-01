from jinja2 import FileSystemLoader, Environment


file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

tm = env.get_template('main.html')
res = tm.render()
print(res)