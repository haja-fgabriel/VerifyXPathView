from pathlib import Path
from types import SimpleNamespace

import pytest


class BaseTest(object):
    
    @pytest.fixture(name="resources", scope="function")
    def resources_fixture(self, request):
        base_path = Path(__file__).parent.parent
        fspath = Path(request.fspath)
        relative_test_path = fspath.relative_to(base_path)
        module_name = relative_test_path.with_suffix("").name.replace("test_", "")
        relative_resources_path = relative_test_path.parent / module_name

        resources_ns = SimpleNamespace(
            path=base_path / 'resources' / relative_resources_path,
        )
        return resources_ns