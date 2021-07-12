import importlib.resources

import pendulum
# import pytest

import plotman.job
import plotman.plotters.madmax
import plotman._tests.resources


def test_byte_by_byte_full_load():
    read_bytes = importlib.resources.read_binary(
        package=plotman._tests.resources,
        resource="2021-07-11T16_52_48.637488+00_00.plot.log",
    )

    parser = plotman.plotters.madmax.Plotter()

    for byte in (bytes([byte]) for byte in read_bytes):
        parser.update(chunk=byte)

    assert parser.info == plotman.plotters.madmax.SpecificInfo(
        phase=plotman.job.Phase(major=4, minor=2),
        started_at=pendulum.datetime(2021, 7, 11, 16, 52, 00, tz=None),
        plot_id="3a3872f5a124497a17fb917dfe027802aa1867f8b0a8cbac558ed12aa5b697b2",
        p1_buckets=256,
        p34_buckets=256,
        threads=9,
        plot_size=32,
        tmp_dir='/farm/yards/907/',
        tmp2_dir='/farm/yards/907/',
        dst_dir='/farm/yards/907/',
        phase1_duration_raw=1851.12,
        phase2_duration_raw=1344.24,
        phase3_duration_raw=1002.89,
        phase4_duration_raw=77.9891,
        total_time_raw=4276.32,
        plot_name="plot-k32-2021-07-11-16-52-3a3872f5a124497a17fb917dfe027802aa1867f8b0a8cbac558ed12aa5b697b2",
    )
