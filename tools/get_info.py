import re
from urllib.parse import urlparse, urljoin
import json
pkgs = """
| [@steeze-ui/heroicons](packages/builders/heroicons-builder)                          | default(outline), solid, mini                      | [tailwindlabs/heroicons](https://github.com/tailwindlabs/heroicons)                                    | [browse](https://heroicons.com/)                                   | <a href="https://www.npmjs.com/package/@steeze-ui/heroicons"><img src="https://img.shields.io/npm/v/@steeze-ui/heroicons.svg?style=flat" /></a>                         | 2.2.0       |
| [@steeze-ui/simple-icons](packages/builders/simple-icons-builder/)                   | default                                            | [simple-icons/simple-icons](https://github.com/simple-icons/simple-icons)                              | [browse](https://simpleicons.org/)                                 | <a href="https://www.npmjs.com/package/@steeze-ui/simple-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/simple-icons.svg?style=flat" /></a>                   | 13.17.0     |
| [@steeze-ui/tabler-icons](packages/builders/tabler-icons-builder/)                   | default(outline), filled                           | [tabler/tabler-icons](https://github.com/tabler/tabler-icons)                                          | [browse](https://tabler-icons.io/)                                 | <a href="https://www.npmjs.com/package/@steeze-ui/tabler-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/tabler-icons.svg?style=flat" /></a>                   | 3.22.0      |
| [@steeze-ui/radix-icons](packages/builders/radix-icons-builder)                      | default                                            | [radix-ui/icons](https://github.com/radix-ui/icons)                                                    | [browse](https://icons.modulz.app/)                                | <a href="https://www.npmjs.com/package/@steeze-ui/radix-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/radix-icons.svg?style=flat" /></a>                     | 5.0.0       |
| [@steeze-ui/material-design-icons](packages/builders/material-design-icons-builder/) | default(filled), outlined, rounded, sharp, twotone | [google/material-design-icons](https://github.com/google/material-design-icons)                        | [browse](https://fonts.google.com/icons)                           | <a href="https://www.npmjs.com/package/@steeze-ui/material-design-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/material-design-icons.svg?style=flat" /></a> | 1.14.9      |
| [@steeze-ui/lucide-icons](packages/builders/lucide-icons-builder)                    | default                                            | [lucide-icons/lucide](https://github.com/lucide-icons/lucide)                                          | [browse](https://lucide.dev/)                                      | <a href="https://www.npmjs.com/package/@steeze-ui/lucide-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/lucide-icons.svg?style=flat" /></a>                   | 0.408.0     |
| [@steeze-ui/phosphor-icons](packages/builders/phosphor-icons-builder/)               | thin, light, default(regular), bold, fill, duotone | [Phosphor Icons](https://phosphoricons.com/)                                                           | [browse](https://phosphoricons.com/)                               | <a href="https://www.npmjs.com/package/@steeze-ui/phosphor-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/phosphor-icons.svg?style=flat" /></a>               | 2.1.1       |
| [@steeze-ui/carbon-icons](packages/builders/carbon-icons-builder/)                   | default                                            | [carbon-design-system/carbon](https://github.com/carbon-design-system/carbon/tree/main/packages/icons) | [browse](https://carbondesignsystem.com/guidelines/icons/library/) | <a href="https://www.npmjs.com/package/@steeze-ui/carbon-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/carbon-icons.svg?style=flat" /></a>                   | 11.21.0     |
| [@steeze-ui/remix-icons](packages/builders/remix-icons-builder)                      | default(outline), solid                            | [Remix-Design/RemixIcon](https://github.com/Remix-Design/remixicon)                                    | [browse](https://remixicon.com/)                                   | <a href="https://www.npmjs.com/package/@steeze-ui/remix-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/remix-icons.svg?style=flat" /></a>                     | 4.2.0       |
| [@steeze-ui/iconic-free](packages/builders/iconic-free-builder)                      | default                                            | [iconic.app](https://iconic.app/)                                                                      | [browse](https://iconic.app/c/availability/free/)                  | <a href="https://www.npmjs.com/package/@steeze-ui/iconic-free"><img src="https://img.shields.io/npm/v/@steeze-ui/iconic-free.svg?style=flat" /></a>                     | -           |
| [@steeze-ui/octicons](packages/builders/octicons-builder)                            | default(16), 24, 12                                | [primer/octicons](https://github.com/primer/octicons)                                                  | [browse](https://primer.style/octicons/)                           | <a href="https://www.npmjs.com/package/@steeze-ui/octicons"><img src="https://img.shields.io/npm/v/@steeze-ui/octicons.svg?style=flat" /></a>                           | 19.3.0      |
| [@steeze-ui/css-gg](packages/builders/css-gg-builder/)                               | default                                            | [CSS.gg Icons](https://css.gg/)                                                                        | [browse](https://css.gg/app)                                       | <a href="https://www.npmjs.com/package/@steeze-ui/css-gg"><img src="https://img.shields.io/npm/v/@steeze-ui/css-gg.svg?style=flat" /></a>                               | 2.1.1       |
| [@steeze-ui/font-awesome](packages/builders/font-awesome-builder/)                   | default, solid                                     | [Font Awesome](https://github.com/FortAwesome/Font-Awesome)                                            | [browse](https://fontawesome.com/search)                           | <a href="https://www.npmjs.com/package/@steeze-ui/font-awesome"><img src="https://img.shields.io/npm/v/@steeze-ui/font-awesome.svg?style=flat" /></a>                   | 6.5.1       |
| [@steeze-ui/feather-icons](packages/builders/feather-icons-builder) (deprecated)     | default                                            | [feathericons/feather](https://github.com/feathericons/feather)                                        | [browse](https://feathericons.com/)                                | <a href="https://www.npmjs.com/package/@steeze-ui/feather-icons"><img src="https://img.shields.io/npm/v/@steeze-ui/feather-icons.svg?style=flat" /></a>                 | 4.29.1      |
"""


def get_info(line: str):
    line = line.strip()
    expr = r"^\|\s+\[(@steeze-ui/.*?)\]\((.*?)\)\s+\|\s+(.*?)\s+\|.*?\((.*?)\)\s+\|.*?\((.*?)\)\s+\|"
    match = re.search(expr, line)
    if not match:
        return None
    name, path, theme, src, web = match.groups()
    path = path if urlparse(path).netloc else urljoin(
        "https://github.com/steeze-ui/icons/blob/main/", path)
    theme = [t.strip() for t in theme.split(",") if t.strip()]
    return dict(name=name, pkg=path, src=src, web=web, theme=theme, imp=f"__IMPORT__'{name}'__IMPORT__")


def get_all_info(pkgs: str):
    lines = pkgs.split("\n")
    infos = [
        get_info(line)
        for line in lines
    ]
    infos = [
        info
        for info in infos
        if info is not None
    ]
    return infos


def to_code(infos: list):
    code = json.dumps(infos, ensure_ascii=False)
    code = code.replace('"__IMPORT__\'', '()=>import(\'')
    code = code.replace('\'__IMPORT__"', '\')')
    return code


if __name__ == "__main__":
    print(to_code(get_all_info(pkgs)))
