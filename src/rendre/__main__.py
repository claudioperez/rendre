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
        "-D","--data-file",
        default="./.aurore/aurore.cache.json"
        )
    parser.add_argument(
        "-o","--output-file",
        nargs="?",
        default="-"
        )
    parser.add_argument("-B","--base-uri", default="")
    parser.add_argument("-E","--book-end", default=True)
    parser.add_argument("-F","--filter-any", nargs="?", action="append")
    # parser.add_argument("-J","--JQ", nargs="?", action="extend")
    parser.add_argument("-d","--defaults")
    parser.add_argument("-v","--verbose", action="count", default=0)
    parser.add_argument("-q","--quiet", action="store_true",default=False)

    subparsers = parser.add_subparsers(title='subcommands') #,description='list of subcommands',help='additional help')

    #-List----------------------------------------------------------
    list_parser= subparsers.add_parser('list',
                        help='list resource metadata files.')
    list_type = list_parser.add_mutually_exclusive_group()
    list_type.add_argument('--items',default=True,action="store_true")
    list_type.add_argument('--templates', action="store_true")
    list_type.add_argument('--categories',action="store_true")

    list_format = list_parser.add_mutually_exclusive_group()
    list_format.add_argument("--table",dest="format_table",default=True,action="store_true")
    list_format.add_argument("--long","--yaml",dest="format_yaml", default=False,action="store_true")
    list_format.add_argument("--json",dest="format_json",default=False,action="store_true")
    list_format.add_argument("--line",dest="format_line",default=False,action="store_true")

    list_parser.add_argument("-i","--include-item",nargs="?", action="append")
    list_parser.add_argument("-e","--include-exclusive",nargs="?", action="append")

    list_parser.add_argument("--flatten-fields",action="store_true",default=False)
    list_parser.add_argument("-s","--separator",default=", ")

    list_parser.add_argument("fields", nargs="*")

    list_parser.set_defaults(template="tmpl-0004")
    list_parser.set_defaults(init=init_report)

    #-Gallery----------------------------------------------------------
    gallery_parser= subparsers.add_parser('gallery',
                        help='generate gallery for resource metadata files.')
    gallery_parser.add_argument("-i","--include-item",nargs="?", action="append")
    gallery_parser.add_argument("-e","--include-exclusive",nargs="?", action="append")

    gallery_parser.add_argument("-f","--field",nargs="?",action="append")
    gallery_parser.set_defaults(template="tmpl-0003")
    gallery_parser.set_defaults(init=init_report)

    #-Print----------------------------------------------------------
    print_parser= subparsers.add_parser('print', help='print resources.')
    print_parser.add_argument("-i","--include-item",nargs="?", action="append")
    print_parser.add_argument("-e","--include-exclusive",nargs="?", action="append")
    print_parser.add_argument("include-item",nargs="*",action="append")
    print_parser.add_argument("-t",'--templates', action="store_true")
    print_parser.add_argument("-c",'--categories',action="store_true")

    print_parser.add_argument("-f","--field",nargs="?",action="append")
    print_parser.set_defaults(template="tmpl-0004")
    print_parser.set_defaults(init=init_report)
    # report_parser.set_defaults(initfunc=report_header_std)


    return parser.parse_args()

def _main_():
    args = parse_args()
    rendre(args)


if __name__ == "__main__": _main_()
