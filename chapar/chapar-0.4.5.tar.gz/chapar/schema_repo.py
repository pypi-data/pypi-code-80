from pulsar.schema import (
    Record,
    String,
    Array,
    Float,
)


class TextSchema(Record):
    uuid = String(required=True)
    text = String()
    sequence_id = String()


class TextEmbeddingSchema(Record):
    uuid = String(required=True)
    text = String()
    embedding = Array(Float())


class TaskSchema(Record):
    task_class = String(required=True)
    task_id = String()
    job_id = String()
    args = String()
    kwargs = String()
