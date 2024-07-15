from tests.base import BaseTest

import florin_libxml2.xmlschemas as xs


class TestXMLSchemas(BaseTest):
    def test_load_schema(self, resources):
        schema_name = "test_schema.xsd"
        assert xs.load_schema(str(resources.path / schema_name))