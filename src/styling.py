# -*- coding: utf-8 -*-
"""Styling documentation


"""
import datetime
from typing import List

import IPython
from IPython.core.magic import Magics, line_magic, magics_class

class JocumentError(TypeError):
    ''' An error from the jocument styling system '''


class CenterOutput():
    ''' Center HTML representation of multiple objects in Jupyter notebook '''

    def __init__(self, *args):
        self.args: List = args

    def _repr_html_(self):
        ''' Return the html representation of each object centered '''
        retlist: List[str] = []
        for arg in self.args:
            if hasattr(arg, '_repr_html_'):
                retlist.append(arg._repr_html_()) #pylint: disable=protected-access
            else:
                retlist.append(str(arg))
        return '\n'.join([f'<center>{x}</center>' for x in retlist])

    def __repr__(self):
        ''' The string representation '''
        return '\n\n'.join([repr(arg)
                            for arg in self.args])


@magics_class
class _JocumentMagics(Magics):
    ''' This is the class that defines all the special magics required for our installation
        of Jupyter
    '''

    def _parse_args(self, line: str, expected: int) -> List[str]:
        ''' Parse a line arg sent to a magic where args are delimited by the pipe
            symbol
        '''
        args: List[str] = line.split('|')
        if len(args) != expected:
            raise JocumentError(f'Expected {expected} arguments in {line}.  Found {len(args)}')
        return args

    def _prepare_return(self, html: str) -> str:
        ''' Do all the magic required to return the HTML correctly.

                This proved to be a real ball ache.  It turns out that
                a) It's hard to get Jupyter to just output
                    the CSS once or set up a site wide custom CSS
                b) For some reason, NB convert gets confused with
                    embedded HTML in markdown cells
                   *but only if there is more than one line and it begins
                   with a space*.  WTF?

        '''
        return IPython.display.display_html(html.replace('\n', ' ').strip(), raw=True)

    @line_magic
    def centerplots(self):
        ''' A little line magic which will horizontally center your matplot output in the
            notebook.  This looks better than left aligned plots.
        '''
        center_css = """
            .output_png img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            }
            """
        return self._prepare_return(f'<style>{center_css}</style>')

    @line_magic
    def pageheader(self, line: str) -> str:
        ''' Create and display a napkin style PageHeaderContinuation display.
            Called with a single parameter either as
                %pageheader The Remainder Of the Line Is The title
            in code cells or
                {{%pageheader The Remainder Of The Line Is the Title}}
            in markdown cells.
        '''
        args: List[str] = self._parse_args(line, 1)
        html: str = '''
                <div class="pageheader">
                    <span class="maintext">{}</span>
            </div>'''.format(args[0])
        return self._prepare_return(html)

    @line_magic
    def titleblock(self, line: str) -> str:
        ''' Create and display a standard document header display.

            Magics only pass the remainder of the line to to pass multiple arguments
            you use the '|' pipe symbol.

            In a markdown cell one has
                {{%titleblock The Title Of the Document|The Subtitle Of The Document|The Author}}
            The second two arguments are optional
        '''
        args: List[str] = self._parse_args(line, 3)
        html: str = '''
            <div class="title_block">
                <div class="navigator">
                    <span class="title">{}</span>
                    <span class="date">{}</span>
                </div>
            </div>
            <div class="notebook_subtitle">{}</div>
            <div class="notebook_author">{}</div>'''.format(args[0],
                                                            datetime.date.today(),
                                                            args[1],
                                                            args[2])
        return self._prepare_return(html)

    @line_magic
    def frontpage(self, line: str) -> str:
        ''' Create and display a napkin style FrontPage display.
            Magics only pass the remainder of the line to to pass multiple arguments
            you use the '|' pipe symbol.

            In a markdown cell one has
                {{%titleblock The Title Of the Document|The Subtitle Of The Document|The Author}}
            The second two arguments are optional
        '''
        args: List[str] = self._parse_args(line, 3)
        html = '''
            <div class="front_page">
                <div class="front_band">
                    <div class="maintext1">{}</div>
                    <div class="maintext2">{}</div>
                    <div class="maintext3">{}</div>
                </div>
            </div>'''.format(args[0], args[1], args[2])
        return self._prepare_return(html)

    @line_magic
    def sectionpage(self, line: str) -> str:
        ''' Create and display a SectionPage display.
            Depends on being able to display HTML in the notebook.
        '''
        args: List[str] = self._parse_args(line, 3)
        html = '''
            <div class="section_page">
                <div class="section_band">
                    <div class="maintext1">{}</div>
                    <div class="maintext2">{}</div>
                    <div class="maintext3">{}</div>
                </div>
            </div>'''.format(args[0], args[1], args[2])
        return self._prepare_return(html)


    @line_magic
    def prompt(self, line):
        ''' Set up the prompts.
            Used as
                %prompt off
            or
                %prompt on (or indeed any other string other than 'off')

        '''
        args: List[str] = self._parse_args(line, 1)
        if args[0] == "off":
            output = '<style>div.prompt {display:none}</style>'
        else:
            output = '<style>div.prompt {display:block}</style>'
        return self._prepare_return(output)

    @line_magic
    def j_css(self, filename):
        ''' Output the CSS for the styling bits '''
        css = CSS_PAGE
        if len(filename) > 0:
            try:
                with open(filename, 'r') as f:
                    css = f.read(filename)
            except FileNotFoundError:
                css = f'<h3 style="textcolor: red"> CSS file {filename} not found'
        self._prepare_return(css)

