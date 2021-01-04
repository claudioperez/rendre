import os
import re
import json
from functools import reduce

import yaml
import jinja2

from aurore.utils.treeutils import iterate_leaves
from aurore.selectors import Pointer


def remove_duplicates(lst: list)->list:
    items = set()
    append = items.add
    return [x for x in lst if not (x in items or append(x))]

def init(args, config)->dict:

    return {
        "items": {},
        "filter_values": {}
    }

def item(rsrc, args:object, config:object, accum:dict)->dict:
    fields = [
            Pointer(
                field,
                truncate=True,
                bracket_as_slice=True
            ).resolve(rsrc)
            for field in remove_duplicates(args.fields)
        ]
    if args.flatten_fields:
        fields = [f for f in iterate_leaves(fields)]
    rsrc.update({
            "fields": fields
    })
    accum['item'] = rsrc
    return accum

def close(args, config, accum):

    if args.format_yaml:
        # Insert newline before each top level mapping
        # key. Keys are assumed to match the following
        # regular expression: /^([-A-z0-9]*:)$/
        return "\n".join(
            re.sub(r"^([-A-z0-9]*:)$","\n\\1", s)  \
            for s in yaml.dump({
                k: v["fields"] for k,v in accum["items"].items()
            }).split("\n")
        )
    elif args.format_line:
        return ' '.join(
            f for v in accum["items"].values() 
              for f in iterate_leaves(v["fields"])
        )

    elif args.format_json:
        return json.dumps(
            {k: v["fields"] for k,v in accum["items"].items()},
            indent=4
        )

    elif args.format_table:
        return args.join_items.join(
            args.separator.join(
                item["fields"]
            ) for item in accum["items"].values()
        )
    #     env = jinja2.Environment(
    #             loader=jinja2.PackageLoader("rendre","report/tmpl_0004")
    #         )
    #     # print(accum["items"])
    #     env.filters["tojson"] = tojson
    #     # env.filters["resolve_fragment"] = resolve_fragment
    #     template = env.get_template("main.html")
    #     page = template.render(
    #         items=accum["items"],
    #         # fields=accum["fields"]
    #         SEP=args.separator
    #     )
    #     return page

# def tojson(obj, **kwds):
#     return jinja2.Markup(json.dump(obj,**kwds))

