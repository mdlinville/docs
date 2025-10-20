#!/usr/bin/env python3
"""
Configure Service API documentation to use the remote OpenAPI specification.

This script doesn't download the spec anymore - instead, the docs.json
is configured to point directly to the Weave service's OpenAPI endpoint.
"""

import sys
from pathlib import Path


def main():
    """Main function."""
    print("Service API configuration:")
    print("  The Service API documentation uses the remote OpenAPI spec directly")
    print("  URL: https://trace.wandb.ai/openapi.json")
    print("  This will be configured in docs.json by update_weave_toc.py")
    print("")
    print("✓ Service API configuration complete!")
    
    # Create the service-api directory if it doesn't exist
    # This ensures the directory structure is in place
    service_api_dir = Path("weave/reference/service-api")
    service_api_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a placeholder index file if it doesn't exist
    index_file = service_api_dir / "index.mdx"
    if not index_file.exists():
        index_content = """---
title: "Service API"
description: "REST API endpoints for the Weave service"
---

# Weave Service API

The Weave Service API provides REST endpoints for interacting with the Weave tracing service.

This documentation is automatically generated from the OpenAPI specification at https://trace.wandb.ai/openapi.json.

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


if __name__ == "__main__":
    main()