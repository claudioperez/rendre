import re
import warnings
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.other import TocTree
from sphinx.util import logging

from rendre.__main__ import create_parser
from rendre import rendre

parser = create_parser()

logger = logging.getLogger(__name__)

def setup(app):
    app.add_config_value('rendre_config', {}, 'html')
    app.add_config_value('rendre_links', {}, 'html')
    app.add_directive('rendre', SphinxRendre)
    return {'version': '0.0.0'}

class SphinxRendre(TocTree):
    """
    Directive to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents like tree in the current document. This
    version filters the entries based on a list of prefixes. We simply filter
    the content of the directive and call the super's version of run. The
    list of exclusions is stored in the **toc_filter_exclusion** list. Any
    table of content entry prefixed by one of these strings will be excluded.
    If `toc_filter_exclusion=['secret','draft']` then all toc entries of the
    form `:secret:ultra-api` or `:draft:new-features` will be excuded from
    the final table of contents. Entries without a prefix are always included.
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
        # print(f"FIELD Points: {field_pointers}\n\n")
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
        print(f"URI: {self.state.document.settings.env.app.builder}")
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
        # print(f"URI:\n{directives.uri('qfem-0001/qfem-0001.png')}")

        # create HTML output
        # parsed_args = parser.parse_args([*base_args, cmd, *cmd_args])
        parsed_args = parser.parse_args([*base_args, "-vv", cmd, "--html", *cmd_args])
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
            parsed_args = parser.parse_args([*base_args, cmd, *cmd_args])
            latex:str = rendre(parsed_args,config=config)
            # print(f"LaTeX: \n{latex}")
            latex_node = nodes.raw("", latex, format="latex")
            latex_node.source, latex_node.line = html_node.source, html_node.line

            if "--link" in cmd_args:
                link = cmd_args[cmd_args.index("--link")+1]
                self.content = self.run_link(base_args,arg_pairs,link)
                self.options = {"hidden": True, "glob": True}
                toc = super().run()
                # print(toc)
            else:
                toc = []
            return [*toc, latex_node, html_node]
