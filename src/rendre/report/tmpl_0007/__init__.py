"""
Template for Sphinx gallery.
"""


import os
import re
import json
from functools import reduce
from sphinx.util.osutil import relative_uri

import yaml
import jinja2

from aurore.utils.treeutils import iterate_leaves
from aurore.selectors import Pointer, PathBuilder


def remove_duplicates(lst: list)->list:
    items = set()
    append = items.add
    return [x for x in lst if not (x in items or append(x))]

def init(args, config)-> dict:

    return {
        "link": PathBuilder(args.link),
        "items": {},
        "filters": {},
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
    link = accum["link"].resolve(rsrc)
    image_path = relative_uri(
        config["base_uri"], os.path.join(
            "_images", rsrc["logo"]
        )
    )
    rsrc.update({
        "fields": fields,
        "url": link,
        "image": image_path
    })
    try:
        for k, v in rsrc["categories"].items():
            print(k,v)
            accum["filters"][k].update({v})
    except:
        for k, v in rsrc["categories"].items():
            accum["filters"][k] = set([v])
    accum['item'] = rsrc
    
    return accum

def close(args, config, accum):
    print(f"\nFilters: {accum['filters']}\n")
    if not args.fields:
        fields = {k: v for k, v in accum["items"]}
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

    elif args.format_json:
        return json.dumps(
            {k: v["fields"] for k,v in accum["items"].items()},
            indent=4
        )

    elif args.format_html:
        env = jinja2.Environment(
                loader=jinja2.PackageLoader("rendre","report/tmpl_0007")
            )
        # print(accum["items"])
        env.filters["tojson"] = tojson
        # env.filters["resolve_fragment"] = resolve_fragment
        template = env.get_template("main.html")
        page = template.render(
            items=accum["items"],
            filters=accum["filters"],
            filter_values = accum["filter_values"]
        )
        return page

def tojson(obj, **kwds):
    return jinja2.Markup(json.dump(obj,**kwds))

