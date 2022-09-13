# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import pytest

from logger.logger_factory import LoggerFactory


@pytest.fixture
def logger_factory(faker, tmpdir):
    yield LoggerFactory(faker.slug(), logs_path=tmpdir)


class TestLoggerFactory:
    def test_logger_factory_creates_logs_folder_in_working_directory(self, monkeypatch, faker, tmpdir):
        folder = tmpdir.mkdtemp()
        monkeypatch.chdir(folder)
        expected_folder = folder / 'logs'

        LoggerFactory(faker.slug())

        assert Path(expected_folder).is_dir() is True

    def test_get_logger_returns_logger_with_expected_list_of_handlers(self, logger_factory):
        logger = logger_factory.get_logger()

        expected_handlers = [
            TimedRotatingFileHandler,
            StreamHandler,
            StreamHandler,
        ]

        for idx, expected_handler in enumerate(expected_handlers):
            assert isinstance(logger.handlers[idx], expected_handler) is True
