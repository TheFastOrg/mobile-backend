from pathlib import Path

import pytest
from pytestarch import (
    EvaluableArchitecture,
    get_evaluable_architecture,
    LayeredArchitecture,
    LayerRule,
    Rule,
)
from pytestarch.query_language.base_language import BaseLayeredArchitecture


class TestArchitecture:
    @pytest.fixture(scope="session")
    def pytestarch_architecture(self) -> EvaluableArchitecture:
        """Running the test in isolation leads to a different cwd than when running via the full pytest suite. Therefore,
        walk up in the file hierarchy until the top level folder is reached."""
        cwd = Path.cwd()
        while cwd.stem != "mobile-backend":
            cwd = cwd.parent
        src_folder = str(cwd / "src")

        return get_evaluable_architecture(
            src_folder,
            src_folder,
            ("*__pycache__", "*__init__.py"),
        )

    @pytest.fixture(scope="session")
    def architecture(self) -> BaseLayeredArchitecture:
        return (
            LayeredArchitecture()
            .layer("core")
            .containing_modules(["src.core"])
            .layer("api")
            .containing_modules(["src.app"])
            .layer("db_migration")
            .containing_modules(["src.alembic"])
        )

    def test_core_layer_should_not_access_any_layer(
        self,
        architecture: BaseLayeredArchitecture,
        pytestarch_architecture: EvaluableArchitecture,
    ):
        rule = (
            LayerRule()
            .based_on(architecture)
            .layers_that()
            .are_named("core")
            .should_not()
            .access_any_layer()
        )
        rule.assert_applies(pytestarch_architecture)

    def test_api_layer_should_access_core_layer(
        self,
        architecture: BaseLayeredArchitecture,
        pytestarch_architecture: EvaluableArchitecture,
    ):
        rule = (
            LayerRule()
            .based_on(architecture)
            .layers_that()
            .are_named("api")
            .should()
            .access_layers_that()
            .are_named("core")
        )
        rule.assert_applies(pytestarch_architecture)

    def test_api_layer_should_not_accessed_by_any_layer(
        self,
        architecture: BaseLayeredArchitecture,
        pytestarch_architecture: EvaluableArchitecture,
    ):
        rule = (
            LayerRule()
            .based_on(architecture)
            .layers_that()
            .are_named("api")
            .should_not()
            .be_accessed_by_layers_except_layers_that()
            .are_named("db_migration")
        )
        rule.assert_applies(pytestarch_architecture)

    def test_services_should_only_be_imported_by_app(
        self, pytestarch_architecture: EvaluableArchitecture
    ):
        rule = (
            Rule()
            .modules_that()
            .are_named("src.core.services")
            .should_only()
            .be_imported_by_modules_that()
            .are_named("src.app")
        )
        rule.assert_applies(pytestarch_architecture)

    def test_dtos_should_only_be_imported_by_endpoints_and_mappers(
        self, pytestarch_architecture: EvaluableArchitecture
    ):
        rule = (
            Rule()
            .modules_that()
            .are_named("src.app.dtos")
            .should_only()
            .be_imported_by_modules_that()
            .are_named(["src.app.endpoints", "src.app.mappers"])
        )
        rule.assert_applies(pytestarch_architecture)

    def test_db_should_not_be_imported_by_endpoints(
        self, pytestarch_architecture: EvaluableArchitecture
    ):
        rule = (
            Rule()
            .modules_that()
            .are_named("src.app.db")
            .should_not()
            .be_imported_by_modules_that()
            .are_named("src.app.endpoints")
        )
        rule.assert_applies(pytestarch_architecture)
