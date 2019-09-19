# -*- coding: utf-8 -*-
"""References documentation

"""
from typing import Tuple, List, Dict


class JocumentStyle():
    ''' A class designed to be used only as a singleton which defines the
        formatting and CSS to be used with the Jocument helper classes and
        functions
    '''

    def footnote_reference(self, number: int, name: str, text: str) -> str: #pylint: disable=unused-argument
        '''Formats the footnote reference in the text

        Args:
            number: The numeric reference to the footnote
            name: The friendly name that you called the footnote
            text: The footnote text.  It is rare to output this where
                the footnote is defined although if you want to do
                some javascript magic and make
                your footnotes pop up windows then this text will be useful.

        Returns:
            A raw HTML string.

        The default implementation returns::

            f'<sup><a id=fnret_{number} href=#fn_{number}>{number}</a></sup>'

        This is a superscript number which is hyperlinked to a location
        with id :code:`fn_<the number>`
    '''
        return f'<sup><a id=fnret_{number} href=#fn_{number}>{number}</a></sup>'

    def footnote_number(self, number: int) -> str:
        '''Formats the just the number of the footnote

        Args:
            number (int): The numeric reference to the footnote

        Returns:
            A raw HTML string.

        The default implementation returns::

                f'<a id=fnret_{number} href=#fn_{number}>{number}</a>'

        This is a superscript number which is hyperlinked to a location
        with id :code:`fn_<the number>`
    '''
        return f'<a id=fnret_{number} href=#fn_{number}>{number}</a>'

    def footnotes_start(self) -> str:
        ''' Called at the beginning of outputting footnotes

        Returns:
            A raw HTML string.

        The default implementation returns::

                <ol>
        '''
        return '<ol>'

    def footnote_output(self, number: int, name: str, text: str) -> str: #pylint: disable=unused-argument
        '''Output one footnote

        Args:
            number (int): The numeric reference to the footnote
            name (str): The friendly name that you called the footnote
            text (str): The footnote text.
        Returns:
            A raw HTML string.

        The default implementation returns::

            f'<li id=fn_{number}>{text}<a href=#fnret_{number}>&#8629;</a></li>' # noqa 501

        This is a superscript number which is hyperlinked to a location
        with id fn_<the number>
        '''
        return f'<li id=fn_{number}>{text}<a href=#fnret_{number}>&#8629;</a></li>' # noqa 501

    def footnotes_end(self):
        ''' Called at the end beginning of outputting footnotes

        Returns:
            A raw HTML string.

        The default implementation returns::

                </ol>
        '''
        return '</ol>'

    def cite(self, number: int, name: str, reference: tuple) -> str: #pylint: disable=unused-argument
        '''Format a citation in the text.

        Args:
            number: The number of this reference
            name: The friendly name of this reference
            reference: A three tuple of strings consisting of Author, Title
                        and Source

        Returns:
            A raw HTML string.

        The default implementation returns::

            f'<a id=citeret_{number} href=#cite_{number}>[{number}]</a>'
        '''
        return f'<a id=citeret_{number} href=#cite_{number}>[{number}]</a>'

    def references_start(self) -> str:
        ''' Called at the beginning of outputting references

        Returns:
            A raw HTML string.

        The default implementation returns::

                <ol>
        '''
        return '<ol>'

    def reference_output(self, number: int, name: str, ref: Tuple) -> str: #pylint: disable=unused-argument
        '''Output one reference

        Args:
            number: The numeric reference to the footnote
            name: The friendly name that you called the footnote
            ref A three tuple of (author, title, source).

        Returns:
            A raw HTML string.

        The default implementation formats the reference as as
        string **Author**, *Title*, Source and returns a list item::

            ref_str = f'<strong>{ref[0]}</strong>, <em>{ref[1]}</em>, {ref[2]}' # noqa 501
            f'<li id=cite_{number}>{ref_str}<a href=#citeret_{number}>&#8629;</a></li>' # noqa 501

        '''
        ref_str = '<strong>{0}</strong>, <em>{1}</em>, {2}'.format(*ref)
        return (f'<li id=cite_{number}>{ref_str}<a href=#citeret_{number}>&#8629;'
                f'</a></li>')

    def references_end(self):
        ''' Called at the end beginning of outputting footnotes

        Returns:
            A raw HTML string.

        The default implementation returns::

                </ol>
        '''
        return '</ol>'

    def label(self, ref_type: str, number: int, name: str, title: str) -> str: #pylint: disable=unused-argument
        ''' The styler for a Label.

            Typically these are charts, graphs or tables and so
            we want the type, the number and maybe the title.

            The default implemention returns::

                f'<div class="labelcaption" id=ref_{ref_type}{number}><{ref_type} {number}<br>{title}</div>'  #pylint: disable=line-too-long

            if the title has been set otherwise, if it's none it returns::

                f'<div class="labelcaption" id=ref_{ref_type}{number}><{ref_type} {number}</div>' # noqa 501

            By default, if you use the standard jocument styling magics
            then the css for labelcaption is::

                div.labelcaption {
                    text-align: center;
                    font-style: italic;
                    font-size: smaller;
                    padding: 0px;
                    margin: 0 auto;
                    width: 50%;
                    }

            Although this can obviously be changed.
        '''
        style = 'text-align: center;font-style: italic;font-size: smaller;padding: 0px;margin: 0 auto;width: 50%;'
        caption_html = (f'<div style="{style}" id=ref_{ref_type}{number}>'
                        f'{ref_type} {number}')
        caption_html += f'<br>{title}</div>' if title is not None else '</div>'
        return caption_html

    def label_ref(self, ref_type: str, number: int) -> str:
        ''' The Styling for a label reference in the text

            The default implementation returns::

                f'<a href=#ref_{ref_type}{number}>{ref_type} {number}</a>'

            i.e. of the ref_type is "Figure" then this will return "Figure 1".

            This will be hyperlinked to the actual figure, chart,
            table etc in the text.
        '''

        return f'<a href=#ref_{ref_type}{number}>{ref_type} {number}</a>'


