# API Documentation for main.py

This document provides detailed descriptions of the API endpoints in the `main.py` file of the 3D Printer Monitor project.

## Endpoints

### GET /

This is the root endpoint that redirects to `/index.html`.

### GET /machines

This endpoint returns all the machines. It returns the `machines.json` file, which may not be up-to-date. To update the `machines.json` file, use the `/update_machines` endpoint.

### GET /update_machines?base_ip={base_ip}&mask={mask}

This endpoint updates the `machines.json` file. It takes two optional query parameters: `base_ip` (default is the local IP) and `mask` (default is 16).

### GET /relay?ip={ip}&path={path}

This endpoint relays a request to a machine. It takes two required query parameters: `ip` and `path`.

### GET /status

This endpoint returns the status of all machines.

### GET /status?ip={ip}

This endpoint returns the status of a specific machine. It requires a query parameter: `ip`.

### GET /printer

This endpoint returns the printer details of all machines.

### GET /printer?ip={ip}

This endpoint returns the printer details of a specific machine. It requires a query parameter: `ip`.

### GET /index.html

This endpoint returns the `index.html` file.

### GET /printer_ips

This endpoint returns a list of IP addresses of all printers.

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of a request. The body of the response will contain more detailed information about the result of the request.