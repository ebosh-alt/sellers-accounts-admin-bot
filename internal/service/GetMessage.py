from jinja2 import Environment, PackageLoader, select_autoescape


def get_text(text: str) -> str:
    # text = text.replace("_", r"\_")
    text = text.replace("{", r"\{")
    text = text.replace("}", r"\}")
    text = text.replace("[", r"\[")
    text = text.replace("]", r"\]")
    text = text.replace("<", r"\<")
    text = text.replace(">", r"\>")
    text = text.replace("(", r"\(")
    text = text.replace(")", r"\)")
    text = text.replace("#", r"\#")
    text = text.replace("+", r"\+")
    text = text.replace("-", r"\-")
    text = text.replace(".", r"\.")
    text = text.replace("!", r"\!")
    text = text.replace("=", r"\=")
    text = text.replace("|", r"\|")
    # text = text.replace("*", r"\*")
    return text


def get_mes(
        path: str,
        screening: bool = True,
        **kwargs,
):
    env = Environment(
        loader=PackageLoader(
            package_name="main", package_path="internal/messages", encoding="utf-8"
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )

    if ".md" not in path:
        path = path + ".md"
    tmpl = env.get_template(path)
    if screening:
        return get_text(tmpl.render(kwargs))
    else:
        return tmpl.render(kwargs)


def rounding_numbers(number: str):
    return int(number[:-1]) if number[-1] == "." else float(number)
