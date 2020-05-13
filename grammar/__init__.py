from os.path import dirname, join
from textx import language, metamodel_from_file

@language("Srvy", "*.srvy")
def srvy():
    "A domain-specific language for definining web-based surveys."
    return metamodel_from_file(join(dirname(__file__), "grammar.tx"))