# Register our magic functions
_IPYTHON = IPython.core.getipython.get_ipython()
if _IPYTHON is not None:
    _IPYTHON.register_magics(_JocumentMagics)

# And set up the CSS_page
CSS_PAGE = '''
    <style>
    div.labelcaption {
        text-align: center;
        font-style: italic;
        font-size: smaller;
        padding: 0px;
        margin: 0 auto;
        width: 50%;
    }


    /*************************
    The Title Block for a report
    **************************/
    div.title_block{
        -webkit-print-color-adjust: exact;
        position:relative;
        background-image: linear-gradient(to bottom right, #667D83,
                                            #B3C7BF) !important;
        height:210px !important;
        color:white;
        line-height:1em;
    }

     div.title_block div.logo{
        height:             75%;
    }

    div.title_block div.navigator{
        position:absolute;
        height:25%;
        bottom:0px;
        width:100%;
        background-color:   rgba(50, 50, 50, 0.7) !important;
    }

    div.title_block span.title{
        text-transform: uppercase;
        font-size:2em;
        position: absolute;
        bottom: 40%;
        left: 1em;
    }

    div.title_block span.date{
        text-transform: capitalize;
        font-size:1.5em;
        position: absolute;
        bottom: 40%;
        right: 1em;
    }

    div.notebook_subtitle{
        text-transform:uppercase;
        margin-top:2em;
        margin-bottom:1em;
        font-size:2em;
        font-weight:bold;
        text-align:center;
    }

    div.notebook_author{
        font-weight:bold;
        text-align:center;
        margin-bottom:3em;
    }

    /*************************
    Page Headers
    **************************/

    div.pageheader{
        -webkit-print-color-adjust:exact !important;
        height: 50px;
        width: 100% !important;
        border-bottom-style: solid;
        border-bottom-width: thin;
        border-bottom-color: #667D83;
    }

    div.pageheader span.maintext{
        color:          #B3C7BF;
        position:       relative;
        font-size:      1.5em;
        bottom:         0%;
        vertical-align:  bottom;
    }



    /*************************
    The Presentation Section Pages
    **************************/

    div.section_page{
        height:             80vh;
        background-color:   rgb(255, 255, 255);
        background-position: right bottom;
        background-repeat:  no-repeat;
    }

    div.section_page div.section_band{
        background-color:   rgba(80, 87, 92, 0.7);
        position:           relative;
        top:                30%;
        height:             40%;
        width:              100%;
    }

    div.section_band div.section_text{
        position: relative;
        color: #FFFFFF;
        top: 25%;
        left: 10%;
        width: 80%;
        font-size: 2em;
    }

    div.section_band div.maintext1 {
        position: relative;
        color: #FFFFFF;
        top: 20%;
        left: 10%;
        width: 80%;
        font-size: 2em;
    }
    div.section_band div.maintext2 {
        position: relative;
        color: #FFFFFF;
        top: 40%;
        left: 10%;
        width: 80%;
        font-size: 2em;
    }
    div.section_band div.maintext3 {
        position: relative;
        color: #FFFFFF;
        top: 60%;
        left: 10%;
        width: 80%;
        font-size: 2em;
    }

     /*********************************************
     Presentation Cover Pages
     *****************************************************/
    div.front_page{
        height:             80vh;
        background-color:   rgb(128, 128, 128);
        background-position: right bottom;
        background-repeat:  no-repeat;
        width: 100% !important;
    }

    div.front_page div.front_band{
        background-color:   rgba(80, 87, 92, 0.7);
        position:           relative;
        top:                30%;
        height:             40%;
        width:              100%;
    }

    div.front_band div.front_text{
        position: relative;
        color: #FFFFFF;
        top: 25%;
        left: 10%;
        width: 80%;
        font-size: 2em;
    }

    div.front_band div.maintext1 {
        position: relative;
        color: #FFFFFF;
        top: 20%;
        left: 10%;
        width: 80%;
        font-size: 1.5em;
    }
    div.front_band div.maintext2 {
        position: relative;
        color: #FFFFFF;
        top: 30%;
        left: 10%;
        width: 80%;
        font-size: 1.5em;
    }
    div.front_band div.maintext3 {
        position: relative;
        color: #FFFFFF;
        top: 40%;
        left: 10%;
        width: 80%;
        font-size: 1.5em;
    }
    </style>
'''.replace('\n', ' ').strip()
