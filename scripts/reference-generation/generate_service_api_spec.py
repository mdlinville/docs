#!/usr/bin/env python3
"""
Download and process the Weave Service API OpenAPI specification.

This script fetches the OpenAPI spec from the Weave service and applies
necessary fixes for documentation generation.
"""

import json
import requests
import sys
from pathlib import Path


def download_openapi_spec():
    """Download the OpenAPI spec from Weave service."""
    url = "https://trace.wandb.ai/openapi.json"
    
    print(f"Downloading OpenAPI spec from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error downloading OpenAPI spec: {e}", file=sys.stderr)
        sys.exit(1)


def apply_mapper(raw_json, mapper):
    """Apply a mapper function recursively to all values in the JSON."""
    if isinstance(raw_json, dict):
        return mapper({k: apply_mapper(v, mapper) for k, v in raw_json.items()})
    elif isinstance(raw_json, list):
        return mapper([apply_mapper(v, mapper) for v in raw_json])
    else:
        return mapper(raw_json)


def apply_doc_fixes(spec):
    """Apply fixes to the OpenAPI spec for documentation generation."""
    
    # Fix 1: Remove the nasty recursion caused by the Mongo query expr.
    # Fix 1.a: Change the `Query.expr` field to be an object.
    # This stops a deadly recursion in docs gen.
    expr = (
        spec.get("components", {})
        .get("schemas", {})
        .get("Query", {})
        .get("properties", {})
        .get("$expr")
    )
    if expr is not None:
        if "anyOf" in expr:
            del expr["anyOf"]
        expr["type"] = "object"
    
    # Fix 1.b: Remove all the operations to prevent recursion
    remove_keys = [
        k
        for k in spec.get("components", {}).get("schemas", {}).keys()
        if k.endswith("Operation")
    ]
    for k in remove_keys:
        if k in spec["components"]["schemas"]:
            del spec["components"]["schemas"][k]
    
    def remove_dependencies_mapper(value):
        if (
            isinstance(value, dict)
            and "$ref" in value
            and any(value["$ref"].endswith(k) for k in remove_keys)
        ):
            return {"type": "object"}
        return value
    
    spec = apply_mapper(spec, remove_dependencies_mapper)
    
    # Fix 2: Fix the `anyOf` fields that are not supported by the docs generator.
    # Specifically, when we have Optional[Any] or Optional[Dict] fields
    def optional_any_fix_mapper(value):
        if (
            isinstance(value, dict)
            and "anyOf" in value
            and value["anyOf"] == [{}, {"type": "null"}]
        ):
            del value["anyOf"]
            value["type"] = "object"
        return value
    
    spec = apply_mapper(spec, optional_any_fix_mapper)
    
    return spec


def update_spec_for_mintlify(spec):
    """Update the OpenAPI spec for better Mintlify presentation."""
    # Ensure the production server is listed
    if "servers" not in spec or not spec["servers"]:
        spec["servers"] = []
    spec["servers"] = [{"url": "https://trace.wandb.ai"}]
    
    # Update the title and description for better presentation
    if "info" in spec:
        spec["info"]["title"] = "Weave Service API"
        spec["info"]["description"] = "REST API endpoints for the Weave service"
    
    return spec


def save_openapi_spec(spec, output_path):
    """Save the OpenAPI spec to a file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(spec, f, indent=2)
    
    print(f"✓ OpenAPI spec saved to {output_path}")


def main():
    """Main function."""
    # Download the spec
    spec = download_openapi_spec()
    
    # Apply fixes for documentation generation
    spec = apply_doc_fixes(spec)
    
    # Update for Mintlify
    spec = update_spec_for_mintlify(spec)
    
    # Save to the appropriate location for Mintlify
    output_path = "weave/reference/service-api/openapi.json"
    save_openapi_spec(spec, output_path)
    
    # Also create the service-api directory structure
    service_api_dir = Path("weave/reference/service-api")
    service_api_dir.mkdir(parents=True, exist_ok=True)
    
    # Create an index file if it doesn't exist
    index_file = service_api_dir / "index.mdx"
    if not index_file.exists():
        index_content = """---
title: "Service API"
description: "REST API endpoints for the Weave service"
---

# Weave Service API

The Weave Service API provides REST endpoints for interacting with the Weave tracing service.

## Authentication

Most endpoints require authentication. Include your W&B API key in the request headers:

```
Authorization: Bearer YOUR_API_KEY
```

## Base URL

All API requests should be made to:

```
https://trace.wandb.ai
```
"""
        index_file.write_text(index_content)
        print(f"✓ Created Service API index at {index_file}")
    
    # Print summary
    paths = spec.get("paths", {})
    print(f"\n✓ Service API spec generation complete!")
    print(f"  Total endpoints: {len(paths)}")
    
    # Check for specific endpoints
    if '/table/query_stats_batch' in paths:
        print("  ✓ /table/query_stats_batch included")
    if '/files/query_stats' in paths:
        print("  ✓ /files/query_stats included")


if __name__ == "__main__":
    main()