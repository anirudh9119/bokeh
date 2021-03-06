from __future__ import print_function

import os
import boto
import pytest
from boto.s3.key import Key as S3Key
from boto.exception import NoAuthHandlerFound
from os.path import join

s3_bucket = "bokeh-travis"
s3 = "https://s3.amazonaws.com/%s" % s3_bucket
build_id = os.environ.get("TRAVIS_BUILD_ID")
# Can we make this not hard coded and read in the report location from pytest?
report_file = "tests/pytest-report.html"


def pytest_sessionfinish(session, exitstatus):

    if os.environ.get("UPLOAD_PYTEST_HTML", "False") != "True":
        return

    if hasattr(session.config, 'slaveinput'):
        # when slave nodes (xdist) finish, the report won't be ready
        return

    try:
        conn = boto.connect_s3()
        bucket = conn.get_bucket(s3_bucket)

        with open(report_file, "r") as f:
            html = f.read()

        filename = join(build_id, "report.html")
        key = S3Key(bucket, filename)
        key.set_metadata("Content-Type", "text/html")
        key.set_contents_from_string(html, policy="public-read")
        print("\n%s Access report at: %s" % ("---", join(s3, filename)))

    except NoAuthHandlerFound:
        print("Upload was requested but could not connect to S3.")

    except OSError:
        print("Upload was requested but report was not generated.")


@pytest.fixture(scope="session")
def capabilities(capabilities):
    capabilities["browserName"] = "firefox"
    capabilities["tunnel-identifier"] = os.environ.get("TRAVIS_JOB_NUMBER")
    return capabilities
