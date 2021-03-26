# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing
import urllib.parse

import opentelemetry.trace as trace
from opentelemetry import baggage
from opentelemetry.context import Context, get_current
from opentelemetry.propagators.textmap import (
    CarrierT,
    Getter,
    Setter,
    TextMapPropagator,
    default_getter,
    default_setter,
)
from opentelemetry.trace import format_span_id, format_trace_id


class JaegerPropagator(TextMapPropagator):
    """Propagator for the Jaeger format.

    See: https://www.jaegertracing.io/docs/1.19/client-libraries/#propagation-format
    """

    TRACE_ID_KEY = "uber-trace-id"
    BAGGAGE_PREFIX = "uberctx-"
    DEBUG_FLAG = 0x02

    def extract(
        self,
        carrier: CarrierT,
        context: typing.Optional[Context] = None,
        getter: Getter = default_getter,
    ) -> Context:

        if context is None:
            context = get_current()
        header = getter.get(carrier, self.TRACE_ID_KEY)
        if not header:
            return trace.set_span_in_context(trace.INVALID_SPAN, context)
        fields = _extract_first_element(header).split(":")

        context = self._extract_baggage(getter, carrier, context)
        if len(fields) != 4:
            return trace.set_span_in_context(trace.INVALID_SPAN, context)

        trace_id, span_id, _parent_id, flags = fields
        if (
            trace_id == trace.INVALID_TRACE_ID
            or span_id == trace.INVALID_SPAN_ID
        ):
            return trace.set_span_in_context(trace.INVALID_SPAN, context)

        span = trace.NonRecordingSpan(
            trace.SpanContext(
                trace_id=int(trace_id, 16),
                span_id=int(span_id, 16),
                is_remote=True,
                trace_flags=trace.TraceFlags(
                    int(flags, 16) & trace.TraceFlags.SAMPLED
                ),
            )
        )
        return trace.set_span_in_context(span, context)

    def inject(
        self,
        carrier: CarrierT,
        context: typing.Optional[Context] = None,
        setter: Setter = default_setter,
    ) -> None:
        span = trace.get_current_span(context=context)
        span_context = span.get_span_context()
        if span_context == trace.INVALID_SPAN_CONTEXT:
            return

        span_parent_id = span.parent.span_id if span.parent else 0
        trace_flags = span_context.trace_flags
        if trace_flags.sampled:
            trace_flags |= self.DEBUG_FLAG

        # set span identity
        setter.set(
            carrier,
            self.TRACE_ID_KEY,
            _format_uber_trace_id(
                span_context.trace_id,
                span_context.span_id,
                span_parent_id,
                trace_flags,
            ),
        )

        # set span baggage, if any
        baggage_entries = baggage.get_all(context=context)
        if not baggage_entries:
            return
        for key, value in baggage_entries.items():
            baggage_key = self.BAGGAGE_PREFIX + key
            setter.set(carrier, baggage_key, urllib.parse.quote(str(value)))

    @property
    def fields(self) -> typing.Set[str]:
        return {self.TRACE_ID_KEY}

    def _extract_baggage(self, getter, carrier, context):
        baggage_keys = [
            key
            for key in getter.keys(carrier)
            if key.startswith(self.BAGGAGE_PREFIX)
        ]
        for key in baggage_keys:
            value = _extract_first_element(getter.get(carrier, key))
            context = baggage.set_baggage(
                key.replace(self.BAGGAGE_PREFIX, ""),
                urllib.parse.unquote(value).strip(),
                context=context,
            )
        return context


def _format_uber_trace_id(trace_id, span_id, parent_span_id, flags):
    return "{trace_id}:{span_id}:{parent_id}:{:02x}".format(
        flags,
        trace_id=format_trace_id(trace_id),
        span_id=format_span_id(span_id),
        parent_id=format_span_id(parent_span_id),
    )


def _extract_first_element(
    items: typing.Iterable[CarrierT],
) -> typing.Optional[CarrierT]:
    if items is None:
        return None
    return next(iter(items), None)
