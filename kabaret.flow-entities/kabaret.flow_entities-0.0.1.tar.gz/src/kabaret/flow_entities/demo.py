from kabaret import flow

from .store import EntityStore
from .entities import (
    EntityCollection,
    CreateEntitiesAction,
    DeleteEntitiesAction,
    Entity,
    Property,
    PropertyValue,
)


class NoDialogAction(flow.Action):
    def needs_dialog(self):
        return False


class Asset(Entity):

    asset_type = Property()
    mod_status = Property()
    surf_status = Property()

    some_action = flow.Child(NoDialogAction)


class Assets(EntityCollection):

    create_assets = flow.Child(CreateEntitiesAction)
    delete_assets = flow.Child(DeleteEntitiesAction)

    @classmethod
    def mapped_type(cls):
        return Asset

    def summary(self):
        return "{} entities here".format(len(self))


class _StatusAction(flow.Action):

    STATUS_TO_SET = None
    _property_value = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        self._property_value.set(self.STATUS_TO_SET)


class NYSAction(_StatusAction):
    STATUS_TO_SET = "NYS"
    ICON = ("icons.status", "NYS")


class WIPAction(_StatusAction):
    STATUS_TO_SET = "WIP"
    ICON = ("icons.status", "WIP")


class DONEAction(_StatusAction):
    STATUS_TO_SET = "DONE"
    ICON = ("icons.status", "DONE")


class DeptStatusPropertyValue(PropertyValue):

    NYS = flow.Child(NYSAction)
    WIP = flow.Child(WIPAction)
    DONE = flow.Child(DONEAction)


class Shot(Entity):

    film = Property()
    sequence = Property()
    anim_status = Property(DeptStatusPropertyValue)
    render_status = Property(DeptStatusPropertyValue)

    casting = flow.Child(flow.Map)


class CreateManyShotsAction(flow.Action):

    _collection = flow.Parent()

    first = flow.Param(1)
    last = flow.Param(10)

    def needs_dialog(self):
        return True

    def get_buttons(self):
        return ["Create Shots"]

    def run(self, button):
        names = [
            "P{:03}".format(i) for i in range(self.first.get(), self.last.get() + 1)
        ]
        self._collection.ensure_exist(names)
        self._collection.touch()


class Shots(EntityCollection):

    create_shots = flow.Child(CreateEntitiesAction)
    create_many_shots = flow.Child(CreateManyShotsAction)
    delete_shots = flow.Child(DeleteEntitiesAction)

    @classmethod
    def mapped_type(cls):
        return Shot

    def summary(self):
        return "{} entities here".format(len(self))


class ToggleNYSAction(flow.Action):

    _collection = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        param = self._collection.include_nys
        param.set(not param.get())
        self._collection.touch()


class WIPShots(EntityCollection):

    _parent = flow.Parent()

    toggle_nys = flow.Child(ToggleNYSAction).ui(label="Toggle NYS")
    include_nys = flow.BoolParam(False)

    @classmethod
    def mapped_type(cls):
        return Shot

    def collection_name(self):
        """
        Using the same name a the Shot collection
        to show the same entitie.
        """
        return self._parent.shots.collection_name()

    def query_filter(self):
        """
        Listing only shots with a WIP status
        """
        match = "WIP"
        if self.include_nys.get():
            match = {"$in": ["WIP", "NYS"]}
        return {
            "$or": [
                {"anim_status": match},
                {"render_status": match},
            ]
        }

    def summary(self):
        inex = "Ex"
        if self.include_nys.get():
            inex = "In"
        return "{} Shots here ({}cluding NYS)".format(len(self), inex)

    def _fill_row_style(self, style, item, row):
        style["Anim Status_icon"] = ("icons.status", row["Anim Status"])
        style["Render Status_icon"] = ("icons.status", row["Render Status"])


class Admin(flow.Object):

    store = flow.Child(EntityStore)


class EntitiesDemo(flow.Object):

    assets = flow.Child(Assets)
    shots = flow.Child(Shots)
    wip_shots = flow.Child(WIPShots)

    admin = flow.Child(Admin)

    def get_entity_store(self):
        """
        This needs to be implemented to your project
        for the entity system to work.
        """
        return self.admin.store
