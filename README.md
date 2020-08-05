# classifieds

classifieds is a basic classifieds API for seller buyer interaction

## Overview

classifieds handles user authentication and permissions, a profile API, and a sellers items API.

## Authentication

This API uses Token authentication. For each endpoint that requires authorization, the Headers must contain

```sh
Header			Value
Authorization	Token AUTH_TOKEN
```

Tokens are generated at the /api/user/token endpoint.

## Error Codes

Create endpoints have a predefined payload structure. Incorrect payloads yield a `400 BAD REQUEST` response.

Certain endpoints require authentication. Unauthenticated requests get a `401 UNAUTHORIZED` response.

Some endpoints require admin level permission. Requests from a non-staff user get a `403 FORBIDDEN` response.

Some endpoints place owner access restrictions on resources. Requests from a non-owner yield a `403 FORBIDDEN` response.

Detail endpoints will return a `404 NOT FOUND` response if provided a non-existing detail ID.

Requests made to certain endpoints with unimplemented methods return a `405 METHOD NOT ALLOWED` response.

## Rate limit

There are currently no limits on the number of requests any user can send.

## Documentation

The full documentation of classifieds is published [here](https://documenter.getpostman.com/view/6516182/T1DpDJ7Z)
