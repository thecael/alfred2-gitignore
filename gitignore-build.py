# encoding: utf-8
"""
Build a .gitignore file from a list of templates.

This script builds a .gitignore file from a list of template names. Each
template is looked up in the local clone of the github/gitignore repository,
and then written to a temporary .gitignore file.
"""
import hashlib
import os
import sys

from workflow import Workflow

workflow = Workflow()
repo_dir = workflow.datafile("gitignore")


def main(wf):
    """
    Build a .gitignore file from a list of templates.

    This method builds a .gitignore file from a list of templates, supplied as
    arguments to the script (i.e. argv). Each template name is compared against
    the templates in the github/gitignore repository, and if the names match,
    that .gitignore template is written to the temporary .gitignore file for
    the user.

    The scripts output on STDOUT is used by Alfred as the content of a
    notification. This way, the user can be notified of the build's result.

    :param wf: The workflow object
    """
    if len(sys.argv) < 2:
        print "No templates were selected, so nothing was built."
        return

    if not os.path.isdir(repo_dir):
        print "Please run gitignore-update first to download the templates."

    templates = sys.argv[1:]

    tmp_file_name = hashlib.md5(" ".join(templates)).hexdigest()
    tmp_file_path = "/tmp/" + tmp_file_name

    if os.path.isfile(tmp_file_path):
        os.system("open %s" % tmp_file_path)
        return

    formatted_templates = set()

    for t in templates:
        formatted_templates.add(t.lower() + ".gitignore")

    for root, dirs, files in os.walk(repo_dir):
        for name in files:
            if name.lower() in formatted_templates:
                with open(os.path.join(root, name)) as in_file:
                    with open(tmp_file_path, "a+") as out_file:
                        out_file.write("### %s\n\n" % name)
                        for line in in_file:
                            out_file.write(line)
                        out_file.write("\n\n")

    print "Successfully built .gitignore file. Have fun!"
    os.system("open %s" % tmp_file_path)
    return


if __name__ == u"__main__":
    sys.exit(workflow.run(main))