class Footnotes():
    ''' A little class to do footnotes (or strictly end notes)

        Usage is as follows::

            footnotes = Footnotes()
            footnotes.add('the_note_label',
                          "This is the footnote text.")


        Generally footnotes should all be in one code cell at the beginning
        of the notebook but if they don't have to be. For convenience they
        should be in a cell *after* the creation of the Footnotes object
        and *before* you start to reference the footnotes.

        When you want to output the footnotes create a markdown cell with::

            ### Footnotes
            {{footnotes.output()}}


        The default template outputs ordered list will be
        inserted with the footnotes as list items and a hyper
        link to return to the text.

        Earlier on in the text, one can put in the footnote by
        adding :code:`{{footnotes.ref('the_note_label')}}` in the markdown.
        The default template inserts a numeric
        reference to the note in superscript
        with a hyperlink to the correct footnote.
    '''

    def __init__(self, styler: JocumentStyle = None):
        if styler is None:
            self.styler: JocumentStyle = JocumentStyle()
        else:
            self.styler = styler
        self.names: List = []
        self.name_fn_map: Dict = {}

    def add(self, name: str, note_text: str) -> None:
        ''' Make a new footnote

        Args:
            name: A friendly name that you can use in the text
            note_text: The footnote text.

        Returns:
            None
        '''
        self.name_fn_map[name] = note_text.replace('\n', ' ')

    def ref(self, name: str) -> str:
        ''' Reference the footnote in the text

        Args:
            name: The friendly name.

        Returns:
            The html for the reference.  Calls
            :py:class:`JocumentStyle.footnote_reference`
        '''
        try:
            if name not in self.names:
                self.names.append(name)
            number = self.names.index(name) + 1
            return self.styler.footnote_reference(number, name,
                                                  self.name_fn_map[name])
        except ValueError:
            return '<sup>**"{}" not found**</sup>'.format(name)

    def num(self, name: str) -> str:
        ''' Output the number of the footnote to refer to it in the text.

            This would be used where you have already defined the footnote and
            rather than having it displayed as hyperlink you wish to write text
            like "This point is expanded more fully in
            Footnote {{footnotes.num('expanded_argument)}}" for example

        Args:
            name (str): The friendly name.

        Returns:
            Just the numeric identifier of the footnote.
            Calls :py:meth:`JocumentStyle.footnote_number`
        '''
        try:
            if name not in self.names:
                self.names.append(name)
            number = self.names.index(name) + 1
            return self.styler.footnote_number(number)
        except ValueError:
            return '** Footnote "{}" not found**'.format(name)

    def output(self) -> str:
        ''' Output the all the footnotes suitably formatted

            First calls :py:meth:`JocumentStyle.footnotes_start` then for each
            footnote calls :py:meth:`JocumentStyle.footnote_output`
            and then finally calls :py:meth:`JocumentStyle.footnotes_end` and
            returns all the collected HTML.

        Returns:
            The html for all the footnotes
        '''
        html = [self.styler.footnotes_start()]
        for index, name in enumerate(self.names):
            number = index + 1
            text = self.name_fn_map[name]
            html.append(self.styler.footnote_output(number, name, text))
        html.append(self.styler.footnotes_end())
        return ''.join(html)


