from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor, ConsoleSpanExporter
)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from flask_app.settings import settings


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(
        resource=Resource.create({SERVICE_NAME: "auth"})
    ))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.AGENT_HOST_NAME,
                agent_port=settings.AGENT_PORT,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
