# Cloud Notes API

**AWS Lambda handler samples for saving and retrieving one note per authenticated user.**

These JavaScript handlers connect API Gateway HTTP API events to a DynamoDB table. The user ID comes from the JWT authorizer's `sub` claim, so each user's note is stored under their authenticated identity.

This branch contains the original handler samples. For my runnable Python + SQLite project, visit the [main project index](https://github.com/Stormshaper455/My-projects-).

## Request flow

```mermaid
flowchart LR
    A[Client with JWT] --> B[API Gateway JWT authorizer]
    B --> C[Lambda handler]
    C --> D[(DynamoDB: UserNotes)]
```

| Handler | Operation | Result |
| --- | --- | --- |
| [Get_Notes](Get_Notes) | `GetCommand` using the authenticated `UserId` | Returns the saved note, or an empty string when no item exists |
| [Save_Notes](Save_Notes) | `UpdateCommand` setting the `note` attribute | Creates or replaces the user's current note and returns a confirmation |

## Expected AWS configuration

These are backend source samples, not a complete deployment package. To run them in AWS, configure:

1. A DynamoDB table named `UserNotes` with a string partition key named `UserId`.
2. Lambda functions using a supported Node.js runtime and ES modules.
3. AWS SDK for JavaScript v3 dependencies: `@aws-sdk/client-dynamodb` and `@aws-sdk/lib-dynamodb`.
4. An execution role with the necessary `dynamodb:GetItem` or `dynamodb:UpdateItem` permission for this table.
5. An API Gateway HTTP API with a JWT authorizer that supplies `event.requestContext.authorizer.jwt.claims.sub`.

The original files are named `Get_Notes` and `Save_Notes`. For deployment, save each as an ES module (for example, `get-notes.mjs` and `save-notes.mjs`) and use `get-notes.handler` and `save-notes.handler` as the corresponding Lambda handler names. Supply the SDK dependencies in that package or a Lambda layer.

No AWS credentials belong in this repository. The handlers obtain AWS access through their execution environment.

## Example payloads

Save request body:

```json
{"note":"Review database project before the interview."}
```

Save response body:

```json
{"message":"Note saved"}
```

Read response body:

```json
{"note":"Review database project before the interview."}
```

These JSON examples illustrate the handler contract; they are not responses captured from a live deployment.

## Technical decisions and limitations

- **One item per user:** the `UserId` partition key keeps the data model simple. Saving replaces the current note; it does not keep note history.
- **Identity from the authorizer:** the handlers use the verified request context instead of accepting a user ID in the request body. The authorizer must be configured correctly before invoking the handlers.
- **Document client:** DynamoDB's document client accepts plain JavaScript values.
- **Current gaps:** malformed JSON, missing claims, invalid note values, and database failures are not yet handled explicitly. CORS headers are permissive and should be narrowed to the intended frontend origin before a production deployment.

The repository does not include a frontend, infrastructure templates, a public endpoint, or live AWS integration tests. No cloud resources are created by cloning or reading this project.

---

Part of [Joshua Wilson's project portfolio](https://github.com/Stormshaper455/My-projects-).