class Citations():
    ''' A little class to do citations.

        For example, in a jupyter notebook, one can have a code cell at the top
        containing::

            citations = Citations()
            citations.cite('the_paper_I_refer_to',
                            authors='Author1 and Author2'],
                            title='Title',
                            source='Source')

        this outputs nothing.


        Later on in the text, one can refer to the reference by adding
        :code:`{{citations.ref('the_paper_I_referred_to')}}`
        in the markdown and it will automatically insert the text `[1]`
        with a hyperlink to the reference.

        Finally, at the end of the document have a markdown cell with::

            ### Citations
            {{citations.output()}}

        and all your citations will be inserted (generally left justified
        paragraph) with the
        text "[1]: Author1, Author2, Title, 2008" (assuming this is the
        first reference) and a hyperlink to return.

        Args:
            styler: A :py:class:`jocument.JocumentStyle` object if the
                citation format needs to be customised.
    '''

    def __init__(self, styler: 'JocumentStyle' = None):

        if styler is None:
            self.styler: JocumentStyle = JocumentStyle()
        else:
            self.styler: JocumentStyle = styler
        self.references: Dict = {}
        self.names: List = []

    def reference(self, name: str, author: str = '', title: str = '',
                  source: str = '') -> None:
        ''' Store a citation keyed by name.

        Args:
            name: the friendly name or this citation
            author: The author or authors of the paper
            title: The title of the paper
            source: The source of the pape
        Returns:
            None
        '''
        self.references[name] = (author, title, source)

    def cite(self, name: str) -> str:
        ''' Reference the citation in the text

        Returns the citation formatted using
        :py:meth:`jocument.JocumentStyle.cite` method

        Args:
            name: The friendly name for this citation

        '''
        try:
            if name not in self.names:
                self.names.append(name)
            number = self.names.index(name) + 1
            return self.styler.cite(number, name, self.references[name])

        except ValueError:
            return f'**Citation "{name}" not found**'

    def output(self) -> str:
        ''' Output the all the citations suitably formatted

        All the references are output.  First the
        :py:meth:`JocumentStyle.references_start` is
        called then for each reference,
        :py:meth:`JocumentStyle.reference_output` is called
        and then finally :py:meth:`JocumentStyle.references_end`
        '''
        html = [self.styler.references_start()]
        for index, name in enumerate(self.names):
            html.append(self.styler.reference_output(index + 1, name,
                                                     self.references[name]))
        html.append(self.styler.references_end())
        return ''.join(html)


class Labels():
    ''' A little class to do equation and table and figure numbering.

        Usage is as follows::

            tables = Label('Table')
            figures = Label('Figure')

        After the instance is created, labels and references
        can be added to each instance.

        .. note::
            Optionally, a :py:class:`jocument.JocumentStyle` object can be passed
            in if customised formatting is required.

        For example, in a jupyter notebook, one can have a markdown cell
        after a table or a graph containing the markdown::

            {{tables.add('this_table_reference')}}

        and a div of class `labelcaption` will be inserted (by default
        centered and italic) with the text "Table 1" (assuming this is
        the first table).  If it was added to the figure_ref instance
        it would display "Figure 1".

        Later on in the text, one can refer to the reference
        by adding {{tables.ref('this_table_reference)}}
        in the markdown and it will automatically insert the number "1".

        If you wish you can add a title to the table by adding the
        reference as follows::

            {{table_ref.add('this_table_reference', title='This is the description of the table')}} #pylint: disable=line-too-long

        and it will do the right thing.

        Finally, it is sometimes the case that you want to
        refer to a table before the table position
        in the document.  In this case you insert::

            {{table_ref.add('this_table_reference', title='This is the description of the table', forward=True)}} #pylint: disable=line-too-long

        Args:
            reference_type: The string (which will be displayed) for this type
            styler: :py:class:`jocument.JocumentStyle` object.
    '''

    def __init__(self, reference_type: str, styler: JocumentStyle = None):
        if styler is None:
            self.styler: JocumentStyle = JocumentStyle()
        else:
            self.styler: JocumentStyle = styler
        self.names: List = []
        self.name_title_map: Dict = {}
        self.reference_type: str = reference_type

    def add(self, name: str, title: str, forward: int = False) -> str:
        ''' Make a new label.

        Args:
            name (str): The friendly name for the label
            forward (bool): Defaults to False.  If you want to refer
                            to a table/chart/equation
                            before it the caption is output then
                            set this to true.
            title (str): The optional title to the table/chart/equation

        Returns (str):
            If forward is True, returns the styler table_ref
            html (default is <Reference Type> [num])
            If forward is False, returns the styler.label html
        '''
        if name not in self.names:
            self.names.append(name)
        self.name_title_map[name] = title
        if forward:
            return self.ref(name)
        else:
            number = self.names.index(name) + 1
            return self.styler.label(self.reference_type, number, name, title)

    def ref(self, name: str) -> str:
        ''' Get a reference to a label

        Args:
            name (str): The friendly name for the label

        Returns (str):
            returns the styler.label html
        '''
        try:
            number = self.names.index(name) + 1
            return self.styler.label_ref(self.reference_type, number)
        except ValueError:
            return f'**{self.reference_type} "{name}" not defined**'
