# encoding: utf-8
"""
Incrementally build up a list of template names using Alfred.

This script is responsible for incrementally creating the list of template
names the user wants to combine into a single file. It works heavily with the
workflow module and Alfred to achieve this result.

The user can enter the name of templates in Alfred's dialog, and using fuzzy
matching, suggestions are presented based on the available templates in the
github/gitignore repository.
"""
import argparse
import sys

from workflow import Workflow, ICON_WARNING

workflow = Workflow()


def main(wf):
    """
    Incrementally build up list of templates.

    The user can enter the names of templates he wants to combine into a single
    file using Alfred's dialog. This method is responsible for presenting the
    auto-complete options in Alfred as well as building a final string that is
    passed along to the build module.

    :param wf:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='*', default=None)

    args = parser.parse_args(wf.args)
    templates = wf.stored_data("templates")

    if len is None:
        wf.add_item(
            title="Templates missing",
            subtitle=(
                "Please run gitignore-update to install the templates..."
            ),
            icon=ICON_WARNING,
            valid=False
        )
    else:
        if args.query:
            query = args.query
            input = query[-1]
            current_query = " ".join(query[:-1])

            filtered_templates = [
                i for i in templates if input.lower() in i.lower()
            ]

            if len(filtered_templates) >= 1:
                templates = filtered_templates

            wf.add_item(
                title="Build .gitignore file",
                subtitle=(
                    "Combine the chosen templates to a single .gitignore "
                    "file..."
                ),
                uid="build_gitignore",
                arg=" ".join(query),
                valid=True,
            )

            for i in templates:
                add_template(i, query=current_query)
        else:
            for i in templates:
                add_template(i)

    wf.send_feedback()


def add_template(template_name, query=""):
    """
    Add template in Alfred interface.

    This function adds the given template as a new item to Alfred's XML output.

    :param template_name: The template to add
    :param query: The current query
    """
    autocomplete = build_autocomplete(template_name, query)

    workflow.add_item(
        title=template_name,
        uid=template_name,
        autocomplete=autocomplete,
        valid=False
    )


def build_autocomplete(template_name, query):
    """
    Build the autocomplete string.

    From the template name and the current query a new string is built that can
    be used as the value for an item's autocomplete attribute.

    :param template_name: The template to add
    :param query: The complete query
    :return: The new query
    """
    if len(query) > 0:
        autocomplete = " ".join([query, template_name])
    else:
        autocomplete = template_name

    return " ".join([autocomplete, ""])


if __name__ == u"__main__":
    sys.exit(workflow.run(main))
