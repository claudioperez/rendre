import os
import json
from functools import reduce

import yaml
import jinja2

from aurore.uri_utils import resolve_fragment
from rendre.utils import get_resource_location
from rendre.api import get_item

def init(args, config)-> dict:

    return {
        "items": {},
        "fields": args.field if args.field else [],
        "filter_values": {}
    }

item = get_item

def close(args, config, accum):
    env = jinja2.Environment(
            loader=jinja2.PackageLoader("rendre","report/tmpl_0004")
        )
    # print(accum["items"])
    env.filters["tojson"] = lambda obj,**kwargs: jinja2.Markup(json.dumps(obj, **kwargs))
    env.filters["resolve_fragment"] = resolve_fragment
    template = env.get_template("main.html")
    page = template.render(
        items=accum["items"],
        fields=accum["fields"]
    )
    return page


    