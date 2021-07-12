import importlib.resources
import typing

import attr
import pytest

import plotman.plotters
import plotman.plotters.chianetwork
import plotman.plotters.madmax
import plotman._tests.resources



# @attr.frozen
# class DecoderExample:
#     bytes: bytes
#     lines: typing.List[str]
#
#
# @pytest.fixture(
#     name="decoder_example",
#     params=[
#         DecoderExample(
#             bytes=b'abc\n123\n\xc3\xa4\xc3\xab\xc3\xaf\n',
#             lines=["abc", "123", "äëï"],
#         ),
#         DecoderExample(
#             bytes=b'abc\n123\n\xc3\xa4\xc3\xab\xc3\xaf',
#             lines=["abc", "123", "äëï"],
#         ),
#     ],
# )
# def decoder_example_fixture(request):
#     return request.param
#
#
# @pytest.fixture(name="line_decoder")
# def line_decoder_fixture():
#     decoder = plotman.plotters.LineDecoder()
#     yield decoder
#     assert decoder.buffer == ""
#
#
# def test_decoder_single_chunk(
#         line_decoder: plotman.plotters.LineDecoder,
#         decoder_example: DecoderExample,
# ) -> None:
#     lines = line_decoder.update(decoder_example.bytes)
#
#     assert lines == decoder_example.lines
#
#
# def test_decoder_individual_byte_chunks(
#         line_decoder: plotman.plotters.LineDecoder,
#         decoder_example: DecoderExample,
# ) -> None:
#     lines = []
#     for byte in decoder_example.bytes:
#         lines.extend(line_decoder.update(bytes([byte])))
#
#     assert lines == decoder_example.lines


@pytest.fixture(name="line_decoder")
def line_decoder_fixture():
    decoder = plotman.plotters.LineDecoder()
    yield decoder
    # assert decoder.buffer == ""


def test_decoder_single_chunk(line_decoder: plotman.plotters.LineDecoder):
    lines = line_decoder.update(b'abc\n123\n\xc3\xa4\xc3\xab\xc3\xaf\n')

    assert lines == ["abc", "123", "äëï"]


def test_decoder_individual_byte_chunks(line_decoder: plotman.plotters.LineDecoder):
    lines = []
    for byte in b'abc\n123\n\xc3\xa4\xc3\xab\xc3\xaf\n':
        lines.extend(line_decoder.update(bytes([byte])))

    assert lines == ["abc", "123", "äëï"]


def test_decoder_partial_line_with_final(line_decoder: plotman.plotters.LineDecoder):
    lines = []
    lines.extend(line_decoder.update(b'abc\n123\n\xc3\xa4\xc3\xab'))
    lines.extend(line_decoder.update(b'\xc3\xaf', final=True))

    assert lines == ["abc", "123", "äëï"]


def test_decoder_partial_line_without_final(line_decoder: plotman.plotters.LineDecoder):
    lines = []
    lines.extend(line_decoder.update(b'abc\n123\n\xc3\xa4\xc3\xab'))
    lines.extend(line_decoder.update(b'\xc3\xaf'))

    assert lines == ["abc", "123"]


@pytest.mark.parametrize(
    argnames=["resource_name", "correct_plotter"],
    argvalues=[
        ["2021-04-04T19_00_47.681088-0400.log", plotman.plotters.chianetwork.Plotter],
        ["2021-07-11T16_52_48.637488+00_00.plot.log", plotman.plotters.madmax.Plotter],
    ],
)
def test_plotter_identifies_log(resource_name, correct_plotter):
    with importlib.resources.open_text(
        package=plotman._tests.resources,
        resource=resource_name,
        encoding='utf-8',
    ) as f:
        plotter = plotman.plotters.get_plotter_from_log(lines=f)

    assert plotter == correct_plotter
