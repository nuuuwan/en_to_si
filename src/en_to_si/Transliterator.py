from functools import cache, cached_property


class Transliterator:
    CONSONANTS = [
        # 1
        ('ක', 'k'),
        ('ඛ', 'K'),
        ('ග', 'g'),
        ('ඝ', 'G'),
        ('ඞ', 'w'),
        ('ඟ', 'F'),
        ('හ', 'h'),
        # 2
        ('ච', 'c'),
        ('ඡ', 'C'),
        ('ජ', 'j'),
        ('ඣ', 'J'),
        ('ඤ', 'W'),
        ('ය', 'y'),
        ('ශ', 'x'),
        ('ඥ', 'M'),
        # 3
        ('ට', 'z'),
        ('ඨ', 'Z'),
        ('ඩ', 'q'),
        ('ඪ', 'Q'),
        ('ණ', 'N'),
        ('ඬ', 'R'),
        ('ල', 'l'),
        ('ෂ', 'X'),
        ('ළ', 'L'),
        # 4
        ('ත', 't'),
        ('ථ', 'T'),
        ('ද', 'd'),
        ('ධ', 'D'),
        ('න', 'n'),
        ('ඳ', 'S'),
        ('ර', 'r'),
        ('ස', 's'),
        # 5
        ('ප', 'p'),
        ('ඵ', 'P'),
        ('බ', 'b'),
        ('භ', 'B'),
        ('ම', 'm'),
        ('ඹ', 'Y'),
        ('ව', 'v'),
        ('ෆ', 'f'),
    ]

    VOWELS = [
        ('්', "-"),
        #
        ('ා', 'A'),
        ('ැ', 'æ'),
        ('ෑ', 'Æ'),
        ('ො', 'o'),
        ('ෝ', 'O'),
        ('ි', 'i'),
        ('ී', 'I'),
        #
        ('ු', 'u'),
        ('ූ', 'U'),
        ('ෙ', 'e'),
        ('ේ', 'E'),
        #
        ('ං', '='),
        #
        ('‍', '$'),
        #
        ('අ', ':a'),
        ('ආ', ':A'),
        ('ඇ', ':æ'),
        ('ඈ', ':Æ'),
        ('ඉ', ':i'),
        ('ඊ', ':I'),
        #
        ('උ', ':u'),
        ('ඌ', ':U'),
        ('එ', ':e'),
        ('ඒ', ':E'),
        ('ඔ', ':o'),
        ('ඕ', ':O'),
        #
        ('අං', ':='),
        ('අඃ', ':_'),
    ]

    LANG_TO_I = {
        'si': 0,
        'en': 1,
    }

    IGNORE_CHARS = [
        ',',
        '.',
        '!',
        '?',
        '(',
        ')',
        '‘',
        '’',
        '“',
        '”',
        ';',
        ' ',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '0',
    ]

    DATA_PAIRS = CONSONANTS + VOWELS

    def __init__(self, lang_src, lang_dest):
        self.lang_src = lang_src
        self.lang_dest = lang_dest

    @cached_property
    def i_src(self):
        return self.LANG_TO_I[self.lang_src]

    @cached_property
    def i_dest(self):
        return self.LANG_TO_I[self.lang_dest]

    @staticmethod
    @cache
    def get_tokens(word):
        tokens = []
        prev_c = None
        for c in word:
            if prev_c == ':':
                tokens[-1] += c
            else:
                tokens.append(c)
            prev_c = c

        return tokens

    @cache
    def get_idx(self):
        idx = {}
        for d in self.DATA_PAIRS:
            src = d[self.i_src]
            dest = d[self.i_dest]

            if src not in idx:
                idx[src] = dest
        return idx

    @cache
    def transliterate_word(self, word_src):
        idx = self.get_idx()
        word_dest = ''

        for c in Transliterator.get_tokens(word_src):
            if c in Transliterator.IGNORE_CHARS:
                word_dest += c
                continue
            if c not in idx:
                print(f"('{c}', ''),")
            word_dest += idx.get(c, '?')

        return word_dest

    @cache
    def transliterate(self, text_src):
        return ' '.join(
            self.transliterate_word(word_src) for word_src in text_src.split()
        )
