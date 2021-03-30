class TopLevelRuleRequiresNameException(Exception):
    """Exception raised if top level aggregators don't have a human readable name"""

    pass


class MethodNotAllowedException(Exception):
    """Exception raised if a forbidden RuleauDict method is called"""

    pass
