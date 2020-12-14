#!/usr/bin/env python
import argparse
from rendre import rendre
from .report import init_report
from .api import \
    post_init, post_close, \
    get_init, get_item, get_close



def pass_item(item, args, config, accum:dict)->dict:
    return accum


def parse_args():
    parser = argparse.ArgumentParser(prog='rendre', description="Description text.")
    parser.add_argument(
        "-C","--cache-file",
        nargs="?", action="append",
        default="./.aurore/aurore.cache.json"
        )
    parser.add_argument(
        "-o","--output-file",
        nargs="?",
        default="-"
        )
    parser.add_argument("-B","--base-uri", default="")
    parser.add_argument("-E","--book-end", default=True)
    parser.add_argument("-F","--filter-any", nargs="?", action="extend")
    parser.add_argument("-A","--filter-all", nargs="?", action="append")
    parser.add_argument("-J","--JQ", nargs="?", action="extend")
    parser.add_argument("-d","--defaults")
    parser.add_argument("-v","--verbose", action="count", default=0)
    parser.add_argument("-q","--quiet", action="store_true",default=False)

    subparsers = parser.add_subparsers(title='subcommands') #,description='list of subcommands',help='additional help')
    
    #-List----------------------------------------------------------
    list_parser= subparsers.add_parser('list',
                        help='list resource metadata files.')
    list_parser.add_argument("-j",'--jq')
    list_parser.add_argument('--items',default=True,action="store_true")
    list_parser.add_argument('--templates', action="store_true")
    list_parser.add_argument('--categories',action="store_true")
    list_parser.add_argument("-i","--include-item",nargs="?", action="append")

    list_parser.add_argument("-f","--field",nargs="?",action="extend")
    list_parser.add_argument("fields",nargs="*",action="append")
    list_parser.set_defaults(template="tmpl-0004")
    list_parser.set_defaults(init=init_report)

    #-List----------------------------------------------------------
    list_parser= subparsers.add_parser('list',
                        help='list resource metadata files.')
    list_type = list_parser.add_mutually_exclusive_group()
    list_type.add_argument('--items',default=True,action="store_true")
    list_type.add_argument('--templates', action="store_true")
    list_type.add_argument('--categories',action="store_true")
    list_parser.add_argument("-i","--include-item",nargs="?", action="append")

    list_parser.add_argument("fields",
        default=[r"%i", "%t"],
        nargs="*",
        action="extend")

    list_parser.set_defaults(template="tmpl-0004")
    list_parser.set_defaults(init=init_report)
    
    #-Gallery----------------------------------------------------------
    gallery_parser= subparsers.add_parser('gallery',
                        help='generate gallery for resource metadata files.')
    gallery_parser.add_argument("-i","--include-item",nargs="?", action="append")

    gallery_parser.add_argument("-f","--field",nargs="?",action="append")
    gallery_parser.set_defaults(template="tmpl-0003")
    gallery_parser.set_defaults(init=init_report)

    #-Print----------------------------------------------------------
    print_parser= subparsers.add_parser('print',
                        help='print resources.')
    print_parser.add_argument("-i","--include-item",nargs="?", action="append")
    print_parser.add_argument("include-item",nargs="*",action="append")
    print_parser.add_argument("-t",'--templates', action="store_true")
    print_parser.add_argument("-c",'--categories',action="store_true")

    print_parser.add_argument("-f","--field",nargs="?",action="append")
    print_parser.set_defaults(template="tmpl-0004")
    print_parser.set_defaults(init=init_report)
    # report_parser.set_defaults(initfunc=report_header_std)

    #-Feed----------------------------------------------------------
    report_parser= subparsers.add_parser('feed',
                        help='report resource metadata files.')
    report_parser.add_argument("-t",'--template',default="tmpl-0004")
    report_parser.add_argument("-p","--print",nargs="+",action="extend",default=[])
    # report_parser.add_argument("-D","--collection", nargs="+", action="extend")
    report_parser.add_argument('--title')
    report_parser.set_defaults(init=init_report)
    # report_parser.set_defaults(initfunc=report_header_std)

    return parser.parse_args()

def _main_():
    args = parse_args()
    rendre(args)


if __name__ == "__main__": _main_()
