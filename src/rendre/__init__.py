
__version__ = "0.0.0"

import os, re, sys, distutils, shutil, logging
import json
from distutils import dir_util
import urllib.parse
from pathlib import Path

from aurore.uri_utils import resolve_uri
from aurore.selectors import check_includes

import yaml


from .core import Config, InitOperation, ItemOperation
from .utils import copy_tree, get_resource_location, isrepository




def proc_filters(field_filter,FILTERS={}):
    for fltr in field_filter:
        if "=" in fltr:
            field, pattern = fltr.rsplit("=",1)
        else:
            pattern = fltr 
            field = "key"

        if field in FILTERS:
            FILTERS[field].append(re.compile(pattern))
        else:
            FILTERS.update({field: [re.compile(pattern)]})
    return FILTERS
    

def _apply_filter(rsrc:dict,filter:dict)->set:
    if "match" in filter:
        for key, pattern in filter["match"].items():
            if re.match(pattern,rsrc[key]):
                continue
            else:
                return False
    return set(filter["rules"]) if "rules" in filter else True

def apply_field_filters(resource,filters:dict)->bool:
    matches = []
    for field,fltrs in filters.items():
        j_matches = []
        if ":" in field:
            elem_name, attrib = field.split(":")
            for fltr in fltrs:
                fltr_j_matched = False
                for el in resource.findall(elem_name):
                    if fltr.search(el.attrib[attrib]):
                        fltr_j_matched = True
                        break
                j_matches.append(fltr_j_matched)
        matches.append(all(j_matches))

    return all(matches)

def rendre(args, config={})->str:
    logger = logging.getLogger("rendre")

    #-Logging-----------------------------------------------------------
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    levelNames = ["ERROR", "WARN", "INFO", "DEBUG"]
    logger.setLevel(levels[
        0 if args.quiet else min(args.verbose,3) if args.verbose else 0
        ])
    try:
        import coloredlogs
        coloredlogs.install(level=levelNames[
            0 if args.quiet else min(args.verbose,3) if args.verbose else 0
            ])
    except:
        pass

    #-Defaults----------------------------------------------------------
    defaults = {}
    if "load_defaults" in args and args.load_defaults:
        logger.debug("Loading defaults")
        defaults = resolve_uri(args.load_defaults)
    elif "default_set" in args and args.default_set:
        defaults = config["def-defaults"][args.default_set]
    
    for key, value in defaults.items():
        if key.replace("-","_") == "include_item":
            if not args.include_item:
                setattr(args,"include_item",value)
            else:
                args.include_item.extend([
                    arg for arg in value if arg not in args.include_item
                ])
            # args.include_item.extend()
        elif key not in args or not getattr(args,key):
            if isinstance(value,dict) and not all(value.values()):
                value = list(value.keys())
            vars(args)[key.replace("-","_")] = value
        else:
            pass


    logger.debug(f"Namespace: {args}")

    #-Input-------------------------------------------------------------
    if args.data_file == "-":
        cache = json.load(sys.stdin)
    else:
        with open(os.path.expandvars(args.data_file), "r") as f:
            cache = json.load(f)

    # logger.debug(f"Items: {cache['items']}")

    if not config: config = Config()

    #-Fields------------------------------------------------------------
    if "fields" not in args or not args.fields:
        setattr(args,"fields",[r"%i", r"%t"])

    #-Filters-----------------------------------------------------------
    FILTERS = proc_filters(args.filter_any) if args.filter_any else {}

    logger.info(f"Filters: {FILTERS}")
    #-------------------------------------------------------------------
    if "init" in args:
        args.initfunc, args.func, args.closefunc = args.init(args,config)

    if "initfunc" in args:
        accum = args.initfunc(args,config)
    else:
        accum = {}

    logger.debug(f"accum: {accum}")

    if "func" in args and args.func:
        for name, resource in cache["items"].items():
            # resource = resolve_uri(os.path.join(args.base_uri , ref))
            if apply_field_filters(resource,FILTERS):
            # if True:
                logger.info("Entering {}".format(name))
                accum = args.func(resource, args, config, accum)
                included = check_includes(args, {"id":name, **accum["item"]})
                if "item" in accum and included:
                    accum["items"].update({name: accum["item"]})
    
    if "closefunc" in args:
        output = args.closefunc(args, config, accum)
        if output and output[-1] != "\n":
            output = "".join((output,"\n"))

    #-Output------------------------------------------------------------
    
    return output

