from typing import AnyStr

from ruleau.exceptions import TopLevelRuleRequiresNameException
from ruleau.execute import ExecutionResult
from ruleau.rule import rule


def _validate_name(name):
    """Validator to check if top level rule has a human readable name
    :raises: TopLevelRuleRequiresNameException
    """
    if not name or not isinstance(name, str):
        raise TopLevelRuleRequiresNameException()


def Any(name: AnyStr, *args):
    """Aggregator to implement OR operation
    Returns truthy, if any one of the rule result is truthy
    """
    _validate_name(name)

    @rule(name=name, depends_on=args)
    def any_aggregator(context: ExecutionResult, _):
        return any(result.value for result in context.dependant_results)

    return any_aggregator


def All(name: AnyStr, *args):
    """Aggregator to implement AND operation
    Returns truthy, if and all of the rule results are truthy
    """
    _validate_name(name)

    @rule(name=name, depends_on=args)
    def all_aggregator(context: ExecutionResult, _):
        return all(result.value for result in context.dependant_results)

    return all_aggregator
