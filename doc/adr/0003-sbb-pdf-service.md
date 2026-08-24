# 3. SBB PDF-Service

Date: 2026-08-20

## Status

Accepted

## Context

The Schweizerische Bundesbahnen (SBB) has developed an open-source (Apache-2.0 license) weasyprint-service that is also 
providing a REST-endpoint to create PDFs from HTMLs using weasyprint.

[https://github.com/SchweizerischeBundesbahnen/weasyprint-service](https://github.com/SchweizerischeBundesbahnen/weasyprint-service)

This service can be used just like our own by providing a html-file to an endpoint. For this the CSS needs to be
included in the HTML and images need to be converted to data-uris and then also included in the HTML. This is a simple
pre-processing step.
With this change our service and the sbb-weasyprint-service are creating almost identical PDF-files.

Additionally, the SBB-weasyprint-service has already solved various problems and added features we would otherwise not
have or would need to implement and maintain ourselves:

1. Memory Cleanup after PDF creation
2. Monitoring & Metrics: The service includes monitoring endpoints (and a dashboard)
3. Documentation of the functionality and running of the service
4. Active maintenance (multiple updates in the last month; Renovate is used for dependency updates)

## Decision

We deploy the sbb-weasyprint-service and stop developing our own ris-pdf-printservice.

## Consequences

1. In case we need any additional features we would need to either fork the service or work together with the SBB in adding
them.
2. We can remove our own service and no longer need to maintain it
