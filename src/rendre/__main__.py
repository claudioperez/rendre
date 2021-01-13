#!/usr/bin/env python
import argparse
from rendre import rendre
from .report import init_report
from .api import \
    post_init, post_close, \
    get_init, get_item, get_close


def pass_item(item, args, config, accum:dict)->dict:
    return accum


def create_parser():
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
    parser.add_argument("-l","--load-defaults", help="load defaults from a specified file.")
    parser.add_argument("-d","--default-set", help="identify a previously named set of defaults.")
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
    list_parser.add_argument("-x","--exclude-item",nargs="?", action="append")
    list_parser.add_argument("-e","--include-exclusive",nargs="?", action="append")

    list_parser.add_argument("--flatten-fields",action="store_true",default=False)
    list_parser.add_argument("-s","--separator",default=", ")
    list_parser.add_argument("-j","--join-items",default="\n")

    list_parser.add_argument("fields", nargs="*")

    list_parser.set_defaults(template="tmpl-0004")
    list_parser.set_defaults(init=init_report)
    
    #-PATH----------------------------------------------------------
    path_parser= subparsers.add_parser('path',
                        help='generate paths.')
    path_type = path_parser.add_mutually_exclusive_group()

    path_type.add_argument('--pointer-delimeter',default=":")

    path_format = path_parser.add_mutually_exclusive_group()
    path_format.add_argument("--table",dest="format_table",default=True,action="store_true")
    path_format.add_argument("--flat",dest="format_flat",default=False,action="store_true")
    # path_format.add_argument("--long","--yaml",dest="format_yaml", default=False,action="store_true")
    # path_format.add_argument("--json",dest="format_json",default=False,action="store_true")

    path_parser.add_argument("-i","--include-item",nargs="?", action="append")
    path_parser.add_argument("-x","--exclude-item",nargs="?", action="append")
    path_parser.add_argument("-e","--include-exclusive",nargs="?", action="append")

    path_parser.add_argument("--unpack-fields",action="store_true",default=True)
    path_parser.add_argument("-s","--separator",default=" ")
    path_parser.add_argument("-j","--join-items",default="\n")

    path_parser.add_argument("paths", nargs="*")

    path_parser.set_defaults(template="tmpl-0008")
    path_parser.set_defaults(init=init_report)

    #-Gallery-------------------------------------------------------
    gallery_parser= subparsers.add_parser('filtered-gallery',
                        help='generate a filtered gallery.')
    gallery_type = gallery_parser.add_mutually_exclusive_group()
    gallery_type.add_argument('--items',default=True,action="store_true")
    # gallery_type.add_argument('--templates', action="store_true")
    # gallery_type.add_argument('--categories',action="store_true")

    gallery_format = gallery_parser.add_mutually_exclusive_group()
    gallery_format.add_argument("--html",dest="format_html",default=True,action="store_true")
    gallery_format.add_argument("--long","--yaml",dest="format_yaml", default=False,action="store_true")
    gallery_format.add_argument("--json",dest="format_json",default=False,action="store_true")
    gallery_format.add_argument("--latex",dest="format_latex",default=False,action="store_true")

    gallery_parser.add_argument("-i","--include-item",nargs="?", action="append")
    gallery_parser.add_argument("-x","--exclude-item",nargs="?", action="append")
    gallery_parser.add_argument("-e","--include-exclusive",nargs="?", action="append")

    gallery_parser.add_argument("--flatten-fields",action="store_true",default=False)
    gallery_parser.add_argument("-s","--separator",default=", ")
    gallery_parser.add_argument("-j","--join-items",default="\n")
    
    gallery_parser.add_argument("--link",default="")

    gallery_parser.add_argument("fields", nargs="*")

    gallery_parser.set_defaults(template="tmpl-0007")
    gallery_parser.set_defaults(init=init_report)

    #-CLI-Gallery----------------------------------------------------------
    cli_gallery_parser= subparsers.add_parser('cli-gallery',
                        help='generate gallery for resource metadata files.')
    cli_gallery_format = cli_gallery_parser.add_mutually_exclusive_group()
    cli_gallery_format.add_argument("--html",dest="format_html",default=True,action="store_true")
    cli_gallery_format.add_argument("--long","--yaml",dest="format_yaml", default=False,action="store_true")
    cli_gallery_format.add_argument("--json",dest="format_json",default=False,action="store_true")
    cli_gallery_format.add_argument("--latex",dest="format_latex",default=False,action="store_true")

    cli_gallery_parser.add_argument("-i","--include-item",nargs="?", action="append")
    cli_gallery_parser.add_argument("-x","--exclude-item",nargs="?", action="append")
    cli_gallery_parser.add_argument("-e","--include-exclusive",nargs="?", action="append")

    cli_gallery_parser.add_argument("-f","--field",nargs="?",action="append")
    cli_gallery_parser.set_defaults(template="tmpl-0003")
    cli_gallery_parser.set_defaults(init=init_report)

    return parser

def _main_():
    import sys
    args = create_parser().parse_args()
    output = rendre(args)
    
    if args.output_file == "-":
        sys.stdout.write(output)
    else:
        with open(args.output_file, "w") as f:
            f.write(output)



if __name__ == "__main__": _main_()
