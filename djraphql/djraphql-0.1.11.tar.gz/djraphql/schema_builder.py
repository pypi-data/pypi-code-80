from graphene import ObjectType
from .type_registry import TypeRegistry
from .schemas.default import DefaultSchema


class SchemaBuilder(object):
    """Entry point into the library. It is responsible for passing Entity classes
    to the TypeRegistry instance (via register_entity_classes) and building the
    root Query and Mutation types.

    Exposes QueryRoot and MutationRoot, which should then be passed to a
    graphene.Schema instance.
    """

    def __init__(self, schema=None):
        self.schema = schema or DefaultSchema()
        self.registry = TypeRegistry(self.schema)

    def register_entity_classes(self, *entity_classes):
        self.registry.register_entity_classes(*entity_classes)

    @property
    def QueryRoot(self):
        return self._build_root_type(
            "QueryRoot", "query_classes", self.schema.DEFAULT_QUERIES
        )

    @property
    def MutationRoot(self):
        return self._build_root_type(
            "MutationRoot", "mutation_classes", self.schema.DEFAULT_MUTATIONS
        )

    def _build_root_type(
        self, type_name, root_type_classes_key, root_type_classes_default
    ):
        """Used to build a root type, e.g. Query or Mutation. Iterates through
        the Entity class's root-type field as specified by root_type_classes_key
        and checks whether the access_permissions field allows the root type to
        exist (i.e. we don't create an insertFoo mutation for a read-only FooEntity)
        and if so, updates the result with the fields returned by the get_root_fields
        method of the root-type.

        Args:
            type_name: str. One of "MutationRoot" or "QueryRoot"
            root_type_classes_key: str: One of "mutation_classes" or "query_classes"
            root_type_classes_default: A list root type classes, which will come from
                djraphql.schemas.default.types.queries|mutations.
        Returns:
            Graphene type representing the root type for GraphQL queries or mutations.
        """

        attrs = {}
        for model_class in self.registry.get_available_model_classes():
            entity_class = self.registry.get_entity_class(model_class)

            # Add the query/mutation fields to the root type being built.
            root_types = getattr(entity_class, root_type_classes_key)

            # If the Entity class does not override query_classes or mutation_classes,
            # then we use the DEFAULT_QUERIES or DEFAULT_MUTATIONS from the schema.
            if root_types is None:
                root_types = root_type_classes_default

            for root_type in root_types:
                # Check permissions before we add the query/mutation type to the root.
                # E.g. insertFoo requires CREATE permission, so we only want to
                # define the insertFoo operation if the FooEntity has a Create in
                # its access_permissions field.
                root_type_permissions = root_type.get_required_access_permissions()
                if not entity_class.allows_permissions(root_type_permissions):
                    continue

                attrs.update(root_type.get_root_fields(self.registry, model_class))

        return type(type_name, (ObjectType,), attrs)
