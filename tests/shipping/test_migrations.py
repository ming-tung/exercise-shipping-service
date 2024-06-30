import io

import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestStartup:
    def test_check_command(self):
        output = io.StringIO()
        call_command(
            'check',
            stdout=output,
        )
        output.seek(0)
        assert output.read() == 'System check identified no issues (0 silenced).\n'

    def test_makemigrations_command(self):
        output = io.StringIO()
        call_command(
            'makemigrations',
            interactive=False,
            dry_run=True,
            check=True,
            stdout=output,
        )
        output.seek(0)
        assert output.read() == 'No changes detected\n'
