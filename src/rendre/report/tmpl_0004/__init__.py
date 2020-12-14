import os
import json
from functools import reduce

import yaml
import jinja2

from aurore.selectors import Pointer
from aurore.uri_utils import resolve_fragment
from rendre.utils import get_resource_location
from rendre.api import get_item


def remove_duplicates(lst: list)->list:
    items = set()
    append = items.add
    return [x for x in lst if not (x in items or append(x))]

def init(args, config)-> dict:

    return {
        "items": {},
        # "fields": remove_duplicates(args.fields) if args.fields else [],
        "filter_values": {}
    }

def item(rsrc, args:object, config:object, accum:dict)->dict:
    rsrc.update({
        "fields": \
            [Pointer(field).resolve(rsrc) for field in remove_duplicates(args.fields)]
        })
    accum['item'] = rsrc
    return accum

def close(args, config, accum):
    env = jinja2.Environment(
            loader=jinja2.PackageLoader("rendre","report/tmpl_0004")
        )
    # print(accum["items"])
    env.filters["tojson"] = tojson
    env.filters["resolve_fragment"] = resolve_fragment
    template = env.get_template("main.html")
    page = template.render(
        items=accum["items"],
        # fields=accum["fields"]
    )
    return page

def tojson(obj, **kwds):
    return jinja2.Markup(json.dump(obj,**kwds))
    