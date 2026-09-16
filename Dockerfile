# syntax=docker/dockerfile:1
# Build context is the PARENT directory: the generator reads its sources from the sibling checkouts
# dca-guide/ (guide text), dca-java/ (marker javadoc, rules.json, rule classes) and dca-dotnet/ (rules.json, rule classes).
#   docker build -f dca-knowledge-catalog/Dockerfile -t dca-knowledge-catalog ..
# `docker build` succeeds exactly when generate, lint and the conformance tests pass; the image carries
# the freshly generated bundle under /out/bundle. The `tools` stage is the toolchain alone (python, git,
# pytest); compose.yaml runs it against the mounted checkout.
FROM docker.io/library/python:3.12-slim AS tools
WORKDIR /repo
RUN apt-get update -qq && apt-get install -qq -y --no-install-recommends git > /dev/null && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir --root-user-action=ignore "pytest>=7" "pyyaml>=6"

FROM tools
COPY dca-guide ./dca-guide
COPY dca-java/rules.json dca-java/RULES.md ./dca-java/
COPY dca-java/dca-building-blocks/src/main ./dca-java/dca-building-blocks/src/main
COPY dca-java/dca-archunit/src/main ./dca-java/dca-archunit/src/main
COPY dca-dotnet/rules.json ./dca-dotnet/
COPY dca-dotnet/src/DomainCentric.ArchRules ./dca-dotnet/src/DomainCentric.ArchRules
COPY dca-knowledge-catalog ./dca-knowledge-catalog
WORKDIR /repo/dca-knowledge-catalog
ENV PYTHONPATH=src
RUN python3 -m dca_catalog.generate --no-default-mirror \
 && python3 -m dca_catalog.lint \
 && python3 -m pytest tests/ -q \
 && mkdir -p /out && cp -r bundle /out/bundle
CMD ["ls", "/out/bundle"]
