import re, os
import warnings

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.other import TocTree
from sphinx.util import logging

from rendre.__main__ import create_parser
from rendre import rendre, __version__

parser = create_parser()

logger = logging.getLogger(__name__)

def setup(app):
    app.add_config_value('rendre_config', {}, 'html')
    app.add_config_value('rendre_links', {}, 'html')
    app.add_directive('rendre', SphinxRendre)
    return {'version': __version__}

class SphinxRendre(TocTree):
    """

    """
    arg_pat = re.compile('^\s*:([A-z-]+):(.+)$')
    option_spec = {
        k.replace("--",""): str
          for k in parser._option_string_actions if "--" in k
    }
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True

    def proc_args(self, arg_pairs)->list:
        """create flat list of alternating option strings and values"""
        return [x.strip() for pair in arg_pairs for x in pair]

    def format_arg_options(self,args: list)->list:
        """append "--" indicator to option strings"""
        return ["--"+arg if (i-1)%2 else arg for i, arg in enumerate(args)]

    def run_link(self,base_args,arg_pairs,fields):
        """
        Create links for items as if they were included in a `toctree` call
        """
        template = fields.replace("--link","").strip()
        filt_args = [x for pair in arg_pairs for x in pair
            if pair[0] in ["include-item","exclusive-include"] ]
        filt_args = ["--" + x if (i+1)%2 else x.strip() for i, x in enumerate(filt_args)]
        args = parser.parse_args([*base_args, "path", "--sort","--no-quotes", *filt_args,"--",template])
        items = rendre(args).strip()
        logger.debug(f"run_link:items : {items}")
        res = [
            i.strip()[2:] if i[:2]=="./" else i.strip() for i in items.split("\n")
        ]
        return res


    def run(self):
        config = self.state.document.settings.env.config.rendre_config
        config.update({
            "base_uri":
                self.state.document.settings.env.app.srcdir,
                # self.state.document.settings.env.app.builder.get_target_uri(
                #     self.state.document.settings.env.docname
                # ),
            "src_uri":
                self.state.document.settings.env.app.srcdir
            })
        cmd = self.arguments[0]
        if "verbose" in self.options:
            verbosity:int = self.options["verbose"]
            del self.options["verbose"]
        else:
            verbosity = 0


        base_args = self.format_arg_options([
            i for k_v in self.options.items() for i in k_v
        ])

        if verbosity:
            base_args.append("-"+"".join(["v"]*int(verbosity)))

        arg_pairs = [self.arg_pat.match(arg).groups() for arg in self.content]
        cmd_args = self.format_arg_options(self.proc_args(arg_pairs))

        # create HTML output
        parsed_args = parser.parse_args([*base_args, cmd, "--html", *cmd_args])
        html_attributes = {"format": "html"}
        try:
            html:str = rendre(parsed_args,config=config)
        except Exception as e:
            logger.error(e)
            return [nodes.raw("", e, format="html")]
        else:
            html_node = nodes.raw("", html, **html_attributes)
            (html_node.source,
            html_node.line) = self.state_machine.get_source_and_line(self.lineno)

            # create LaTeX output
            parsed_args = parser.parse_args([*base_args, cmd, "--latex", *cmd_args])
            latex:str = rendre(parsed_args,config=config)
            # print(f"LaTeX: \n{latex}")
            latex_node = nodes.raw("", latex, format="latex")
            latex_node.source, latex_node.line = html_node.source, html_node.line

            if "--link" in cmd_args:
                # print(f"\n\nLinking page...\n\n")
                link = cmd_args[cmd_args.index("--link")+1]
                self.content = self.run_link(base_args,arg_pairs,link)
                self.options = {"hidden": True, "glob": True, "numbered": False}
                toc = super().run()
            else:
                toc = []
            return [*toc, latex_node, html_node]


