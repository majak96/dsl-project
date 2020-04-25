from textx import metamodel_from_file, TextXSyntaxError, TextXSemanticError
from textx.export import metamodel_export, model_export
import textx.scoping as scoping
import textx.scoping.providers as scoping_providers


def get_metamodel():
    metamodel = metamodel_from_file('grammar.tx')
    metamodel.register_scope_providers({
        "*.*": scoping_providers.PlainName(),
        "ParameterValue.name": scoping_providers.RelativeName(
            "parent.type.parameters"),
    })

    return metamodel
