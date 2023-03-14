import pdoc

modules = ['main.py', 'db.py']  # Публичные субмодули импортируются автоматически
context = pdoc.Context()
modules = [pdoc.Module(mod, context=context)
           for mod in modules]
pdoc.link_inheritance(context)


def recursive_htmls(mod):
    yield mod.name, mod.html()
    for submod in mod.submodules():
        yield from recursive_htmls(submod)


for mod in modules:
    for module_name, html in recursive_htmls(mod):
        with open('doc\ ' + module_name + ".html", 'w', encoding="utf-8") as f:
            f.write(html)
