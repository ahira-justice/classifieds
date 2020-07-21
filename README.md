# c2c-api

Classifieds API is a basic classifieds API for seller buyer interaction

## Overview

Classifieds API handles user authentication and permissions, a profile API, and a sellers items API.

## Authentication

This API uses Token authentication. For each endpoint that requires authorization, the Headers must contain

```sh
Header			Value
Authorization	Token AUTH_TOKEN
```

Tokens are generated at the /api/user/token endpoint.

## Error Codes

Create endpoints have a predefined payload structure. Incorrect payloads yield a HTTP_400_BAD_REQUEST response.

Certain endpoints require authentication. Unauthenticated requests get a HTTP_401_UNAUTHORIZED response.

Some endpoints require admin level permission. Requests from a non-staff user get a HTTP_403_FORBIDDEN response.

Some endpoints place owner access restrictions on resources. Requests from a non-owner yield a HTTP_403_FORBIDDEN response.

Detail endpoints will return a HTTP_404_NOT_FOUND response if provided a non-existing detail ID.

Requests made to certain endpoints with unimplemented methods return a HTTP_405_METHOD_NOT_ALLOWED response.

## Rate limit

There are currently no limits on the number of requests any user can send.
