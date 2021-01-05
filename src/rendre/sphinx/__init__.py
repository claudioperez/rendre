import re
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
    # arg_pat = re.compile('^\s*:(.+):(.+)$')
    arg_pat = re.compile('^\s*:([A-z-]+):(.+)$')
    option_spec = {
        k.replace("--",""): str  
          for k in parser._option_string_actions 
            if "--" in k
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
        template = fields.replace("--link","").strip()
        field_pointers = [f for f in template.split("/") if "%" in f]
        filt_args = [x for pair in arg_pairs for x in pair 
            if pair[0] in ["include-item","exclusive-include"] ]
        filt_args = ["--" + x if (i+1)%2 else x.strip() for i, x in enumerate(filt_args)]
        args = parser.parse_args([*base_args, "list", "-s"," =^= ",*filt_args,"--"," ".join(field_pointers)])
        items = rendre(args).strip()
        res = []
        for item in items.split("\n"):
            link = template
            for i,sub in enumerate(item.split("=^=")):
                link = link.replace(field_pointers[i],sub)
            res.append(link)
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
        base_args = self.format_arg_options([
            i for k_v in self.options.items() for i in k_v
        ])
        arg_pairs = [self.arg_pat.match(arg).groups() for arg in self.content]
        cmd_args = self.format_arg_options(self.proc_args(arg_pairs))

        # create HTML output
        parsed_args = parser.parse_args([*base_args, "-vv", cmd, "--html", *cmd_args])
        html_attributes = {"format": "html"}
        try:
        #     "a"+0
        # except:
            html:str = rendre(parsed_args,config=config)
        except Exception as e:
            logger.error(e)
            return [nodes.raw("", e, format="html")]
        else:
        # if True:
            html_node = nodes.raw("", html, **html_attributes)
            (html_node.source,
            html_node.line) = self.state_machine.get_source_and_line(self.lineno)

            # create LaTeX output
            parsed_args = parser.parse_args([*base_args, cmd, "--latex", *cmd_args])
            latex:str = rendre(parsed_args,config=config)
            print(f"LaTeX: \n{latex}")
            latex_node = nodes.raw("", latex, format="latex")
            latex_node.source, latex_node.line = html_node.source, html_node.line

            if "--link" in cmd_args:
                # print(f"\n\nLinking page...\n\n")
                link = cmd_args[cmd_args.index("--link")+1]
                self.content = self.run_link(base_args,arg_pairs,link)
                self.options = {"hidden": True, "glob": True}
                toc = super().run()
            else:
                toc = []
            return [*toc, latex_node, html_node]


