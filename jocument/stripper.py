'''
'''

import nbconvert
import nbformat

from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup


BLOG_CSS = '''
<style type="text/css">

a.anchor-link {
    visibility: hidden;
}

div.labelcaption {
        text-align: center;
        font-style: italic;
        font-size: smaller;
        padding: 0px;
        margin: 0 auto;
        width: 50%;
}
ul {
    list-style: disc;
    text-indent: 0;
}
</style>
'''


def strip_and_save_html(html):
    ''' Takes the HTML from converting a notebook to HTML and use Beautiful Soup to
        identify those bits of the file that we want to keep.  These are concatenated
        and then written out to a file and also copied to the clipboard
        for more easily paste into the control panel at www.cantabcapital.com
    '''
    print('Writing specialised blog css')
    soup = BeautifulSoup(html, 'html.parser')
    output_soup = BeautifulSoup(BLOG_CSS, 'html.parser')
    for i, cell_div in enumerate(soup.find_all(class_="cell")):
        print('Outputting cell {}'.format(i))
        # Rewrite footnotes
        html_output = cell_div.find(class_="text_cell_render")
        if html_output is not None:
            output_soup.append(html_output)
        output_areas = cell_div.find_all(class_="output_subarea")
        for output_area in output_areas:
            output_soup.append(output_area)
    output_lines = output_soup.prettify().splitlines()
    output_file_path = dialog_select_file(title='Output Stripped HTML file Name',
                                          starting_directory=user_home_path(),
                                          for_write=True)
    if len(output_file_path) != 0:
        if not output_file_path.endswith('.html'):
            output_file_path = output_file_path + '.html'
        print(f'Writing {output_file_path}')
        with open(output_file_path, 'wt') as output_file:
            output_file.write('\n'.join(output_lines))
    print('Stripped html written to clipboard')
    QApplication.clipboard().setText('\n'.join(output_lines))


def get_file_for_blog():
    ''' Export a notebook to HTML within Jupyter Notebook and then use this function.

        The exported file is stored in 'H:/.ccp/Exodus_Chrome/Downloads" normally (don't ask why)

        Then call strip_and_save_html() and do the conversion.
    '''
    input_file_path = dialog_select_file(title='Select Input HTML File for Conversion',
                                         starting_directory=user_home_path())
    if len(input_file_path) == 0:
        return
    print(f'Reading {input_file_path}')
    with open(input_file_path, 'rt') as input_file:
        html = input_file.read()
    strip_and_save_html(html)


def get_script_for_blog():
    ''' Open the script dialog, showing the visible scripts in the current database path
        for this user.  Load the notebook script, use nbconvert to convert it
        to HTML and then call strip_and_save_html() to turn it into a suitable
        format for the blogs.
    '''
    visible_scripts = pydb.get_visible_scripts()
    items = [pydb.Script.get(x).path for x in visible_scripts.keys() if x.endswith('.ipynb')]
    script_name = dialog_list_searchable(sorted(items, key=lambda x: x.lower()),
                                         title='Notebooks in your current path',
                                         allow_multiple_selection=False)
    if script_name is None:
        return
    script = pydb.Script.get(script_name)
    notebook = nbformat.reads(script.contents, as_version=4)
    html_exporter = nbconvert.HTMLExporter()
    html_exporter.template_file = 'basic'
    # Process the notebook we loaded earlier
    (html, resources) = html_exporter.from_notebook_node(notebook)
    strip_and_save_html(html)


def main():
    ''' The main function.  It's called main because it's the main man '''
    choices = ['Load HTML from File', 'Load Script']
    if open_single_dropdown_dialog(choices) == choices[1]:
        get_script_for_blog()
    else:
        get_file_for_blog()

if __name__ == '__main__':
    main()