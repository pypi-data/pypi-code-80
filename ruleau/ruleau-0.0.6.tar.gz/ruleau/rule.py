import uuid

from ruleau.constants import OverrideLevel


class Rule:
    def __init__(
        self,
        logic_func,
        name,
        depends_on,
        override_level,
        lazy_dependencies,
    ):
        """
        :param logic_func: User defined rule
        :param name: User defined human readable name of the rule
        :param depends_on: Rule dependencies
        :param override_level: Override level
        :param lazy_dependencies: Flag to switch loading of rule dependencies lazily
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.logic_func = logic_func
        self.depends_on = depends_on
        self.override_level = override_level
        self.__name__ = logic_func.__name__
        self.lazy_dependencies = lazy_dependencies

    def __str__(self) -> str:
        return self.__name__

    def __call__(self, *args, **kwargs) -> bool:
        return self.logic_func(*args, **kwargs)


def rule(
    name=None,
    depends_on=None,
    override_level=OverrideLevel.ANY_OVERRIDE,
    lazy_dependencies=False,
):
    """Decorator to encapsulate a function into a rule"""
    depends_on = depends_on or []

    def rule_decorator(func) -> Rule:
        return Rule(func, name, depends_on, override_level, lazy_dependencies)

    return rule_decorator
