# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from nose.tools import assert_equal, nottest
import jctconv
from functools import partial

assert_equal.__self__.maxDiff = None

HIRAGANA = ('ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞた',
            'だちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽま',
            'みむめもゃやゅゆょよらりるれろわをんーゎゐゑゕゖゔゝゞ・「」。、')
FULL_KANA = ('ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタ',
             'ダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマ',
             'ミムメモャヤュユョヨラリルレロワヲンーヮヰヱヵヶヴヽヾ・「」。、')
HALF_KANA = ('ｧｱｨｲｩｳｪｴｫｵｶｶﾞｷｷﾞｸｸﾞｹｹﾞｺｺﾞｻｻﾞｼｼﾞｽｽﾞｾｾﾞｿｿﾞﾀ',
             'ﾀﾞﾁﾁﾞｯﾂﾂﾞﾃﾃﾞﾄﾄﾞﾅﾆﾇﾈﾉﾊﾊﾞﾊﾟﾋﾋﾞﾋﾟﾌﾌﾞﾌﾟﾍﾍﾞﾍﾟﾎﾎﾞﾎﾟﾏ',
             'ﾐﾑﾒﾓｬﾔｭﾕｮﾖﾗﾘﾙﾚﾛﾜｦﾝｰヮヰヱヵヶｳﾞヽヾ･｢｣｡､')
HALF_ASCII = ('!"#$%&\'()*+,-./:;<=>?@[\\]^_`~',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              'abcdefghijklmnopqrstuvwxyz{|} ')
HALF_DIGIT = '0123456789'
FULL_ASCII = ('！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀～',
              'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ',
              'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝　')
FULL_DIGIT = '０１２３４５６７８９'


@nottest
def _compare(mathod, lhs, rhs):
    for i in range(len(lhs)):
        assert_equal(mathod(lhs[i]), rhs[i])


@nottest
def _concat(*iterables):
    result = ''
    for iterable in iterables:
        result += ''.join(iterable)
    return result


def test_hira2kata():
    assert_equal(jctconv.hira2kata('ともえまみ'), 'トモエマミ')
    assert_equal(jctconv.hira2kata('まどまぎ', ignore='ど'), 'マどマギ')
    _compare(jctconv.hira2kata, HIRAGANA, FULL_KANA)


def test_hira2hkata():
    assert_equal(jctconv.hira2hkata('ともえまみ'), 'ﾄﾓｴﾏﾐ')
    _compare(jctconv.hira2hkata, HIRAGANA, HALF_KANA)


def test_kata2hira():
    assert_equal(jctconv.kata2hira('巴マミ'), '巴まみ')
    assert_equal(jctconv.kata2hira('マミサン', ignore='ン'), 'まみさン')
    _compare(jctconv.kata2hira, FULL_KANA, HIRAGANA)


def test_h2z():
    assert_equal(jctconv.h2z('ﾃｨﾛﾌｨﾅｰﾚ'), 'ティロフィナーレ')
    assert_equal(jctconv.h2z('ﾃｨﾛﾌｨﾅｰﾚ', ignore='ｨ'), 'テｨロフｨナーレ')
    _compare(jctconv.h2z, HALF_KANA, FULL_KANA)
    _compare(partial(jctconv.h2z, ascii=True), HALF_ASCII, FULL_ASCII)
    _compare(partial(jctconv.h2z, digit=True), HALF_DIGIT, FULL_DIGIT)
    assert_equal(jctconv.h2z(_concat(HALF_KANA, HALF_ASCII, HALF_DIGIT),
                             ascii=True, digit=True, kana=True),
                 _concat(FULL_KANA, FULL_ASCII, FULL_DIGIT))


def test_z2h():
    assert_equal(jctconv.z2h('ティロフィナーレ'), 'ﾃｨﾛﾌｨﾅｰﾚ')
    assert_equal(jctconv.z2h('ティロフィナーレ', ignore='ィ'), 'ﾃィﾛﾌィﾅｰﾚ')
    _compare(partial(jctconv.z2h, kana=True), FULL_KANA, HALF_KANA)
    _compare(partial(jctconv.z2h, ascii=True), FULL_ASCII, HALF_ASCII)
    _compare(partial(jctconv.z2h, digit=True), FULL_DIGIT, HALF_DIGIT)
    assert_equal(jctconv.z2h(_concat(FULL_KANA, FULL_ASCII, FULL_DIGIT),
                             ascii=True, digit=True, kana=True),
                 _concat(HALF_KANA, HALF_ASCII, HALF_DIGIT))


def test_normalize():
    assert_equal(jctconv.normalize('ﾃｨﾛ･フィナ〜レ', 'NFKC'), 'ティロ・フィナーレ')
    assert_equal(jctconv.normalize(_concat(HALF_KANA, FULL_DIGIT), 'NFKC'),
                 ''.join(FULL_KANA)+''.join(HALF_DIGIT))
