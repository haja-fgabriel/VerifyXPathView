import pytest

from tests.base import BaseTest

import florin_libxml2.xmlschemas as xs


class TestXMLSchemas(BaseTest):
    def test_load_schema(self, resources):
        schema_name = "test_schema.xsd"
        schema = xs.load_schema(str(resources.path / schema_name))
        assert schema is not None
    
    def test_inexistent_schema(self, resources):
        schema_name = "test_inexistent_schema.xsd"
        with pytest.raises(xs.LibxmlInternalError):
            assert xs.load_schema(str(resources.path / schema_name)) is None

    def test_invalid_schema(self, resources):
        schema_name = "test_invalid_schema.xsd"
        with pytest.raises(xs.LibxmlInternalError):
            assert xs.load_schema(str(resources.path / schema_name)) is None