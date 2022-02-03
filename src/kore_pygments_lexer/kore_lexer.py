from pygments.lexer import RegexLexer, bygroups, default, include, words
from pygments.token import Comment, Keyword, Name, Number, Operator,\
    Punctuation, Text, String
from pygments.util import shebang_matches

__all__ = ['KoreLexer']


class KoreLexer(RegexLexer):
    """Lexer for the kore programming language."""

    name = 'kore'
    aliases = ['korelang', 'kore-lang']
    filenames = ['*.kore']

    identifier = r'[a-zA-Z_]\w*'

    keywords = [
        'if',
        'else',
        'elseif',
        'match',
        'enum',
        'return',
        'some',
        'try',
        'type',
    ]

    builtin_types = [
        'byte',
        'i8',
        'i16',
        'i32',
        'i64',
        'u8',
        'u16',
        'u32',
        'u64',
        'f32',
        'f64',
        'bool',
        'str',
        'char',
    ]

    tokens = {
        'root': [
            (r'\A#!.+$', Comment.Hashbang),
            (
                r'^(\s*)(#@(?:.|\n)*?@#)',
                bygroups(Text, String.Doc)
            ),
            include('comments'),
            include('whitespace'),
            (
                r'(import)(\s+)(.+)',
                bygroups(Keyword.Namespace, Text, Name.Namespace),
                'import'
            ),
            (
                r'\b(module)(\s+)(.+)\b',
                bygroups(Keyword.Namespace, Text, Name.Namespace)
            ),
            include('strings'),
            include('numbers'),
            include('types'),
            (r'\@\d+', Name.Variable.Magic),
            include('operators'),
            (r'!=|==|<<|>>|:=|[-~+/*%=<>&^|.]', Operator),
            (r'[]{}:(),;[]', Punctuation),
            (words(keywords, prefix=r'(?<!\.)\b', suffix=r'\b'), Keyword),
            (r'(var|struct)\b', Keyword.Declaration),
            (
                rf'(func)(\s+)({identifier})',
                bygroups(Keyword.Declaration, Text, Name.Function)
            ),
            (rf'@{identifier}', Name.Decorator),
            (r'(true|false|none|nan)\b', Keyword.Constant),
            (r'\b(map|set)\b', Name.Builtin),
            (identifier, Name),
        ],
        'comments': [
            (r'^#!', Comment.Shebang),
            (r'#\*', Comment.Multiline, 'multiline-comment'),
            (r'#.*$', Comment),
        ],
        'multiline-comment': [
            (r'[^*#]+', Comment.Multiline),
            (r'\*#', Comment.Multiline, '#pop'),
        ],
        'numbers': [
            (r'0[bB][01][01_]+', Number.Bin),
            (r'0[xX][0-9a-fA-F][0-9a-fA-F_]+', Number.Hex),
            (r'0[oO][0-7][0-7_]+', Number.Oct),
            (r'[0-9][0-9_]+\.([0-9]+)?', Number.Float),
            (r'[0-9_]+', Number),
        ],
        'inner-string': [
            (r'@\{', String.Interpol, 'string-interpolation'),
            (r'[^"]+', String),
            (r'"', String, '#pop:2'),
        ],
        'strings': [
            ('"', String, 'inner-string'),
            (
                "(')([^'])(')",
                bygroups(String.Single, String.Char, String.Single)
            ),
        ],
        'string-interpolation': [
            (r'\}', String.Interpol, '#pop'),
            (r'[^}]+', String.Interpol),
            default('#pop'),
            # include('root'),
        ],
        'import': [
            (r'\.', Name.Namespace),
            (identifier, Name.Namespace),
            (r'(\s*)(,)(\s*)', bygroups(Text, Operator, Text)),
            default('#pop'),
        ],
        'operators': [
            (r'\.\.|=>', Operator),
            (r'\+\+|--|~|\?\?=?|\?|:|\\(?=\n)|'
             r'(<<|>>>?|==?|!=?|(?:\*\*|\|\||&&|[-<>+*%&|^/]))=?', Operator),
        ],
        'types': [
            # Optional types
            (rf"({'|'.join(builtin_types)})\?", Keyword.Type),
            # Array types
            (rf"({'|'.join(builtin_types)})(\[])+", Keyword.Type),
            (
                # Plain types
                words(builtin_types, prefix=r'\b', suffix=r'\b'),
                Keyword.Type
            ),
        ],
        'whitespace': [
            (r'\n', Text),
            (r'\s+', Text),
        ],
    }

    def analyse_text(text):
        return shebang_matches(text, r'kore')
